#pragma once
#include "driver/i2c_master.h"
#include "esp_err.h"
typedef struct { float vbus_in_v; float batt_v; float sys5v_v; float sys3v3_v; } ihap55_rail_health_t;
esp_err_t ihap55_health_adc_init(i2c_master_bus_handle_t bus);
esp_err_t ihap55_health_adc_read(ihap55_rail_health_t *out);
