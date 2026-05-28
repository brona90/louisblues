"""The 12-bar blues form in E — diagrammed, comped, and tab'd.

Three cards:
- The skeleton: 12 bars of chord names, the form on one page.
- Quick-change variant.
- A simple comping rhythm rendered in tab.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tab import tab_line
from fretboard import chord_strip

E7_OPEN_S   = [0, 2, 0, 1, 0, 0]
A7_OPEN_S   = [None, 0, 2, 0, 2, 0]
B7_OPEN_S   = [None, 2, 1, 2, 0, 2]
E7_BARRE_7S = [None, 7, 9, 7, 9, 7]
E7_OPEN_R = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}
A7_OPEN_R = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
B7_OPEN_R = {5: 'R', 4: '3', 3: 'b7', 2: '5', 1: 'b7'}
E7_BARRE_R = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}

THREE_CHORDS = [('E7 — I⁷', E7_OPEN_S, E7_OPEN_R),
                ('A7 — IV⁷', A7_OPEN_S, A7_OPEN_R),
                ('B7 — V⁷', B7_OPEN_S, B7_OPEN_R)]


# Slash-chart — pure HTML/CSS so it reflows on narrow screens.
# 4 bars per row on desktop, 2 per row on tablet, 1 per row on phone.
def bar_grid(bars):
    """Render the 12-bar form as a responsive HTML/CSS grid."""
    cells = []
    for i, ch in enumerate(bars):
        last = ' chart-bar-last' if i == len(bars) - 1 else ''
        cells.append(
            f'<div class="chart-bar{last}">'
            f'<span class="chart-bar-num">{i + 1}</span>'
            f'<span class="chart-chord">{ch}</span>'
            f'<span class="chart-slashes">/ / / /</span>'
            f'</div>'
        )
    return f'<div class="chart-grid">{"".join(cells)}</div>'


QC_FORM = ['E7', 'A7', 'E7', 'E7',
           'A7', 'A7', 'E7', 'E7',
           'B7', 'A7', 'E7', 'B7']

# Voicings for progression playback — match the chord-strip diagrams 1:1
# so the lit-dot animation can land on the right chord-box per bar.
E7_VOICE = [0, 2, 0, 1, 0, 0]      # open E7
A7_VOICE = [None, 0, 2, 0, 2, 0]   # open A7
B7_VOICE = [None, 2, 1, 2, 0, 2]   # open B7

CHORD_TO_SHAPE = {'E7': E7_VOICE, 'A7': A7_VOICE, 'B7': B7_VOICE}


# A simple two-chord comp pattern (one bar of E7 then one of A7, A-shape voicings):
# Charleston-ish: chord on 1, rest, chord on the "and of 2", chord on 4. Render as tab.
# We use the A-shape E7 barre at fret 7 and open A7.
E7_BARRE = [(5,7),(4,9),(3,7),(2,9),(1,7)]  # for tab
A7_OPEN_NOTES = [(5,0),(4,2),(3,0),(2,2),(1,0)]


def comp_card():
    # 16 sixteenth-note slots per bar of comping for clean rendering: simplify to 16-slot lines.
    # Pattern (8 slots = eighth notes per bar): X . X . . X . .  (Charleston)
    # Two bars, 16 slots total.
    events_bar1 = []
    pattern = [True, False, False, True, False, True, False, False]  # 8th-note pattern
    for hit in pattern:
        if hit:
            events_bar1.append(('chord', E7_BARRE))
        else:
            events_bar1.append(('rest',))
    events_bar2 = []
    for hit in pattern:
        if hit:
            events_bar2.append(('chord', A7_OPEN_NOTES))
        else:
            events_bar2.append(('rest',))
    events = events_bar1 + events_bar2
    return tab_line(events, beats_per_line=16, bar_lines=[8, 16], labels=[(0, 'E7'), (8, 'A7')], width=900, height=160)


EXERCISE = {
    "slug": "form",
    "order": 1,
    "section": "The Form",
    "title_one": "Twelve-Bar",
    "title_em": "Form",
    "eyebrow": "E Blues · The Skeleton",
    "eyebrow_short": "The Form",
    "subtitle": "Three chords, twelve bars, the whole language.",
    "intro_prose": """
      <p>The 12-bar blues form is the most-played progression in popular
      music. Every blues, every bebop head built on a blues, every funk
      tune, half of rock — they sit on this skeleton.</p>
      <p>In E, the three chords are <strong>E7</strong> (I⁷),
      <strong>A7</strong> (IV⁷), and <strong>B7</strong> (V⁷). Every chord
      is a <em>dominant 7</em> — that's the defining harmonic feature of
      the blues. The tonic isn't a maj7. The IV isn't a maj7. Every chord
      pulls toward something else, and nothing ever fully resolves.</p>
      <p>We use the <em>quick-change</em> (jazz) form: bar 2 hits the IV,
      then returns to I. Bars 5–6 sit on IV. Bar 9 is V. Bars 11–12 are the
      turnaround. This is the form behind every bebop blues head and most
      modern blues.</p>
    """,
    "intro_pills": [
        ("Three chords", "I⁷  IV⁷  V⁷  →  E7  A7  B7 — all dominant 7."),
        ("Twelve bars", "Four bars of I, two of IV, two of I, then V–IV–I–V."),
    ],
    "sections": [
        {
            "heading": "The form",
            "blurb": "Jazz / quick-change blues — bar 2 drops to the IV before returning home. This is the form behind every bebop blues head (<em>Billie's Bounce, Now's The Time, Tenor Madness</em>) and most modern blues.",
            "layout": "full",
            "cards": [
                {
                    "num": "12 bars",
                    "title": "Jazz blues in E — quick change",
                    "role": "I — IV — I — I / IV — IV — I — I / V — IV — I — V",
                    "body": chord_strip(THREE_CHORDS) + bar_grid(QC_FORM),
                    "caption": "The one bar of IV in position 2 wakes up the form. Bar 9 hits V; bars 11–12 are the turnaround. Tap to hear it.",
                    "audio": {"type": "progression", "bpm": 80,
                              "bars": [{"shape": CHORD_TO_SHAPE[ch], "beats": 4} for ch in QC_FORM]},
                },
            ],
        },
        {
            "heading": "Comping skeleton",
            "blurb": "A Charleston-style rhythm — chord on beat 1, on the \"and\" of 2, on beat 4. Bar 1 is E7 (A-shape barre, fret 7); bar 2 is open A7. Loop it.",
            "layout": "full",
            "cards": [
                {
                    "num": "Pattern",
                    "title": "Charleston comp — I⁷ → IV⁷",
                    "role": "Eighth notes · accent the off-beat",
                    "body": chord_strip([('E7 — A barre, fret 7', E7_BARRE_7S, E7_BARRE_R),
                                         ('A7 — open', A7_OPEN_S, A7_OPEN_R)]) + comp_card(),
                    "caption": "Don't strum all six strings — pick the chord and let the bass note ring. Mute the strings between hits with your fretting hand.",
                    "audio": {
                        "type": "comp", "bpm": 100, "duration": 8,
                        # Match the chord-strip exactly so the lit-dot animation
                        # fires on the right chord-box per beat.
                        # Bar 1 → E7 A-shape barre fret 7, bar 2 → A7 open.
                        "hits": [
                            {"beat": 0.0, "shape": E7_BARRE_7S},
                            {"beat": 1.5, "shape": E7_BARRE_7S},
                            {"beat": 2.5, "shape": E7_BARRE_7S},
                            {"beat": 4.0, "shape": A7_OPEN_S},
                            {"beat": 5.5, "shape": A7_OPEN_S},
                            {"beat": 6.5, "shape": A7_OPEN_S},
                        ],
                    },
                },
            ],
        },
    ],
    "next_step": {
        "heading_one": "Where the ",
        "heading_em": "language",
        "heading_two": " starts",
        "body": "<p>Memorise the form first. Then memorise it in <em>quick change</em>. Then play it through with just bass-note shells — root on 1, fifth on 3. Once you can play the form without thinking about it, the chord shapes pages and the scale pages start to land harder.</p>",
        "items": [
            ("3 min", "Count the form aloud: <em>one — four — one — one — four — four — one — one — five — four — one — five</em>. Two times through."),
            ("5 min", "Loop the form on open chords. E7 (open) → A7 (open) → B7 (open). Land each chord on beat 1."),
            ("4 min", "Add the comping pattern above. Don't worry about beauty — worry about hitting the bar lines."),
        ],
    },
    "closing": "Twelve bars. Three chords. A hundred years of music.",
}
