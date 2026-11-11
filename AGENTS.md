# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview

ZMK firmware configuration for Corne split keyboard with nice!view display. This is a user config repo that references the main ZMK firmware.

## Build System

Firmware is built via GitHub Actions - no local toolchain needed.

**To build:** Push changes to GitHub → Actions tab → Download `firmware.zip` artifact

**Build matrix defined in:** `build.yaml` - lists board/shield combinations to compile

## Key Files for Customization

| File | Purpose |
|------|---------|
| `config/<board>.keymap` | Layer definitions, key bindings |
| `config/<board>.conf` | Board-specific settings (RGB, display, BT) |
| `config/<board>.json` | Physical layout for visualizers |
| `build.yaml` | GitHub Actions build matrix |

## Keymap Structure

Keymaps use ZMK devicetree syntax:
- `&kp KEY` - key press
- `&mo N` - momentary layer
- `&trans` - transparent (pass to lower layer)
- `&bt BT_SEL N` - Bluetooth profile select
- Layers indexed 0-8; layer 0 is default

## Configured Board

- `corne_choc_pro` - 42-key split + encoders + nice_view display

## Required Actions

**When modifying keymap layouts:** Run `python3 .cursor/skills/verify-keymap-contract/scripts/check_keymap.py` before you finish. It fails when a layer picture does not match the keymap.
