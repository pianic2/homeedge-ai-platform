#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

/*
 * ESP32-C3 native USB disappears briefly when RST is pressed.  The host
 * collector reconnects successfully, but the original harness emitted its
 * one-shot boot and sensor-probe records before Linux had recreated the
 * serial device.  Delay the validation application startup so those records
 * are emitted only after USB re-enumeration has had time to complete.
 *
 * This delay belongs exclusively to the IHAP-45 validation harness.  It is
 * not production firmware behavior and does not define the final node boot
 * sequence.
 */
#define IHAP45_USB_REENUMERATION_GUARD_MS 3500

#define app_main ihap45_original_app_main
#include "main.c"
#undef app_main

void app_main(void)
{
    vTaskDelay(pdMS_TO_TICKS(IHAP45_USB_REENUMERATION_GUARD_MS));
    ihap45_original_app_main();
}
