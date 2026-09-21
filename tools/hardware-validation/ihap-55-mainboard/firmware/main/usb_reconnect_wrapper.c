#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

/*
 * Native USB Serial/JTAG on ESP32-C3 can disappear and re-enumerate around reset.
 * IHAP-53 physical validation already established that a short startup guard keeps
 * the host collector from racing the device re-enumeration. Reuse that proven
 * validation-tool pattern here; this is not a product-firmware timing contract.
 */
#define IHAP50_USB_REENUMERATION_GUARD_MS 3500

#define app_main ihap50_original_app_main
#include "main.c"
#undef app_main

void app_main(void)
{
    vTaskDelay(pdMS_TO_TICKS(IHAP50_USB_REENUMERATION_GUARD_MS));

    /* Emitted before peripheral initialization so serial transport can be
       distinguished from later sensor/I2C initialization failures. */
    printf("{\"record_type\":\"harness_ready\",\"usb_reenumeration_guard_ms\":%d}\n",
           IHAP50_USB_REENUMERATION_GUARD_MS);
    fflush(stdout);

    ihap50_original_app_main();
}
