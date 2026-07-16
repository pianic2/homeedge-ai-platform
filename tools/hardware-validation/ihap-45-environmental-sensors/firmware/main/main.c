#include <inttypes.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "driver/gpio.h"
#include "driver/i2c_master.h"
#include "esp_check.h"
#include "esp_err.h"
#include "esp_idf_version.h"
#include "esp_system.h"
#include "esp_rom_sys.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define HARNESS_SCHEMA_VERSION "1.0.0"
#define HARNESS_FIRMWARE_NAME "ihap-45-environmental-sensor-harness"

#define DHT11_SENSOR_ID "DHT11-OWNED-01"
#define DHT22_SENSOR_ID "DHT22-OWNED-01"
#define BME280_SENSOR_ID "BME280-OWNED-01"

#define BME280_ADDRESS_LOW 0x76
#define BME280_ADDRESS_HIGH 0x77
#define BME280_REG_CHIP_ID 0xD0
#define BME280_REG_RESET 0xE0
#define BME280_REG_CTRL_HUM 0xF2
#define BME280_REG_CTRL_MEAS 0xF4
#define BME280_REG_CONFIG 0xF5
#define BME280_REG_TEMP_MSB 0xFA
#define BME280_REG_CALIB00 0x88
#define BME280_REG_CALIB26 0xE1
#define BME280_CHIP_ID 0x60
#define BMP280_CHIP_ID 0x58
#define BMP280_SAMPLE_CHIP_ID_1 0x56
#define BMP280_SAMPLE_CHIP_ID_2 0x57
#define BME280_RESET_COMMAND 0xB6

#define BME280_OSRS_H_X1 0x01
#define BME280_OSRS_T_X1 (0x01 << 5)
#define BME280_OSRS_P_SKIPPED (0x00 << 2)
#define BME280_MODE_FORCED 0x01

#define I2C_TIMEOUT_MS 100
#define DHT_BIT_THRESHOLD_US 50

#ifndef CONFIG_IHAP45_DHT11_GPIO
#define CONFIG_IHAP45_DHT11_GPIO 3
#endif
#ifndef CONFIG_IHAP45_DHT22_GPIO
#define CONFIG_IHAP45_DHT22_GPIO 4
#endif
#ifndef CONFIG_IHAP45_I2C_SDA_GPIO
#define CONFIG_IHAP45_I2C_SDA_GPIO 5
#endif
#ifndef CONFIG_IHAP45_I2C_SCL_GPIO
#define CONFIG_IHAP45_I2C_SCL_GPIO 6
#endif
#ifndef CONFIG_IHAP45_SAMPLE_INTERVAL_MS
#define CONFIG_IHAP45_SAMPLE_INTERVAL_MS 5000
#endif
#ifndef CONFIG_IHAP45_I2C_FREQUENCY_HZ
#define CONFIG_IHAP45_I2C_FREQUENCY_HZ 100000
#endif

#if CONFIG_IHAP45_DHT11_GPIO == 2 || CONFIG_IHAP45_DHT22_GPIO == 2 || \
    CONFIG_IHAP45_I2C_SDA_GPIO == 2 || CONFIG_IHAP45_I2C_SCL_GPIO == 2
#error "GPIO2 is excluded from the IHAP-45 validation harness by ADR-0001."
#endif

#if CONFIG_IHAP45_DHT11_GPIO == CONFIG_IHAP45_DHT22_GPIO || \
    CONFIG_IHAP45_DHT11_GPIO == CONFIG_IHAP45_I2C_SDA_GPIO || \
    CONFIG_IHAP45_DHT11_GPIO == CONFIG_IHAP45_I2C_SCL_GPIO || \
    CONFIG_IHAP45_DHT22_GPIO == CONFIG_IHAP45_I2C_SDA_GPIO || \
    CONFIG_IHAP45_DHT22_GPIO == CONFIG_IHAP45_I2C_SCL_GPIO || \
    CONFIG_IHAP45_I2C_SDA_GPIO == CONFIG_IHAP45_I2C_SCL_GPIO
#error "Every IHAP-45 signal must use a distinct GPIO."
#endif

typedef enum {
    DHT_KIND_11 = 11,
    DHT_KIND_22 = 22,
} dht_kind_t;

