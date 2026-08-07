#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "driver/i2c_master.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define HARNESS_NAME "ihap53-local-display-harness"
#define I2C_SDA_GPIO 5
#define I2C_SCL_GPIO 6
#define I2C_FREQUENCY_HZ 100000
#define I2C_TIMEOUT_MS 100
#define OLED_WIDTH 128
#define OLED_HEIGHT 64
#define OLED_PAGES (OLED_HEIGHT / 8)
#define OLED_BUFFER_SIZE (OLED_WIDTH * OLED_PAGES)

static const char *TAG = "IHAP53";
static uint8_t s_framebuffer[OLED_BUFFER_SIZE];

static esp_err_t transmit(i2c_master_dev_handle_t dev, const uint8_t *data, size_t len)
{
    return i2c_master_transmit(dev, data, len, I2C_TIMEOUT_MS);
}

static esp_err_t send_commands(i2c_master_dev_handle_t dev, const uint8_t *commands, size_t len)
{
    if (len > 63) {
        return ESP_ERR_INVALID_SIZE;
    }

    uint8_t payload[64];
    payload[0] = 0x00;
    memcpy(&payload[1], commands, len);
    return transmit(dev, payload, len + 1);
}

static esp_err_t send_framebuffer(i2c_master_dev_handle_t dev)
{
    const uint8_t address_window[] = {0x21, 0x00, 0x7F, 0x22, 0x00, 0x07};
    esp_err_t err = send_commands(dev, address_window, sizeof(address_window));
    if (err != ESP_OK) {
        return err;
    }

    uint8_t payload[17];
    payload[0] = 0x40;
    for (size_t offset = 0; offset < OLED_BUFFER_SIZE; offset += 16) {
        memcpy(&payload[1], &s_framebuffer[offset], 16);
        err = transmit(dev, payload, sizeof(payload));
        if (err != ESP_OK) {
            return err;
        }
    }
    return ESP_OK;
}

static esp_err_t ssd1306_init(i2c_master_dev_handle_t dev)
{
    const uint8_t init_sequence[] = {
        0xAE,
        0xD5, 0x80,
        0xA8, 0x3F,
        0xD3, 0x00,
        0x40,
        0x8D, 0x14,
        0x20, 0x00,
        0xA1,
        0xC8,
        0xDA, 0x12,
        0x81, 0x7F,
        0xD9, 0xF1,
        0xDB, 0x40,
        0xA4,
        0xA6,
        0xAF,
    };
    return send_commands(dev, init_sequence, sizeof(init_sequence));
}

static void set_pixel(int x, int y, bool on)
{
    if (x < 0 || x >= OLED_WIDTH || y < 0 || y >= OLED_HEIGHT) {
        return;
    }

    const size_t index = (size_t)x + ((size_t)y / 8U) * OLED_WIDTH;
    const uint8_t mask = (uint8_t)(1U << (y & 7));
    if (on) {
        s_framebuffer[index] |= mask;
    } else {
        s_framebuffer[index] &= (uint8_t)~mask;
    }
}

static void glyph(char c, uint8_t out[5])
{
    const uint8_t blank[5] = {0, 0, 0, 0, 0};
    const uint8_t *g = blank;

    static const uint8_t A[5] = {0x7E, 0x11, 0x11, 0x11, 0x7E};
    static const uint8_t D[5] = {0x7F, 0x41, 0x41, 0x22, 0x1C};
    static const uint8_t E[5] = {0x7F, 0x49, 0x49, 0x49, 0x41};
    static const uint8_t G[5] = {0x3E, 0x41, 0x49, 0x49, 0x7A};
    static const uint8_t H[5] = {0x7F, 0x08, 0x08, 0x08, 0x7F};
    static const uint8_t I[5] = {0x41, 0x41, 0x7F, 0x41, 0x41};
    static const uint8_t M[5] = {0x7F, 0x02, 0x0C, 0x02, 0x7F};
    static const uint8_t O[5] = {0x3E, 0x41, 0x41, 0x41, 0x3E};
    static const uint8_t P[5] = {0x7F, 0x09, 0x09, 0x09, 0x06};
    static const uint8_t THREE[5] = {0x22, 0x41, 0x49, 0x49, 0x36};
    static const uint8_t FIVE[5] = {0x4F, 0x49, 0x49, 0x49, 0x31};

    switch (c) {
        case 'A': g = A; break;
        case 'D': g = D; break;
        case 'E': g = E; break;
        case 'G': g = G; break;
        case 'H': g = H; break;
        case 'I': g = I; break;
        case 'M': g = M; break;
        case 'O': g = O; break;
        case 'P': g = P; break;
        case '3': g = THREE; break;
        case '5': g = FIVE; break;
        default: break;
    }

    memcpy(out, g, 5);
}

static void draw_text(int x, int y, const char *text)
{
    for (const char *p = text; *p != '\0'; ++p) {
        uint8_t columns[5];
        glyph(*p, columns);
        for (int col = 0; col < 5; ++col) {
            for (int row = 0; row < 7; ++row) {
                if ((columns[col] >> row) & 0x01U) {
                    set_pixel(x + col, y + row, true);
                }
            }
        }
        x += 6;
    }
}

static void draw_border(void)
{
    for (int x = 0; x < OLED_WIDTH; ++x) {
        set_pixel(x, 0, true);
        set_pixel(x, OLED_HEIGHT - 1, true);
    }
    for (int y = 0; y < OLED_HEIGHT; ++y) {
        set_pixel(0, y, true);
        set_pixel(OLED_WIDTH - 1, y, true);
    }
}

