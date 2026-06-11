"""A7 chord shapes — the IV⁷ in E blues — all CAGED positions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import chord_box


A7_OPEN     = [None, 0, 2, 0, 2, 0]        # open A7
A7_G_SHAPE  = [5, 4, 2, 2, 2, 3]           # G7 shape at fret 2 (low A on string 5 fret 0)
A7_E_BARRE  = [5, 7, 5, 6, 5, 5]           # E-shape barre at fret 5
A7_D_SHAPE  = [None, None, 7, 9, 8, 9]     # D-shape at fret 7
A7_C_SHAPE  = [None, 12, 11, 12, 10, 9]    # C-shape barre at fret 9
A7_A_BARRE  = [None, 12, 14, 12, 14, 12]   # A-shape barre at fret 12 (one octave up)


A7_OPEN_ROLES  = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
A7_G_ROLES     = {6: 'R', 5: '3', 4: '5', 3: 'R', 2: '3', 1: 'b7'}
A7_E_ROLES     = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}
A7_D_ROLES     = {4: 'R', 3: '5', 2: 'b7', 1: '3'}
A7_C_ROLES     = {5: 'R', 4: '3', 3: 'b7', 2: 'R', 1: '3'}
A7_A_BARRE_ROLES = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}


def make_card(num, title, role, shape, role_labels, caption):
    body = chord_box(shape, title=title, role_labels=role_labels)
    return {"num": num, "title": title, "role": role, "body": body, "caption": caption,
            "audio": {"type": "chord", "shape": shape, "direction": "down"}}


EXERCISE = {
    "slug": "a7_shapes",
    "order": 3,
    "section": "Chord Shapes",
    "title_one": "A7",
    "title_em": "shapes",
    "eyebrow": "The IV⁷ — the Subdominant",
    "eyebrow_short": "IV⁷ · Subdominant",
    "subtitle": "Every A7 voicing up the neck.",
    "intro_prose": """
      <p>A7 is the IV⁷ in E blues — the chord that gives the form its
      pull. <em>Quick change</em> blues hits A7 in bar 2; standard blues
      stays on E7. Either way, A7 owns bars 5–6 and bar 10.</p>
      <p>Chord tones: <strong>A · C♯ · E · G</strong>. Six positions, same
      four notes, every position on the neck.</p>
    """,
    "intro_pills": [
        ("Chord tones", "R · 3 · 5 · ♭7 — A · C♯ · E · G"),
        ("Function", "The IV⁷. Pulls back to I — that's the whole engine of the form."),
    ],
    "sections": [
        {
            "heading": "Six positions, low to high",
            "blurb": "Same CAGED order as E7 but starting on A. Try alternating between E7 and A7 in matching positions — the geometry is identical.",
            "cards": [
                make_card("Position 1", "A7 — open",
                          "A-shape · root on 5th string",
                          A7_OPEN, A7_OPEN_ROLES,
                          "Open A7. Pair it with open E7 for two-chord blues."),
                make_card("Position 2", "A7 — G-shape",
                          "Root on 5th string, fret 0 / 6th string fret 5",
                          A7_G_SHAPE, A7_G_ROLES,
                          "G7 fingering shifted up two. Big six-string voicing for funky comping."),
                make_card("Position 3", "A7 — E-shape barre",
                          "Root on 6th string, fret 5",
                          A7_E_BARRE, A7_E_ROLES,
                          "The everyone-knows-it barre. Pair with E7 open or E7 barred at 12."),
                make_card("Position 4", "A7 — D-shape",
                          "Root on 4th string, fret 7",
                          A7_D_SHAPE, A7_D_ROLES,
                          "Four-string voicing high on the neck. Skip the wound strings, get a piano-like sound."),
                make_card("Position 5", "A7 — C-shape",
                          "Root on 5th string, fret 12",
                          A7_C_SHAPE, A7_C_ROLES,
                          "C-shape way up the neck. Useful when you're soloing high and want a quick chord stab."),
                make_card("Position 6", "A7 — A-shape barre",
                          "Root on 5th string, fret 12",
                          A7_A_BARRE, A7_A_BARRE_ROLES,
                          "Open A7 fingering, barred at the 12th fret. One octave above the open shape."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Two chords, ",
        "heading_em": "twelve bars",
        "heading_two": "",
        "body": "<p>If you only learn E7 and A7, you can play eight of the twelve bars. Pick one position for each, then start swapping the position pairs — open E7 with open A7, E-barre A7 at fret 5 with E7 open. The shape changes; the sound is identical.</p>",
        "items": [
            ("4 min", "Open E7 → open A7 → open E7. Bars 1–3 of the slow blues. Land on beat 1."),
            ("4 min", "E-shape barre A7 at fret 5 ↔ A-shape barre E7 at fret 7. Same neck region, two-fret slide."),
            ("3 min", "Pick any E7 position and find its <em>nearest</em> A7. That's voice-leading — the closest move that gets the chord across."),
        ],
    },
    "closing": "The chord that pulls home. Without the IV, there's no blues.",
}