typedef enum {
    SAMPLE_OK = 0,
    SAMPLE_ERR_NO_RESPONSE,
    SAMPLE_ERR_TIMEOUT,
    SAMPLE_ERR_CHECKSUM,
    SAMPLE_ERR_RANGE,
    SAMPLE_ERR_I2C,
    SAMPLE_ERR_UNSUPPORTED_DEVICE,
    SAMPLE_ERR_NOT_INITIALIZED,
} sample_status_t;

typedef struct {
    bool valid;
    double temperature_c;
    double humidity_percent;
    sample_status_t status;
    int64_t read_duration_us;
} sensor_sample_t;

typedef struct {
    uint16_t dig_t1;
    int16_t dig_t2;
    int16_t dig_t3;
    uint8_t dig_h1;
    int16_t dig_h2;
    uint8_t dig_h3;
    int16_t dig_h4;
    int16_t dig_h5;
    int8_t dig_h6;
} bme280_calibration_t;

typedef struct {
    i2c_master_bus_handle_t bus;
    i2c_master_dev_handle_t device;
    uint8_t address;
    uint8_t chip_id;
    bool initialized;
    bme280_calibration_t calibration;
} bme280_context_t;

static portMUX_TYPE s_dht_lock = portMUX_INITIALIZER_UNLOCKED;
static bme280_context_t s_bme280 = {0};

static const char *status_code(sample_status_t status)
{
    switch (status) {
        case SAMPLE_OK:
            return "OK";
        case SAMPLE_ERR_NO_RESPONSE:
            return "NO_RESPONSE";
        case SAMPLE_ERR_TIMEOUT:
            return "TIMEOUT";
        case SAMPLE_ERR_CHECKSUM:
            return "CHECKSUM";
        case SAMPLE_ERR_RANGE:
            return "OUT_OF_RANGE";
        case SAMPLE_ERR_I2C:
            return "I2C_ERROR";
        case SAMPLE_ERR_UNSUPPORTED_DEVICE:
            return "UNSUPPORTED_DEVICE";
        case SAMPLE_ERR_NOT_INITIALIZED:
            return "NOT_INITIALIZED";
        default:
            return "UNKNOWN";
    }
}

static const char *detected_device_name(uint8_t chip_id)
{
    switch (chip_id) {
        case BME280_CHIP_ID:
            return "BME280";
        case BMP280_CHIP_ID:
            return "BMP280";
        case BMP280_SAMPLE_CHIP_ID_1:
            return "BMP280_SAMPLE_0x56";
        case BMP280_SAMPLE_CHIP_ID_2:
            return "BMP280_SAMPLE_0x57";
        default:
            return "UNKNOWN";
    }
}

static int16_t sign_extend_12(uint16_t value)
{
    if ((value & 0x0800U) != 0U) {
        value |= 0xF000U;
    }
    return (int16_t)value;
}

static uint16_t read_u16_le(const uint8_t *buffer)
{
    return (uint16_t)buffer[0] | ((uint16_t)buffer[1] << 8);
}

static int16_t read_s16_le(const uint8_t *buffer)
{
    return (int16_t)read_u16_le(buffer);
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

static void dht_prepare_gpio(gpio_num_t gpio)
{
    gpio_config_t config = {
        .pin_bit_mask = 1ULL << gpio,
        .mode = GPIO_MODE_INPUT_OUTPUT_OD,
#if CONFIG_IHAP45_DHT_INTERNAL_PULLUPS
        .pull_up_en = GPIO_PULLUP_ENABLE,
#else
        .pull_up_en = GPIO_PULLUP_DISABLE,
#endif
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&config));
    ESP_ERROR_CHECK(gpio_set_level(gpio, 1));
}