static esp_err_t show_visual_sequence(i2c_master_dev_handle_t dev)
{
    memset(s_framebuffer, 0xFF, sizeof(s_framebuffer));
    ESP_RETURN_ON_ERROR(send_framebuffer(dev), TAG, "full-on transfer failed");
    ESP_LOGI(TAG, "{\"event\":\"visual\",\"stage\":\"full_on\",\"result\":\"PASS_TRANSFER\"}");
    vTaskDelay(pdMS_TO_TICKS(2000));

    memset(s_framebuffer, 0x00, sizeof(s_framebuffer));
    ESP_RETURN_ON_ERROR(send_framebuffer(dev), TAG, "full-off transfer failed");
    ESP_LOGI(TAG, "{\"event\":\"visual\",\"stage\":\"full_off\",\"result\":\"PASS_TRANSFER\"}");
    vTaskDelay(pdMS_TO_TICKS(2000));

    for (size_t i = 0; i < sizeof(s_framebuffer); ++i) {
        s_framebuffer[i] = (i & 1U) ? 0xAA : 0x55;
    }
    ESP_RETURN_ON_ERROR(send_framebuffer(dev), TAG, "checkerboard transfer failed");
    ESP_LOGI(TAG, "{\"event\":\"visual\",\"stage\":\"checkerboard\",\"result\":\"PASS_TRANSFER\"}");
    vTaskDelay(pdMS_TO_TICKS(2000));

    memset(s_framebuffer, 0x00, sizeof(s_framebuffer));
    draw_border();
    draw_text(8, 12, "HOMEEDGE");
    draw_text(8, 28, "IHAP53");
    ESP_RETURN_ON_ERROR(send_framebuffer(dev), TAG, "text-card transfer failed");
    ESP_LOGI(TAG, "{\"event\":\"visual\",\"stage\":\"text_card\",\"result\":\"PASS_TRANSFER\"}");
    return ESP_OK;
}

void app_main(void)
{
    ESP_LOGI(TAG, "{\"event\":\"boot\",\"harness\":\"%s\",\"sda\":%d,\"scl\":%d}",
             HARNESS_NAME, I2C_SDA_GPIO, I2C_SCL_GPIO);

    i2c_master_bus_config_t bus_config = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = I2C_SDA_GPIO,
        .scl_io_num = I2C_SCL_GPIO,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = false,
    };

    i2c_master_bus_handle_t bus = NULL;
    ESP_ERROR_CHECK(i2c_new_master_bus(&bus_config, &bus));

    const uint8_t candidates[] = {0x3C, 0x3D};
    uint8_t found_address = 0;
    int found_count = 0;

    for (size_t i = 0; i < sizeof(candidates); ++i) {
        const esp_err_t probe = i2c_master_probe(bus, candidates[i], I2C_TIMEOUT_MS);
        ESP_LOGI(TAG, "{\"event\":\"probe\",\"address\":\"0x%02X\",\"ack\":%s}",
                 candidates[i], probe == ESP_OK ? "true" : "false");
        if (probe == ESP_OK) {
            found_address = candidates[i];
            ++found_count;
        }
    }

    if (found_count != 1) {
        ESP_LOGE(TAG, "{\"event\":\"gate\",\"stage\":\"probe\",\"result\":\"FAIL\",\"candidate_count\":%d}", found_count);
        return;
    }

    i2c_device_config_t device_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = found_address,
        .scl_speed_hz = I2C_FREQUENCY_HZ,
    };

    i2c_master_dev_handle_t display = NULL;
    ESP_ERROR_CHECK(i2c_master_bus_add_device(bus, &device_config, &display));

    esp_err_t err = ssd1306_init(display);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "{\"event\":\"gate\",\"stage\":\"ssd1306_init\",\"result\":\"FAIL\",\"error\":\"%s\"}", esp_err_to_name(err));
        return;
    }

    ESP_LOGI(TAG, "{\"event\":\"gate\",\"stage\":\"ssd1306_init\",\"result\":\"PASS\",\"address\":\"0x%02X\"}", found_address);

    err = show_visual_sequence(display);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "{\"event\":\"gate\",\"stage\":\"visual_sequence\",\"result\":\"FAIL\",\"error\":\"%s\"}", esp_err_to_name(err));
        return;
    }

    ESP_LOGI(TAG, "{\"event\":\"gate\",\"stage\":\"short_functional\",\"result\":\"PASS_TRANSFER\"}");
    ESP_LOGI(TAG, "{\"event\":\"stability\",\"stage\":\"start\",\"target_minutes\":60}");

    const int64_t started_us = esp_timer_get_time();
    uint32_t cycle = 0;
    int previous_marker = -1;

    while (true) {
        const int marker = (int)(cycle % 126U) + 1;
        if (previous_marker >= 0) {
            set_pixel(previous_marker, 62, false);
        }
        set_pixel(marker, 62, true);
        previous_marker = marker;

        err = send_framebuffer(display);
        const int64_t elapsed_s = (esp_timer_get_time() - started_us) / 1000000;
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "{\"event\":\"heartbeat\",\"cycle\":%lu,\"elapsed_s\":%lld,\"result\":\"FAIL\",\"error\":\"%s\"}",
                     (unsigned long)cycle, (long long)elapsed_s, esp_err_to_name(err));
            return;
        }

        ESP_LOGI(TAG, "{\"event\":\"heartbeat\",\"cycle\":%lu,\"elapsed_s\":%lld,\"result\":\"PASS\"}",
                 (unsigned long)cycle, (long long)elapsed_s);
        ++cycle;
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}
