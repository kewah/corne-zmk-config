#!/usr/bin/env python3
"""HID order when the top-left key cancels the app switcher.

macOS commits Cmd-Tab when Command goes up. Escape cancels the switcher
only while Command is still down. The tri-state listener runs before the
keymap and, on any other key, releases Command before that key is sent.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KEYMAP = ROOT / "config" / "corne_choc_pro.keymap"
CANCEL_C = ROOT / "behaviors" / "swapper_cancel.c"
HOST_C = Path(__file__).resolve().parent / "swapper_cancel_host.c"
INCLUDE = ROOT / "behaviors"

WANTED_CANCEL = "Escape down, Escape up, Command up"


def behavior_body(text: str, name: str) -> str:
    match = re.search(rf"\n        {name}: {name} \{{(.*?)\n        \}};", text, re.S)
    if match is None:
        raise SystemExit(f"ERROR\nThe keymap has no {name} behavior.")
    return match.group(1)


def prop(body: str, name: str) -> str | None:
    match = re.search(rf"{re.escape(name)} = <([^>]*)>;", body)
    if match is None:
        return None
    return match.group(1).strip()


def ext_top_left(text: str) -> str:
    match = re.search(r'label = "EXT";\s*bindings = <\s*(&[^&\n]+)', text)
    if match is None:
        raise SystemExit("ERROR\nThe EXT layer has no first binding.")
    return match.group(1).strip()


def upstream_cancel_trace() -> str:
    """Current interrupt path. Command releases before the EXT binding."""
    return "Command up, Cmd+grave"


def compile_cancel_trace() -> str | None:
    if not CANCEL_C.is_file():
        return None
    with tempfile.TemporaryDirectory() as directory:
        binary = Path(directory) / "swapper_cancel_host"
        compiled = subprocess.run(
            [
                "gcc",
                "-std=c11",
                "-Wall",
                "-Werror",
                "-I",
                str(INCLUDE),
                str(CANCEL_C),
                str(HOST_C),
                "-o",
                str(binary),
            ],
            capture_output=True,
            text=True,
        )
        if compiled.returncode != 0:
            raise SystemExit(
                "ERROR\nThe cancel model failed to compile.\n"
                + compiled.stderr
                + compiled.stdout
            )
        ran = subprocess.run([str(binary)], capture_output=True, text=True)
        if ran.returncode != 0:
            raise SystemExit("ERROR\nThe cancel model exited nonzero.\n" + ran.stdout + ran.stderr)
        return ran.stdout


def findings() -> list[str]:
    text = KEYMAP.read_text()
    swapper = behavior_body(text, "swapper")
    tabs = behavior_body(text, "tab_swapper")
    problems: list[str] = []

    positions = prop(swapper, "cancel-key-positions")
    keycode = prop(swapper, "cancel-keycode")
    if positions != "0" or keycode != "ESC":
        problems.append(
            "swapper does not cancel from the top-left key. "
            f"cancel-key-positions is {positions or 'unset'} and "
            f"cancel-keycode is {keycode or 'unset'}. "
            "Both have to be position 0 and ESC."
        )
    if prop(tabs, "cancel-key-positions") is not None or prop(tabs, "cancel-keycode") is not None:
        problems.append(
            "tab_swapper also declares a cancel key. "
            "Only the Cmd-Tab swapper cancels from Escape."
        )
    top_left = ext_top_left(text)
    if top_left != "&kp LG(GRAVE)":
        problems.append(
            f"EXT top-left is {top_left}. "
            "It has to stay &kp LG(GRAVE) when the app switcher is idle."
        )
    for name, body in (("swapper", swapper), ("tab_swapper", tabs)):
        ignored = prop(body, "ignored-key-positions")
        if ignored != "15":
            problems.append(
                f"{name} ignores {ignored or 'nothing'}. "
                "The reverse-shift key has to stay position 15."
            )

    compiled = compile_cancel_trace()
    if compiled is None:
        got = upstream_cancel_trace()
        if got != WANTED_CANCEL:
            problems.append(
                "Top-left while Cmd-Tab is held sends "
                f"{got}. macOS needs {WANTED_CANCEL}."
            )
        return problems

    lines = dict(
        line.split(" handled ", 1)
        for line in compiled.splitlines()
        if " handled " in line
    )
    cancel = lines.get("cancel", "")
    handled, _, trace = cancel.partition(":")
    trace = trace.strip()
    if handled != "1" or trace != WANTED_CANCEL:
        problems.append(
            "Top-left while Cmd-Tab is held sends "
            f"{trace or 'nothing'} (handled {handled or 'missing'}). "
            f"macOS needs {WANTED_CANCEL}."
        )
    for label in ("other", "shift", "own"):
        entry = lines.get(label, "")
        other_handled, _, other_trace = entry.partition(":")
        if other_handled != "0" or other_trace.strip():
            problems.append(
                f"The {label} key is treated as cancel ({entry or 'missing'}). "
                "Only the top-left key cancels, and the reverse-shift key "
                "still has to leave Command held."
            )
    return problems


def main() -> int:
    problems = findings()
    if problems:
        print("FAIL")
        for index, problem in enumerate(problems, start=1):
            print(f"{index}. {problem}")
        return 1
    print("PASS")
    print(
        "While Cmd-Tab is held, the top-left key sends "
        f"{WANTED_CANCEL}. Idle EXT top-left stays Cmd+grave. "
        "Shift still reverses without releasing Command."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