static sensor_sample_t dht_read(gpio_num_t gpio, dht_kind_t kind)
{
    sensor_sample_t sample = {
        .valid = false,
        .temperature_c = NAN,
        .humidity_percent = NAN,
        .status = SAMPLE_ERR_TIMEOUT,
        .read_duration_us = 0,
    };
    uint8_t data[5] = {0};
    uint32_t pulse_duration = 0;
    const int64_t read_start = esp_timer_get_time();

    gpio_set_direction(gpio, GPIO_MODE_OUTPUT_OD);
    gpio_set_level(gpio, 0);
    esp_rom_delay_us(kind == DHT_KIND_11 ? 20000 : 2000);

    portENTER_CRITICAL(&s_dht_lock);
    gpio_set_level(gpio, 1);
    esp_rom_delay_us(30);
    gpio_set_direction(gpio, GPIO_MODE_INPUT);

    if (!wait_while_level(gpio, 1, 120, &pulse_duration)) {
        sample.status = SAMPLE_ERR_NO_RESPONSE;
        goto done;
    }
    if (!wait_while_level(gpio, 0, 120, &pulse_duration)) {
        sample.status = SAMPLE_ERR_NO_RESPONSE;
        goto done;
    }
    if (!wait_while_level(gpio, 1, 120, &pulse_duration)) {
        sample.status = SAMPLE_ERR_NO_RESPONSE;
        goto done;
    }

    for (int bit_index = 0; bit_index < 40; ++bit_index) {
        uint32_t low_duration = 0;
        uint32_t high_duration = 0;
        if (!wait_while_level(gpio, 0, 100, &low_duration)) {
            sample.status = SAMPLE_ERR_TIMEOUT;
            goto done;
        }
        if (!wait_while_level(gpio, 1, 120, &high_duration)) {
            sample.status = SAMPLE_ERR_TIMEOUT;
            goto done;
        }
        data[bit_index / 8] <<= 1;
        if (high_duration > DHT_BIT_THRESHOLD_US) {
            data[bit_index / 8] |= 1U;
        }
    }

    if ((uint8_t)(data[0] + data[1] + data[2] + data[3]) != data[4]) {
        sample.status = SAMPLE_ERR_CHECKSUM;
        goto done;
    }

    if (kind == DHT_KIND_11) {
        sample.humidity_percent = (double)data[0] + ((double)data[1] / 10.0);
        sample.temperature_c = (double)data[2] + ((double)(data[3] & 0x7FU) / 10.0);
        if ((data[3] & 0x80U) != 0U) {
            sample.temperature_c = -sample.temperature_c;
        }
    } else {
        const uint16_t raw_humidity = ((uint16_t)data[0] << 8) | data[1];
        const uint16_t raw_temperature = ((uint16_t)(data[2] & 0x7FU) << 8) | data[3];
        sample.humidity_percent = (double)raw_humidity / 10.0;
        sample.temperature_c = (double)raw_temperature / 10.0;
        if ((data[2] & 0x80U) != 0U) {
            sample.temperature_c = -sample.temperature_c;
        }
    }

    if (!isfinite(sample.temperature_c) || !isfinite(sample.humidity_percent) ||
        sample.humidity_percent < 0.0 || sample.humidity_percent > 100.0 ||
        sample.temperature_c < -50.0 || sample.temperature_c > 100.0) {
        sample.status = SAMPLE_ERR_RANGE;
        goto done;
    }

    sample.valid = true;
    sample.status = SAMPLE_OK;

done:
    gpio_set_direction(gpio, GPIO_MODE_INPUT);
    portEXIT_CRITICAL(&s_dht_lock);
    sample.read_duration_us = esp_timer_get_time() - read_start;
    return sample;
}

static esp_err_t bme280_read_registers(uint8_t register_address, uint8_t *buffer, size_t length)
{
    return i2c_master_transmit_receive(
        s_bme280.device,
        &register_address,
        1,
        buffer,
        length,
        I2C_TIMEOUT_MS
    );
}

static esp_err_t bme280_write_register(uint8_t register_address, uint8_t value)
{
    const uint8_t payload[2] = {register_address, value};
    return i2c_master_transmit(s_bme280.device, payload, sizeof(payload), I2C_TIMEOUT_MS);
}

