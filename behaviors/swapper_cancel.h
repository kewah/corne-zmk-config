#pragma once

#include <stddef.h>
#include <stdint.h>

enum {
    SWAPPER_HID_CANCEL_DOWN = 1,
    SWAPPER_HID_CANCEL_UP = 2,
    SWAPPER_HID_RELEASE_MODIFIER = 3,
};

#define SWAPPER_CANCEL_POSITIONS_MAX 8

struct swapper_slot {
    uint8_t active;
    uint8_t owns_position;
    uint8_t cancel;
    uint8_t ignored;
};

typedef void (*swapper_emit_fn)(int event, void *ctx);

int swapper_play_cancel(const struct swapper_slot *slots, size_t count, swapper_emit_fn emit,
                        void *ctx);
