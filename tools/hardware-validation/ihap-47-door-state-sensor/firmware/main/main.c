#include <ctype.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "driver/gpio.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_rom_sys.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define SCHEMA_VERSION "1.0.0"
#define HARNESS_VERSION "0.1.0"
#define DOOR_CONTACT_GPIO GPIO_NUM_6
#define DEFAULT_SAMPLE_PERIOD_US 250U
#define MIN_SAMPLE_PERIOD_US 250U
#define MAX_SAMPLE_PERIOD_US 10000U
#define MAX_TRANSITIONS 1024U
#define TOKEN_MAX_LEN 48U
#define COMMAND_LINE_MAX_LEN 192U

static const char *TAG = "ihap47_door_harness";

typedef struct
{
    int64_t offset_us;
    int raw_level;
} transition_t;

typedef struct
{
    bool active;
    bool overflow;
    char test_id[TOKEN_MAX_LEN];
    char specimen_id[TOKEN_MAX_LEN];
    int64_t start_us;
    int initial_level;
    int last_level;
    uint32_t sample_period_us;
    size_t transition_count;
    transition_t transitions[MAX_TRANSITIONS];
} capture_state_t;

static capture_state_t g_capture = {
    .active = false,
    .overflow = false,
    .test_id = "UNSET",
    .specimen_id = "UNSET",
    .start_us = 0,
    .initial_level = -1,
    .last_level = -1,
    .sample_period_us = DEFAULT_SAMPLE_PERIOD_US,
    .transition_count = 0,
};

static portMUX_TYPE g_capture_lock = portMUX_INITIALIZER_UNLOCKED;

static const char *circuit_state_from_level(int level)
{
    return level == 0 ? "closed" : "open";
}

static void emit_common_prefix(const char *record_type)
{
    printf("{\"record_type\":\"%s\",\"schema_version\":\"%s\",\"harness_version\":\"%s\"",
           record_type,
           SCHEMA_VERSION,
           HARNESS_VERSION);
}

static void emit_error(const char *code, const char *message)
{
    emit_common_prefix("error");
    printf(",\"error_code\":\"%s\",\"message\":\"%s\"}\n", code, message);
    fflush(stdout);
}

static bool sanitize_token(const char *input, char *output, size_t output_size)
{
    size_t length = 0;

    if (input == NULL || output == NULL || output_size < 2)
    {
        return false;
    }

    while (*input != '\0' && length + 1 < output_size)
    {
        unsigned char c = (unsigned char)*input;

        if (!(isalnum(c) || c == '-' || c == '_'))
        {
            return false;
        }

        output[length++] = (char)c;
        input++;
    }

    if (*input != '\0' || length == 0)
    {
        return false;
    }

    output[length] = '\0';
    return true;
}

static void emit_status(void)
{
    bool active;
    bool overflow;
    int initial_level;
    int last_level;
    uint32_t sample_period_us;
    size_t transition_count;
    char test_id[TOKEN_MAX_LEN];
    char specimen_id[TOKEN_MAX_LEN];

    portENTER_CRITICAL(&g_capture_lock);
    active = g_capture.active;
    overflow = g_capture.overflow;
    initial_level = g_capture.initial_level;
    last_level = g_capture.last_level;
    sample_period_us = g_capture.sample_period_us;
    transition_count = g_capture.transition_count;
    strlcpy(test_id, g_capture.test_id, sizeof(test_id));
    strlcpy(specimen_id, g_capture.specimen_id, sizeof(specimen_id));
    portEXIT_CRITICAL(&g_capture_lock);

    emit_common_prefix("status");
    printf(",\"gpio\":%d,\"pull\":\"internal_up\",\"contact_to\":\"ground\","
           "\"sample_period_us\":%" PRIu32 ",\"capture_active\":%s,"
           "\"test_id\":\"%s\",\"specimen_id\":\"%s\","
           "\"initial_level\":%d,\"last_level\":%d,"
           "\"transition_count\":%u,\"buffer_overflow\":%s}\n",
           (int)DOOR_CONTACT_GPIO,
           sample_period_us,
           active ? "true" : "false",
           test_id,
           specimen_id,
           initial_level,
           last_level,
           (unsigned)transition_count,
           overflow ? "true" : "false");
    fflush(stdout);
}

static void emit_snapshot(void)
{
    int level = gpio_get_level(DOOR_CONTACT_GPIO);
    int64_t uptime_us = esp_timer_get_time();

    emit_common_prefix("snapshot");
    printf(",\"uptime_us\":%" PRId64 ",\"gpio\":%d,\"raw_level\":%d,"
           "\"circuit_state\":\"%s\",\"interpretation\":\"electrical_only\"}\n",
           uptime_us,
           (int)DOOR_CONTACT_GPIO,
           level,
           circuit_state_from_level(level));
    fflush(stdout);
}

