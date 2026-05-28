"""E minor pentatonic — five box positions up the neck.

This is the bedrock soloing scale for blues. We render each box as a
horizontal scale diagram with the root marked.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import scale_box, chord_strip
from tab import n, render_tab

E7_BY_POSITION = {
    1: ('E7 — open',         [0, 2, 0, 1, 0, 0],            {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}),
    2: ('E7 — D-shape, fr2', [None, None, 2, 4, 3, 4],      {4: 'R', 3: '5', 2: 'b7', 1: '3'}),
    3: ('E7 — C-shape, fr4', [None, 7, 6, 7, 5, 4],         {5: 'R', 4: '3', 3: 'b7', 2: 'R', 1: '3'}),
    4: ('E7 — A barre, fr7', [None, 7, 9, 7, 9, 7],         {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}),
    5: ('E7 — G-shape, fr9', [12, 11, 9, 9, 9, 10],         {6: 'R', 5: '3', 4: '5', 3: 'R', 2: '3', 1: 'b7'}),
}


# Each box: list of (string_num, fret, role) tuples; string 1 = high E (top).

# Box 1 — at the open position (mirror at fret 12)
BOX1 = [
    (6, 0, 'R'), (6, 3, 'b3'),
    (5, 0, '4'), (5, 2, '5'),
    (4, 0, 'b7'), (4, 2, 'R'),
    (3, 0, 'b3'), (3, 2, '4'),
    (2, 0, '5'), (2, 3, 'b7'),
    (1, 0, 'R'), (1, 3, 'b3'),
]
# Box 2 — frets 2–5
BOX2 = [
    (6, 3, 'b3'), (6, 5, '4'),
    (5, 2, '5'), (5, 5, 'b7'),
    (4, 2, 'R'), (4, 5, 'b3'),
    (3, 2, '4'), (3, 4, '5'),
    (2, 3, 'b7'), (2, 5, 'R'),
    (1, 3, 'b3'), (1, 5, '4'),
]
# Box 3 — frets 4–7
BOX3 = [
    (6, 5, '4'), (6, 7, '5'),
    (5, 5, 'b7'), (5, 7, 'R'),
    (4, 5, 'b3'), (4, 7, '4'),
    (3, 4, '5'), (3, 7, 'b7'),
    (2, 5, 'R'), (2, 8, 'b3'),
    (1, 5, '4'), (1, 7, '5'),
]
# Box 4 — frets 7–10
BOX4 = [
    (6, 7, '5'), (6, 10, 'b7'),
    (5, 7, 'R'), (5, 10, 'b3'),
    (4, 7, '4'), (4, 9, '5'),
    (3, 7, 'b7'), (3, 9, 'R'),
    (2, 8, 'b3'), (2, 10, '4'),
    (1, 7, '5'), (1, 10, 'b7'),
]
# Box 5 — frets 9–12
BOX5 = [
    (6, 10, 'b7'), (6, 12, 'R'),
    (5, 10, 'b3'), (5, 12, '4'),
    (4, 9, '5'), (4, 12, 'b7'),
    (3, 9, 'R'), (3, 12, 'b3'),
    (2, 10, '4'), (2, 12, '5'),
    (1, 10, 'b7'), (1, 12, 'R'),
]


def _ordered_for_play(positions):
    # Ascending: sort by pitch (open-midi[string] + fret), descending played by JS.
    OPEN_MIDI = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
    nps = sorted({(OPEN_MIDI[s] + f, s, f) for (s, f, _) in positions})
    return [[s, f] for _, s, f in nps]


def _build_scale_tab(notes):
    """Asc + desc as tab events, split into bars of 8 eighth notes each."""
    desc = notes[:-1][::-1]
    full = notes + desc
    events = [n(s, f, dur=0.5) for s, f in full]
    bars = [events[i:i + 8] for i in range(0, len(events), 8)]
    return render_tab(bars, bars_per_line=4, width=900, show_bar_numbers=False)


def make_card(num, title, role, positions, fret_range, caption, box_n=None):
    body = scale_box(positions, fret_range, title=title)
    notes = _ordered_for_play(positions)
    tab_svg = _build_scale_tab(notes)
    strip = ''
    if box_n and box_n in E7_BY_POSITION:
        strip = chord_strip([E7_BY_POSITION[box_n]])
    return {"num": num, "title": title, "role": role,
            "body": strip + body + tab_svg, "caption": caption,
            "audio": {"type": "scale", "notes": notes}}


EXERCISE = {
    "slug": "pentatonic",
    "order": 5,
    "section": "Scales",
    "title_one": "E Minor",
    "title_em": "pentatonic",
    "eyebrow": "The Soloing Scale",
    "eyebrow_short": "Pentatonic",
    "subtitle": "Five notes, five boxes, the whole neck.",
    "intro_prose": """
      <p>The E minor pentatonic scale is the foundation of blues, rock, and
      every adjacent style. Five notes: <strong>E · G · A · B · D</strong>
      — the 1, ♭3, 4, 5, and ♭7. No half-steps, no dissonance — every note
      sounds &ldquo;in&rdquo; against E7, A7, and B7.</p>
      <p>The five boxes below are five regions of the neck where you can
      play the scale. They overlap: the last few notes of Box 1 are the
      first few notes of Box 2. Memorise Box 1 first — it's the classic
      &ldquo;open E minor pentatonic&rdquo; that lives at the 12th fret too.
      Then work up the neck.</p>
    """,
    "intro_pills": [
        ("The five notes", "E (R) · G (♭3) · A (4) · B (5) · D (♭7)"),
        ("Why minor pentatonic over E7?", "The ♭3 against E7's major 3 is the blue note. Tension is the point."),
    ],
    "sections": [
        {
            "heading": "Five boxes, low to high",
            "blurb": "Each box gives you all five notes in a four-fret span. The root (R) is the home base — start there, end there, find your way back.",
            "layout": "full",
            "cards": [
                make_card("Box 1", "Box 1 — open position (or fret 12)",
                          "Root on 6th string · the classic box",
                          BOX1, (0, 4),
                          "The famous one. The root sits on the open low E. Same shape lives at the 12th fret, one octave up.", box_n=1),
                make_card("Box 2", "Box 2 — fret 2",
                          "Root on 4th string, fret 2",
                          BOX2, (2, 6),
                          "Slides up two frets from Box 1. The ♭3 (G) sits on the low E string fret 3 — the first &ldquo;blue&rdquo; bend zone.", box_n=2),
                make_card("Box 3", "Box 3 — fret 4",
                          "Root on 5th string, fret 7",
                          BOX3, (4, 8),
                          "Centres on the 7th-fret root (5th string). The B note on string 3 fret 4 lives here — bend that to C for the blues colour.", box_n=3),
                make_card("Box 4", "Box 4 — fret 7",
                          "Root on 5th string, fret 7 / 3rd string fret 9",
                          BOX4, (7, 11),
                          "The big middle box. Pretty much every classic rock solo lives in here, around frets 7–10.", box_n=4),
                make_card("Box 5", "Box 5 — fret 9",
                          "Root on 6th string, fret 12",
                          BOX5, (9, 13),
                          "Top of the neck. Connects back to Box 1 at fret 12 — that's the whole loop.", box_n=5),
            ],
        },
    ],
    "next_step": {
        "heading_one": "From shapes to ",
        "heading_em": "lines",
        "heading_two": "",
        "body": "<p>Knowing five boxes is not the same as playing music. The point is to <em>connect</em> them — to be able to start a phrase in Box 1 and end it in Box 3 without thinking. Then the neck stops being five separate rooms and becomes one continuous instrument.</p>",
        "items": [
            ("3 min", "Play Box 1 ascending then descending. Land on the root each time."),
            ("4 min", "Box 1 → Box 2 → Box 1. Walk the bridge note between them: the A (5th string fret 0) is shared."),
            ("5 min", "Solo over a slow E7 vamp using only Box 1. Use rests. Bend the G into G♯."),
            ("3 min", "Pick a single phrase from Box 1 and translate it to Box 3 — same shape, different frets."),
        ],
    },
    "closing": "Five notes. Whole neck. Welcome to the blues.",
}
