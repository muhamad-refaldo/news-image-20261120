#!/usr/bin/env python3
"""news-image-20261120 v2 entrypoint.

Copies the pre-built front-page image (entry.png, in the same directory as
this script) to the output directory. No network, no regeneration, no writes
beside the script: the repo is read-only at grading time, so the only write
is the copy into $MAKEFUN_OUTPUT_DIR (or /output).
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
