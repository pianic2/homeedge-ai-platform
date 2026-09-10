#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "driver/gpio.h"
#include "driver/i2c_master.h"
#include "driver/uart.h"
#include "esp_check.h"
#include "esp_err.h"
#include "esp_idf_version.h"
#include "esp_rom_sys.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define HARNESS_NAME "ihap50-integrated-interconnect-harness"
#define SCHEMA_VERSION "1.2.0"

#define PIN_RADAR_RX GPIO_NUM_0
#define PIN_RADAR_TX_SERVICE GPIO_NUM_1
#define PIN_DOOR GPIO_NUM_3
#define PIN_DHT GPIO_NUM_4
#define PIN_ADC_SPARE GPIO_NUM_5
#define PIN_I2C_SDA GPIO_NUM_6
#define PIN_I2C_SCL GPIO_NUM_7
#define PIN_DIGITAL_SPARE GPIO_NUM_10

#define I2C_TIMEOUT_MS 100
#define I2C_FREQ_HZ 100000
#define OLED_ADDR 0x3C
#define BME280_ADDR 0x76
#define BME280_CHIP_ID_REG 0xD0
#define BME280_CHIP_ID 0x60

#define LD2410_UART UART_NUM_1
#define LD2410_BAUD 256000
#define UART_RX_BUFFER_SIZE 1024
#define FRAME_BUFFER_SIZE 128
#define DHT_BIT_THRESHOLD_US 50

static const uint8_t FRAME_HEADER[] = {0xF4, 0xF3, 0xF2, 0xF1};
static const uint8_t FRAME_FOOTER[] = {0xF8, 0xF7, 0xF6, 0xF5};

static i2c_master_bus_handle_t s_i2c_bus;
static i2c_master_dev_handle_t s_oled;
static i2c_master_dev_handle_t s_bme;
static bool s_bme_present;
static portMUX_TYPE s_dht_lock = portMUX_INITIALIZER_UNLOCKED;
static portMUX_TYPE s_radar_lock = portMUX_INITIALIZER_UNLOCKED;

typedef struct {
    bool valid;
    float temperature_c;
    float humidity_percent;
    const char *status;
} dht_sample_t;

typedef struct {
    bool has_valid_frame;
    uint8_t target_state;
    int64_t last_valid_frame_us;
    uint32_t valid_frames;
    uint32_t invalid_frames;
    uint32_t uart_bytes;
} radar_state_t;

static radar_state_t s_radar;

static uint16_t read_le16(const uint8_t *data)
{
    return (uint16_t)data[0] | ((uint16_t)data[1] << 8);
}

static bool wait_while_level(gpio_num_t gpio, int level, uint32_t timeout_us, uint32_t *duration_us)
{
    const int64_t start = esp_timer_get_time();
    while (gpio_get_level(gpio) == level) {
        if ((uint64_t)(esp_timer_get_time() - start) > timeout_us) {
            return false;
        }
    }
    *duration_us = (uint32_t)(esp_timer_get_time() - start);
    return true;
}

static void configure_dht(void)
{
    const gpio_config_t config = {
        .pin_bit_mask = 1ULL << PIN_DHT,
        .mode = GPIO_MODE_INPUT_OUTPUT_OD,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&config));
    ESP_ERROR_CHECK(gpio_set_level(PIN_DHT, 1));
}

