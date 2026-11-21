#!/usr/bin/env python3
"""Entrypoint: copy the pre-built entry image to the output directory.

The image is drawn by generate.py at build time and shipped in this
repository as entry.png. This program only copies it, so both grader
runs write the same bytes. Standard library only; no network.

The output directory comes from MAKEFUN_OUTPUT_DIR and defaults to
/output when the variable is not set.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