static esp_err_t bme280_read_calibration(void)
{
    uint8_t calib_primary[26] = {0};
    uint8_t calib_humidity[7] = {0};

    ESP_RETURN_ON_ERROR(
        bme280_read_registers(BME280_REG_CALIB00, calib_primary, sizeof(calib_primary)),
        "IHAP45",
        "Failed to read BME280 primary calibration"
    );
    ESP_RETURN_ON_ERROR(
        bme280_read_registers(BME280_REG_CALIB26, calib_humidity, sizeof(calib_humidity)),
        "IHAP45",
        "Failed to read BME280 humidity calibration"
    );

    s_bme280.calibration.dig_t1 = read_u16_le(&calib_primary[0]);
    s_bme280.calibration.dig_t2 = read_s16_le(&calib_primary[2]);
    s_bme280.calibration.dig_t3 = read_s16_le(&calib_primary[4]);
    s_bme280.calibration.dig_h1 = calib_primary[25];
    s_bme280.calibration.dig_h2 = read_s16_le(&calib_humidity[0]);
    s_bme280.calibration.dig_h3 = calib_humidity[2];
    s_bme280.calibration.dig_h4 = sign_extend_12(
        ((uint16_t)calib_humidity[3] << 4) | (calib_humidity[4] & 0x0FU)
    );
    s_bme280.calibration.dig_h5 = sign_extend_12(
        ((uint16_t)calib_humidity[5] << 4) | (calib_humidity[4] >> 4)
    );
    s_bme280.calibration.dig_h6 = (int8_t)calib_humidity[6];

    return ESP_OK;
}

static void bme280_emit_probe(const char *status)
{
    printf(
        "{\"record_type\":\"sensor_probe\",\"schema_version\":\"%s\","
        "\"sensor_id\":\"%s\",\"i2c_address\":\"0x%02X\","
        "\"chip_id\":\"0x%02X\",\"detected_type\":\"%s\","
        "\"humidity_supported\":%s,"
        "\"status\":\"%s\"}\n",
        HARNESS_SCHEMA_VERSION,
        BME280_SENSOR_ID,
        s_bme280.address,
        s_bme280.chip_id,
        detected_device_name(s_bme280.chip_id),
        s_bme280.chip_id == BME280_CHIP_ID ? "true" : "false",
        status
    );
    fflush(stdout);
}

static esp_err_t bme280_initialize(void)
{
    i2c_master_bus_config_t bus_config = {
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .i2c_port = I2C_NUM_0,
        .scl_io_num = CONFIG_IHAP45_I2C_SCL_GPIO,
        .sda_io_num = CONFIG_IHAP45_I2C_SDA_GPIO,
        .glitch_ignore_cnt = 7,
#if CONFIG_IHAP45_I2C_INTERNAL_PULLUPS
        .flags.enable_internal_pullup = true,
#else
        .flags.enable_internal_pullup = false,
#endif
    };

    ESP_RETURN_ON_ERROR(i2c_new_master_bus(&bus_config, &s_bme280.bus), "IHAP45", "I2C bus init failed");

    uint8_t selected_address = 0;
    if (i2c_master_probe(s_bme280.bus, BME280_ADDRESS_LOW, I2C_TIMEOUT_MS) == ESP_OK) {
        selected_address = BME280_ADDRESS_LOW;
    } else if (i2c_master_probe(s_bme280.bus, BME280_ADDRESS_HIGH, I2C_TIMEOUT_MS) == ESP_OK) {
        selected_address = BME280_ADDRESS_HIGH;
    } else {
        s_bme280.address = 0;
        s_bme280.chip_id = 0;
        bme280_emit_probe("I2C_NOT_FOUND");
        return ESP_ERR_NOT_FOUND;
    }

    i2c_device_config_t device_config = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = selected_address,
        .scl_speed_hz = CONFIG_IHAP45_I2C_FREQUENCY_HZ,
        .scl_wait_us = 20000,
    };
    ESP_RETURN_ON_ERROR(
        i2c_master_bus_add_device(s_bme280.bus, &device_config, &s_bme280.device),
        "IHAP45",
        "I2C device registration failed"
    );

    s_bme280.address = selected_address;
    ESP_RETURN_ON_ERROR(
        bme280_read_registers(BME280_REG_CHIP_ID, &s_bme280.chip_id, 1),
        "IHAP45",
        "Chip ID read failed"
    );

    if (s_bme280.chip_id != BME280_CHIP_ID) {
        bme280_emit_probe("REJECTED_NOT_BME280");
        return ESP_ERR_NOT_SUPPORTED;
    }

    ESP_RETURN_ON_ERROR(bme280_write_register(BME280_REG_RESET, BME280_RESET_COMMAND), "IHAP45", "Reset failed");
    vTaskDelay(pdMS_TO_TICKS(10));
    ESP_RETURN_ON_ERROR(bme280_read_calibration(), "IHAP45", "Calibration read failed");

    ESP_RETURN_ON_ERROR(
        bme280_write_register(BME280_REG_CTRL_HUM, BME280_OSRS_H_X1),
        "IHAP45",
        "Humidity oversampling configuration failed"
    );
    ESP_RETURN_ON_ERROR(bme280_write_register(BME280_REG_CONFIG, 0x00), "IHAP45", "Config write failed");

    s_bme280.initialized = true;
    bme280_emit_probe("OK");
    return ESP_OK;
}

