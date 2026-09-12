#include "health_adc.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#define TLA2024_ADDR 0x48
#define TLA2024_CONFIG 0x01
#define TLA2024_CONVERSION 0x00
static i2c_master_dev_handle_t s_adc;
static esp_err_t read_channel(unsigned channel,float *rail_v){
 if(!s_adc||!rail_v||channel>3)return ESP_ERR_INVALID_ARG;
 /* OS=1, MUX=100..111 single-ended, PGA=001 (+/-4.096 V), MODE=1,
    DR=100 (1600 SPS), reserved=00011. TI SBAS846. */
 const unsigned mux=4U+channel; const uint16_t cfg=(1U<<15)|(mux<<12)|(1U<<9)|(1U<<8)|(4U<<5)|0x03U;
 const uint8_t write_cfg[]={TLA2024_CONFIG,(uint8_t)(cfg>>8),(uint8_t)cfg};
 esp_err_t e=i2c_master_transmit(s_adc,write_cfg,sizeof(write_cfg),100); if(e!=ESP_OK)return e;
 vTaskDelay(pdMS_TO_TICKS(2));
 const uint8_t reg=TLA2024_CONVERSION; uint8_t data[2]={0}; e=i2c_master_transmit_receive(s_adc,&reg,1,data,2,100); if(e!=ESP_OK)return e;
 int16_t raw=(int16_t)(((uint16_t)data[0]<<8)|data[1]); raw>>=4;
 /* +/-4.096 V FSR => 2 mV/LSB. Each board input has a 47k/47k divider. */
 *rail_v=(float)raw*0.002f*2.0f; return ESP_OK;
}
esp_err_t ihap55_health_adc_init(i2c_master_bus_handle_t bus){
 if(!bus)return ESP_ERR_INVALID_ARG; const i2c_device_config_t cfg={.dev_addr_length=I2C_ADDR_BIT_LEN_7,.device_address=TLA2024_ADDR,.scl_speed_hz=100000}; return i2c_master_bus_add_device(bus,&cfg,&s_adc);
}
esp_err_t ihap55_health_adc_read(ihap55_rail_health_t *out){
 if(!out)return ESP_ERR_INVALID_ARG; esp_err_t e;
 if((e=read_channel(0,&out->vbus_in_v))!=ESP_OK)return e;
 if((e=read_channel(1,&out->batt_v))!=ESP_OK)return e;
 if((e=read_channel(2,&out->sys5v_v))!=ESP_OK)return e;
 return read_channel(3,&out->sys3v3_v);
}