static void start_capture(const char *test_token, const char *specimen_token)
{
    char test_id[TOKEN_MAX_LEN];
    char specimen_id[TOKEN_MAX_LEN];
    int initial_level;
    int64_t start_us;
    uint32_t sample_period_us;

    if (!sanitize_token(test_token, test_id, sizeof(test_id)) ||
        !sanitize_token(specimen_token, specimen_id, sizeof(specimen_id)))
    {
        emit_error("INVALID_TOKEN", "test_id and specimen_id must use letters, digits, hyphen or underscore");
        return;
    }

    initial_level = gpio_get_level(DOOR_CONTACT_GPIO);
    start_us = esp_timer_get_time();

    portENTER_CRITICAL(&g_capture_lock);
    if (g_capture.active)
    {
        portEXIT_CRITICAL(&g_capture_lock);
        emit_error("CAPTURE_ACTIVE", "end the active capture before starting another");
        return;
    }

    g_capture.active = true;
    g_capture.overflow = false;
    strlcpy(g_capture.test_id, test_id, sizeof(g_capture.test_id));
    strlcpy(g_capture.specimen_id, specimen_id, sizeof(g_capture.specimen_id));
    g_capture.start_us = start_us;
    g_capture.initial_level = initial_level;
    g_capture.last_level = initial_level;
    g_capture.transition_count = 0;
    sample_period_us = g_capture.sample_period_us;
    portEXIT_CRITICAL(&g_capture_lock);

    emit_common_prefix("capture_started");
    printf(",\"test_id\":\"%s\",\"specimen_id\":\"%s\","
           "\"start_uptime_us\":%" PRId64 ",\"gpio\":%d,"
           "\"sample_period_us\":%" PRIu32 ",\"initial_level\":%d,"
           "\"initial_circuit_state\":\"%s\"}\n",
           test_id,
           specimen_id,
           start_us,
           (int)DOOR_CONTACT_GPIO,
           sample_period_us,
           initial_level,
           circuit_state_from_level(initial_level));
    fflush(stdout);
}

static void end_capture(void)
{
    char test_id[TOKEN_MAX_LEN];
    char specimen_id[TOKEN_MAX_LEN];
    size_t transition_count;
    bool overflow;
    int initial_level;
    int final_level;
    int64_t start_us;
    int64_t end_us;
    uint32_t sample_period_us;

    portENTER_CRITICAL(&g_capture_lock);
    if (!g_capture.active)
    {
        portEXIT_CRITICAL(&g_capture_lock);
        emit_error("NO_ACTIVE_CAPTURE", "start a capture before calling end");
        return;
    }

    g_capture.active = false;
    transition_count = g_capture.transition_count;
    overflow = g_capture.overflow;
    initial_level = g_capture.initial_level;
    final_level = g_capture.last_level;
    start_us = g_capture.start_us;
    sample_period_us = g_capture.sample_period_us;
    strlcpy(test_id, g_capture.test_id, sizeof(test_id));
    strlcpy(specimen_id, g_capture.specimen_id, sizeof(specimen_id));
    portEXIT_CRITICAL(&g_capture_lock);

    end_us = esp_timer_get_time();

    for (size_t index = 0; index < transition_count; index++)
    {
        emit_common_prefix("raw_transition");
        printf(",\"test_id\":\"%s\",\"specimen_id\":\"%s\","
               "\"sequence\":%u,\"offset_us\":%" PRId64 ","
               "\"raw_level\":%d,\"circuit_state\":\"%s\"}\n",
               test_id,
               specimen_id,
               (unsigned)(index + 1),
               g_capture.transitions[index].offset_us,
               g_capture.transitions[index].raw_level,
               circuit_state_from_level(g_capture.transitions[index].raw_level));
    }

    emit_common_prefix("capture_ended");
    printf(",\"test_id\":\"%s\",\"specimen_id\":\"%s\","
           "\"duration_us\":%" PRId64 ",\"sample_period_us\":%" PRIu32 ","
           "\"initial_level\":%d,\"final_level\":%d,"
           "\"transition_count\":%u,\"buffer_capacity\":%u,"
           "\"buffer_overflow\":%s}\n",
           test_id,
           specimen_id,
           end_us - start_us,
           sample_period_us,
           initial_level,
           final_level,
           (unsigned)transition_count,
           (unsigned)MAX_TRANSITIONS,
           overflow ? "true" : "false");
    fflush(stdout);
}

static void set_sample_period(const char *value_token)
{
    char *end = NULL;
    unsigned long value;

    if (value_token == NULL)
    {
        emit_error("MISSING_VALUE", "set-sample-us requires a numeric value");
        return;
    }

    value = strtoul(value_token, &end, 10);
    if (end == value_token || *end != '\0' || value < MIN_SAMPLE_PERIOD_US || value > MAX_SAMPLE_PERIOD_US)
    {
        emit_error("INVALID_SAMPLE_PERIOD", "sample period must be between 250 and 10000 microseconds");
        return;
    }

    portENTER_CRITICAL(&g_capture_lock);
    if (g_capture.active)
    {
        portEXIT_CRITICAL(&g_capture_lock);
        emit_error("CAPTURE_ACTIVE", "sample period cannot change during a capture");
        return;
    }
    g_capture.sample_period_us = (uint32_t)value;
    portEXIT_CRITICAL(&g_capture_lock);

    emit_common_prefix("configuration_changed");
    printf(",\"sample_period_us\":%lu}\n", value);
    fflush(stdout);
}

