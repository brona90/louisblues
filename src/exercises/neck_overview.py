"""Whole-neck pentatonic overview — see all five boxes at once.

This is the "aha moment" page: once you can see all five boxes as one
continuous map, the neck stops being five rooms and becomes one
instrument.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import scale_box, chord_strip
from tab import n, render_tab


OPEN_MIDI = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}


# Five CAGED boxes of E minor pentatonic, each centred on a different
# region of the neck. Within each box, the positions ascend in pitch.
PENT_BOXES = [
    # Box 1 — open position (also 12th fret)
    [(6, 0), (6, 3), (5, 0), (5, 2), (4, 0), (4, 2), (3, 0), (3, 2),
     (2, 0), (2, 3), (1, 0), (1, 3)],
    # Box 2 — fret 2–5
    [(6, 3), (6, 5), (5, 2), (5, 5), (4, 2), (4, 5), (3, 2), (3, 4),
     (2, 3), (2, 5), (1, 3), (1, 5)],
    # Box 3 — fret 4–7
    [(6, 5), (6, 7), (5, 5), (5, 7), (4, 5), (4, 7), (3, 4), (3, 7),
     (2, 5), (2, 8), (1, 5), (1, 7)],
    # Box 4 — fret 7–10
    [(6, 7), (6, 10), (5, 7), (5, 10), (4, 7), (4, 9), (3, 7), (3, 9),
     (2, 8), (2, 10), (1, 7), (1, 10)],
    # Box 5 — fret 9–12
    [(6, 10), (6, 12), (5, 10), (5, 12), (4, 9), (4, 12), (3, 9), (3, 12),
     (2, 10), (2, 12), (1, 10), (1, 12)],
]
# Box 1 again one octave up at fret 12 — completes the walk to the top of the neck
PENT_BOXES.append([(6, 12), (6, 15), (5, 12), (5, 14), (4, 12), (4, 14),
                    (3, 12), (3, 14), (2, 12), (2, 15), (1, 12), (1, 15)])


def _box_asc_desc(box):
    """Sort the box's positions ascending by pitch, then add the descending
    pass back down (without repeating the highest note)."""
    asc = sorted(box, key=lambda sf: OPEN_MIDI[sf[0]] + sf[1])
    desc = list(reversed(asc[:-1]))
    return asc + desc


def _pent_walk():
    """Walk every CAGED box up-and-down before moving to the next position."""
    seq = []
    for box in PENT_BOXES:
        seq.extend(_box_asc_desc(box))
    return seq


# Same idea for the blues scale (pentatonic + ♭5)
BLUES_BOXES = [
    [(6, 0), (6, 3), (5, 0), (5, 1), (5, 2), (4, 0), (4, 2), (3, 0), (3, 2),
     (3, 3), (2, 0), (2, 3), (1, 0), (1, 3)],
    [(6, 3), (6, 5), (6, 6), (5, 2), (5, 5), (4, 2), (4, 5), (3, 2), (3, 3),
     (3, 4), (2, 3), (2, 5), (1, 3), (1, 5)],
    [(6, 5), (6, 6), (6, 7), (5, 5), (5, 7), (4, 5), (4, 7), (4, 8), (3, 4),
     (3, 7), (2, 5), (2, 8), (1, 5), (1, 6), (1, 7)],
    [(6, 7), (6, 10), (5, 7), (5, 10), (4, 7), (4, 8), (4, 9), (3, 7), (3, 9),
     (2, 8), (2, 10), (2, 11), (1, 7), (1, 10)],
    [(6, 10), (6, 12), (5, 10), (5, 12), (5, 13), (4, 9), (4, 12), (3, 9),
     (3, 12), (2, 10), (2, 11), (2, 12), (1, 10), (1, 12)],
]
BLUES_BOXES.append([(6, 12), (6, 15), (5, 12), (5, 13), (5, 14), (4, 12), (4, 14),
                     (3, 12), (3, 14), (3, 15), (2, 12), (2, 15), (1, 12), (1, 15)])


def _blues_walk():
    seq = []
    for box in BLUES_BOXES:
        seq.extend(_box_asc_desc(box))
    return seq

E7_ALL_POSITIONS = [
    ('E7 — open',         [0, 2, 0, 1, 0, 0],            {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}),
    ('E7 — A barre, fr7', [None, 7, 9, 7, 9, 7],         {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}),
    ('E7 — E barre, fr12', [12, 14, 12, 13, 12, 12],     {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}),
]
E7_BARRE_7_CTX = ('E7 — A barre, fr7', [None, 7, 9, 7, 9, 7], {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'})


# Full E minor pentatonic across frets 0–15 — all notes
# E minor pentatonic = E G A B D
FULL_PENT_POSITIONS = []
# Notes for each string up to fret 15:
# String 6 (E low): E=0, G=3, A=5, B=7, D=10, E=12, G=15
# String 5 (A):     A=0, B=2, D=5, E=7, G=10, A=12, B=14
# String 4 (D):     D=0, E=2, G=5, A=7, B=9, D=12, E=14
# String 3 (G):     G=0, A=2, B=4, D=7, E=9, G=12, A=14
# String 2 (B):     B=0, D=3, E=5, G=8, A=10, B=12, D=15
# String 1 (E):     E=0, G=3, A=5, B=7, D=10, E=12, G=15

def role_of(note):
    return {'E': 'R', 'G': 'b3', 'A': '4', 'B': '5', 'D': 'b7'}[note]

NOTES_BY_STRING = {
    6: [('E', 0), ('G', 3), ('A', 5), ('B', 7), ('D', 10), ('E', 12), ('G', 15)],
    5: [('A', 0), ('B', 2), ('D', 5), ('E', 7), ('G', 10), ('A', 12), ('B', 14)],
    4: [('D', 0), ('E', 2), ('G', 5), ('A', 7), ('B', 9), ('D', 12), ('E', 14)],
    3: [('G', 0), ('A', 2), ('B', 4), ('D', 7), ('E', 9), ('G', 12), ('A', 14)],
    2: [('B', 0), ('D', 3), ('E', 5), ('G', 8), ('A', 10), ('B', 12), ('D', 15)],
    1: [('E', 0), ('G', 3), ('A', 5), ('B', 7), ('D', 10), ('E', 12), ('G', 15)],
}

for s, notes in NOTES_BY_STRING.items():
    for name, fret in notes:
        FULL_PENT_POSITIONS.append((s, fret, role_of(name)))


# E blues scale (add b5 = Bb)
BLUES_EXTRAS_BY_STRING = {
    6: [('Bb', 6)],
    5: [('Bb', 1), ('Bb', 13)],
    4: [('Bb', 8)],
    3: [('Bb', 3), ('Bb', 15)],
    2: [('Bb', 11)],
    1: [('Bb', 6)],
}
FULL_BLUES_POSITIONS = list(FULL_PENT_POSITIONS)
for s, notes in BLUES_EXTRAS_BY_STRING.items():
    for _name, fret in notes:
        FULL_BLUES_POSITIONS.append((s, fret, 'b5'))


# BB box — frets 7–10 area where all the King-family blues licks live.
# Subset of pentatonic + a couple of bend-target notes.
BB_BOX = [
    (1, 7, '5'), (1, 8, 'b6'),    # b6 isn't pentatonic but is in the BB box
    (2, 8, 'b3'), (2, 10, '4'),
    (3, 7, 'b7'), (3, 9, 'R'),
    (4, 9, 'b3'),
]


def card(num, title, role, positions, fret_range, caption, width=900, height=210,
         chords=None, walk=None):
    body = scale_box(positions, fret_range, title=title, width=width, height=height)
    if walk:
        # Walk position-by-position: each CAGED box plays its own asc + desc,
        # then move up the neck to the next box. The walk list is already a
        # complete sequence (asc+desc baked in per box) so the JS skips the
        # auto-reverse that `playScaleAscDesc` would otherwise do.
        audio_notes = [[s, f] for s, f in walk]
    else:
        nps = sorted({(OPEN_MIDI[s] + f, s, f) for (s, f, _) in positions})
        audio_notes = [[s, f] for _, s, f in nps]
    # Tab below the diagram — same notes the audio plays. For walks the list
    # is already asc+desc-per-box; otherwise asc+desc the whole thing.
    if walk:
        tab_notes = audio_notes
    else:
        desc = audio_notes[:-1][::-1]
        tab_notes = audio_notes + desc
    tab_events = [n(s, f, dur=0.5) for s, f in tab_notes]
    tab_bars = [tab_events[i:i + 8] for i in range(0, len(tab_events), 8)]
    tab_svg = render_tab(tab_bars, bars_per_line=4, width=width, show_bar_numbers=False)
    strip = chord_strip(chords) if chords else ''
    audio = {"type": "scale", "notes": audio_notes}
    if walk:
        audio["skip_desc"] = True
    return {
        "num": num, "title": title, "role": role,
        "body": strip + body + tab_svg, "caption": caption,
        "audio": audio,
    }


EXERCISE = {
    "slug": "neck_overview",
    "order": 7,  # right after the basic scale pages
    "section": "Scales",
    "title_one": "Whole",
    "title_em": "neck",
    "eyebrow": "Pentatonic — the Big Picture",
    "eyebrow_short": "Neck Overview",
    "subtitle": "All five boxes shown as one continuous map.",
    "intro_prose": """
      <p>The five boxes are pedagogical — they're how you <em>learn</em> the
      scale, four frets at a time. But the actual neck doesn't have boxes.
      It has notes. Once you can see the whole pentatonic at once, you
      stop &ldquo;changing boxes&rdquo; mid-solo and start playing the
      scale instead.</p>
      <p>This page shows the whole E minor pentatonic across frets 0–15,
      then the E blues scale (same plus the ♭5), then a zoomed view on the
      <em>BB box</em> — the most-used 4-fret region of the entire blues
      vocabulary.</p>
    """,
    "intro_pills": [
        ("Whole neck", "Same 5 notes, 17 frets of fretboard. Find E in seven octaves."),
        ("BB box", "Frets 7–10 on strings 1–3. Where every King-family lick lives."),
    ],
    "sections": [
        {
            "heading": "E minor pentatonic — the whole neck",
            "blurb": "All five boxes joined. Trace the roots (R, in lavender) — there are six of them across the neck. Find them first, then everything else snaps into place.",
            "layout": "full",
            "cards": [
                card("Map", "E minor pentatonic — frets 0–15",
                     "All five boxes connected · R G A B D",
                     FULL_PENT_POSITIONS, (0, 15),
                     "Every E in the scale is a lavender <em>R</em>. There are six of them — string 6 frets 0 and 12, string 5 fret 7, string 4 fret 2 and 14, string 3 fret 9, string 2 fret 5, string 1 frets 0 and 12. <strong>Memorise the roots first.</strong>",
                     width=1140, height=240, chords=E7_ALL_POSITIONS,
                     walk=_pent_walk()),
            ],
        },
        {
            "heading": "E blues scale — the whole neck",
            "blurb": "Same map plus the ♭5 added everywhere it falls. The ♭5 is the bend target — find one near you and start there.",
            "layout": "full",
            "cards": [
                card("Map", "E blues scale — frets 0–15",
                     "Minor pentatonic + ♭5 (B♭) · the blue note",
                     FULL_BLUES_POSITIONS, (0, 15),
                     "Every <strong>♭5</strong> dot is a bend target. The cleanest ones: string 3 fret 3 and string 5 fret 1 (low &ldquo;cowboy&rdquo; bend zone), and string 2 fret 11 (Box 4 BB-style bend).",
                     width=1140, height=240, chords=E7_ALL_POSITIONS,
                     walk=_blues_walk()),
            ],
        },
        {
            "heading": "The BB Box — where the language lives",
            "blurb": "If you can play one box from memory, make it this one. Frets 7–10 on strings 1–3 — about a square inch of neck — and 90% of recorded blues lead vocabulary lives inside.",
            "layout": "full",
            "cards": [
                card("Box", "BB box — frets 7–10",
                     "Strings 1–3 · the lead vocabulary headquarters",
                     BB_BOX, (7, 10),
                     "Six notes. <strong>String 3 fret 9</strong> = E (root). <strong>String 2 fret 10</strong> = A (4). <strong>String 1 fret 7</strong> = B (5). Bend the b3 (string 2 fret 8) toward the 3. Bend the 4 (string 2 fret 10) toward the 5 (string 2 fret 12). That's the whole BB King songbook.",
                     width=900, height=180, chords=[E7_BARRE_7_CTX]),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Seeing the ",
        "heading_em": "whole neck",
        "heading_two": "",
        "body": "<p>The transition from &ldquo;I know five boxes&rdquo; to &ldquo;I see the neck&rdquo; takes months. The shortcut: <em>find the roots first</em>. Memorise where E lives in every position. Then everything else is just &ldquo;a few frets away from E&rdquo;.</p>",
        "items": [
            ("Daily", "Find the six E's (R dots) on the whole-neck diagram without looking. Play them low to high, then high to low."),
            ("3 min", "Pick any random fret. Tell me what note it is, what scale degree, and whether it's in the pentatonic. (Cheating: just check the diagram.)"),
            ("5 min", "Solo over E7 using ONLY the BB box. Don't leave those four frets. Notice how much vocabulary fits in such a small space."),
            ("Bonus", "When you can navigate boxes 1–5, the real skill is <em>connecting</em> them with slides. Practise a slide from any Box-1 note to its Box-2 equivalent on the same string."),
        ],
    },
    "closing": "Five boxes, one neck. Five rooms become one house.",
}
