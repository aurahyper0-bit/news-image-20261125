#!/usr/bin/env python3
"""Entrypoint for 'The World — 25 November 2026' (make.fun news-image-20261125).

The repository holds the finished front page as entry.png; this program
places an exact copy at $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png
when the variable is unset) and checks the copy is a genuine 1024x1024 PNG
before reporting its size. Standard library only; every run writes the
same bytes.

Run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_png_dimensions(path):
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        fail(path + " is not a PNG file")
    if head[12:16] != b"IHDR":
        fail(path + " has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        fail("entry.png is missing next to main.py")

    width, height = read_png_dimensions(source)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if os.path.getsize(source) == 0:
        fail("entry.png is empty")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)

    copied = os.path.getsize(target)
    if copied != os.path.getsize(source):
        fail("copy size mismatch for entry.png")
    target_width, target_height = read_png_dimensions(target)
    if (target_width, target_height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("copied entry.png is %dx%d, expected 1024x1024"
             % (target_width, target_height))
    print("wrote %s (%d bytes, %dx%d)" % (target, copied, width, height))


if __name__ == "__main__":
    main()
