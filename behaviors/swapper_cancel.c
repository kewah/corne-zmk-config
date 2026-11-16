#include "swapper_cancel.h"

static int slot_cancels(const struct swapper_slot *slot) {
    return slot->active && slot->cancel && !slot->owns_position;
}

int swapper_play_cancel(const struct swapper_slot *slots, size_t count, swapper_emit_fn emit,
                        void *ctx) {
    size_t i;
    int cancel = 0;

    for (i = 0; i < count; i++) {
        if (slot_cancels(&slots[i])) {
            cancel = 1;
            break;
        }
    }
    if (!cancel) {
        return 0;
    }
    emit(SWAPPER_HID_CANCEL_DOWN, ctx);
    emit(SWAPPER_HID_CANCEL_UP, ctx);
    emit(SWAPPER_HID_RELEASE_MODIFIER, ctx);
    return 1;
}
