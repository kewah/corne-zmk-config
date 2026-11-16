---
name: verify-keymap-contract
description: >
  Checks the Corne Choc Pro keymap contract: combo positions, the Cmd-Tab
  reverse-shift, Backspace and Space fallthrough, and that Bluetooth and
  output commands resolve only while the BT layer supplies them, and that
  the README layer pictures match the keymap. Use when editing
  config/corne_choc_pro.keymap, corne_choc_pro-layouts.dtsi, layer order,
  combos, tri-state swappers, sticky layers, the layer pictures, or the
  README layout, and before trusting a keymap change.
---

# Verify the Corne keymap contract

## Property

Every chord, the Cmd-Tab reverse-shift, Backspace, Space, and the Bluetooth maintenance keys resolve to the bindings the layout names, and a Bluetooth or output command is produced only while the BT layer supplies that command.

Harm: a shifted index makes a chord type the wrong shortcut, drops Cmd when reverse-cycling the app switcher, or clears Bluetooth bonds from an ordinary key. The firmware still builds.

## Run

From the repo root:

```bash
python3 .cursor/skills/verify-keymap-contract/scripts/check_keymap.py
```

`--dump` prints the contract bindings the checker read. The script uses the Python 3 standard library. There is nothing to install.

Exit 0: the contract holds and the layer pictures match the keymap.
Exit 1: a finding. A keymap line is a counterexample. A picture line names the stale file and the command that rewrites it.
Exit 2: the checker could not parse the files or could not run the picture check. That is a fault in the checker, not a finding. Fix the checker. Do not edit the keymap to silence it.

A pass covers this contract and the layer pictures. It does not mean the rest of the keymap is right.

## Read a failure

Replay the line against `config/corne_choc_pro.keymap`. If every step is a binding, combo, or layer that exists, it is a bug in the keymap. Report it. Do not change the contract or the keymap to make the check pass unless the user asked.

If a step cannot happen in the keymap, the checker is wrong. Fix the checker and say what was wrong.

A line that names a file under `docs/layouts` is a stale picture. Run `python3 docs/generate_layouts.py`. Do not edit the SVG by hand, and do not change the keymap to silence it.

README prose keeps behavior the picture does not draw, such as what QSWAP sends. Do not add a sentence that only names a key's position and its label. The picture already shows that.

Two failures that must keep failing, checked against the real file and then reverted:

- `swapper` `ignored-key-positions = <28>` instead of `<15>`: Cmd-Tab releases when the home-row Shift is tapped.
- `&bt BT_CLR` on the BASE B key: with only BASE active, that key resolves to `&bt BT_CLR`.

## Coverage

Checked code:

- `config/corne_choc_pro.keymap` — layer nodes in order, `bindings` on each layer, the six combos, `ext_mod`, `sticky_layer`, `backspace_delete`, `swapper`, `tab_swapper`, `cancel-key-positions`, and `chosen { zmk,physical-layout }`.
- `behaviors/behavior_tri_state.c` and `behaviors/swapper_cancel.c` — Escape is emitted before Command releases. The host model is `scripts/test_swapper_cancel.py`.
- `boards/arm/corne_choc_pro/corne_choc_pro-layouts.dtsi` — `default_layout` key count and `default_map` positions.
- `docs/layouts/*.svg` — the pictures `docs/generate_layouts.py --check` renders from the keymap. A difference is a finding.

The contract tables `OWN`, `FALLTHROUGH`, `COMBOS`, and `SWAPPERS` live in `scripts/check_keymap.py`. They were transcribed from the keymap header and from README.md sections Layout Notes, Layer Access, the thumb and outer-key diagrams, Combos, and Bluetooth. The checker does not parse the README. If those sections change, re-read them before trusting a pass.

The build uses `config/corne_choc_pro.keymap` for both `corne_choc_pro_left` and `corne_choc_pro_right`, because ZMK strips `_left` / `_right` and prefers `config/` over the board keymap. `boards/arm/corne_choc_pro/corne_choc_pro.keymap` is the stock fallback and is not checked.

