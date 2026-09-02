#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "driver/gpio.h"
#include "driver/uart.h"
#include "esp_check.h"
#include "esp_err.h"
#include "esp_idf_version.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "sdkconfig.h"

#define IHAP46_SCHEMA_VERSION "1.0.0"
#define IHAP46_FIRMWARE_NAME "ihap46-presence-sensor-harness"
#define LD2410_UART UART_NUM_1
#define LD2410_BAUD 256000
#define UART_RX_BUFFER_SIZE 1024
#define FRAME_BUFFER_SIZE 128

static const char *TAG = "ihap46";

static const uint8_t FRAME_HEADER[] = {0xF4, 0xF3, 0xF2, 0xF1};
static const uint8_t FRAME_FOOTER[] = {0xF8, 0xF7, 0xF6, 0xF5};

typedef struct {
    bool has_valid_frame;
    uint8_t target_state;
    uint16_t moving_distance_cm;
    uint8_t moving_energy;
    uint16_t static_distance_cm;
    uint8_t static_energy;
    uint16_t detection_distance_cm;
    int64_t last_valid_frame_us;
    uint32_t valid_frames;
    uint32_t invalid_frames;
    uint32_t uart_bytes;
} ld2410_state_t;

static ld2410_state_t g_ld_state;
static portMUX_TYPE g_ld_mux = portMUX_INITIALIZER_UNLOCKED;

static bool gpio_enabled(int gpio_num)
{
    return gpio_num >= 0;
}

static bool read_gpio_optional(int gpio_num)
{
    return gpio_enabled(gpio_num) ? gpio_get_level((gpio_num_t)gpio_num) != 0 : false;
}

static uint16_t read_le16(const uint8_t *data)
{
    return (uint16_t)data[0] | ((uint16_t)data[1] << 8);
}

static void register_invalid_frame(void)
{
    portENTER_CRITICAL(&g_ld_mux);
    g_ld_state.invalid_frames++;
    portEXIT_CRITICAL(&g_ld_mux);
}

static bool parse_ld2410_frame(const uint8_t *frame, size_t frame_length)
{
    if (frame_length < 23 || memcmp(frame, FRAME_HEADER, sizeof(FRAME_HEADER)) != 0) {
        return false;
    }

    const uint16_t payload_length = read_le16(&frame[4]);
    const size_t expected_length = (size_t)payload_length + 10U;
    if (expected_length != frame_length || payload_length < 13U) {
        return false;
    }
    if (memcmp(&frame[frame_length - 4U], FRAME_FOOTER, sizeof(FRAME_FOOTER)) != 0) {
        return false;
    }

    const uint8_t *payload = &frame[6];
    if (payload[0] != 0x02 || payload[1] != 0xAA || payload[11] != 0x55 || payload[12] != 0x00) {
        return false;
    }

    portENTER_CRITICAL(&g_ld_mux);
    g_ld_state.has_valid_frame = true;
    g_ld_state.target_state = payload[2];
    g_ld_state.moving_distance_cm = read_le16(&payload[3]);
    g_ld_state.moving_energy = payload[5];
    g_ld_state.static_distance_cm = read_le16(&payload[6]);
    g_ld_state.static_energy = payload[8];
    g_ld_state.detection_distance_cm = read_le16(&payload[9]);
    g_ld_state.last_valid_frame_us = esp_timer_get_time();
    g_ld_state.valid_frames++;
    portEXIT_CRITICAL(&g_ld_mux);
    return true;
}

static void consume_uart_stream(uint8_t *buffer, size_t *used)
{
    while (*used >= sizeof(FRAME_HEADER)) {
        size_t header_index = 0;
        while (header_index + sizeof(FRAME_HEADER) <= *used &&
               memcmp(&buffer[header_index], FRAME_HEADER, sizeof(FRAME_HEADER)) != 0) {
            header_index++;
        }

        if (header_index > 0) {
            memmove(buffer, &buffer[header_index], *used - header_index);
            *used -= header_index;
        }
        if (*used < 6U) {
            return;
        }

        const uint16_t payload_length = read_le16(&buffer[4]);
        const size_t total_length = (size_t)payload_length + 10U;
        if (total_length > FRAME_BUFFER_SIZE || total_length < 10U) {
            register_invalid_frame();
            memmove(buffer, &buffer[1], *used - 1U);
            (*used)--;
            continue;
        }
        if (*used < total_length) {
            return;
        }

        if (!parse_ld2410_frame(buffer, total_length)) {
            register_invalid_frame();
        }
        memmove(buffer, &buffer[total_length], *used - total_length);
        *used -= total_length;
    }
}

static void ld2410_uart_task(void *argument)
{
    (void)argument;
    uint8_t read_buffer[128];
    uint8_t frame_buffer[FRAME_BUFFER_SIZE];
    size_t used = 0;

    while (true) {
        const int count = uart_read_bytes(
            LD2410_UART,
            read_buffer,
            sizeof(read_buffer),
            pdMS_TO_TICKS(100));
        if (count <= 0) {
            continue;
        }

        portENTER_CRITICAL(&g_ld_mux);
        g_ld_state.uart_bytes += (uint32_t)count;
        portEXIT_CRITICAL(&g_ld_mux);

        for (int index = 0; index < count; index++) {
            if (used == sizeof(frame_buffer)) {
                register_invalid_frame();
                memmove(frame_buffer, &frame_buffer[1], sizeof(frame_buffer) - 1U);
                used--;
            }
            frame_buffer[used++] = read_buffer[index];
            consume_uart_stream(frame_buffer, &used);
        }
    }
}

