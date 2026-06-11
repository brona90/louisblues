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


# Keys every EXERCISE dict must define for build.py + render.py to work.
REQUIRED_KEYS = (
    'slug', 'order', 'section',
    'title_one', 'title_em', 'eyebrow', 'subtitle',
)


def load_exercise(slug):
    path = os.path.join(EXERCISES_DIR, f'{slug}.py')
    spec = importlib.util.spec_from_file_location(f'ex_{slug}', path)
    if spec is None or spec.loader is None:
        raise ValueError(f'{path}: could not create import spec')
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        raise ValueError(f'{path}: failed to import module: {e}') from e

    ex = getattr(mod, 'EXERCISE', None)
    if ex is None:
        raise ValueError(f'{path}: module defines no EXERCISE dict')
    if not isinstance(ex, dict):
        raise ValueError(
            f'{path}: EXERCISE must be a dict, got {type(ex).__name__}'
        )
    for key in REQUIRED_KEYS:
        if key not in ex:
            raise ValueError(f'{path}: EXERCISE missing required key {key!r}')
    return ex


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


# apple-touch-icon.png is a REQUIRED build product: the service worker's
# cache.addAll() is atomic, so a missing icon makes the SW install reject
# and breaks offline mode entirely. Treat anything under this as a failure.
MIN_ICON_BYTES = 1024


def require_apple_touch_icon():
    """Assert apple-touch-icon.png exists and is a non-trivial PNG."""
    out_png = os.path.join(ROOT, 'apple-touch-icon.png')
    if not os.path.exists(out_png):
        sys.exit(
            'ERROR: apple-touch-icon.png was not produced. ImageMagick could '
            'not rasterise icon.svg (missing binary or SVG delegate). This '
            'icon is a required build product — a missing icon makes the '
            'service worker install reject and breaks offline mode. '
            'Install ImageMagick (magick or convert) plus an SVG delegate '
            '(librsvg2-bin) and rebuild.'
        )
    size = os.path.getsize(out_png)
    if size <= MIN_ICON_BYTES:
        sys.exit(
            f'ERROR: apple-touch-icon.png is only {size} bytes '
            f'(expected > {MIN_ICON_BYTES}). The rasterisation likely '
            'failed silently. Check the ImageMagick SVG delegate '
            '(librsvg2-bin) and rebuild.'
        )


def main():
    exs = discover_exercises()
    print(f'Found {len(exs)} exercises:')
    for e in exs:
        print(f'  · {e["slug"]} ({e["section"]})')

    render.build_assets(exs)
    print('Built manifest.webmanifest, sw.js, icon.svg')

    build_apple_touch_icon()
    require_apple_touch_icon()

    for e in exs:
        path = render.build_page(e, exs)
        print(f'[page] {os.path.relpath(path, ROOT)}')

    path = render.build_index(exs)
    print(f'[index] {os.path.relpath(path, ROOT)}')


if __name__ == '__main__':
    main()
