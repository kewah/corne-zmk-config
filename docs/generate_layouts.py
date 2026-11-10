"""Generate full, consistently positioned Corne SVGs from the keymap (stdlib only)."""
import argparse
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS = ROOT / "docs/layouts"

# Keyboard viewing order. Columns 0-5 are the left half, 7-8 are the center
# keys, and 10-15 are the right half. The thumb row sits under the inner columns.
PLACEMENT = {}
for index in range(6):
    PLACEMENT[index] = (index, 0)
    PLACEMENT[8 + index] = (10 + index, 0)
    PLACEMENT[14 + index] = (index, 1)
    PLACEMENT[22 + index] = (10 + index, 1)
    PLACEMENT[28 + index] = (index, 2)
    PLACEMENT[34 + index] = (10 + index, 2)
PLACEMENT.update({
    6: (7, 0), 7: (8, 0), 20: (7, 1), 21: (8, 1),
    40: (3, 3), 41: (4, 3), 42: (5, 3),
    43: (10, 3), 44: (11, 3), 45: (12, 3),
})

KEY_LABELS = {
    "LSHFT": "Shift", "LALT": "Alt", "RALT": "RAlt", "LCTRL": "Ctrl",
    "LGUI": "Cmd", "HYPER_MOD": "Hyper", "ESC": "Esc", "RET": "Enter",
    "SPACE": "Space", "TAB": "Tab", "DEL": "Del", "BSPC": "Bksp",
    "HOME": "Home", "END": "End", "PG_UP": "PgUp", "PG_DN": "PgDn",
    "LEFT": "←", "RIGHT": "→", "UP": "↑", "DOWN": "↓",
    "SQT": "'", "DQT": '"', "COMMA": ",", "DOT": ".", "FSLH": "/",
    "BSLH": "\\", "GRAVE": "`", "TILDE": "~", "CARET": "^", "AMPS": "&",
    "PIPE": "|", "AT": "@", "HASH": "#", "DLLR": "$", "MINUS": "−",
    "UNDER": "_", "LPAR": "(", "RPAR": ")", "LT": "<", "GT": ">",
    "LBKT": "[", "RBKT": "]", "LBRC": "{", "RBRC": "}",
    "COLON": ":", "SEMI": ";", "PRCNT": "%", "EXCL": "!",
    "PLUS": "+", "ASTRK": "*", "EQUAL": "=", "C_MUTE": "Mute",
    "C_VOL_DN": "Vol−", "C_VOL_UP": "Vol+", "C_BRI_DN": "Bri−",
    "C_BRI_UP": "Bri+", "C_PREV": "Prev", "C_PP": "Play/Pause",
    "C_NEXT": "Next", "C_STOP": "Stop",
}
BEHAVIOR_LABELS = {
    "&none": "—", "&trans": "·", "&apo_dquote": "' / \"",
    "&comma_qmark": ", / ?", "&dot_excl": ". / !", "&slash_bslash": "/ / \\",
    "&backspace_delete": "Bksp/Del", "&ext_mod EXT MOD": "EXT/MOD",
    "&quick_swap": "QSWAP", "&swapper": "SWAP", "&tab_swapper": "TSWAP",
    "&tmx": "TMX", "&out OUT_USB": "OUT USB", "&out OUT_BLE": "OUT BLE",
    "&rgb_ug RGB_TOG": "RGB On/Off", "&rgb_ug RGB_HUI": "Hue+",
    "&rgb_ug RGB_HUD": "Hue−", "&rgb_ug RGB_BRI": "RGB Bri+",
    "&rgb_ug RGB_BRD": "RGB Bri−", "&rgb_ug RGB_EFF": "Effect+",
    "&rgb_ug RGB_EFR": "Effect−", "&rgb_ug RGB_SPI": "Speed+",
    "&rgb_ug RGB_SPD": "Speed−", "&rgb_ug RGB_STATUS": "Status",
    "&rgb_ug RGB_SAI": "Sat+", "&rgb_ug RGB_SAD": "Sat−",
    "&bt BT_CLR": "BT CLR", "&bt BT_PRV": "BT Prev", "&bt BT_NXT": "BT Next",
}


