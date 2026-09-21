#include "health_adc.h"

#include <stdint.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define TLA2024_ADDR 0x48
#define TLA2024_CONFIG 0x01
#define TLA2024_CONVERSION 0x00
#define I2C_TIMEOUT_MS 100

static i2c_master_dev_handle_t s_adc;

static esp_err_t read_channel(unsigned channel, float *rail_v)
{
    if (s_adc == NULL || rail_v == NULL || channel > 3) {
        return ESP_ERR_INVALID_ARG;
    }

    /* OS=1, MUX=100..111 single-ended, PGA=001 (+/-4.096 V),
       MODE=1, DR=100 (1600 SPS), comparator disabled. */
    const uint16_t config = (uint16_t)((1U << 15) | ((4U + channel) << 12) |
                                       (1U << 9) | (1U << 8) | (4U << 5) | 0x03U);
    const uint8_t write_config[] = {
        TLA2024_CONFIG, (uint8_t)(config >> 8), (uint8_t)config,
    };
    esp_err_t result = i2c_master_transmit(s_adc, write_config,
                                           sizeof(write_config), I2C_TIMEOUT_MS);
    if (result != ESP_OK) {
        return result;
    }

    /* 1600 SPS conversion period is 0.625 ms; allow more than 2 periods. */
    vTaskDelay(pdMS_TO_TICKS(2));
    const uint8_t register_address = TLA2024_CONVERSION;
    uint8_t data[2] = {0};
    result = i2c_master_transmit_receive(s_adc, &register_address, 1,
                                         data, sizeof(data), I2C_TIMEOUT_MS);
    if (result != ESP_OK) {
        return result;
    }

    const int16_t word = (int16_t)(((uint16_t)data[0] << 8) | data[1]);
    const int16_t code = word / 16; /* signed 12-bit left-aligned conversion */
    /* +/-4.096 V FSR => 2 mV/LSB. Each board input has a 47k/47k divider. */
    *rail_v = (float)code * 0.004f;
    return ESP_OK;
}

esp_err_t ihap55_health_adc_init(i2c_master_bus_handle_t bus)
{
    if (bus == NULL) {
        return ESP_ERR_INVALID_ARG;
    }
    const i2c_device_config_t config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = TLA2024_ADDR,
        .scl_speed_hz = 100000,
    };
    return i2c_master_bus_add_device(bus, &config, &s_adc);
}

esp_err_t ihap55_health_adc_read(ihap55_rail_health_t *out)
{
    if (out == NULL) {
        return ESP_ERR_INVALID_ARG;
    }
    esp_err_t result = read_channel(0, &out->vbus_in_v);
    if (result != ESP_OK) {
        return result;
    }
    result = read_channel(1, &out->batt_v);
    if (result != ESP_OK) {
        return result;
    }
    result = read_channel(2, &out->sys5v_v);
    if (result != ESP_OK) {
        return result;
    }
    return read_channel(3, &out->sys3v3_v);
}
