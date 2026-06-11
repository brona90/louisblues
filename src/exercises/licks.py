"""Classic E blues licks — the actual vocabulary.

Each card is a short tab phrase with bends, slides, hammer-ons, pull-offs.
These are the moves you steal from every blues record.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tab import n, c, r, br, render_tab
from fretboard import chord_strip


# Common chord shapes for context cards
E7_OPEN     = [0, 2, 0, 1, 0, 0]
E7_BARRE_7  = [None, 7, 9, 7, 9, 7]
E7_BARRE_12 = [12, 14, 12, 13, 12, 12]
B7_OPEN     = [None, 2, 1, 2, 0, 2]

E7_OPEN_ROLES   = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}
E7_BARRE_ROLES  = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
B7_OPEN_ROLES   = {5: 'R', 4: '3', 3: 'b7', 2: 'R', 1: '5'}


# ─────────────────────────────────────────────────────────────────────────────
# Audio sequence helper — turn a list of tab events into the audio JSON.
# Skips ornaments (just plays the principal note); good enough for hearing.
# ─────────────────────────────────────────────────────────────────────────────

def audio_from_bars(bars, bpm=85, strum=False):
    seq = []
    for bar in bars:
        for ev in bar:
            kind = ev[0]
            if kind == 'note':
                _, s, f, opts = ev
                seq.append({"string": s, "fret": f, "dur": opts.get('dur', 0.5)})
            elif kind == 'chord':
                _, notes, opts = ev
                if notes:
                    key = 'strum' if strum else 'chord'
                    seq.append({key: notes, "dur": opts.get('dur', 0.5)})
            elif kind == 'rest':
                _, opts = ev
                seq.append({"rest": True, "dur": opts.get('dur', 0.5)})
    return {"type": "sequence", "notes": seq, "bpm": bpm, "gain": 0.42}


# ─────────────────────────────────────────────────────────────────────────────
# Lick 1: The all-time classic — Box 1 pull-off lick over E7
# ─────────────────────────────────────────────────────────────────────────────
# This is the "first lick every blues guitarist learns".
# Phrase: high E fret 3 (G) → pull off to open E, hit string 2 open B, then
# string 3 fret 2 (A) → string 3 open G (b3), then E root on string 4 fret 2.
LICK1 = [[
    n(1, 3, dur=0.5, pull_to=0), n(1, 0, dur=0.5),
    n(2, 0, dur=0.5),
    n(3, 2, dur=0.5, pull_to=0), n(3, 0, dur=0.5),
    n(4, 2, dur=1.0, vibrato=True),
    r(1.0),
]]

# ─────────────────────────────────────────────────────────────────────────────
# Lick 2: The BB King bend — half-step bend on string 3 fret 8, in the BB box.
# ─────────────────────────────────────────────────────────────────────────────
LICK2 = [[
    n(1, 8, dur=0.5),  # G (b3)
    n(2, 8, dur=0.5),  # G (b3)? wait, B-string fret 8 is G. We want fret 10 = A.
    # restart properly:
]]
# rewrite
LICK2 = [[
    n(2, 10, dur=0.5),                 # D — bend up half-step to D#? No, in BB box: B-string fret 10 = A, bend to A#? Just use the b3→3 bend.
    n(3, 9, dur=0.5, bend_to=11, vibrato=True),  # G string fret 9 = E, bend full to F#. Actually the iconic move is b3->3 on string 3 fret 8 in box 4. Let me redo.
]]
# BB-style lick: string 2 fret 8 (G = b3), bend half-step to G# (3). String 2 fret 10 (A) frames it.
LICK2 = [[
    n(2, 10, dur=0.5),                                    # A
    n(3, 9, dur=0.5),                                     # E
    n(2, 8, dur=1.0, bend_to=9, vibrato=True),            # G (b3) → bend half-step to G# (3)
    r(0.5),
    n(2, 10, dur=0.5),                                    # A
    n(1, 7, dur=1.0, vibrato=True),                       # B
    r(1.0),
]]

# ─────────────────────────────────────────────────────────────────────────────
# Lick 3: Chuck Berry style double-stop on strings 2 & 3
# ─────────────────────────────────────────────────────────────────────────────
# Slides into a double stop, then walks chromatic.
LICK3 = [[
    c([(2, 5), (3, 4)], dur=0.5, slide_into_dir='up'),   # E + B = a fourth apart; slide into the box-3 double-stop
    c([(2, 5), (3, 4)], dur=0.5),
    c([(2, 7), (3, 7)], dur=0.5, slide_into_dir='up'),   # higher pair
    c([(2, 7), (3, 7)], dur=0.5),
    n(4, 9, dur=0.5),                                    # B (root-fifth area)
    n(4, 7, dur=0.5),                                    # A
    n(5, 7, dur=1.0, vibrato=True),                      # E
    r(0.5),
]]

# ─────────────────────────────────────────────────────────────────────────────
# Lick 4: Turnaround #1 — chromatic descending on strings 4 & 1
# ─────────────────────────────────────────────────────────────────────────────
# Bars 11–12 of an E blues. Two voices walk down chromatically against the open
# high E pedal, landing on B7 on beat 1 of bar 12.
TURN1 = [[
    c([(1, 0), (4, 5)], dur=1.0),
    c([(1, 0), (4, 4)], dur=1.0),
    c([(1, 0), (4, 3)], dur=1.0),
    c([(1, 0), (4, 2)], dur=1.0),
], [
    c([(5, 2), (4, 1), (3, 2), (2, 0)], dur=4.0),   # B7 on beat 1, hold the bar
]]

# ─────────────────────────────────────────────────────────────────────────────
# Lick 5: Turnaround #2 — Robert Johnson style
# ─────────────────────────────────────────────────────────────────────────────
# Triplet feel: descending half-steps on strings 3 & 1, classic 2-bar turn.
TURN2 = [[
    n(1, 0, dur=0.25), n(3, 3, dur=0.25), r(0.5),
    n(1, 0, dur=0.25), n(3, 2, dur=0.25), r(0.5),
    n(1, 0, dur=0.25), n(3, 1, dur=0.25), r(0.5),
    n(1, 0, dur=0.25), n(3, 0, dur=0.25), r(0.5),
], [
    c([(5, 2), (4, 1), (3, 2), (2, 0)], dur=2.0),  # B7
    n(6, 0, dur=2.0),                              # low E pickup back to top
]]

# ─────────────────────────────────────────────────────────────────────────────
# Lick 6: The bending intro — Albert King–style
# ─────────────────────────────────────────────────────────────────────────────
# Big full bend on string 3, vibrato, descending phrase to root.
LICK6 = [[
    n(3, 9, dur=0.5, bend_to=11, vibrato=True),   # E, bend up full to F#
    n(3, 9, dur=0.5),                              # release
    n(2, 8, dur=0.5),                              # G (b3)
    n(2, 10, dur=0.5, hammer_to=12),               # A → hammer to B
    n(2, 12, dur=0.5, pull_to=10),                 # B → pull to A
    n(2, 10, dur=0.5),                             # A
    n(3, 9, dur=1.0, vibrato=True),                # E with vibrato
    r(0.5),
]]


# ─────────────────────────────────────────────────────────────────────────────
# Lick 7: An ending lick — the classic "I, IV, I" turnaround replacement
# ─────────────────────────────────────────────────────────────────────────────
# E7#9 "Hendrix chord": x 7 6 7 8 x → E (R) G# (3) D (b7) G (#9).
E7SHARP9 = [(5, 7), (4, 6), (3, 7), (2, 8)]
LICK7 = [[
    c(E7SHARP9, dur=1.0),                          # E7#9 (the Hendrix chord)
    c(E7SHARP9, dur=1.0),
    c(E7SHARP9, dur=2.0),
], [
    n(6, 0, dur=0.5), n(6, 1, dur=0.5),
    n(6, 2, dur=0.5), n(6, 3, dur=0.5),
    n(6, 4, dur=0.5), n(5, 2, dur=0.5),
    c([(5, 2), (4, 1), (3, 2)], dur=1.0),          # B7 stab
]]


def make_card(num, title, role, bars, caption, chord_labels=None, bpm=85, bars_per_line=4,
              chords=None, strum=True):
    """chords: list of (label, shape, role_labels) tuples to show above the tab."""
    tab_svg = render_tab(bars, chord_labels=chord_labels, bars_per_line=bars_per_line,
                          width=600 if len(bars) <= 1 else 880)
    strip = chord_strip(chords) if chords else ''
    return {
        "num": num, "title": title, "role": role,
        "body": strip + tab_svg, "caption": caption,
        "audio": audio_from_bars(bars, bpm=bpm, strum=strum),
    }


EXERCISE = {
    "slug": "licks",
    "order": 8,
    "section": "Vocabulary",
    "title_one": "Classic",
    "title_em": "licks",
    "eyebrow": "The Vocabulary",
    "eyebrow_short": "Licks",
    "subtitle": "Six moves you'll hear on every blues record. Steal them.",
    "intro_prose": """
      <p>Knowing the scales is necessary but not sufficient. Blues is a
      <em>language</em>: it has phrases, idioms, accents. These six licks
      are the foundational vocabulary — pull-off licks, BB-style bends,
      Chuck Berry double-stops, two classic turnarounds, an Albert King
      bend, and an ending phrase. Every player in the canon plays
      versions of these.</p>
      <p>Notation: <strong>H</strong> = hammer-on, <strong>P</strong> =
      pull-off, the up-arrow on a fret number means a <em>bend</em> (½ =
      half-step, full = whole-step), squiggle on top means
      <em>vibrato</em>. Tap any card to hear it. Then learn it slow and
      add it to your toolkit.</p>
    """,
    "intro_pills": [
        ("Practice", "Slow first. Memorise the fingering before the rhythm."),
        ("Steal", "Lift these directly. Then change one note. Then change two. That's how style happens."),
    ],
    "sections": [
        {
            "heading": "Single-bar phrases",
            "blurb": "Each fits in one or two bars over E7. Hear them, learn them, drop them into your solos.",
            "layout": "full",
            "cards": [
                make_card("Lick 1", "Pull-off lick — Box 1",
                          "The first lick every blues player learns",
                          LICK1,
                          "Hammer the high E fret 3 (G — the ♭3), pull off to open E. Then string 2 open (B), pull-off on string 3, land on E with vibrato. Pure Box-1 pentatonic.",
                          chord_labels=['E7'], bars_per_line=1, bpm=80,
                          chords=[('E7 — open', E7_OPEN, E7_OPEN_ROLES)]),
                make_card("Lick 2", "BB King–style half-step bend (Box 4)",
                          "Bend the ♭3 toward the 3 — and back",
                          LICK2,
                          "The signature BB King move. String 2 fret 8 (G — the ♭3) bent half-step to G♯ (the major 3) — then sit on the A above it with vibrato. <em>Don't release</em> the bend immediately. Let it cry.",
                          chord_labels=['E7'], bars_per_line=1, bpm=80,
                          chords=[('E7 — A barre, fret 7', E7_BARRE_7, E7_BARRE_ROLES)]),
                make_card("Lick 3", "Chuck Berry double-stops",
                          "Slide into pairs of notes on strings 2 & 3",
                          LICK3,
                          "Double-stops give you instant Chuck Berry. Slide into each pair (the slash before the chord). Walk down to E on string 5 with vibrato.",
                          chord_labels=['E7'], bars_per_line=1, bpm=90,
                          chords=[('E7 — A barre, fret 7', E7_BARRE_7, E7_BARRE_ROLES)]),
                make_card("Lick 6", "Albert King–style — full bend + hammer/pull",
                          "Big bend, then a hammer/pull figure",
                          LICK6,
                          "Full bend on string 3 fret 9 (E → F♯). Release. Then a hammer-on/pull-off pair on string 2 at frets 10–12. Land on E with vibrato. This is the move that built blues-rock guitar.",
                          chord_labels=['E7'], bars_per_line=1, bpm=80,
                          chords=[('E7 — A barre, fret 7', E7_BARRE_7, E7_BARRE_ROLES)]),
            ],
        },
        {
            "heading": "Two-bar turnarounds",
            "blurb": "Bars 11 and 12 of the form. The turnaround is where the personality lives — these two will get you started.",
            "layout": "full",
            "cards": [
                make_card("Turn 1", "Chromatic descending turnaround",
                          "Inner voice walks down, open E pedal on top",
                          TURN1,
                          "Hold the open high E. On string 4, walk down fret 5 → 4 → 3 → 2. Land on B7 on bar 12, beat 1. Classic. Used by everybody from T-Bone Walker to Eric Clapton.",
                          chord_labels=['E7', 'B7'], bars_per_line=2, bpm=80,
                          chords=[('E7 — open', E7_OPEN, E7_OPEN_ROLES),
                                  ('B7 — open', B7_OPEN, B7_OPEN_ROLES)]),
                make_card("Turn 2", "Robert Johnson triplet turnaround",
                          "Open E pedal + descending half-steps on string 3",
                          TURN2,
                          "Triplet feel. The open high E rings while string 3 walks down chromatically. End on B7 then a low E pickup into the next chorus. The Robert Johnson signature.",
                          chord_labels=['E7', 'B7 → E7'], bars_per_line=2, bpm=80,
                          chords=[('E7 — open', E7_OPEN, E7_OPEN_ROLES),
                                  ('B7 — open', B7_OPEN, B7_OPEN_ROLES)]),
                make_card("Ending", "Hendrix-style ending (E7♯9 + chromatic walk-up)",
                          "The blues ending you've heard a hundred times",
                          LICK7,
                          "The E7♯9 (the &ldquo;Hendrix chord&rdquo;: E · G♯ · D · G) stabbed three times. Then a chromatic walk-up on the low E string into a B7 stab. This is the &ldquo;and we're out&rdquo; sound.",
                          chord_labels=['E7♯9', 'walk → B7'], bars_per_line=2, bpm=90,
                          chords=[('E7♯9 — Hendrix', [None, 7, 6, 7, 8, None], {5: 'R', 4: '3', 3: 'b7', 2: '#9'}),
                                  ('B7 — open', B7_OPEN, B7_OPEN_ROLES)]),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Make them ",
        "heading_em": "yours",
        "heading_two": "",
        "body": "<p>Vocabulary is what you have to <em>learn</em>; style is what happens when you start <em>changing</em> the vocabulary. After you can play these clean, change one note in each lick. Move it to a different box. Play it backwards. Phrase it differently. The endless variation is the actual instrument.</p>",
        "items": [
            ("Daily", "Pick one lick. Loop it for 5 minutes against an E7 backing track. Then move it to A7 (= same lick, +5 frets)."),
            ("Steal", "Listen to BB King, Albert King, Freddie King, T-Bone Walker, Robert Johnson. Find one phrase you love. Steal it directly."),
            ("Vary", "After two days of any lick, change one thing — the rhythm, a single note, the bend amount. After a week it'll feel like yours."),
        ],
    },
    "closing": "The licks are the language. Memorise them, then start lying.",
}
