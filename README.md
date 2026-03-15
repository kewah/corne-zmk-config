# Corne Choc Pro ZMK Config

Personal ZMK firmware configuration for the Corne Choc Pro split keyboard.

Inspired by [Seniply](https://stevep99.github.io/seniply/) and [Callum](https://github.com/callum-oakley/qmk_firmware/tree/master/users/callum#readme).

## Layout Notes

- Base layer uses Graphite.
- Only the inner 5 columns per half are used for alpha/layer keys. Extra keys are mapped as follows:
  - Middle-row outer keys carry isolated outer key bindings (`mouseless`, `mo BT`).
  - Top-row outer keys, bottom-row outer keys, and center keys are unused.
- The layer diagrams omit unused extra keys unless one is used on that layer.
- `Mod/Ext` is the main layer key:
  - tap = sticky `MOD`
  - hold = `EXT`
- `MF` is a momentary thumb-chord layer:
  - hold both middle thumbs = `MF`
- `BT` is reached from `MF`:
  - hold both middle thumbs for `MF`, then hold the right middle-row outer key for `BT`
- `MOD` keys are hybrid modifiers:
  - tap = sticky mod
  - hold = normal held mod
- `TMX` on `MOD` sends the tmux prefix (`Ctrl+Space`)
- Encoders: top-left press = `MUTE`, top-right press = `PLAY/PAUSE`, rotation = volume/page/track/brightness

## Layer Access

| Layer | Access                       |
| ----- | ---------------------------- |
| MOD   | tap `Mod/Ext`                |
| EXT   | hold `Mod/Ext`               |
| SYM   | hold `Bspc/Sym`              |
| NUM   | hold `Space/Num`             |
| MF    | hold both middle thumbs      |
| BT    | hold right outer key on `MF` |

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
| `ESC`      | `MOD/EXT`   | `RET`      | `BSP/SYM`   | `SPC/NUM`    | `SHIFT`     |

Outer keys

| Left outer | Right outer |
| ---------- | ----------- |
| `ML`       |             |

## MOD (tap `Mod/Ext`)

Left half

| Row    | Col 1    | Col 2  | Col 3   | Col 4  | Col 5 |
| ------ | -------- | ------ | ------- | ------ | ----- |
| Top    |          |        |         |        |       |
| Home   | `SHIFT*` | `ALT*` | `CTRL*` | `CMD*` |       |
| Bottom |          |        |         |        |       |

Right half

| Row    | Col 1 | Col 2  | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ------ | ----- | ----- | ----- |
| Top    |       |        |       |       |       |
| Home   |       | `HYP*` |       |       | `TMX` |
| Bottom |       |        |       |       |       |

## EXT (hold `Mod/Ext`)

Left half

| Row    | Col 1   | Col 2 | Col 3  | Col 4 | Col 5 |
| ------ | ------- | ----- | ------ | ----- | ----- |
| Top    |         |       |        |       |       |
| Home   | `SHIFT` | `ALT` | `CTRL` | `CMD` |       |
| Bottom |         |       |        |       |       |

Right half

| Row    | Col 1  | Col 2  | Col 3 | Col 4   | Col 5  |
| ------ | ------ | ------ | ----- | ------- | ------ |
| Top    | `RALT` | `HOME` | `END` |         | `PGUP` |
| Home   | `LEFT` | `DOWN` | `UP`  | `RIGHT` |        |
| Bottom |        | `TAB`  | `DEL` |         | `PGDN` |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
|            | `EXT`       |            |             | `SPC`        |             |

## SYM (hold `Bspc/Sym`)

Left half

| Row    | Col 1   | Col 2 | Col 3  | Col 4 | Col 5 |
| ------ | ------- | ----- | ------ | ----- | ----- |
| Top    | `` ` `` | `~`   | `@`    | `#`   | `$`   |
| Home   | `SHIFT` | `ALT` | `CTRL` | `CMD` | `HYP` |
| Bottom | `^`     | `&`   | `!`    | `?`   | `\|`  |

Right half

| Row    | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ----- | ----- | ----- | ----- |
| Top    |       | `/`   | `:`   | `;`   | `\`   |
| Home   | `<`   | `(`   | `{`   | `[`   | `-`   |
| Bottom | `>`   | `)`   | `}`   | `]`   | `_`   |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
|            |             |            | `SYM`       |              |             |

## NUM (hold `Space/Num`)

Left half

| Row    | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
| ------ | ----- | ----- | ----- | ----- | ----- |
| Top    | `/`   | `7`   | `8`   | `9`   | `%`   |
| Home   | `-`   | `1`   | `2`   | `3`   | `+`   |
| Bottom | `x`   | `4`   | `5`   | `6`   | `*`   |

Right half

| Row    | Col 1 | Col 2 | Col 3  | Col 4 | Col 5   |
| ------ | ----- | ----- | ------ | ----- | ------- |
| Top    |       |       |        |       |         |
| Home   | `HYP` | `CMD` | `CTRL` | `ALT` | `SHIFT` |
| Bottom |       |       |        |       |         |

Thumbs

| Left outer | Left middle | Left inner | Right inner | Right middle | Right outer |
| ---------- | ----------- | ---------- | ----------- | ------------ | ----------- |
| `:`        | `0`         | `=`        |             | `NUM`        |             |

## MF (hold both middle thumbs)

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

Outer keys

| Left outer | Right outer |
| ---------- | ----------- |
|            | `BT`        |

## BT (hold the right outer key on `MF`)

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
- `SHIFT*`, `ALT*`, `CTRL*`, `CMD*`, `HYP*` on `MOD`:
  - tap = sticky modifier
  - hold = normal held modifier
- `HYP` = Hyper (`Ctrl+Alt+Cmd+Shift`)
- `TMX` = tmux prefix (`Ctrl+Space`)
- `RALT` = Right Alt (used for VoiceInk speech-to-text)
- `ML` = Mouseless trigger (`Hyper+Enter`)
- `BT 0`–`BT 4` = directly select Bluetooth profile slots 0–4
- `BT CLR` = clear Bluetooth bonds
- `BT NXT` / `BT PRV` = switch Bluetooth profile
- `OUT USB` / `OUT BLE` = explicitly select USB or Bluetooth output
- `RGB TOG` = toggle RGB underglow on/off
- `RGB HUI` / `RGB HUD` = increase/decrease hue
- `RGB SAI` / `RGB SAD` = increase/decrease saturation
- `RGB BRI` / `RGB BRD` = increase/decrease brightness
- `RGB EFF` = cycle RGB effect
- Middle-row left outer key = `ML` on `BASE`
- Middle-row right outer key on `MF` momentarily opens `BT`
- Top-row outer keys, bottom-row outer keys, and center keys are unused

## Bluetooth Recovery

If Bluetooth stops working after a firmware change:

1. Forget the keyboard in macOS Bluetooth settings.
2. Hold both middle thumbs to reach `MF`, then hold the right middle-row outer key to reach `BT`.
3. Press `BT CLR`.
4. Use `BT 0`–`BT 4` to jump directly to the host profile you want, or `BT NXT` / `BT PRV` to cycle.
5. If the board is on the wrong output, press `OUT BLE` or `OUT USB`.
6. If that still does not recover it, flash the `settings_reset` UF2 to both halves, then re-flash the normal left/right firmware.

## Combos (EXT layer)

| Keys | Output                 |
| ---- | ---------------------- |
| H+A  | Opt+Left (word left)   |
| A+E  | Opt+Right (word right) |

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
