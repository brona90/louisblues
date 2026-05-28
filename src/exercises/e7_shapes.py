"""E7 chord shapes — all five CAGED positions up the neck.

Each card shows one voicing. Together they cover the whole neck.
Order: open E-shape → D-shape → C-shape → A-shape barre → G-shape → E-shape barre.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import chord_box


# shape: low-E (6th) → high-E (1st). None or -1 = muted, 0 = open.

E7_OPEN     = [0, 2, 0, 1, 0, 0]          # open E7 — frets 0–2
E7_D_SHAPE  = [None, None, 2, 4, 3, 4]    # D-shape at fret 2
E7_C_SHAPE  = [None, 7, 6, 7, 5, 4]       # C-shape spanning frets 4–7
E7_A_BARRE  = [None, 7, 9, 7, 9, 7]       # A-shape barre at fret 7
E7_G_SHAPE  = [12, 11, 9, 9, 9, 10]       # G-shape spanning 9–12
E7_E_BARRE  = [12, 14, 12, 13, 12, 12]    # E-shape barre at fret 12

E7_OPEN_ROLES   = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}
E7_D_ROLES      = {4: 'R', 3: '5', 2: 'b7', 1: '3'}
E7_C_ROLES      = {5: 'R', 4: '3', 3: 'b7', 2: 'R', 1: '3'}
E7_A_ROLES      = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
E7_G_ROLES      = {6: 'R', 5: '3', 4: '5', 3: 'R', 2: '3', 1: 'b7'}
E7_E_BAR_ROLES  = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}


def make_card(num, title, role, shape, role_labels, caption):
    body = chord_box(shape, title=title, role_labels=role_labels)
    return {
        "num": num,
        "title": title,
        "role": role,
        "body": body,
        "caption": caption,
        "audio": {"type": "chord", "shape": shape, "direction": "down"},
    }


EXERCISE = {
    "slug": "e7_shapes",
    "order": 2,
    "section": "Chord Shapes",
    "title_one": "E7",
    "title_em": "shapes",
    "eyebrow": "The I⁷ — the Tonic Chord",
    "eyebrow_short": "I⁷ · Tonic",
    "subtitle": "Every E7 voicing up the neck, with chord-tone roles labelled.",
    "intro_prose": """
      <p>E7 is the home chord of the E blues — it's the I⁷. Five CAGED
      shapes, six places to play it: <em>open E</em>, then D-shape at fret 2,
      C-shape spanning 4–7, A-shape barre at 7, G-shape at 9–12, and the
      E-shape barre at 12. Same four notes (<strong>E · G♯ · B · D</strong>),
      every position.</p>
      <p>The labels under each dot show the chord tone:
      <strong>R</strong> root, <strong>3</strong> major 3rd,
      <strong>5</strong> 5th, <strong>♭7</strong> minor 7th.
      Memorise where the root sits in each shape — that's how you transpose
      every shape into A7 and B7 below.</p>
    """,
    "intro_pills": [
        ("Chord tones", "R · 3 · 5 · ♭7 — E · G♯ · B · D"),
        ("Function", "The I⁷. Lives 8 of 12 bars. Never resolves — that's blues."),
    ],
    "sections": [
        {
            "heading": "Six positions, low to high",
            "blurb": "Move through them in order. The root marker (R) tells you which string carries E.",
            "cards": [
                make_card("Position 1", "E7 — open",
                          "E-shape · root on 6th string",
                          E7_OPEN, E7_OPEN_ROLES,
                          "Open E7. Everyone's first blues chord. Root on 6 open."),
                make_card("Position 2", "E7 — D-shape",
                          "Root on 4th string, fret 2",
                          E7_D_SHAPE, E7_D_ROLES,
                          "Four strings, no barre. Bright, top-string voicing — great for fills."),
                make_card("Position 3", "E7 — C-shape",
                          "Root on 5th string, fret 7",
                          E7_C_SHAPE, E7_C_ROLES,
                          "C-shape spans four frets. Index barres fret 4 across strings 1 & 2."),
                make_card("Position 4", "E7 — A-shape barre",
                          "Root on 5th string, fret 7",
                          E7_A_BARRE, E7_A_ROLES,
                          "Classic A7 shape barred at fret 7. The workhorse voicing for blues comping."),
                make_card("Position 5", "E7 — G-shape",
                          "Root on 6th string, fret 12",
                          E7_G_SHAPE, E7_G_ROLES,
                          "Six-string voicing, mostly fret 9. Octave-up sound, great for solo intros."),
                make_card("Position 6", "E7 — E-shape barre",
                          "Root on 6th string, fret 12",
                          E7_E_BARRE, E7_E_BAR_ROLES,
                          "Same fingering as open E7, barred at the 12th fret. One octave up."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "From shapes to ",
        "heading_em": "vocabulary",
        "heading_two": "",
        "body": "<p>The point isn't memorising six shapes. It's <em>seeing the neck as a single chord</em> — the same four notes (E G♯ B D) repeating in seven octaves, with the shape changing because the string spacing isn't uniform. Once that clicks, every shape becomes obvious.</p>",
        "items": [
            ("3 min", "Play each shape, name the chord tone of every string out loud as you fret it (\"root… five… flat-seven… third…\")."),
            ("5 min", "Hold one shape and finger-pick the chord tones up and down. Hear which note is which."),
            ("2 min", "Move the A-shape barre between frets 7 (E7) and 5 (D7). Same fingering, different chord. That's the entire point of the CAGED system."),
        ],
    },
    "closing": "Five shapes. One chord. The whole fretboard, finally legible.",
}