static sensor_sample_t bme280_read_temperature_humidity(void)
{
    sensor_sample_t sample = {
        .valid = false,
        .temperature_c = NAN,
        .humidity_percent = NAN,
        .status = SAMPLE_ERR_NOT_INITIALIZED,
        .read_duration_us = 0,
    };
    const int64_t read_start = esp_timer_get_time();

    if (!s_bme280.initialized) {
        sample.status = s_bme280.chip_id == BME280_CHIP_ID
            ? SAMPLE_ERR_NOT_INITIALIZED
            : SAMPLE_ERR_UNSUPPORTED_DEVICE;
        sample.read_duration_us = esp_timer_get_time() - read_start;
        return sample;
    }

    const uint8_t ctrl_meas = BME280_OSRS_T_X1 | BME280_OSRS_P_SKIPPED | BME280_MODE_FORCED;
    if (bme280_write_register(BME280_REG_CTRL_HUM, BME280_OSRS_H_X1) != ESP_OK ||
        bme280_write_register(BME280_REG_CTRL_MEAS, ctrl_meas) != ESP_OK) {
        sample.status = SAMPLE_ERR_I2C;
        sample.read_duration_us = esp_timer_get_time() - read_start;
        return sample;
    }

    vTaskDelay(pdMS_TO_TICKS(10));

    uint8_t raw[5] = {0};
    if (bme280_read_registers(BME280_REG_TEMP_MSB, raw, sizeof(raw)) != ESP_OK) {
        sample.status = SAMPLE_ERR_I2C;
        sample.read_duration_us = esp_timer_get_time() - read_start;
        return sample;
    }

    const int32_t adc_temperature = ((int32_t)raw[0] << 12) | ((int32_t)raw[1] << 4) | (raw[2] >> 4);
    const int32_t adc_humidity = ((int32_t)raw[3] << 8) | raw[4];
    const bme280_calibration_t *cal = &s_bme280.calibration;

    const double var_t1 = (((double)adc_temperature / 16384.0) - ((double)cal->dig_t1 / 1024.0)) * (double)cal->dig_t2;
    const double var_t2_base = ((double)adc_temperature / 131072.0) - ((double)cal->dig_t1 / 8192.0);
    const double var_t2 = var_t2_base * var_t2_base * (double)cal->dig_t3;
    const double t_fine = var_t1 + var_t2;
    sample.temperature_c = t_fine / 5120.0;

    double humidity = t_fine - 76800.0;
    humidity = ((double)adc_humidity -
                (((double)cal->dig_h4 * 64.0) +
                 (((double)cal->dig_h5 / 16384.0) * humidity))) *
               (((double)cal->dig_h2 / 65536.0) *
                (1.0 + (((double)cal->dig_h6 / 67108864.0) * humidity *
                        (1.0 + (((double)cal->dig_h3 / 67108864.0) * humidity)))));
    humidity = humidity * (1.0 - ((double)cal->dig_h1 * humidity / 524288.0));
    if (humidity > 100.0) {
        humidity = 100.0;
    } else if (humidity < 0.0) {
        humidity = 0.0;
    }
    sample.humidity_percent = humidity;

    if (!isfinite(sample.temperature_c) || !isfinite(sample.humidity_percent) ||
        sample.temperature_c < -50.0 || sample.temperature_c > 100.0 ||
        sample.humidity_percent < 0.0 || sample.humidity_percent > 100.0) {
        sample.status = SAMPLE_ERR_RANGE;
        sample.read_duration_us = esp_timer_get_time() - read_start;
        return sample;
    }

    sample.valid = true;
    sample.status = SAMPLE_OK;
    sample.read_duration_us = esp_timer_get_time() - read_start;
    return sample;
}

