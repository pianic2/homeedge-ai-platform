idf_component_register(
    SRCS "usb_reconnect_wrapper.c"
    INCLUDE_DIRS "."
    PRIV_REQUIRES
	esp_timer
	esp_driver_i2c
	esp_driver_gpio
)