static dht_sample_t read_dht11(void)
{
    dht_sample_t sample = {
        .valid = false,
        .temperature_c = 0.0f,
        .humidity_percent = 0.0f,
        .status = "TIMEOUT",
    };
    uint8_t data[5] = {0};
    uint32_t pulse = 0;

    gpio_set_direction(PIN_DHT, GPIO_MODE_OUTPUT_OD);
    gpio_set_level(PIN_DHT, 0);
    vTaskDelay(pdMS_TO_TICKS(20));

    portENTER_CRITICAL(&s_dht_lock);
    gpio_set_level(PIN_DHT, 1);
    esp_rom_delay_us(30);
    gpio_set_direction(PIN_DHT, GPIO_MODE_INPUT);

    if (!wait_while_level(PIN_DHT, 1, 120, &pulse) ||
        !wait_while_level(PIN_DHT, 0, 120, &pulse) ||
        !wait_while_level(PIN_DHT, 1, 120, &pulse)) {
        sample.status = "NO_RESPONSE";
        goto done;
    }

    for (int bit = 0; bit < 40; ++bit) {
        uint32_t low_us = 0;
        uint32_t high_us = 0;
        if (!wait_while_level(PIN_DHT, 0, 100, &low_us) ||
            !wait_while_level(PIN_DHT, 1, 120, &high_us)) {
            sample.status = "TIMEOUT";
            goto done;
        }
        data[bit / 8] <<= 1;
        if (high_us > DHT_BIT_THRESHOLD_US) {
            data[bit / 8] |= 1U;
        }
    }

    if ((uint8_t)(data[0] + data[1] + data[2] + data[3]) != data[4]) {
        sample.status = "CHECKSUM";
        goto done;
    }

    sample.humidity_percent = (float)data[0] + ((float)data[1] / 10.0f);
    sample.temperature_c = (float)data[2] + ((float)(data[3] & 0x7FU) / 10.0f);
    if ((data[3] & 0x80U) != 0U) {
        sample.temperature_c = -sample.temperature_c;
    }
    sample.valid = sample.humidity_percent >= 0.0f && sample.humidity_percent <= 100.0f;
    sample.status = sample.valid ? "OK" : "OUT_OF_RANGE";

done:
    gpio_set_direction(PIN_DHT, GPIO_MODE_INPUT);
    portEXIT_CRITICAL(&s_dht_lock);
    return sample;
}

static esp_err_t add_i2c_device(uint8_t address, i2c_master_dev_handle_t *device)
{
    i2c_device_config_t cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = address,
        .scl_speed_hz = I2C_FREQ_HZ,
    };
    return i2c_master_bus_add_device(s_i2c_bus, &cfg, device);
}

static esp_err_t configure_i2c(void)
{
    i2c_master_bus_config_t cfg = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = PIN_I2C_SDA,
        .scl_io_num = PIN_I2C_SCL,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = false,
    };
    ESP_RETURN_ON_ERROR(i2c_new_master_bus(&cfg, &s_i2c_bus), "IHAP50", "I2C bus init");

    const esp_err_t oled_probe = i2c_master_probe(s_i2c_bus, OLED_ADDR, I2C_TIMEOUT_MS);
    const esp_err_t bme_probe = i2c_master_probe(s_i2c_bus, BME280_ADDR, I2C_TIMEOUT_MS);
    s_bme_present = bme_probe == ESP_OK;

    printf("{\"record_type\":\"i2c_probe\",\"oled_0x3c\":%s,\"bme280_0x76\":%s}\n",
           oled_probe == ESP_OK ? "true" : "false",
           s_bme_present ? "true" : "false");
    fflush(stdout);

    ESP_RETURN_ON_ERROR(oled_probe, "IHAP50", "OLED 0x3C not found");
    ESP_RETURN_ON_ERROR(add_i2c_device(OLED_ADDR, &s_oled), "IHAP50", "OLED add");
    if (s_bme_present) {
        ESP_RETURN_ON_ERROR(add_i2c_device(BME280_ADDR, &s_bme), "IHAP50", "BME add");
    }
    return ESP_OK;
}

static esp_err_t oled_init(void)
{
    const uint8_t sequence[] = {
        0x00,
        0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
        0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12,
        0x81, 0x7F, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6, 0xAF,
    };
    return i2c_master_transmit(s_oled, sequence, sizeof(sequence), I2C_TIMEOUT_MS);
}

static bool oled_visual_gate(void)
{
    const uint8_t all_on[] = {0x00, 0xA5};
    const uint8_t ram_display[] = {0x00, 0xA4};
    if (i2c_master_transmit(s_oled, all_on, sizeof(all_on), I2C_TIMEOUT_MS) != ESP_OK) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
    return i2c_master_transmit(s_oled, ram_display, sizeof(ram_display), I2C_TIMEOUT_MS) == ESP_OK;
}

static bool oled_ping(void)
{
    const uint8_t command[] = {0x00, 0xA4};
    return i2c_master_transmit(s_oled, command, sizeof(command), I2C_TIMEOUT_MS) == ESP_OK;
}

static bool bme280_read_chip_id(uint8_t *chip_id)
{
    if (!s_bme_present || s_bme == NULL) {
        return false;
    }
    const uint8_t reg = BME280_CHIP_ID_REG;
    return i2c_master_transmit_receive(s_bme, &reg, 1, chip_id, 1, I2C_TIMEOUT_MS) == ESP_OK;
}

static void configure_door(void)
{
    const gpio_config_t cfg = {
        .pin_bit_mask = 1ULL << PIN_DOOR,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&cfg));
}

