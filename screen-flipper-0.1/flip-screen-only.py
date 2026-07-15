#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys


def detect_display_name(xrandr_output):
    for line in xrandr_output.splitlines():
        if " connected" not in line:
            continue

        parts = line.split()
        if not parts:
            continue

        name = parts[0]
        if "primary" in line.lower():
            return name

    for line in xrandr_output.splitlines():
        if " connected" in line:
            return line.split()[0]

    raise RuntimeError("No connected display found")


def apply_orientation(mode, output_name=None):
    if mode not in ("normal", "inverted"):
        raise ValueError("mode must be 'normal' or 'inverted'")

    if shutil.which("kscreen-doctor"):
        target_output = output_name or ""
        if target_output:
            rotate_value = "none" if mode == "normal" else "inverted"
            subprocess.run(["kscreen-doctor", f"output.{target_output}.rotation.{rotate_value}"], check=True)
            return

        try:
            display_output = subprocess.check_output(["xrandr", "--query"], text=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise RuntimeError("Unable to detect a display for kscreen-doctor") from exc

        target_output = detect_display_name(display_output)
        rotate_value = "none" if mode == "normal" else "inverted"
        subprocess.run(["kscreen-doctor", f"output.{target_output}.rotation.{rotate_value}"], check=True)
        return

    try:
        display_output = subprocess.check_output(["xrandr", "--query"], text=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError("Neither kscreen-doctor nor xrandr is available") from exc

    target_output = detect_display_name(display_output)
    subprocess.run(["xrandr", "--output", target_output, "--rotate", mode], check=True)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Apply a screen orientation change")
    parser.add_argument("mode", nargs="?", choices=("normal", "inverted"), default="inverted")
    parser.add_argument("--output", default=None, help="Optional output name for kscreen-doctor")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    try:
        apply_orientation(args.mode, args.output)
        print(f"Applied {args.mode} rotation to {args.output or 'primary display'}")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
