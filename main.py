#!/usr/bin/env python3
"""Entry program for the 20 November 2026 news-image bounty.

The front page is pre-drawn (entry.png, built by generate.py in the same
session that wrote this file). At grade time the repository is read-only
and there is no network, so this program only copies the finished image
into the output directory. It writes nothing next to itself.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print(f"missing {src}", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    print(f"wrote {dst} {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