## What the checker assumes

Layer ids are keymap node order and must match `#define BASE 0` through `#define BT 6`.

For a press, resolution walks from the highest active layer down to BASE. `&trans` continues. `&none` stops and sends nothing. Any other behavior stops. That is `zmk_keymap_position_state_changed` in ZMK `app/src/keymap.c`: a return greater than 0 continues, and `ZMK_BEHAVIOR_TRANSPARENT` is 1. The checker tries every subset of the upper layers with BASE held, 46 positions by 64 masks. The default layer is assumed to stay BASE. A `&dft` binding fails the check instead of being modeled.

`ext_mod` is a hold-tap whose first slot is `&mo` and whose second is `&sl`, so `&ext_mod EXT MOD` holds EXT and taps sticky MOD. `sticky_layer` is a sticky-key whose binding is `&mo`.

A combo's `layers` list is the filter in `combo_active_on_layer` in ZMK `app/src/combo.c`: the combo may arm only when the highest active layer is in that list. The checker checks the positions, the layer filter, and the binding. It does not step through timeouts.

`&bt BT_CLR` is two devicetree cells because ZMK `dt-bindings/zmk/bt.h` defines `BT_CLR` as `BT_CLR_CMD 0`. The RGB macros in `rgb.h` expand the same way. Those expansions are copied in `MULTI_TOKEN` from zmk `main` on 2026-11-10. `config/west.yml` tracks `main` without a pin. An unknown behavior is exit 2, so a new macro cannot pass silently.

`ignored-key-positions` is the tri-state rule in `behaviors/behavior_tri_state.c`. A press at a listed position does not release the held modifier. Both swappers must ignore only position 15, and EXT's own binding there must be `&sk LSHFT`. `swapper` also sets `cancel-key-positions = <0>` and `cancel-keycode = <ESC>`. That press sends Escape before Command releases, and the layer binding is not sent. `tab_swapper` has no cancel key.

## Not covered

- Hold-tap timing on `ext_mod` and `hm`: flavor, tapping term, quick-tap, retro-tap. That procedure is ZMK's `behavior_hold_tap.c`, which is not in this repo.
- When a sticky layer releases, including `ignore-modifiers` and `release-after-ms`.
- Whether the BT combo still arms if some other layer is already the highest layer. The keymap sets `layers = <BASE>` on that combo.
- Layer stacks above EXT that cover position 15. The reverse-shift promise is for the EXT binding the swapper uses.
- Encoder `sensor-bindings`, RGB positions, and `five_col_layout`.
- The stock board keymap, and keymap edits made later in ZMK Studio. `build.yaml` enables Studio on the left half only.

## Update the contract

Change `OWN`, `FALLTHROUGH`, `COMBOS`, or `SWAPPERS` only when the keymap and the README both show that the promise changed on purpose. Keep the old wording in the report. Do not drop a check because it fails.

After a change to covered code, rerun the command. Move the sync commit below only once the check passes on the committed tree and you have confirmed the script still describes that tree. A pass against an old description is not a pass. If the covered files changed and this skill was not rerun, use `/maintain-formal-verification-skill`.

## Sync

- Sync commit: `c982af627c1db2e7b5dc2d795cf8a1108b572a5b`
- `config/corne_choc_pro.keymap` `00e9bb2e882b73b5bb73f8961584eff45b3a24b337bfc9b79921f60d5c3d7468`
- `boards/arm/corne_choc_pro/corne_choc_pro-layouts.dtsi` `a66831b4136504a4577e298e0e0a83ae36be2e6cf4e558f80a9d05ff47746d04`
- `README.md` `b5054cf06fffdde92cbe0527e4c5966486bbc127ba96068045ba1a536e8397c7`

Those hashes are the file contents the check was run on. They match that commit. The layout hash is still the one from `665053b`. If a hash differs, the check is stale.
