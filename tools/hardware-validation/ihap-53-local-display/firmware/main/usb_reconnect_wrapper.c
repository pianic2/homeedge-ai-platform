#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define IHAP53_USB_REENUMERATION_GUARD_MS 3500

#define app_main ihap53_original_app_main
#include "main.c"
#undef app_main

void app_main(void)
{
    vTaskDelay(pdMS_TO_TICKS(IHAP53_USB_REENUMERATION_GUARD_MS));
    ihap53_original_app_main();
}
