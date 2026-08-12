# Corne Choc Pro ZMK Config

Personal ZMK firmware configuration for the Corne Choc Pro split keyboard.

Inspired by [Seniply](https://stevep99.github.io/seniply/) and [Callum](https://github.com/callum-oakley/qmk_firmware/tree/master/users/callum#readme).

## Layout Notes

- Base layer uses Graphite.
- Only the inner 5 columns per half are used for alpha/layer keys. Extra keys are mapped as follows:
  - Middle-row left outer carries `mouseless` on `BASE` and `` CMD+` `` on `MOD`/`EXT`.
  - Middle-row right outer, top-row outer keys, and bottom-row outer keys are unused.
  - The two top center keys are encoder presses; the remaining center keys are unused.
- The layer diagrams omit unused extra keys unless one is used on that layer.
- `Mod/Ext` is the main layer key:
  - tap = sticky `MOD`
  - hold = `EXT`
- The remaining thumb keys are organized by role:
  - tap `Esc/Shift` for Escape; hold it for Shift
  - tap `Sym` or `Num` for one sticky layer key; hold for a sequence
  - `Enter` and `Space` are dedicated, normally repeatable keys
  - hold `Esc/Shift` with the left thumb and tap `Enter` with the right thumb for Shift+Enter
  - tap or hold `Mod/Ext`, then tap `Enter` for an alternate resting-thumb Shift+Enter chord
- `Backspace` occupies the Space position on both `MOD` and `EXT`:
  - tap `Mod/Ext`, then tap Space for a one-shot edit
  - hold `Mod/Ext`, then hold Space for normal key repeat
- `Delete` is available on the `EXT` comma position.
- `EXT` left half is a one-handed mouse companion: app switching, tab cycling, window cycling, back/forward, close, select all, undo/cut/copy/paste while the right hand stays on the mouse.
- `MF` is a momentary thumb-chord layer:
  - hold both inner layer thumbs (`Sym` + `Num`) = `MF`
- `BT` is a momentary thumb-chord layer:
  - hold `Mod/Ext` + `Num` = `BT`
- `MOD`, `SYM`, and `NUM` home-row modifiers are hybrid modifiers:
  - tap = sticky mod
  - hold = normal held mod
- Sticky `SYM` and `NUM` remain active while modifiers are entered, then release on the shortcut key. For example, tap `NUM`, tap `CTRL*` and `SHIFT*`, then tap `1` for Ctrl+Shift+1.
- `TMX` on `MOD` sends the tmux prefix (`Ctrl+Space`)
- Encoders: top-left press = `MUTE`, top-right press = `PLAY/PAUSE`, rotation = volume/page/track/brightness

### Thumb Placement Philosophy

`Mod/Ext` and `Space` occupy the middle resting positions. `Sym` and `Num` mirror each other on the inner thumbs, while `Esc/Shift` and `Enter` mirror each other on the outer thumbs for a simple two-thumb Shift+Enter chord. Enter and Space stay dedicated and repeatable, and the layer triggers consistently use sticky tap and momentary hold.

## Layer Access

| Layer | Access                                       |
| ----- | -------------------------------------------- |
| MOD   | tap `Mod/Ext`                                |
| EXT   | hold `Mod/Ext`                               |
| SYM   | tap `Sym` for sticky; hold for momentary     |
| NUM   | tap `Num` for sticky; hold for momentary     |
| MF    | hold both inner thumbs (`Sym` + `Num`)       |
| BT    | hold `Mod/Ext` + `Num`                       |

## BASE (Graphite)

Left half

| Row    | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ----- | ----- | ----- | ----- |
| Top    | `B`   | `L`   | `D`   | `W`   | `Z`   |
| Home   | `N`   | `R`   | `T`   | `S`   | `G`   |
| Bottom | `Q`   | `X`   | `M`   | `C`   | `V`   |

Right half

| Row    | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ----- | ----- | ----- | ----- |
| Top    | `'/"` | `F`   | `O`   | `U`   | `J`   |
| Home   | `Y`   | `H`   | `A`   | `E`   | `I`   |
| Bottom | `K`   | `P`   | `,/?` | `./!` | `/\`  |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
| `ESC/SHIFT` | `MOD/EXT`  | `SYM†`     | `NUM†`      | `SPC`        | `RET`       |

Outer keys

| Left outer | Right outer |
| ---------- | ----------- |
| `ML`       |             |

## MOD (tap `Mod/Ext`)

Left half

| Row    | Col 1   | Col 2     | Col 3  | Col 4  | Col 5   |
| ------ | ------- | --------- | ------ | ------ | ------- |
| Top    | `CMD+[` | `CTRL+TAB` | `QSWAP` | `CMD+W` | `CMD+Z` |
| Home   | `SHIFT*` | `ALT*`   | `CTRL*` | `CMD*` | `CMD+R` |
| Bottom | `CMD+]` | `CMD+X`   | `CMD+A` | `CMD+C` | `CMD+V` |

Right half

| Row    | Col 1 | Col 2  | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ------ | ----- | ----- | ----- |
| Top    |       |        |       |       |       |
| Home   |       | `HYP*` |       |       | `TMX` |
| Bottom |       |        |       |       |       |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
|            | `MOD`       |            |             | `BSP`        | `SHIFT+RET` |

Outer keys

| Left outer | Right outer |
| ---------- | ----------- |
| `` CMD+` `` |             |

## EXT (hold `Mod/Ext`)

Left half

| Row    | Col 1   | Col 2  | Col 3 | Col 4  | Col 5   |
| ------ | ------- | ------ | ----- | ------ | ------- |
| Top    | `CMD+[` | `TSWAP` | `SWAP` | `CMD+W` | `CMD+Z` |
| Home   | `SHIFT†` | `ALT†` | `CTRL†` | `CMD†` | `CMD+R` |
| Bottom | `CMD+]` | `CMD+X` | `CMD+A` | `CMD+C` | `CMD+V` |

Right half

| Row    | Col 1  | Col 2  | Col 3 | Col 4   | Col 5  |
| ------ | ------ | ------ | ----- | ------- | ------ |
| Top    | `RALT` | `HOME` | `END` |         | `PGUP` |
| Home   | `LEFT` | `DOWN` ① | `UP` ①② | `RIGHT` ② |        |
| Bottom |        | `TAB`  | `DEL` |         | `PGDN` |

Word-navigation chords (press the marked keys together):

| Chord | Base positions | Output |
| ----- | -------------- | ------ |
| ① `DOWN` + `UP` | `H` + `A` | Opt+Left |
| ② `UP` + `RIGHT` | `A` + `E` | Opt+Right |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
|            | `EXT`       |            |             | `BSP`        | `SHIFT+RET` |

Outer keys

| Left outer | Right outer |
| ---------- | ----------- |
| `` CMD+` `` |             |

## SYM (tap `Sym` for sticky; hold for momentary)

Left half

| Row    | Col 1   | Col 2 | Col 3  | Col 4 | Col 5 |
| ------ | ------- | ----- | ------ | ----- | ----- |
| Top    |         | `^`   | `&`    | `\|`  |       |
| Home   | `SHIFT*` | `ALT*` | `CTRL*` | `CMD*` | `HYP*` |
| Bottom |         |       |        |       |       |

Right half

| Row    | Col 1  | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ------ | ----- | ----- | ----- | ----- |
| Top    | `~`    | `@`   | `` ` `` | `#`   | `$`   |
| Home   | `-`    | `(` ① | `{` ① | `[`   | `:`   |
| Bottom | `_`    | `)` ② | `}` ② | `]`   | `;`   |

Angle-bracket chords (press the marked keys together):

| Chord | Output |
| ----- | ------ |
| ① `(` + `{` | `<` |
| ② `)` + `}` | `>` |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
|            |             | `SYM`      | `NUM†`      | `SPC`        | `RET`       |

## NUM (tap `Num` for sticky; hold for momentary)

Left half

| Row    | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ----- | ----- | ----- | ----- |
| Top    | `/`   | `7`   | `8`   | `9`   | `%`   |
| Home   | `-`   | `1`   | `2`   | `3`   | `+`   |
| Bottom | `:`   | `4`   | `5`   | `6`   | `*`   |

Right half

| Row    | Col 1 | Col 2 | Col 3  | Col 4 | Col 5   |
| ------ | ----- | ----- | ------ | ----- | ------- |
| Top    |       |       |        |       |         |
| Home   | `HYP*` | `CMD*` | `CTRL*` | `ALT*` | `SHIFT*` |
| Bottom |       |       |        |       |         |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
| `.`        | `0`         | `=`        | `NUM`       | `SPC`        | `RET`       |

## MF (hold both inner layer thumbs: `Sym` + `Num`)

Left half

| Row    | Col 1  | Col 2        | Col 3  | Col 4  | Col 5 |
| ------ | ------ | ------------ | ------ | ------ | ----- |
| Top    |        | `MUTE`       | `VOL-` | `VOL+` |       |
| Home   | `STOP` | `PLAY/PAUSE` | `PREV` | `NEXT` |       |
| Bottom |        |              | `BRI-` | `BRI+` |       |

Right half

| Row    | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ----- | ----- | ----- | ----- |
| Top    | `F12` | `F7`  | `F8`  | `F9`  |       |
| Home   | `F10` | `F1`  | `F2`  | `F3`  |       |
| Bottom | `F11` | `F4`  | `F5`  | `F6`  |       |

## BT (hold `Mod/Ext` + `Num`)

Left half

| Row    | Col 1    | Col 2     | Col 3     | Col 4  | Col 5    |
| ------ | -------- | --------- | --------- | ------ | -------- |
| Top    | `BT CLR` | `OUT USB` | `OUT BLE` |        |          |
| Home   | `BT PRV` | `BT 0`    | `BT 1`    | `BT 2` | `BT NXT` |
| Bottom |          | `BT 3`    | `BT 4`    |        |          |

Right half

| Row    | Col 1     | Col 2     | Col 3     | Col 4     | Col 5     |
| ------ | --------- | --------- | --------- | --------- | --------- |
| Top    | `RGB TOG` | `RGB HUI` | `RGB HUD` | `RGB BRI` | `RGB BRD` |
| Home   | `RGB EFF` | `RGB SAI` | `RGB SAD` |           |           |
| Bottom |           |           |           |           |           |

## Legend

- `X/Y` = tap `X`, hold `Y`
- `SYM†`, `NUM†` = tap for a sticky one-key layer, hold for a momentary layer
- `BSP` on `MOD` and `EXT`:
  - tap `Mod/Ext`, then tap `Space` for one Backspace
  - hold `Mod/Ext`, then hold `Space` for repeating Backspace
- `SHIFT+RET` on `MOD` and `EXT` provides Shift+Enter from the same layer trigger used for Backspace.
- `DEL` is on the `EXT` comma position.
- `SHIFT*`, `ALT*`, `CTRL*`, `CMD*`, `HYP*` on `MOD`:
  - tap = sticky modifier
  - hold = normal held modifier
- `SHIFT*`, `ALT*`, `CTRL*`, `CMD*`, `HYP*` on `SYM` and `NUM` use the same tap/hold behavior as `MOD`, so modifier muscle memory carries across all three layers.
- `SHIFT†`, `ALT†`, `CTRL†`, `CMD†` on `EXT`:
  - sticky modifiers (tap to activate, auto-release after next keypress)
  - stackable: tap multiple to combine (e.g., `CMD†` then `SHIFT†` then `F` = Cmd+Shift+F)
- `SWAP` = Cmd+Tab app switcher (tri-state): tap to open the macOS switcher and advance, Cmd stays held across taps, tap `SHIFT†` to cycle backward, release `Mod/Ext` (or press any other key) to commit
- `QSWAP` = instant switch to previous app (Cmd+Tab with immediate release, no switcher UI), same key as `SWAP`
- `TSWAP` = Ctrl+Tab tab switcher (tri-state): holds Ctrl across taps so the browser tab switcher stays up, tap `SHIFT†` to reverse (Ctrl+Shift+Tab), release `Mod/Ext` to commit. Sits beside `SWAP`
- `CTRL+TAB` on `MOD` = plain one-shot Ctrl+Tab, same key position as `TSWAP`
- `CMD+[` / `CMD+]` = back / forward
- `CMD+Z/X/C/V/W` sit on their Graphite letter positions as mnemonics
- `CMD+A` (select all) sits left of `CMD+C` to cluster select/copy/paste for one-handed use
- `CMD+R` (reload) sits on the home row inner column
- Left-hand `CMD` shortcuts exist on both layers: tap `Mod/Ext` for a one-shot (`MOD`), hold for repeats and `SWAP` cycling (`EXT`)
- `HYP` = Hyper (`Ctrl+Alt+Cmd+Shift`)
- `TMX` = tmux prefix (`Ctrl+Space`)
- `RALT` = Right Alt (used for VoiceInk speech-to-text)
- `ML` = Mouseless trigger (`Hyper+Enter`); its position sends `` CMD+` `` on `MOD`/`EXT`
- `BT 0`–`BT 4` = directly select Bluetooth profile slots 0–4
- `BT CLR` = clear Bluetooth bonds
- `BT NXT` / `BT PRV` = switch Bluetooth profile
- `OUT USB` / `OUT BLE` = explicitly select USB or Bluetooth output
- `RGB TOG` = toggle RGB underglow on/off
- `RGB HUI` / `RGB HUD` = increase/decrease hue
- `RGB SAI` / `RGB SAD` = increase/decrease saturation
- `RGB BRI` / `RGB BRD` = increase/decrease brightness
- `RGB EFF` = cycle RGB effect
- Middle-row left outer key = `ML` on `BASE`, `` CMD+` `` on `MOD`/`EXT`
- Middle-row right outer key, top-row outer keys, and bottom-row outer keys are unused

## Bluetooth Recovery

If Bluetooth stops working after a firmware change:

1. Forget the keyboard in macOS Bluetooth settings.
2. Hold `Mod/Ext` + `Num` to reach `BT`.
3. Press `BT CLR`.
4. Use `BT 0`–`BT 4` to jump directly to the host profile you want, or `BT NXT` / `BT PRV` to cycle.
5. If the board is on the wrong output, press `OUT BLE` or `OUT USB`.
6. If that still does not recover it, flash the `settings_reset` UF2 to both halves, then re-flash the normal left/right firmware.

## Combos

| Layer | Keys      | Output                 |
| ----- | --------- | ---------------------- |
| EXT   | `H` + `A` | Opt+Left (word left)   |
| EXT   | `A` + `E` | Opt+Right (word right) |
| SYM   | `(` + `{` | `<`                    |
| SYM   | `)` + `}` | `>`                    |

## Encoders

| Encoder      | Press        | Rotate             |
| ------------ | ------------ | ------------------ |
| Top-left     | `MUTE`       | Volume down/up     |
| Top-right    | `PLAY/PAUSE` | Page up/down       |
| Bottom-left  | —            | Track prev/next    |
| Bottom-right | —            | Brightness down/up |

## Build

Push to GitHub → Actions tab → Download `firmware.zip`.

## Flash

1. Connect keyboard half via USB.
2. Double-tap reset button (enters bootloader).
3. Copy `.uf2` file to mounted USB drive.
4. Repeat for other half.
