"""B7 chord shapes — the V⁷ in E blues — all CAGED positions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import chord_box


B7_OPEN     = [None, 2, 1, 2, 0, 2]        # classic open B7
B7_A_BARRE  = [None, 2, 4, 2, 4, 2]        # A-shape barre at fret 2
B7_G_SHAPE  = [7, 6, 4, 4, 4, 5]           # G7 shape shifted up to B
B7_E_BARRE  = [7, 9, 7, 8, 7, 7]           # E-shape barre at fret 7
B7_D_SHAPE  = [None, None, 9, 11, 10, 11]  # D-shape at fret 9
B7_C_SHAPE  = [None, 14, 13, 14, 12, 11]   # C-shape at fret 11


B7_OPEN_ROLES  = {5: 'R', 4: '3', 3: 'b7', 2: 'R', 1: '5'}
B7_A_ROLES     = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
B7_G_ROLES     = {6: 'R', 5: '3', 4: '5', 3: 'R', 2: '3', 1: 'b7'}
B7_E_ROLES     = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}
B7_D_ROLES     = {4: 'R', 3: '5', 2: 'b7', 1: '3'}
B7_C_ROLES     = {5: 'R', 4: '3', 3: 'b7', 2: 'R', 1: '3'}


def make_card(num, title, role, shape, role_labels, caption):
    body = chord_box(shape, title=title, role_labels=role_labels)
    return {"num": num, "title": title, "role": role, "body": body, "caption": caption,
            "audio": {"type": "chord", "shape": shape, "direction": "down"}}


EXERCISE = {
    "slug": "b7_shapes",
    "order": 4,
    "section": "Chord Shapes",
    "title_one": "B7",
    "title_em": "shapes",
    "eyebrow": "The V⁷ — the Dominant",
    "eyebrow_short": "V⁷ · Dominant",
    "subtitle": "Every B7 voicing up the neck.",
    "intro_prose": """
      <p>B7 is the V⁷ — it gets just two bars (9 and the turnaround at 12),
      but they're the most charged bars of the form. The V⁷ is the chord
      that <em>wants</em> to resolve — and on the turnaround, that resolution
      back to I starts the form all over again.</p>
      <p>Chord tones: <strong>B · D♯ · F♯ · A</strong>. The open voicing is
      one of the all-time great blues sounds — those three open-position B7
      fingerings under your fingers, the rest are barres.</p>
    """,
    "intro_pills": [
        ("Chord tones", "R · 3 · 5 · ♭7 — B · D♯ · F♯ · A"),
        ("Function", "The V⁷. Hits in bars 9 and 12. Pulls hard back to I⁷."),
    ],
    "sections": [
        {
            "heading": "Six positions, low to high",
            "blurb": "Same shape grid as E7 and A7, transposed to B. The open B7 is a fingering all its own — learn it as a separate one-off voicing.",
            "cards": [
                make_card("Position 1", "B7 — open",
                          "Five-string open voicing",
                          B7_OPEN, B7_OPEN_ROLES,
                          "The cowboy B7. Stretchy four-finger shape, no barre."),
                make_card("Position 2", "B7 — A-shape barre",
                          "Root on 5th string, fret 2",
                          B7_A_BARRE, B7_A_ROLES,
                          "A-shape barre at fret 2. Adjacent to open A7 — that's the whole tone V → IV move."),
                make_card("Position 3", "B7 — G-shape",
                          "Root on 5th string, fret 2 (low B on 6th, fret 7)",
                          B7_G_SHAPE, B7_G_ROLES,
                          "G7 fingering shifted up four. Big six-string voicing."),
                make_card("Position 4", "B7 — E-shape barre",
                          "Root on 6th string, fret 7",
                          B7_E_BARRE, B7_E_ROLES,
                          "E-shape barre at fret 7. Sits right next to A-shape E7 — both at fret 7."),
                make_card("Position 5", "B7 — D-shape",
                          "Root on 4th string, fret 9",
                          B7_D_SHAPE, B7_D_ROLES,
                          "Four-string voicing high up. Pair with D-shape A7 at fret 7 for a tight V → IV."),
                make_card("Position 6", "B7 — C-shape",
                          "Root on 5th string, fret 14",
                          B7_C_SHAPE, B7_C_ROLES,
                          "C-shape, high in the register. Useful for the last chord of the turnaround."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "The ",
        "heading_em": "turnaround",
        "heading_two": " V",
        "body": "<p>The V⁷ in bar 12 (the last bar of the form) is what makes the blues a loop. It doesn't resolve — it sets up another chorus. Land hard on beat 1 of that bar, hold the chord, then drop into the next E7 like the form never ended.</p>",
        "items": [
            ("3 min", "Practise B7 → E7 in matching positions: A-barre B7 (fret 2) → A-barre E7 (fret 7). Five-fret jump, same shape."),
            ("4 min", "Slide between B7 and A7 using the A-shape barre — frets 2 ↔ 0. Bars 9–10 of the form, one finger moving."),
            ("3 min", "Open B7 → open E7 → start over. Hear how V calls I home, then I refuses to settle. That's the blues secret."),
        ],
    },
    "closing": "The dominant. The pull. The reason the form doesn't end.",
}