static void emit_sample(
    uint64_t batch_id,
    int64_t uptime_ms,
    const char *sensor_id,
    const char *sensor_type,
    const sensor_sample_t *sample
)
{
    printf(
        "{\"record_type\":\"sample\",\"schema_version\":\"%s\","
        "\"batch_id\":%" PRIu64 ",\"uptime_ms\":%" PRId64 ","
        "\"sensor_id\":\"%s\",\"sensor_type\":\"%s\","
        "\"valid\":%s,\"error_code\":",
        HARNESS_SCHEMA_VERSION,
        batch_id,
        uptime_ms,
        sensor_id,
        sensor_type,
        sample->valid ? "true" : "false"
    );

    if (sample->status == SAMPLE_OK) {
        printf("null");
    } else {
        printf("\"%s\"", status_code(sample->status));
    }

    if (sample->valid) {
        printf(
            ",\"temperature_c\":%.3f,\"humidity_percent\":%.3f",
            sample->temperature_c,
            sample->humidity_percent
        );
    } else {
        printf(",\"temperature_c\":null,\"humidity_percent\":null");
    }

    printf(",\"read_duration_us\":%" PRId64 "}\n", sample->read_duration_us);
    fflush(stdout);
}

static void emit_boot_record(void)
{
    printf(
        "{\"record_type\":\"harness_boot\",\"schema_version\":\"%s\","
        "\"firmware\":\"%s\",\"idf_version\":\"%s\","
        "\"sample_interval_ms\":%d,\"measurement_channels\":[\"temperature_c\",\"humidity_percent\"],"
        "\"pins\":{\"dht11_data\":%d,\"dht22_data\":%d,"
        "\"i2c_sda\":%d,\"i2c_scl\":%d},"
        "\"i2c_frequency_hz\":%d}\n",
        HARNESS_SCHEMA_VERSION,
        HARNESS_FIRMWARE_NAME,
        esp_get_idf_version(),
        CONFIG_IHAP45_SAMPLE_INTERVAL_MS,
        CONFIG_IHAP45_DHT11_GPIO,
        CONFIG_IHAP45_DHT22_GPIO,
        CONFIG_IHAP45_I2C_SDA_GPIO,
        CONFIG_IHAP45_I2C_SCL_GPIO,
        CONFIG_IHAP45_I2C_FREQUENCY_HZ
    );
    fflush(stdout);
}

void app_main(void)
{
    dht_prepare_gpio((gpio_num_t)CONFIG_IHAP45_DHT11_GPIO);
    dht_prepare_gpio((gpio_num_t)CONFIG_IHAP45_DHT22_GPIO);

    emit_boot_record();
    (void)bme280_initialize();

    vTaskDelay(pdMS_TO_TICKS(2000));

    uint64_t batch_id = 0;
    TickType_t next_wake = xTaskGetTickCount();
    while (true) {
        ++batch_id;
        const int64_t uptime_ms = esp_timer_get_time() / 1000;

        const sensor_sample_t dht11 = dht_read((gpio_num_t)CONFIG_IHAP45_DHT11_GPIO, DHT_KIND_11);
        vTaskDelay(pdMS_TO_TICKS(20));
        const sensor_sample_t dht22 = dht_read((gpio_num_t)CONFIG_IHAP45_DHT22_GPIO, DHT_KIND_22);
        const sensor_sample_t bme280 = bme280_read_temperature_humidity();

        emit_sample(batch_id, uptime_ms, DHT11_SENSOR_ID, "DHT11", &dht11);
        emit_sample(batch_id, uptime_ms, DHT22_SENSOR_ID, "DHT22", &dht22);
        emit_sample(batch_id, uptime_ms, BME280_SENSOR_ID, "BME280", &bme280);

        vTaskDelayUntil(&next_wake, pdMS_TO_TICKS(CONFIG_IHAP45_SAMPLE_INTERVAL_MS));
    }
}
