#!/usr/bin/env python3
"""Build all HTML pages, the landing index, manifest, and service worker.

Usage:  python3 build.py
Outputs into the repo root: index.html, <slug>.html for every exercise,
manifest.webmanifest, sw.js, icon.svg, apple-touch-icon.png.
"""

import importlib.util
import os
import sys
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
EXERCISES_DIR = os.path.join(SRC, 'exercises')

sys.path.insert(0, SRC)

import render  # noqa: E402


def load_exercise(slug):
    path = os.path.join(EXERCISES_DIR, f'{slug}.py')
    spec = importlib.util.spec_from_file_location(f'ex_{slug}', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EXERCISE


def discover_exercises():
    """Find all exercise modules and load them, sorted by order."""
    exs = []
    for fn in sorted(os.listdir(EXERCISES_DIR)):
        if fn.endswith('.py') and not fn.startswith('_'):
            slug = fn[:-3]
            exs.append(load_exercise(slug))
    exs.sort(key=lambda e: e.get('order', 999))
    return exs


def build_apple_touch_icon():
    """Use ImageMagick to convert icon.svg → apple-touch-icon.png."""
    icon_svg = os.path.join(ROOT, 'icon.svg')
    out_png = os.path.join(ROOT, 'apple-touch-icon.png')
    if not os.path.exists(icon_svg):
        print(f'[skip png] no icon.svg yet')
        return
    # ImageMagick 7 ships `magick`; v6 (e.g. Ubuntu apt) ships `convert`.
    for cmd in (['magick'], ['convert']):
        try:
            subprocess.run(
                cmd + [icon_svg, '-resize', '180x180', out_png],
                check=True, capture_output=True,
            )
            print(f'[png ok] {os.path.basename(out_png)} (via {cmd[0]})')
            return
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError as e:
            print(f'[png skip] {cmd[0]} failed: {e}')
            return
    print('[png skip] neither magick nor convert found')


def main():
    exs = discover_exercises()
    print(f'Found {len(exs)} exercises:')
    for e in exs:
        print(f'  · {e["slug"]} ({e["section"]})')

    render.build_assets(exs)
    print('Built manifest.webmanifest, sw.js, icon.svg')

    build_apple_touch_icon()

    for e in exs:
        path = render.build_page(e, exs)
        print(f'[page] {os.path.relpath(path, ROOT)}')

    path = render.build_index(exs)
    print(f'[index] {os.path.relpath(path, ROOT)}')


if __name__ == '__main__':
    main()