static bool spare_pin_pull_test(gpio_num_t pin)
{
    gpio_config_t cfg = {
        .pin_bit_mask = 1ULL << pin,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    if (gpio_config(&cfg) != ESP_OK) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(5));
    const int high = gpio_get_level(pin);

    cfg.pull_up_en = GPIO_PULLUP_DISABLE;
    cfg.pull_down_en = GPIO_PULLDOWN_ENABLE;
    if (gpio_config(&cfg) != ESP_OK) {
        return false;
    }
    vTaskDelay(pdMS_TO_TICKS(5));
    const int low = gpio_get_level(pin);

    cfg.pull_up_en = GPIO_PULLUP_DISABLE;
    cfg.pull_down_en = GPIO_PULLDOWN_DISABLE;
    (void)gpio_config(&cfg);
    return high == 1 && low == 0;
}

static void register_invalid_frame(void)
{
    portENTER_CRITICAL(&s_radar_lock);
    s_radar.invalid_frames++;
    portEXIT_CRITICAL(&s_radar_lock);
}

static bool parse_radar_frame(const uint8_t *frame, size_t len)
{
    if (len < 23 || memcmp(frame, FRAME_HEADER, sizeof(FRAME_HEADER)) != 0) {
        return false;
    }
    const uint16_t payload_len = read_le16(&frame[4]);
    if ((size_t)payload_len + 10U != len || payload_len < 13U) {
        return false;
    }
    if (memcmp(&frame[len - 4U], FRAME_FOOTER, sizeof(FRAME_FOOTER)) != 0) {
        return false;
    }
    const uint8_t *payload = &frame[6];
    if (payload[0] != 0x02 || payload[1] != 0xAA || payload[11] != 0x55 || payload[12] != 0x00) {
        return false;
    }

    portENTER_CRITICAL(&s_radar_lock);
    s_radar.has_valid_frame = true;
    s_radar.target_state = payload[2];
    s_radar.last_valid_frame_us = esp_timer_get_time();
    s_radar.valid_frames++;
    portEXIT_CRITICAL(&s_radar_lock);
    return true;
}

static void consume_radar(uint8_t *buffer, size_t *used)
{
    while (*used >= 4U) {
        size_t header = 0;
        while (header + 4U <= *used && memcmp(&buffer[header], FRAME_HEADER, 4) != 0) {
            ++header;
        }
        if (header > 0) {
            memmove(buffer, &buffer[header], *used - header);
            *used -= header;
        }
        if (*used < 6U) {
            return;
        }

        const size_t total = (size_t)read_le16(&buffer[4]) + 10U;
        if (total < 10U || total > FRAME_BUFFER_SIZE) {
            register_invalid_frame();
            memmove(buffer, &buffer[1], *used - 1U);
            --(*used);
            continue;
        }
        if (*used < total) {
            return;
        }
        if (!parse_radar_frame(buffer, total)) {
            register_invalid_frame();
        }
        memmove(buffer, &buffer[total], *used - total);
        *used -= total;
    }
}

static void radar_task(void *arg)
{
    (void)arg;
    uint8_t read_buf[128];
    uint8_t frame_buf[FRAME_BUFFER_SIZE];
    size_t used = 0;

    while (true) {
        const int n = uart_read_bytes(LD2410_UART, read_buf, sizeof(read_buf), pdMS_TO_TICKS(100));
        if (n <= 0) {
            continue;
        }

        portENTER_CRITICAL(&s_radar_lock);
        s_radar.uart_bytes += (uint32_t)n;
        portEXIT_CRITICAL(&s_radar_lock);

        for (int i = 0; i < n; ++i) {
            if (used == sizeof(frame_buf)) {
                register_invalid_frame();
                memmove(frame_buf, &frame_buf[1], sizeof(frame_buf) - 1U);
                --used;
            }
            frame_buf[used++] = read_buf[i];
            consume_radar(frame_buf, &used);
        }
    }
}

