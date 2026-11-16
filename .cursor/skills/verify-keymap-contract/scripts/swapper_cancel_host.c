#include "swapper_cancel.h"

#include <stdio.h>

struct record {
    char text[96];
    int used;
};

static const char *event_name(int event) {
    if (event == SWAPPER_HID_CANCEL_DOWN) {
        return "Escape down";
    }
    if (event == SWAPPER_HID_CANCEL_UP) {
        return "Escape up";
    }
    if (event == SWAPPER_HID_RELEASE_MODIFIER) {
        return "Command up";
    }
    return "unknown";
}

static void emit(int event, void *ctx) {
    struct record *record = ctx;
    const char *name = event_name(event);
    if (record->used != 0) {
        record->used += snprintf(record->text + record->used,
                                  sizeof record->text - (size_t)record->used, ", ");
    }
    record->used += snprintf(record->text + record->used,
                              sizeof record->text - (size_t)record->used, "%s", name);
}

static void play(const char *label, struct swapper_slot slot) {
    struct record record = {.text = "", .used = 0};
    int handled = swapper_play_cancel(&slot, 1, emit, &record);
    printf("%s handled %d: %s\n", label, handled, record.text);
}

int main(void) {
    struct swapper_slot cancel = {.active = 1, .cancel = 1};
    struct swapper_slot other = {.active = 1};
    struct swapper_slot shift = {.active = 1, .ignored = 1};
    struct swapper_slot own = {.active = 1, .owns_position = 1};
    play("cancel", cancel);
    play("other", other);
    play("shift", shift);
    play("own", own);
    return 0;
}
