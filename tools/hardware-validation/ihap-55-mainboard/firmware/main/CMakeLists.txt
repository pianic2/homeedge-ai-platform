idf_component_register(
    SRCS "usb_reconnect_wrapper.c" "health_adc.c"
    INCLUDE_DIRS "."
    REQUIRES driver esp_timer esp_driver_gpio esp_driver_i2c esp_driver_uart
)
