"""E mixolydian — the scale that matches the I⁷ chord.

Two positions: open/12th-fret and the 7th-fret box.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import scale_box, chord_strip
from tab import n, render_tab

E7_OPEN_CTX = ('E7 — open',         [0, 2, 0, 1, 0, 0],            {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'})
E7_BARRE_CTX = ('E7 — A barre, fr7', [None, 7, 9, 7, 9, 7],         {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'})


# E mixolydian: E F# G# A B C# D — the 1 2 3 4 5 6 ♭7 of E.
# Open-position box (low E to fret 4-ish):
MIX_OPEN = [
    (6, 0, 'R'), (6, 2, '2'), (6, 4, '3'),
    (5, 0, '4'), (5, 2, '5'), (5, 4, '6'),
    (4, 0, 'b7'), (4, 2, 'R'), (4, 4, '2'),
    (3, 1, '3'), (3, 2, '4'), (3, 4, '5'),
    (2, 0, '5'), (2, 2, '6'), (2, 3, 'b7'),
    (1, 0, 'R'), (1, 2, '2'), (1, 4, '3'),
]

# 7th fret box (E mix starting on the 5th-string root):
MIX_5TH = [
    (6, 7, '5'), (6, 9, '6'), (6, 10, 'b7'),
    (5, 7, 'R'), (5, 9, '2'), (5, 11, '3'),
    (4, 7, '4'), (4, 9, '5'), (4, 11, '6'),
    (3, 7, 'b7'), (3, 9, 'R'), (3, 11, '2'),
    (2, 9, '3'), (2, 10, '4'), (2, 12, '5'),
    (1, 7, '5'), (1, 9, '6'), (1, 10, 'b7'),
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


def make_card(num, title, role, positions, fret_range, caption, chord_ctx=None):
    body = scale_box(positions, fret_range, title=title)
    notes = _ordered_for_play(positions)
    tab_svg = _build_scale_tab(notes)
    strip = chord_strip([chord_ctx]) if chord_ctx else ''
    return {"num": num, "title": title, "role": role,
            "body": strip + body + tab_svg, "caption": caption,
            "audio": {"type": "scale", "notes": notes}}


EXERCISE = {
    "slug": "mixolydian",
    "order": 7,
    "section": "Scales",
    "title_one": "E",
    "title_em": "mixolydian",
    "eyebrow": "The Chord-Tone Scale",
    "eyebrow_short": "Mixolydian",
    "subtitle": "Major scale with a ♭7 — the scale that matches E7 note-for-note.",
    "intro_prose": """
      <p>Mixolydian is the dominant 7 scale: <strong>E F♯ G♯ A B C♯ D</strong>
      — exactly the notes you'd derive from an E7 arpeggio plus the 2, 4, and 6.
      It has the major 3rd (G♯) that the pentatonic and blues scales <em>lack</em>,
      and it has the ♭7 (D) that distinguishes a dominant 7 from a major 7.</p>
      <p>Use it for sweet, melodic blues solos — the kind that emphasise
      chord tones rather than the bluesy ♭3/♭5 cry. Mix it with the blues
      scale: the major 3rd (G♯) and the ♭3 (G) right next to each other is
      one of the most-used moves in the language. Bend G into G♯ over an
      E7 — that's mixolydian thinking applied with blues-scale fingers.</p>
    """,
    "intro_pills": [
        ("Seven notes", "E F♯ G♯ A B C♯ D — 1 2 3 4 5 6 ♭7"),
        ("Over E7", "Every note matches. Lean on G♯ (3) and D (♭7) — those are E7's defining tones."),
    ],
    "sections": [
        {
            "heading": "Two positions",
            "blurb": "Open position and the 7th-fret box. From these two you can reach any note on the neck — work them, then derive your own boxes.",
            "layout": "full",
            "cards": [
                make_card("Position 1", "E mixolydian — open position",
                          "Root on 6th string open / 4th string fret 2",
                          MIX_OPEN, (0, 4),
                          "Fits next to open E7. The major 3rd (G♯) lives on string 3 fret 1 and string 1 fret 4 — those are the &ldquo;chord tone&rdquo; landing spots.",
                          chord_ctx=E7_OPEN_CTX),
                make_card("Position 2", "E mixolydian — 7th fret",
                          "Root on 5th string fret 7 (matches A-shape barre E7)",
                          MIX_5TH, (7, 12),
                          "Sits in the same neck region as A-shape E7 at fret 7. Useful when you're already comping there and want to flow into a solo without shifting hands.",
                          chord_ctx=E7_BARRE_CTX),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Mixing ",
        "heading_em": "mixolydian",
        "heading_two": " with the blues scale",
        "body": "<p>Pros don't pick one scale and stick to it. They switch — sometimes within a single phrase. Over E7, the ♭3 (G) is bluesy and the 3 (G♯) is sweet. Both are right. Pentatonic gives you cry; mixolydian gives you chord-tone clarity. Combine them and you have the whole vocabulary.</p>",
        "items": [
            ("3 min", "Play E mixolydian open position, ascending and descending. Name the chord tones (R, 3, 5, ♭7) aloud."),
            ("4 min", "Switch between G (♭3, string 1 fret 3) and G♯ (3, string 1 fret 4). Quarter-note pairs. Hear the major / minor flicker."),
            ("3 min", "Solo over E7 using mixolydian, but bend the G into G♯ every time you pass through. That's the move."),
            ("2 min", "Over A7, use A mixolydian (same pattern, root shifted). The fingering at fret 5 on the 6th string starts it."),
        ],
    },
    "closing": "Major scale with a flat 7. The dominant 7 chord, melodicised.",
}