static void print_help(void)
{
    printf("# IHAP-47 commands\n");
    printf("# help\n");
    printf("# status\n");
    printf("# snapshot\n");
    printf("# begin <test_id> <specimen_id>\n");
    printf("# end\n");
    printf("# set-sample-us <250-10000>\n");
    fflush(stdout);
}

static void sampling_task(void *argument)
{
    (void)argument;

    while (true)
    {
        bool active;
        uint32_t sample_period_us;

        portENTER_CRITICAL(&g_capture_lock);
        active = g_capture.active;
        sample_period_us = g_capture.sample_period_us;
        portEXIT_CRITICAL(&g_capture_lock);

        if (!active)
        {
            vTaskDelay(pdMS_TO_TICKS(10));
            continue;
        }

        int level = gpio_get_level(DOOR_CONTACT_GPIO);
        int64_t now_us = esp_timer_get_time();

        portENTER_CRITICAL(&g_capture_lock);
        if (g_capture.active && level != g_capture.last_level)
        {
            if (g_capture.transition_count < MAX_TRANSITIONS)
            {
                transition_t *entry = &g_capture.transitions[g_capture.transition_count++];
                entry->offset_us = now_us - g_capture.start_us;
                entry->raw_level = level;
            }
            else
            {
                g_capture.overflow = true;
            }
            g_capture.last_level = level;
        }
        portEXIT_CRITICAL(&g_capture_lock);

        esp_rom_delay_us(sample_period_us);
        taskYIELD();
    }
}

static void command_task(void *argument)
{
    (void)argument;
    char line[COMMAND_LINE_MAX_LEN];

    while (true)
    {
        if (fgets(line, sizeof(line), stdin) == NULL)
        {
            clearerr(stdin);
            vTaskDelay(pdMS_TO_TICKS(20));
            continue;
        }

        line[strcspn(line, "\r\n")] = '\0';

        char *saveptr = NULL;
        char *command = strtok_r(line, " \t", &saveptr);

        if (command == NULL)
        {
            continue;
        }

        if (strcmp(command, "help") == 0)
        {
            print_help();
        }
        else if (strcmp(command, "status") == 0)
        {
            emit_status();
        }
        else if (strcmp(command, "snapshot") == 0)
        {
            emit_snapshot();
        }
        else if (strcmp(command, "begin") == 0)
        {
            char *test_id = strtok_r(NULL, " \t", &saveptr);
            char *specimen_id = strtok_r(NULL, " \t", &saveptr);

            if (test_id == NULL || specimen_id == NULL)
            {
                emit_error("MISSING_ARGUMENT", "begin requires test_id and specimen_id");
            }
            else
            {
                start_capture(test_id, specimen_id);
            }
        }
        else if (strcmp(command, "end") == 0)
        {
            end_capture();
        }
        else if (strcmp(command, "set-sample-us") == 0)
        {
            set_sample_period(strtok_r(NULL, " \t", &saveptr));
        }
        else
        {
            emit_error("UNKNOWN_COMMAND", "send help to list supported commands");
        }
    }
}

void app_main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    gpio_config_t input_config = {
        .pin_bit_mask = 1ULL << DOOR_CONTACT_GPIO,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };

    ESP_ERROR_CHECK(gpio_config(&input_config));

    int initial_level = gpio_get_level(DOOR_CONTACT_GPIO);

    ESP_LOGI(TAG, "IHAP-47 door contact validation harness");
    ESP_LOGI(TAG, "GPIO%d input with internal pull-up; passive contact to ground", (int)DOOR_CONTACT_GPIO);
    ESP_LOGW(TAG, "Test harness only: raw electrical state is not alarm, access-control or tamper evidence");

    emit_common_prefix("boot");
    printf(",\"gpio\":%d,\"pull\":\"internal_up\",\"contact_to\":\"ground\","
           "\"sample_period_us\":%u,\"initial_level\":%d,"
           "\"initial_circuit_state\":\"%s\","
           "\"physical_test_validated\":false}\n",
           (int)DOOR_CONTACT_GPIO,
           (unsigned)DEFAULT_SAMPLE_PERIOD_US,
           initial_level,
           circuit_state_from_level(initial_level));

    print_help();

    BaseType_t sampler_created = xTaskCreate(sampling_task, "door_sampler", 4096, NULL, 5, NULL);
    BaseType_t command_created = xTaskCreate(command_task, "door_commands", 4096, NULL, 6, NULL);

    if (sampler_created != pdPASS || command_created != pdPASS)
    {
        emit_error("TASK_CREATE_FAILED", "unable to create validation tasks");
        abort();
    }
}
