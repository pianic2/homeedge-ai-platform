idf_component_register(
    SRCS "usb_reconnect_wrapper.c"
    INCLUDE_DIRS "."
    REQUIRES driver esp_timer
)