static esp_err_t configure_optional_input(int gpio_num)
{
    if (!gpio_enabled(gpio_num)) {
        return ESP_OK;
    }
    const gpio_config_t config = {
        .pin_bit_mask = 1ULL << (uint32_t)gpio_num,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    return gpio_config(&config);
}

static esp_err_t configure_ld2410_uart(void)
{
    if (!gpio_enabled(CONFIG_IHAP46_LD2410_RX_GPIO)) {
        ESP_LOGW(TAG, "LD2410C UART disabled because RX GPIO is -1");
        return ESP_OK;
    }

    const uart_config_t uart_config = {
        .baud_rate = LD2410_BAUD,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };
    ESP_RETURN_ON_ERROR(uart_driver_install(LD2410_UART, UART_RX_BUFFER_SIZE, 0, 0, NULL, 0), TAG, "uart install");
    ESP_RETURN_ON_ERROR(uart_param_config(LD2410_UART, &uart_config), TAG, "uart config");
    ESP_RETURN_ON_ERROR(
        uart_set_pin(
            LD2410_UART,
            gpio_enabled(CONFIG_IHAP46_LD2410_TX_GPIO) ? CONFIG_IHAP46_LD2410_TX_GPIO : UART_PIN_NO_CHANGE,
            CONFIG_IHAP46_LD2410_RX_GPIO,
            UART_PIN_NO_CHANGE,
            UART_PIN_NO_CHANGE),
        TAG,
        "uart pins");
    return ESP_OK;
}

static ld2410_state_t snapshot_ld_state(void)
{
    ld2410_state_t snapshot;
    portENTER_CRITICAL(&g_ld_mux);
    snapshot = g_ld_state;
    portEXIT_CRITICAL(&g_ld_mux);
    return snapshot;
}

void app_main(void)
{
    memset(&g_ld_state, 0, sizeof(g_ld_state));
    ESP_ERROR_CHECK(configure_optional_input(CONFIG_IHAP46_LD2410_OUT_GPIO));
    ESP_ERROR_CHECK(configure_optional_input(CONFIG_IHAP46_PIR_OUT_GPIO));
    ESP_ERROR_CHECK(configure_ld2410_uart());

    if (gpio_enabled(CONFIG_IHAP46_LD2410_RX_GPIO)) {
        xTaskCreate(ld2410_uart_task, "ld2410_uart", 4096, NULL, 10, NULL);
    }

    printf(
        "{\"record_type\":\"boot\",\"schema_version\":\"%s\","
        "\"firmware\":\"%s\",\"idf_version\":\"%s\","
        "\"scope\":\"laboratory_evidence_only\","
        "\"ld2410c\":{\"uart_baud\":%d,\"rx_gpio\":%d,\"tx_gpio\":%d,\"out_gpio\":%d},"
        "\"pir\":{\"out_gpio\":%d}}\n",
        IHAP46_SCHEMA_VERSION,
        IHAP46_FIRMWARE_NAME,
        esp_get_idf_version(),
        LD2410_BAUD,
        CONFIG_IHAP46_LD2410_RX_GPIO,
        CONFIG_IHAP46_LD2410_TX_GPIO,
        CONFIG_IHAP46_LD2410_OUT_GPIO,
        CONFIG_IHAP46_PIR_OUT_GPIO);
    fflush(stdout);

    uint32_t sequence = 0;
    while (true) {
        const int64_t now_us = esp_timer_get_time();
        const ld2410_state_t state = snapshot_ld_state();
        const int64_t frame_age_ms = state.has_valid_frame ? (now_us - state.last_valid_frame_us) / 1000 : -1;
        const bool frame_fresh = state.has_valid_frame && frame_age_ms >= 0 && frame_age_ms <= CONFIG_IHAP46_UART_TIMEOUT_MS;
        const bool uart_presence = frame_fresh && state.target_state != 0;
        const bool ld_out = read_gpio_optional(CONFIG_IHAP46_LD2410_OUT_GPIO);
        const bool pir_out = read_gpio_optional(CONFIG_IHAP46_PIR_OUT_GPIO);

        printf(
            "{\"record_type\":\"sample\",\"schema_version\":\"%s\","
            "\"seq\":%" PRIu32 ",\"uptime_ms\":%" PRIi64 ","
            "\"ld2410c\":{\"uart_frame_valid\":%s,\"uart_presence\":%s,"
            "\"frame_age_ms\":%" PRIi64 ",\"target_state\":%u,"
            "\"moving_distance_cm\":%u,\"moving_energy\":%u,"
            "\"static_distance_cm\":%u,\"static_energy\":%u,"
            "\"detection_distance_cm\":%u,\"out_enabled\":%s,\"out\":%s,"
            "\"valid_frames\":%" PRIu32 ",\"invalid_frames\":%" PRIu32 ",\"uart_bytes\":%" PRIu32 "},"
            "\"pir\":{\"enabled\":%s,\"out\":%s}}\n",
            IHAP46_SCHEMA_VERSION,
            sequence++,
            now_us / 1000,
            frame_fresh ? "true" : "false",
            uart_presence ? "true" : "false",
            frame_age_ms,
            state.target_state,
            state.moving_distance_cm,
            state.moving_energy,
            state.static_distance_cm,
            state.static_energy,
            state.detection_distance_cm,
            gpio_enabled(CONFIG_IHAP46_LD2410_OUT_GPIO) ? "true" : "false",
            ld_out ? "true" : "false",
            state.valid_frames,
            state.invalid_frames,
            state.uart_bytes,
            gpio_enabled(CONFIG_IHAP46_PIR_OUT_GPIO) ? "true" : "false",
            pir_out ? "true" : "false");
        fflush(stdout);
        vTaskDelay(pdMS_TO_TICKS(CONFIG_IHAP46_SAMPLE_PERIOD_MS));
    }
}
