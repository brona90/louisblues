"""E blues scale — minor pentatonic plus the ♭5 blue note.

Same five box geometry as the minor pentatonic, with the ♭5 (B♭)
highlighted in each position.
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


# B♭ (the ♭5 of E) on each string: 6: fret 6, 5: fret 1 (and 13), 4: fret 8, 3: fret 3, 2: fret 11, 1: fret 6.
# Add the blue note in each box where it falls.

BOX1 = [
    (6, 0, 'R'), (6, 3, 'b3'),
    (5, 0, '4'), (5, 1, 'b5'), (5, 2, '5'),
    (4, 0, 'b7'), (4, 2, 'R'),
    (3, 0, 'b3'), (3, 2, '4'), (3, 3, 'b5'),
    (2, 0, '5'), (2, 3, 'b7'),
    (1, 0, 'R'), (1, 3, 'b3'),
]
BOX2 = [
    (6, 3, 'b3'), (6, 5, '4'), (6, 6, 'b5'),
    (5, 2, '5'), (5, 5, 'b7'),
    (4, 2, 'R'), (4, 5, 'b3'),
    (3, 2, '4'), (3, 3, 'b5'), (3, 4, '5'),
    (2, 3, 'b7'), (2, 5, 'R'),
    (1, 3, 'b3'), (1, 5, '4'),
]
BOX3 = [
    (6, 5, '4'), (6, 6, 'b5'), (6, 7, '5'),
    (5, 5, 'b7'), (5, 7, 'R'),
    (4, 5, 'b3'), (4, 7, '4'), (4, 8, 'b5'),
    (3, 4, '5'), (3, 7, 'b7'),
    (2, 5, 'R'), (2, 8, 'b3'),
    (1, 5, '4'), (1, 6, 'b5'), (1, 7, '5'),
]
BOX4 = [
    (6, 7, '5'), (6, 10, 'b7'),
    (5, 7, 'R'), (5, 10, 'b3'),
    (4, 7, '4'), (4, 8, 'b5'), (4, 9, '5'),
    (3, 7, 'b7'), (3, 9, 'R'),
    (2, 8, 'b3'), (2, 10, '4'), (2, 11, 'b5'),
    (1, 7, '5'), (1, 10, 'b7'),
]
BOX5 = [
    (6, 10, 'b7'), (6, 12, 'R'),
    (5, 10, 'b3'), (5, 12, '4'), (5, 13, 'b5'),
    (4, 9, '5'), (4, 12, 'b7'),
    (3, 9, 'R'), (3, 12, 'b3'),
    (2, 10, '4'), (2, 11, 'b5'), (2, 12, '5'),
    (1, 10, 'b7'), (1, 12, 'R'),
]


def _ordered_for_play(positions):
    OPEN_MIDI = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
    nps = sorted({(OPEN_MIDI[s] + f, s, f) for (s, f, _) in positions})
    return [[s, f] for _, s, f in nps]


def _build_scale_tab(notes):
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
    "slug": "blues_scale",
    "order": 6,
    "section": "Scales",
    "title_one": "E Blues",
    "title_em": "scale",
    "eyebrow": "Minor Pentatonic + the Blue Note",
    "eyebrow_short": "Blues Scale",
    "subtitle": "Six notes: 1 ♭3 4 ♭5 5 ♭7. The ♭5 is the whole thing.",
    "intro_prose": """
      <p>The blues scale is the minor pentatonic with one extra note: the
      <strong>♭5</strong>. In E that's <strong>B♭</strong> — a tritone above
      the root. It's the &ldquo;blue note,&rdquo; the bend, the cry. It's
      dissonant against every chord in the form, and that's exactly why it
      works.</p>
      <p>The ♭5 should almost never be a target note. It's a passing tone:
      you bend up to it, then bend or slide further to the 5. Or you stop
      on it briefly to add tension, then resolve down to the 4 or up to the
      5. The boxes below are the same five pentatonic shapes with the ♭5
      added in every place it falls.</p>
    """,
    "intro_pills": [
        ("Six notes", "E · G · A · B♭ · B · D"),
        ("The ♭5", "B♭ — the blue note. Use it as passing or bend, not a landing."),
    ],
    "sections": [
        {
            "heading": "Five boxes with the blue note added",
            "blurb": "Same positions as the minor pentatonic. The extra dot is always the ♭5 — find it, bend it, leave it.",
            "layout": "full",
            "cards": [
                make_card("Box 1", "Blues scale — Box 1 (open / 12th fret)",
                          "♭5 on string 5 fret 1, string 3 fret 3",
                          BOX1, (0, 4),
                          "Two ♭5's land inside this box. String 5 fret 1 is the easy one — the cowboy blues bend.", box_n=1),
                make_card("Box 2", "Blues scale — Box 2 (fret 2)",
                          "♭5 on string 6 fret 6, string 3 fret 3",
                          BOX2, (2, 6),
                          "Walk between Box 1 and Box 2 along the b string — fret 3 is the b5, fret 5 is the root.", box_n=2),
                make_card("Box 3", "Blues scale — Box 3 (fret 4)",
                          "♭5 on strings 6, 4, and 1",
                          BOX3, (4, 8),
                          "The middle of the neck. The classic blues bend lives here: bend G♯ on string 3 fret 6 up to A — or use the B♭ on string 4 fret 8 as a passing tone.", box_n=3),
                make_card("Box 4", "Blues scale — Box 4 (fret 7)",
                          "♭5 on string 4 fret 8, string 2 fret 11",
                          BOX4, (7, 11),
                          "Box 4 holds the king bend: bend the G (string 3 fret 8) up half-step — that's the b5/5 oscillation that defines the sound.", box_n=4),
                make_card("Box 5", "Blues scale — Box 5 (fret 9)",
                          "♭5 on string 5 fret 13, string 2 fret 11",
                          BOX5, (9, 13),
                          "Top of the neck. The b5 on string 2 fret 11 is begging for a half-step bend up to the 5 (B).", box_n=5),
            ],
        },
    ],
    "next_step": {
        "heading_one": "How to use ",
        "heading_em": "the ♭5",
        "heading_two": "",
        "body": "<p>The ♭5 doesn't want to be played. It wants to be <em>arrived at</em> — by bend, by slide, by chromatic passing. Hitting it dead-on as a quarter-note is the easiest way to sound like you don't understand the blues. Used right, it's the most identifiable sound in the whole scale.</p>",
        "items": [
            ("3 min", "Box 1 ascending — pass through the ♭5 (string 5 fret 1) on the way to the 5. Don't land on it."),
            ("4 min", "In Box 4, bend the G on string 3 fret 8 up a half-step to G♯. Release. Bend again. That's the sound."),
            ("3 min", "Solo over E7 using only the ♭5 as a passing note. Play 30 seconds — count how many times you stop on it (target: zero)."),
        ],
    },
    "closing": "Six notes. One of them is on fire.",
}