static esp_err_t configure_radar_uart(void)
{
    const uart_config_t cfg = {
        .baud_rate = LD2410_BAUD,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    ESP_RETURN_ON_ERROR(uart_driver_install(LD2410_UART, UART_RX_BUFFER_SIZE, 0, 0, NULL, 0), "IHAP50", "UART install");
    ESP_RETURN_ON_ERROR(uart_param_config(LD2410_UART, &cfg), "IHAP50", "UART config");

    /* Receive-only by design. GPIO1 is reserved in the interconnect contract but
       is not attached to the UART peripheral in this validation harness. */
    return uart_set_pin(LD2410_UART, UART_PIN_NO_CHANGE, PIN_RADAR_RX, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
}

static radar_state_t radar_snapshot(void)
{
    radar_state_t snapshot;
    portENTER_CRITICAL(&s_radar_lock);
    snapshot = s_radar;
    portEXIT_CRITICAL(&s_radar_lock);
    return snapshot;
}

void app_main(void)
{
    memset(&s_radar, 0, sizeof(s_radar));
    configure_door();
    configure_dht();

    const bool adc_spare_gpio_ok = spare_pin_pull_test(PIN_ADC_SPARE);
    const bool digital_spare_gpio_ok = spare_pin_pull_test(PIN_DIGITAL_SPARE);

    ESP_ERROR_CHECK(configure_i2c());
    ESP_ERROR_CHECK(oled_init());
    const bool oled_visual_transfer_ok = oled_visual_gate();
    ESP_ERROR_CHECK(configure_radar_uart());
    xTaskCreate(radar_task, "ihap50_radar", 4096, NULL, 10, NULL);

    const char *detected_profile = s_bme_present ? "precision" : "standard";
    printf(
        "{\"record_type\":\"boot\",\"schema_version\":\"%s\",\"firmware\":\"%s\",\"idf_version\":\"%s\","
        "\"detected_profile\":\"%s\","
        "\"pins\":{\"radar_rx\":0,\"radar_tx_service\":1,\"door\":3,\"dht\":4,\"adc_spare\":5,\"i2c_sda\":6,\"i2c_scl\":7,\"digital_spare\":10},"
        "\"radar_tx_service_configured\":false,\"adc_spare_pull_test\":%s,\"digital_spare_pull_test\":%s,"
        "\"bme280_present\":%s,\"oled_visual_transfer_ok\":%s}\n",
        SCHEMA_VERSION,
        HARNESS_NAME,
        esp_get_idf_version(),
        detected_profile,
        adc_spare_gpio_ok ? "true" : "false",
        digital_spare_gpio_ok ? "true" : "false",
        s_bme_present ? "true" : "false",
        oled_visual_transfer_ok ? "true" : "false");
    fflush(stdout);

    uint32_t seq = 0;
    while (true) {
        uint8_t chip_id = 0;
        const bool bme_read_ok = bme280_read_chip_id(&chip_id);
        const bool bme_ok = bme_read_ok && chip_id == BME280_CHIP_ID;
        const bool oled_ok = oled_ping();
        const dht_sample_t dht = read_dht11();
        const radar_state_t radar = radar_snapshot();
        const int64_t now_us = esp_timer_get_time();
        const int64_t radar_age_ms = radar.has_valid_frame ? (now_us - radar.last_valid_frame_us) / 1000 : -1;
        const bool radar_fresh = radar.has_valid_frame && radar_age_ms >= 0 && radar_age_ms <= 2000;
        const int door = gpio_get_level(PIN_DOOR);

        printf(
            "{\"record_type\":\"integrated_sample\",\"seq\":%lu,"
            "\"profile\":\"%s\",\"oled_ok\":%s,"
            "\"bme280_present\":%s,\"bme280_ok\":%s,\"bme280_chip_id\":\"0x%02X\","
            "\"dht11_ok\":%s,\"dht11_status\":\"%s\",\"temperature_c\":%.1f,\"humidity_percent\":%.1f,"
            "\"radar_fresh\":%s,\"radar_target_state\":%u,\"radar_valid_frames\":%lu,"
            "\"radar_invalid_frames\":%lu,\"radar_uart_bytes\":%lu,\"door_raw\":%d}\n",
            (unsigned long)seq,
            detected_profile,
            oled_ok ? "true" : "false",
            s_bme_present ? "true" : "false",
            bme_ok ? "true" : "false",
            chip_id,
            dht.valid ? "true" : "false",
            dht.status,
            dht.temperature_c,
            dht.humidity_percent,
            radar_fresh ? "true" : "false",
            radar.target_state,
            (unsigned long)radar.valid_frames,
            (unsigned long)radar.invalid_frames,
            (unsigned long)radar.uart_bytes,
            door);
        fflush(stdout);
        ++seq;
        vTaskDelay(pdMS_TO_TICKS(5000));
    }
}
