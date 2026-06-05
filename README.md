# Louis' E Blues

**Live:** https://brona90.github.io/louisblues/

A standalone, offline-capable practice app for the E 12-bar blues on
guitar — the form, the three dominant 7 chords in every position up the
neck, the scales, the licks, the shuffle rhythms, and a daily routine.
Built as a Progressive Web App so it installs from Safari to the iOS
home screen and runs without a network.

Midnight-blue dark theme, cream practice-paper cards, brass-gold italic
accents. Tap any card to play it back through a Karplus-Strong synth;
the chord-box dot or scale-box dot AND the matching tab note light up
in time with the audio.

## Pages

- **The Form** — twelve-bar jazz / quick-change chart with the three
  chord diagrams above and a Charleston comping pattern.
- **E7 / A7 / B7 shapes** — every CAGED inversion up the neck for each
  of the three blues chords.
- **9th chords** — E9, A9, B9, E13, A13, B13 — the Memphis / Wes
  Montgomery / jazz-blues colours.
- **E minor pentatonic** — five box positions across the neck.
- **E blues scale** — pentatonic + the ♭5 blue note at every position.
- **E mixolydian** — open and 7th-fret boxes.
- **Whole neck** — every box joined into one map, played as a
  position-by-position walk (each box up-and-down, then the next).
- **Classic licks** — six iconic phrases: pull-off lick, BB-King bend,
  Chuck Berry double-stops, Albert-King-style bend, two turnarounds,
  and a Hendrix-style ending.
- **Shuffle rhythm** — boogie shuffle, Texas shuffle, slow 12/8.
- **Daily routine** — a 30-minute lap through everything.

## Build

```bash
python3 build.py
```

Outputs `index.html`, one `<slug>.html` per exercise, `manifest.webmanifest`,
`sw.js`, `icon.svg`, and `apple-touch-icon.png` into the repo root. Every
page is fully self-contained — inline CSS, base64-embedded Fraunces font,
inline SVG for every diagram and tab — and works straight off a static
host.

Requires Python 3 and ImageMagick (`magick`) to rasterise the SVG icon.

## Install on iOS

1. Visit https://brona90.github.io/louisblues/ in mobile Safari.
2. Tap the share icon → **Add to Home Screen**.
3. The app installs with the icon, launches in standalone mode, and
   works offline thanks to the service worker.

## Features

- **Karplus-Strong audio** — soft plucked-string tone, no samples
- **Lit notes** — every chord-box dot, scale-box dot, and tab number
  flashes brass-gold the moment its note sounds; both the diagram and
  the tab light up together
- **Metronome controls every playback** — one bpm slider drives the
  entire app, chord strums and scale walks alike
- **Loop** — modal Loop button cycles off → ∞ → 4× → 2× and persists
  the choice across reloads
- **Fullscreen modal** — click any card to see it big; ← / → or swipe
  to navigate; ESC or click-out closes
- **Click-to-play** — every card has a play button (small ▶ top-right
  on the card, big in the modal); click again to stop
- **Silence all** — one button in the metronome panel kills every
  scheduled note and animation
- **Print stylesheet** — tabs and chord diagrams print cleanly without
  the metronome or play buttons

## Layout

```
louisblues/
├── build.py                       # discovers exercises, emits the site
├── src/
│   ├── render.py                  # shared template, CSS, JS, audio synth
│   ├── fretboard.py               # chord-box and scale-box SVG
│   ├── tab.py                     # tab notation SVG
│   ├── font_regular.b64           # Fraunces (variable, normal)
│   ├── font_italic.b64            # Fraunces (variable, italic)
│   └── exercises/
│       ├── form.py
│       ├── e7_shapes.py
│       ├── a7_shapes.py
│       ├── b7_shapes.py
│       ├── ninth_chords.py
│       ├── pentatonic.py
│       ├── blues_scale.py
│       ├── mixolydian.py
│       ├── neck_overview.py
│       ├── licks.py
│       ├── shuffle.py
│       └── routine.py
├── icon.svg                       # generated source for the app icon
├── apple-touch-icon.png           # built from icon.svg
├── manifest.webmanifest           # built
├── sw.js                          # built
├── index.html                     # built
└── <slug>.html × 12               # built (one per exercise)
```

## Adding an exercise

1. Drop a new file into `src/exercises/<slug>.py` exporting an
   `EXERCISE` dict (use any existing file as a template).
2. Run `python3 build.py`.

## Deploying to GitHub Pages

Pushing to `main` triggers `.github/workflows/deploy.yml`, which sets up
Python and ImageMagick, runs `build.py`, and publishes the result to
GitHub Pages — live at https://brona90.github.io/louisblues/. Pages is
configured with source = "GitHub Actions".
