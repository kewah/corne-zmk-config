#!/usr/bin/env python3
"""Check the Corne keymap contract against config/corne_choc_pro.keymap.

Property: every chord, the Cmd-Tab reverse-shift, Backspace, Space, and the
Bluetooth maintenance keys resolve to the bindings the layout names, and a
Bluetooth or output command is resolved only while the BT layer supplies it.

The checker reads the keymap the firmware build uses. It does not model
hold-tap timing, sticky-key release, or combo timeouts. Exit 0 means the
contract holds. Exit 1 is a finding in the keymap. Exit 2 means this checker
could not parse the files, which is a problem in the checker, not a finding.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KEYMAP = ROOT / "config" / "corne_choc_pro.keymap"
LAYOUT = ROOT / "boards" / "arm" / "corne_choc_pro" / "corne_choc_pro-layouts.dtsi"

# Multi-token command macros from ZMK's dt-bindings, included by the keymap.
# bt.h:  `#define BT_CLR BT_CLR_CMD 0` (BT_SEL stays one command plus the
# profile index that follows it). rgb.h: `#define RGB_TOG RGB_TOG_CMD 0`.
# Fetched from zmkfirmware/zmk main on 2026-11-10. west.yml tracks that
# branch without a pin. An unknown behavior is exit 2, not a silent pass.
MULTI_TOKEN = {
    "BT_CLR": ("BT_CLR_CMD", "0"),
    "BT_NXT": ("BT_NXT_CMD", "0"),
    "BT_PRV": ("BT_PRV_CMD", "0"),
    "BT_SEL": ("BT_SEL_CMD",),
    "BT_CLR_ALL": ("BT_CLR_ALL_CMD", "0"),
    "BT_DISC": ("BT_DISC_CMD",),
    "RGB_TOG": ("RGB_TOG_CMD", "0"),
    "RGB_ON": ("RGB_ON_CMD", "0"),
    "RGB_OFF": ("RGB_OFF_CMD", "0"),
    "RGB_HUI": ("RGB_HUI_CMD", "0"),
    "RGB_HUD": ("RGB_HUD_CMD", "0"),
    "RGB_SAI": ("RGB_SAI_CMD", "0"),
    "RGB_SAD": ("RGB_SAD_CMD", "0"),
    "RGB_BRI": ("RGB_BRI_CMD", "0"),
    "RGB_BRD": ("RGB_BRD_CMD", "0"),
    "RGB_SPI": ("RGB_SPI_CMD", "0"),
    "RGB_SPD": ("RGB_SPD_CMD", "0"),
    "RGB_EFF": ("RGB_EFF_CMD", "0"),
    "RGB_EFR": ("RGB_EFR_CMD", "0"),
    "RGB_EFS": ("RGB_EFS_CMD", "0"),
}

# Binding-cell counts for ZMK behaviors this keymap uses but does not define.
# bt and rgb_ug include two_param.yaml. out includes one_param.yaml.
# `&trans` returns ZMK_BEHAVIOR_TRANSPARENT (1) and keymap.c keeps walking.
# `&none` returns ZMK_BEHAVIOR_OPAQUE (0) and the walk stops.
BUILTIN_CELLS = {
    "kp": 1,
    "none": 0,
    "trans": 0,
    "mo": 1,
    "sk": 1,
    "sl": 1,
    "to": 1,
    "tog": 1,
    "bt": 2,
    "out": 1,
    "rgb_ug": 2,
    "kt": 1,
    "inc_dec_kp": 2,
    "macro_press": 1,
    "macro_tap": 1,
    "macro_release": 1,
}

# Node order under the keymap. ZMK assigns layer ids in this order.
LAYER_ORDER = ("BASE", "MOD", "EXT", "SYM", "NUM", "MF", "BT")

# default_map in corne_choc_pro-layouts.dtsi. Keymap index equals this number.
POSITION_ROWS = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
    (14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27),
    (28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39),
    (40, 41, 42, 43, 44, 45),
)

POS_NAME = {
    0: "top-left outer",
    1: "left top, B column",
    2: "left top, L column",
    3: "left top, D column",
    4: "left top, W column",
    5: "left top, Z column",
    6: "left encoder press",
    7: "right encoder press",
    8: "right top, quote column",
    9: "right top, F column",
    10: "right top, O column",
    11: "right top, U column",
    12: "right top, J column",
    13: "top-right outer",
    14: "home-left outer",
    15: "left home, N column",
    16: "left home, R column",
    17: "left home, T column",
    18: "left home, S column",
    19: "left home, G column",
    20: "left center",
    21: "right center",
    22: "right home, Y column",
    23: "right home, H column",
    24: "right home, A column",
    25: "right home, E column",
    26: "right home, I column",
    27: "home-right outer",
    28: "bottom-left outer",
    29: "left bottom, Q column",
    30: "left bottom, X column",
    31: "left bottom, M column",
    32: "left bottom, C column",
    33: "left bottom, V column",
    34: "right bottom, K column",
    35: "right bottom, P column",
    36: "right bottom, comma column",
    37: "right bottom, dot column",
    38: "right bottom, slash column",
    39: "bottom-right outer",
    40: "left outer thumb",
    41: "left middle thumb",
    42: "left inner thumb",
    43: "right inner thumb",
    44: "right middle thumb",
    45: "right outer thumb",
}

# Bindings written on that layer itself, not reached by falling through.
# Transcribed from README.md (Layout Notes, layer diagrams, Combos, Bluetooth)
# and the header comments in config/corne_choc_pro.keymap.
OWN: tuple[tuple[str, int, str, str], ...] = (
    ("BASE", 0, "&kp ESC", "top-left is Escape on BASE"),
    ("MOD", 0, "&kp ESC", "top-left is Escape on MOD"),
    ("EXT", 0, "&kp LG(GRAVE)", "top-left is Cmd+grave on EXT"),
    ("BASE", 13, "&none", "top-right outer is unused on BASE"),
    ("BASE", 14, "&sticky_layer SYM", "home-left outer is sticky SYM"),
    ("BASE", 27, "&sticky_layer NUM", "home-right outer is sticky NUM"),
    ("BASE", 28, "&kp LSHFT", "bottom-left outer is Shift on BASE"),
    ("BASE", 39, "&none", "bottom-right outer is unused on BASE"),
    ("EXT", 15, "&sk LSHFT", "EXT home-row Shift is the reverse-cycle key"),
    ("EXT", 28, "&none", "EXT leaves the bottom-left Shift empty"),
    ("EXT", 2, "&tab_swapper", "TSWAP sits on the left top L column"),
    ("EXT", 3, "&swapper", "SWAP sits on the left top D column"),
    ("BASE", 23, "&kp H", "word-left chord is the H key"),
    ("BASE", 24, "&kp A", "word chords share the A key"),
    ("BASE", 25, "&kp E", "word-right chord is the E key"),
    ("EXT", 23, "&kp DOWN", "word-left presses Down"),
    ("EXT", 24, "&kp UP", "word chords share Up"),
    ("EXT", 25, "&kp RIGHT", "word-right presses Right"),
    ("SYM", 23, "&kp LPAR", "the brace chord presses the parenthesis"),
    ("SYM", 24, "&kp LT", "the brace chord presses the angle bracket"),
    ("SYM", 35, "&kp RPAR", "the closing brace chord presses the parenthesis"),
    ("SYM", 36, "&kp GT", "the closing brace chord presses the angle bracket"),
    ("EXT", 36, "&kp DEL", "Delete stays on the EXT comma key"),
    ("BASE", 40, "&sticky_layer SYM", "left outer thumb is sticky SYM"),
    ("BASE", 41, "&ext_mod EXT MOD", "left middle thumb is hold-EXT, tap-MOD"),
    ("BASE", 42, "&backspace_delete", "left inner thumb is Backspace"),
    ("BASE", 44, "&kp SPACE", "right middle thumb is Space"),
    ("BASE", 45, "&sticky_layer NUM", "right outer thumb is sticky NUM"),
    ("MOD", 43, "&kp LS(RET)", "MOD Enter is Shift+Enter"),
    ("EXT", 43, "&kp LS(RET)", "EXT Enter is Shift+Enter"),
    ("BT", 1, "&bt BT_CLR", "BT clear is the left top B column"),
    ("BT", 2, "&out OUT_USB", "USB output is the left top L column"),
    ("BT", 3, "&out OUT_BLE", "BLE output is the left top D column"),
    ("BT", 15, "&bt BT_PRV", "previous profile is the left home N column"),
    ("BT", 16, "&bt BT_SEL 0", "profile 0 is the left home R column"),
    ("BT", 17, "&bt BT_SEL 1", "profile 1 is the left home T column"),
    ("BT", 18, "&bt BT_SEL 2", "profile 2 is the left home S column"),
    ("BT", 19, "&bt BT_NXT", "next profile is the left home G column"),
    ("BT", 30, "&bt BT_SEL 3", "profile 3 is the left bottom X column"),
    ("BT", 31, "&bt BT_SEL 4", "profile 4 is the left bottom M column"),
)

# README: Backspace and Space keep their base behavior on these layers.
# Checked by resolution, so a transparent key still counts.
FALLTHROUGH_LAYERS = ("MOD", "EXT", "SYM", "NUM")
FALLTHROUGH: tuple[tuple[int, str, str], ...] = (
    (42, "&backspace_delete", "Backspace keeps its base behavior"),
    (44, "&kp SPACE", "Space keeps its base behavior"),
)

COMBOS = {
    "combo_word_left": {
        "positions": (23, 24),
        "layers": ("EXT",),
        "binding": "&kp LA(LEFT)",
        "why": "H+A on EXT sends Opt+Left",
    },
    "combo_word_right": {
        "positions": (24, 25),
        "layers": ("EXT",),
        "binding": "&kp LA(RIGHT)",
        "why": "A+E on EXT sends Opt+Right",
    },
    "combo_sym_lbrc": {
        "positions": (23, 24),
        "layers": ("SYM",),
        "binding": "&kp LBRC",
        "why": "(+< on SYM sends {",
    },
    "combo_sym_rbrc": {
        "positions": (35, 36),
        "layers": ("SYM",),
        "binding": "&kp RBRC",
        "why": ")+> on SYM sends }",
    },
    "combo_mf_layer_thumbs": {
        "positions": (40, 45),
        "layers": ("BASE",),
        "binding": "&mo MF",
        "why": "the outer thumbs open the media layer",
    },
    "combo_bt": {
        "positions": (41, 45),
        "layers": ("BASE",),
        "binding": "&mo BT",
        "why": "Mod/Ext plus Num opens the Bluetooth layer",
    },
}

SWAPPERS = ("swapper", "tab_swapper")
IGNORED_SHIFT = (15,)


class CheckError(Exception):
    """The checker could not read the keymap. Not a finding about the layout."""


@dataclass
class Node:
    label: str | None
    name: str
    props: dict[str, str | None] = field(default_factory=dict)
    children: list[Node] = field(default_factory=list)

    @property
    def ref(self) -> str:
        return self.label or self.name


@dataclass(frozen=True)
class Binding:
    behavior: str
    params: tuple[str, ...]

    def canon(self) -> str:
        if not self.params:
            return self.behavior
        return self.behavior + " " + " ".join(self.params)

    def display(self) -> str:
        """Source spelling, so BT_CLR stays BT_CLR rather than BT_CLR_CMD 0."""
        params = list(self.params)
        shown: list[str] = []
        expansions = sorted(MULTI_TOKEN.items(), key=lambda item: -len(item[1]))
        index = 0
        while index < len(params):
            matched = False
            for name, expansion in expansions:
                width = len(expansion)
                if tuple(params[index : index + width]) == expansion:
                    shown.append(name)
                    index += width
                    matched = True
                    break
            if not matched:
                shown.append(params[index])
                index += 1
        if not shown:
            return "&" + self.behavior
        return "&" + self.behavior + " " + " ".join(shown)


def strip_comments(text: str) -> str:
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                if text[j] == "\\":
                    j += 2
                    continue
                j += 1
            if j >= n:
                raise CheckError("unterminated string in devicetree")
            out.append(text[i : j + 1])
            i = j + 1
            continue
        if text.startswith("//", i):
            nl = text.find("\n", i)
            if nl < 0:
                break
            out.append("\n")
            i = nl
            continue
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end < 0:
                raise CheckError("unterminated block comment")
            out.append(" ")
            i = end + 2
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def strip_directives(text: str) -> tuple[str, dict[str, int]]:
    defines: dict[str, int] = {}
    kept: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("#include"):
            continue
        if stripped.startswith("#define"):
            parts = stripped.split()
            if len(parts) >= 3 and parts[2].lstrip("-").isdigit():
                defines[parts[1]] = int(parts[2])
            continue
        kept.append(line)
    return "".join(kept), defines


def skip_ws(text: str, i: int) -> int:
    while i < len(text) and text[i].isspace():
        i += 1
    return i


def read_name(text: str, i: int) -> tuple[str, int]:
    start = i
    if i < len(text) and text[i] == "#":
        i += 1
    while i < len(text) and (text[i].isalnum() or text[i] in "_-,"):
        i += 1
    if i == start or (text[start] == "#" and i == start + 1):
        snippet = text[start : start + 40].replace("\n", " ")
        raise CheckError(f"expected a devicetree name at {snippet!r}")
    return text[start:i], i


def read_value(text: str, i: int) -> tuple[str, int]:
    start = i
    angle = paren = 0
    while i < len(text):
        c = text[i]
        if c == '"':
            i += 1
            while i < len(text) and text[i] != '"':
                if text[i] == "\\":
                    i += 2
                    continue
                i += 1
            if i >= len(text):
                raise CheckError("unterminated string in a property value")
            i += 1
            continue
        if c == "<":
            angle += 1
        elif c == ">":
            angle -= 1
        elif c == "(":
            paren += 1
        elif c == ")":
            paren -= 1
        elif c == ";" and angle == 0 and paren == 0:
            return text[start:i].strip(), i + 1
        i += 1
    raise CheckError("property value ran off the end of the file")


def parse_body(text: str, i: int, *, top: bool) -> tuple[dict[str, str | None], list[Node], int]:
    props: dict[str, str | None] = {}
    children: list[Node] = []
    n = len(text)
    while True:
        i = skip_ws(text, i)
        if i >= n:
            if top:
                return props, children, i
            raise CheckError("unclosed devicetree node")
        if text[i] == "}":
            if top:
                raise CheckError("unexpected closing brace at the top level")
            return props, children, i
        if text[i] == ";":
            i += 1
            continue
        if text[i] == "/":
            i = skip_ws(text, i + 1)
            if i >= n or text[i] != "{":
                raise CheckError("expected '{' after '/'")
            props_n, children_n, i = parse_body(text, i + 1, top=False)
            if i >= n or text[i] != "}":
                raise CheckError("unclosed root node")
            node = Node(None, "/")
            node.props = props_n
            node.children = children_n
            children.append(node)
            i += 1
            continue
        label, name, i = read_label_and_name(text, i)
        i = skip_ws(text, i)
        if i < n and text[i] == "{":
            props_n, children_n, i = parse_body(text, i + 1, top=False)
            if i >= n or text[i] != "}":
                raise CheckError(f"unclosed node {name}")
            node = Node(label, name)
            node.props = props_n
            node.children = children_n
            children.append(node)
            i += 1
            continue
        prop = name if label is None else None
        if prop is None:
            raise CheckError(f"label {label}: on something that is not a node")
        if i < n and text[i] == "=":
            raw, i = read_value(text, i + 1)
            props[prop] = raw.strip()
            continue
        if i < n and text[i] == ";":
            props[prop] = None
            i += 1
            continue
        snippet = text[i : i + 40].replace("\n", " ")
        raise CheckError(f"expected '=' or '{{' after {prop}, found {snippet!r}")


def read_label_and_name(text: str, i: int) -> tuple[str | None, str, int]:
    name, i = read_name(text, i)
    j = skip_ws(text, i)
    if j < len(text) and text[j] == ":":
        j = skip_ws(text, j + 1)
        node_name, j = read_name(text, j)
        return name, node_name, j
    return None, name, i


def walk(nodes: list[Node]):
    for node in nodes:
        yield node
        yield from walk(node.children)


def unquote(raw: str | None) -> str:
    if raw is None:
        return ""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        return raw[1:-1]
    return raw


def angle_groups(raw: str) -> list[str]:
    groups: list[str] = []
    i = 0
    while True:
        start = raw.find("<", i)
        if start < 0:
            break
        depth = 0
        for k in range(start, len(raw)):
            if raw[k] == "<":
                depth += 1
            elif raw[k] == ">":
                depth -= 1
                if depth == 0:
                    groups.append(raw[start + 1 : k])
                    i = k + 1
                    break
        else:
            raise CheckError("unclosed '<' in a property")
    return groups


def tokenize(body: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        c = body[i]
        if c.isspace() or c == ",":
            i += 1
            continue
        if c == "&":
            j = i + 1
            while j < n and (body[j].isalnum() or body[j] == "_"):
                j += 1
            if j == i + 1:
                raise CheckError(f"empty phandle in {body!r}")
            tokens.append(body[i:j])
            i = j
            continue
        if c == "(":
            depth = 0
            j = i
            while j < n:
                if body[j] == "(":
                    depth += 1
                elif body[j] == ")":
                    depth -= 1
                    if depth == 0:
                        tokens.append(body[i : j + 1])
                        i = j + 1
                        break
                j += 1
            else:
                raise CheckError(f"unbalanced '(' in {body!r}")
            continue
        if c.isalnum() or c == "_":
            j = i + 1
            while j < n and (body[j].isalnum() or body[j] == "_"):
                j += 1
            if j < n and body[j] == "(":
                depth = 0
                k = j
                while k < n:
                    if body[k] == "(":
                        depth += 1
                    elif body[k] == ")":
                        depth -= 1
                        if depth == 0:
                            j = k + 1
                            break
                    k += 1
                else:
                    raise CheckError(f"unbalanced '(' after {body[i:j]!r}")
            tokens.append(body[i:j])
            i = j
            continue
        raise CheckError(f"cannot tokenize {body[i : i + 24]!r}")
    return tokens


def expand(tokens: list[str]) -> list[str]:
    out: list[str] = []
    for token in tokens:
        if token.startswith("&") or token.startswith("("):
            out.append(token)
            continue
        out.extend(MULTI_TOKEN.get(token, (token,)))
    return out


def parse_bindings(raw: str, cells: dict[str, int], where: str) -> list[Binding]:
    groups = angle_groups(raw)
    if len(groups) != 1:
        raise CheckError(f"{where} has {len(groups)} phandle groups; expected one")
    tokens = expand(tokenize(groups[0]))
    bindings: list[Binding] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if not token.startswith("&"):
            raise CheckError(f"{where}: expected a behavior, found {token}")
        behavior = token[1:]
        if behavior not in cells:
            raise CheckError(
                f"{where}: unknown behavior '&{behavior}'. "
                "The cell-count table in this checker does not know it yet."
            )
        count = cells[behavior]
        params = tokens[i + 1 : i + 1 + count]
        if len(params) != count or any(p.startswith("&") for p in params):
            raise CheckError(
                f"{where}: '&{behavior}' needs {count} parameters "
                f"but the following tokens are {tokens[i + 1 : i + 1 + count + 2]}"
            )
        bindings.append(Binding(behavior, tuple(params)))
        i += 1 + count
    return bindings


def parse_spec(spec: str, cells: dict[str, int]) -> Binding:
    return parse_bindings(f"<{spec}>", cells, spec)[0]


def integers(raw: str) -> list[int]:
    groups = angle_groups(raw)
    if not groups:
        raise CheckError(f"no integers in {raw!r}")
    values: list[int] = []
    for group in groups:
        for token in tokenize(group):
            if not token.lstrip("-").isdigit():
                raise CheckError(f"expected an integer, found {token}")
            values.append(int(token))
    return values


def layer_names(raw: str, defines: dict[str, int]) -> tuple[str, ...]:
    groups = angle_groups(raw)
    if len(groups) != 1:
        raise CheckError(f"layer list {raw!r} is not one group")
    inverse = {value: name for name, value in defines.items()}
    names: list[str] = []
    for token in tokenize(groups[0]):
        if token in defines:
            names.append(token)
        elif token.isdigit() and int(token) in inverse:
            names.append(inverse[int(token)])
        else:
            raise CheckError(f"layer token {token} is not one of {LAYER_ORDER}")
    return tuple(names)


def find_one(nodes: list[Node], *, label: str | None = None, name: str | None = None) -> Node:
    found = [
        node
        for node in walk(nodes)
        if (label is None or node.label == label) and (name is None or node.name == name)
    ]
    described = label or name
    if len(found) != 1:
        raise CheckError(f"expected one node {described}, found {len(found)}")
    return found[0]


def compatible_is(node: Node, value: str) -> bool:
    return unquote(node.props.get("compatible")) == value


def binding_cells(roots: list[Node]) -> dict[str, int]:
    cells = dict(BUILTIN_CELLS)
    for node in walk(roots):
        raw = node.props.get("#binding-cells")
        if raw is None:
            continue
        values = integers(raw)
        if len(values) != 1:
            raise CheckError(f"{node.ref} #binding-cells is {raw}")
        cells[node.ref] = values[0]
    return cells


def hold_tap_order(node: Node) -> tuple[str, str]:
    raw = node.props.get("bindings")
    if raw is None:
        raise CheckError(f"{node.ref} has no bindings")
    groups = angle_groups(raw)
    refs: list[str] = []
    for group in groups:
        tokens = tokenize(group)
        if len(tokens) != 1 or not tokens[0].startswith("&"):
            raise CheckError(f"{node.ref} binding slot {group!r} is not a single behavior")
        refs.append(tokens[0][1:])
    if len(refs) != 2:
        raise CheckError(f"{node.ref} has {len(refs)} hold-tap slots, expected 2")
    return refs[0], refs[1]


def resolve(layers: list[list[Binding]], mask: set[int], position: int) -> Binding | None:
    """Highest active layer that is not `&trans`. Mirrors keymap.c.

    zmk_keymap_position_state_changed walks from the top layer down to the
    default layer and continues only when the behavior returns a positive
    code. `&trans` is that case. `&none` is opaque.
    """
    for index in range(len(layers) - 1, -1, -1):
        if index not in mask:
            continue
        binding = layers[index][position]
        if binding.behavior == "trans":
            continue
        return binding
    return None


def mask_text(mask: set[int]) -> str:
    return "+".join(LAYER_ORDER[index] for index in sorted(mask))


def place(position: int) -> str:
    return f"position {position} ({POS_NAME[position]})"


def load() -> tuple[dict[str, int], dict[str, int], list[Node], list[Node]]:
    if not KEYMAP.is_file():
        raise CheckError(f"missing keymap {KEYMAP}")
    if not LAYOUT.is_file():
        raise CheckError(f"missing layout {LAYOUT}")
    keymap_text, defines = strip_directives(strip_comments(KEYMAP.read_text()))
    layout_text, _layout_defines = strip_directives(strip_comments(LAYOUT.read_text()))
    _props, keymap_roots, _end = parse_body(keymap_text, 0, top=True)
    _lprops, layout_roots, _lend = parse_body(layout_text, 0, top=True)
    for name in LAYER_ORDER:
        if defines.get(name) is None:
            raise CheckError(f"keymap does not #define {name}")
    return defines, binding_cells(keymap_roots), keymap_roots, layout_roots


def check(dump: bool) -> list[str]:
    defines, cells, roots, layout_roots = load()
    failures: list[str] = []

    for name, index in zip(LAYER_ORDER, range(len(LAYER_ORDER)), strict=True):
        if defines[name] != index:
            failures.append(
                f"#{name} is defined as {defines[name]}, but ZMK numbers keymap "
                f"nodes from the top, so {name} has to be {index}."
            )

    chosen = [
        node.props.get("zmk,physical-layout")
        for node in walk(roots)
        if "zmk,physical-layout" in node.props
    ]
    if chosen != ["&default_layout"]:
        failures.append(
            "The keymap's chosen physical layout is "
            f"{chosen or 'missing'}, so key numbers are not the default 46-key map."
        )

    position_map = find_one(layout_roots, label="default_map")
    rows_raw = position_map.props.get("positions")
    if rows_raw is None:
        raise CheckError("default_map has no positions")
    rows = [tuple(integers(f"<{group}>")) for group in angle_groups(rows_raw)]
    if tuple(rows) != POSITION_ROWS:
        failures.append(
            "default_map no longer numbers the keys in keymap order "
            f"{POSITION_ROWS}. It is now {tuple(rows)}. Combo indexes would "
            "point at different keys."
        )

    layout = find_one(layout_roots, label="default_layout")
    keys_raw = layout.props.get("keys")
    if keys_raw is None:
        raise CheckError("default_layout has no keys")
    key_count = keys_raw.count("key_physical_attrs")
    expected_count = len(POS_NAME)
    if key_count != expected_count:
        failures.append(
            f"default_layout has {key_count} keys; the contract is {expected_count}."
        )

    keymap = find_one(roots, name="keymap")
    if not compatible_is(keymap, "zmk,keymap"):
        raise CheckError("keymap node is missing compatible = \"zmk,keymap\"")
    layer_nodes = keymap.children
    labels = [unquote(node.props.get("label")) for node in layer_nodes]
    if tuple(labels) != LAYER_ORDER:
        failures.append(
            "Layer nodes are "
            + ", ".join(labels)
            + ". ZMK activates them by node order, and the contract needs "
            + ", ".join(f"{name}={index}" for index, name in enumerate(LAYER_ORDER))
            + "."
        )
        return failures

    layers: list[list[Binding]] = []
    shape_bad = False
    for node in layer_nodes:
        raw = node.props.get("bindings")
        label = unquote(node.props.get("label"))
        if raw is None:
            failures.append(f"{label} has no bindings.")
            shape_bad = True
            continue
        parsed = parse_bindings(raw, cells, f"{label} bindings")
        if len(parsed) != expected_count:
            failures.append(
                f"{label} has {len(parsed)} bindings and the layout has "
                f"{expected_count} keys, so later positions are shifted."
            )
            shape_bad = True
        layers.append(parsed)
    if shape_bad or failures:
        return failures

    by_label = {unquote(node.props.get("label")): bindings for node, bindings in zip(layer_nodes, layers, strict=True)}

    def own(layer: str, position: int) -> Binding:
        return by_label[layer][position]

    if dump:
        for layer, position, spec, why in OWN:
            print(f"{layer:4} {place(position)}: {own(layer, position).display()}  ({why})")

    for layer, position, spec, why in OWN:
        got = own(layer, position)
        want = parse_spec(spec, cells)
        if got != want:
            failures.append(
                f"{why}. {layer} {place(position)} is {got.display()}, "
                f"and the contract says {want.display()}."
            )

    for layer in FALLTHROUGH_LAYERS:
        mask = {defines["BASE"], defines[layer]}
        for position, spec, why in FALLTHROUGH:
            got = resolve(layers, mask, position)
            want = parse_spec(spec, cells)
            got_text = got.display() if got else "nothing"
            if got != want:
                failures.append(
                    f"{why} on {layer}. With {mask_text(mask)} active, "
                    f"{place(position)} resolves to {got_text}, "
                    f"and the contract says {want.display()}."
                )

    # Every mask that includes BASE. BT is the top layer, so a Bluetooth
    # command on any lower layer shows up in the mask that omits BT.
    upper = [defines[name] for name in LAYER_ORDER if name != "BASE"]
    shortest: dict[int, tuple[set[int], Binding]] = {}
    total_masks = 1 << len(upper)
    for bits in range(total_masks):
        mask = {defines["BASE"]}
        for shift, index in enumerate(upper):
            if bits & (1 << shift):
                mask.add(index)
        for position in range(expected_count):
            got = resolve(layers, mask, position)
            if got is None or got.behavior not in ("bt", "out"):
                continue
            supplied = by_label["BT"][position]
            if defines["BT"] in mask and supplied == got:
                continue
            previous = shortest.get(position)
            if previous is None or len(mask) < len(previous[0]):
                shortest[position] = (mask, got)
    for position, (mask, got) in sorted(shortest.items()):
            failures.append(
            "A Bluetooth or output command is reached without the BT layer "
            f"supplying it. With {mask_text(mask)} active, {place(position)} "
            f"resolves to {got.display()}."
        )

    combos_node = find_one(roots, name="combos")
    if not compatible_is(combos_node, "zmk,combos"):
        raise CheckError("combos node is missing compatible = \"zmk,combos\"")
    found_combos = {node.name: node for node in combos_node.children}
    if set(found_combos) != set(COMBOS):
        extra = sorted(set(found_combos) - set(COMBOS))
        missing = sorted(set(COMBOS) - set(found_combos))
        failures.append(
            "The combo list changed. "
            f"Missing: {missing or 'none'}. Extra: {extra or 'none'}."
        )
    for name, spec in COMBOS.items():
        node = found_combos.get(name)
        if node is None:
            continue
        positions_raw = node.props.get("key-positions")
        layers_raw = node.props.get("layers")
        binding_raw = node.props.get("bindings")
        if positions_raw is None or layers_raw is None or binding_raw is None:
            failures.append(f"{name} is missing positions, layers, or a binding.")
            continue
        positions = tuple(integers(positions_raw))
        layer_list = layer_names(layers_raw, defines)
        parsed = parse_bindings(binding_raw, cells, name)
        want = parse_spec(spec["binding"], cells)
        if positions != spec["positions"] or layer_list != spec["layers"] or parsed != [want]:
            got_binding = parsed[0].display() if len(parsed) == 1 else parsed
            failures.append(
                f"{spec['why']}. {name} is positions "
                f"{', '.join(str(p) for p in positions)} on "
                f"{', '.join(layer_list)} sending {got_binding}; the contract is "
                f"positions {', '.join(str(p) for p in spec['positions'])} on "
                f"{', '.join(spec['layers'])} sending {want.display()}."
            )

    behaviors = find_one(roots, name="behaviors")
    behavior_by_ref = {node.ref: node for node in behaviors.children}
    ext_mod = behavior_by_ref.get("ext_mod")
    if ext_mod is None or not compatible_is(ext_mod, "zmk,behavior-hold-tap"):
        failures.append("ext_mod is not a hold-tap, so tap and hold are not MOD and EXT.")
    else:
        hold, tap = hold_tap_order(ext_mod)
        if (hold, tap) != ("mo", "sl"):
            failures.append(
                f"ext_mod hold is {hold} and tap is {tap}. "
                "Hold has to be momentary EXT and tap has to be sticky MOD."
            )

    sticky = behavior_by_ref.get("sticky_layer")
    if sticky is None or not compatible_is(sticky, "zmk,behavior-sticky-key"):
        failures.append("sticky_layer is not a sticky-key wrapping a momentary layer.")
    else:
        raw = sticky.props.get("bindings")
        slots = [tokenize(group) for group in angle_groups(raw or "")]
        if slots != [["&mo"]]:
            failures.append(
                f"sticky_layer activates {raw}, and the contract needs it to activate &mo."
            )

    backspace = behavior_by_ref.get("backspace_delete")
    if backspace is None or not compatible_is(backspace, "zmk,behavior-mod-morph"):
        failures.append(
            "backspace_delete is not a mod-morph, so Shift+Backspace is not Delete."
        )
    else:
        raw = backspace.props.get("bindings") or ""
        groups = [
            parse_bindings(f"<{group}>", cells, "backspace_delete")[0]
            for group in angle_groups(raw)
        ]
        want_groups = [parse_spec("&kp BSPC", cells), parse_spec("&kp DEL", cells)]
        mods = backspace.props.get("mods") or ""
        if groups != want_groups:
            got = ", ".join(item.display() for item in groups) or "nothing"
            failures.append(
                "Shift+Backspace has to send Delete. backspace_delete sends "
                f"{got} instead of &kp BSPC, then &kp DEL."
            )
        elif "MOD_LSFT" not in mods or "MOD_RSFT" not in mods:
            failures.append(
                "Shift+Backspace has to send Delete. backspace_delete watches "
                f"{mods or 'no modifiers'} instead of left and right Shift."
            )

    for name in SWAPPERS:
        node = behavior_by_ref.get(name)
        if node is None or not compatible_is(node, "zmk,behavior-tri-state"):
            failures.append(f"{name} is not a tri-state, so its ignore list does not protect Shift.")
            continue
        raw = node.props.get("ignored-key-positions")
        got = tuple(integers(raw)) if raw else ()
        if got != IGNORED_SHIFT:
            failures.append(
                f"{name} ignores positions {list(got) or 'nothing'}. "
                "It has to ignore only position 15, the EXT home-row Shift, "
                "or Cmd-Tab releases when that Shift is tapped."
            )

    ignored_elsewhere = [
        node.ref
        for node in walk(roots)
        if node.ref not in SWAPPERS and "ignored-key-positions" in node.props
    ]
    if ignored_elsewhere:
        failures.append(
            "These behaviors also ignore key positions, which the contract "
            f"does not: {', '.join(ignored_elsewhere)}."
        )

    # Layer entry. ext_mod's first cell is the held layer and its second is the tap.
    layer_params = {
        "mo": (0,),
        "sl": (0,),
        "to": (0,),
        "tog": (0,),
        "sticky_layer": (0,),
        "ext_mod": (0, 1),
    }
    activations: dict[str, list[str]] = {name: [] for name in LAYER_ORDER}

    def record(site: str, binding: Binding) -> None:
        for slot in layer_params.get(binding.behavior, ()):
            if slot >= len(binding.params):
                continue
            param = binding.params[slot]
            if param not in defines:
                continue
            kind = binding.behavior
            if binding.behavior == "ext_mod":
                kind = "mo" if slot == 0 else "sl"
            if binding.behavior == "sticky_layer":
                kind = "mo"
            activations[param].append(f"{kind} {param} at {site}")

    for label, bindings in by_label.items():
        for position, binding in enumerate(bindings):
            record(f"{label} {place(position)}", binding)
    for name, node in found_combos.items():
        raw = node.props.get("bindings")
        if raw is None:
            continue
        for binding in parse_bindings(raw, cells, name):
            record(name, binding)

    bt_sites = activations["BT"]
    mf_sites = activations["MF"]
    if bt_sites != ["mo BT at combo_bt"]:
        failures.append(
            "BT has to turn on only from combo_bt. It is turned on from: "
            + (", ".join(bt_sites) or "nowhere")
            + "."
        )
    if mf_sites != ["mo MF at combo_mf_layer_thumbs"]:
        failures.append(
            "MF has to turn on only from the outer-thumb combo. It is turned on from: "
            + (", ".join(mf_sites) or "nowhere")
            + "."
        )
    ext_sites = [site for site in activations["EXT"] if site.startswith("mo EXT")]
    mod_sites = [site for site in activations["MOD"] if site.startswith("sl MOD")]
    if ext_sites != ["mo EXT at BASE " + place(41)]:
        failures.append(
            "Hold for EXT has to be only the left middle thumb. Found: "
            + (", ".join(ext_sites) or "nowhere")
            + "."
        )
    if mod_sites != ["sl MOD at BASE " + place(41)]:
        failures.append(
            "Tap for sticky MOD has to be only the left middle thumb. Found: "
            + (", ".join(mod_sites) or "nowhere")
            + "."
        )
    if any(binding.behavior == "dft" for bindings in layers for binding in bindings):
        failures.append(
            "A key changes the default layer. Transparent keys would stop "
            "falling through to BASE, and this checker always falls through to BASE."
        )
    return failures


def main() -> int:
    dump = "--dump" in sys.argv
    try:
        failures = check(dump)
    except CheckError as exc:
        print(f"ERROR\nThis is a problem in the checker, not a keymap finding: {exc}")
        return 2
    if failures:
        print("FAIL")
        for index, failure in enumerate(failures, start=1):
            print(f"{index}. {failure}")
        return 1
    print("PASS")
    print(
        "Every chord, the Cmd-Tab reverse-shift, Backspace, Space, and the "
        "Bluetooth keys match the layout contract."
    )
    print(
        f"Checked {len(POS_NAME)} positions x {1 << (len(LAYER_ORDER) - 1)} "
        "layer masks, 6 combos, and both swappers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