def key_label(code):
    if code in KEY_LABELS:
        return KEY_LABELS[code]
    if re.fullmatch(r"N[0-9]", code):
        return code[1:]
    if re.fullmatch(r"[A-Z]|F(?:[1-9]|1[0-2])", code):
        return code
    shortcut = re.fullmatch(r"(LG|LC|LS|LA)\((.*)\)", code)
    if shortcut:
        modifier = {"LG": "Cmd", "LC": "Ctrl", "LS": "Shift", "LA": "Alt"}[shortcut[1]]
        return f"{modifier}+{key_label(shortcut[2])}"
    raise ValueError(f"Unknown key code: {code}")


def binding_label(binding):
    if binding in BEHAVIOR_LABELS:
        return BEHAVIOR_LABELS[binding]
    behavior, *args = binding.split()
    if behavior == "&kp":
        return key_label(args[0])
    if behavior in ("&mo", "&sticky_layer"):
        return args[0]
    if behavior in ("&sk", "&hm"):
        return key_label(args[0]) + ("†" if behavior == "&sk" else "*")
    if behavior == "&bt" and args[0] == "BT_SEL":
        return f"BT {args[1]}"
    raise ValueError(f"Unknown binding: {binding}")


def render(name, bindings):
    assert len(bindings) == len(PLACEMENT) == 46
    width, height = 1392, 332
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{name} layer</title>',
        '<desc id="desc">Full 46-key Corne layout in keyboard viewing order. '
        'Both halves, the center keys, and the thumb row are shown, including disabled keys.</desc>',
        f'<rect width="{width}" height="{height}" rx="16" fill="#0f172a"/>',
        '<g font-family="system-ui, sans-serif" text-anchor="middle">',
        '<text x="276" y="32" fill="#94a3b8" font-size="14">LEFT</text>',
        '<text x="1116" y="32" fill="#94a3b8" font-size="14">RIGHT</text>',
    ]
    for position, binding in enumerate(bindings):
        column, row = PLACEMENT[position]
        label = binding_label(binding)
        x, y = 24 + 84 * column, 52 + 68 * row
        if binding == "&none":
            fill, stroke, color = "#131e31", "#28364b", "#64748b"
        elif binding == "&trans":
            fill, stroke, color = "#153e48", "#4b9caa", "#a5f3fc"
        else:
            fill, stroke, color = "#243247", "#52647d", "#f1f5f9"
        size = 18 if len(label) <= 6 else 14 if len(label) <= 8 else 11
        lines.extend([
            f'<g data-position="{position}" data-binding="{escape(binding, quote=True)}">',
            f'<title>Position {position}: {escape(binding)}</title>',
            f'<rect x="{x}" y="{y}" width="76" height="50" rx="8" '
            f'fill="{fill}" stroke="{stroke}"/>',
            f'<text x="{x + 38}" y="{y + 31}" fill="{color}" '
            f'font-size="{size}">{escape(label)}</text>',
            "</g>",
        ])
    lines.append("</g></svg>")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if diagrams are stale")
    args = parser.parse_args()
    text = (ROOT / "config/corne_choc_pro.keymap").read_text()
    text = re.sub(r"//[^\n]*|/\*.*?\*/", "", text, flags=re.S)
    stale = []
    expected_paths = set()
    for name, block in re.findall(r'label = "([A-Z]+)";\s*bindings = <(.*?)>;', text, re.S):
        bindings = [" ".join(b.split()) for b in re.findall(r"&\w+[^&]*", block)]
        path = LAYOUTS / f"{name.lower()}.svg"
        expected_paths.add(path)
        svg = render(name, bindings)
        if args.check:
            if not path.exists() or path.read_text() != svg:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(svg)
    obsolete = set(LAYOUTS.glob("*.svg")) - expected_paths
    if args.check:
        stale.extend(str(path.relative_to(ROOT)) for path in sorted(obsolete))
        if stale:
            parser.exit(1, "Stale diagrams: " + ", ".join(stale) + "\n")
    else:
        for path in obsolete:
            path.unlink()


if __name__ == "__main__":
    main()
