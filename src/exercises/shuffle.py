"""Shuffle rhythm — the engine of the blues.

Three patterns: the boogie shuffle (R/5/6/♭7 walking), Texas shuffle
(double-stops with palm mute), and the slow 12/8 triplet shuffle.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tab import n, c, r, render_tab
from fretboard import chord_strip


# Chord-context shapes for these patterns
E7_OPEN     = [0, 2, 0, 1, 0, 0]
E7_BARRE_7  = [None, 7, 9, 7, 9, 7]
A7_OPEN     = [None, 0, 2, 0, 2, 0]
B7_OPEN     = [None, 2, 1, 2, 0, 2]
E7_OPEN_ROLES   = {6: 'R', 5: '5', 4: 'b7', 3: '3', 2: '5', 1: 'R'}
E7_BARRE_ROLES  = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
A7_OPEN_ROLES   = {5: 'R', 4: '5', 3: 'b7', 2: '3', 1: '5'}
B7_OPEN_ROLES   = {5: 'R', 4: '3', 3: 'b7', 2: '5', 1: 'b7'}


def audio_from_bars(bars, bpm=120, gain=0.4, strum=False):
    """Turn rendered tab events into a playable sequence.

    strum=True → multi-note chord events play with a tiny strum offset.
    strum=False → multi-note chord events sound simultaneously (a pick or stab).
    """
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
    return {"type": "sequence", "notes": seq, "bpm": bpm, "gain": gain}


# ─────────────────────────────────────────────────────────────────────────────
# Boogie shuffle — the classic 8-to-the-bar R/5/6/♭7 walking pattern
# ─────────────────────────────────────────────────────────────────────────────
# Over E7: low E pedal on string 6 fret 0, with string 5 walking 2 (B = 5) → 4 (C♯ = 6) → 2 (B = 5) → 4 (C♯ = 6).
# Played in eighth notes, shuffle feel. Each bar is one bar of E7.

def boogie_bar(root_string, root_fret, sixth_fret, palm_mute=True):
    """Boogie 8th-note pattern: R, 5, R, 6 — repeated. PM throughout."""
    # Use double-stops: root pedal on lower string, walking note on next-higher string.
    # For E: low E open (string 6) + string 5 fret 2 (5) → fret 4 (6).
    # We'll play one pluck per chord stack.
    fifth_fret = root_fret + 2 if root_string >= 5 else root_fret  # not used; passed explicit
    return [
        c([(root_string, root_fret), (root_string - 1, root_fret + 2)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, sixth_fret)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, root_fret + 2)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, sixth_fret)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, root_fret + 2)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, sixth_fret)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, root_fret + 2)], dur=0.5, pm=palm_mute),
        c([(root_string, root_fret), (root_string - 1, sixth_fret)], dur=0.5, pm=palm_mute),
    ]


# E boogie: low E (6:0) + string 5 walking 2 → 4
E_BOOGIE = boogie_bar(6, 0, 4)
# A boogie: low A (5:0) + string 4 walking 2 → 4 (E → F♯) — that's the 5 → 6 of A
A_BOOGIE = boogie_bar(5, 0, 4)
# B boogie: low B (5:2) + string 4 walking 4 → 6 — root B, 5 = F♯ (string 4 fret 4), 6 = G♯ (fret 6)
B_BOOGIE = boogie_bar(5, 2, 6)


BOOGIE_FULL = [E_BOOGIE, E_BOOGIE, E_BOOGIE, E_BOOGIE,
               A_BOOGIE, A_BOOGIE, E_BOOGIE, E_BOOGIE,
               B_BOOGIE, A_BOOGIE, E_BOOGIE, B_BOOGIE]
BOOGIE_LABELS = ['E7', None, None, None,
                 'A7', None, 'E7', None,
                 'B7', 'A7', 'E7', 'B7']


# ─────────────────────────────────────────────────────────────────────────────
# Texas shuffle — double-stop chord stabs with palm mute
# ─────────────────────────────────────────────────────────────────────────────
# Stevie Ray Vaughan / Albert Collins style. Chord on beats 1 & 3, double-stop
# on the &. Heavy palm mute, swing feel.

# Two bars of E7 in this style:
TEXAS = [
    # bar 1 of E7
    [
        c([(5, 7), (4, 9), (3, 7)], dur=1.0, pm=True, accent=True),
        c([(5, 7), (4, 9), (3, 7)], dur=0.5, pm=True),
        c([(2, 9), (1, 7)], dur=0.5, pm=True),
        c([(5, 7), (4, 9), (3, 7)], dur=1.0, pm=True, accent=True),
        c([(5, 7), (4, 9), (3, 7)], dur=0.5, pm=True),
        c([(2, 9), (1, 7)], dur=0.5, pm=True),
    ],
    # bar 2 of E7
    [
        c([(5, 7), (4, 9), (3, 7)], dur=1.0, pm=True, accent=True),
        c([(5, 7), (4, 9), (3, 7)], dur=0.5, pm=True),
        c([(2, 9), (1, 7)], dur=0.5, pm=True),
        c([(5, 7), (4, 9), (3, 7)], dur=1.0, pm=True, accent=True),
        c([(5, 7), (4, 9), (3, 7)], dur=0.5, pm=True),
        c([(2, 9), (1, 7)], dur=0.5, pm=True),
    ],
]
TEXAS_LABELS = ['E7', None]


# ─────────────────────────────────────────────────────────────────────────────
# 12/8 slow blues — triplet shuffle in compound time
# ─────────────────────────────────────────────────────────────────────────────
# Each "beat" = a triplet (three eighth notes in compound 12/8). Four beats per bar.
# Pattern: chord on 1, triplet, repeat. We'll render in 4/4 with triplets via dur=1/3 ≈ 0.333.

# E7 slow blues — chord stab + triplet filler.
SLOW_BLUES_E = [
    c([(5, 7), (4, 9), (3, 7), (2, 9), (1, 7)], dur=1.0, accent=True),  # beat 1: E7
    n(3, 7, dur=1/3),  n(3, 8, dur=1/3),  n(3, 7, dur=1/3),              # triplet (D - Eb - D walk)
    c([(5, 7), (4, 9), (3, 7), (2, 9), (1, 7)], dur=1.0, accent=True),
    n(2, 8, dur=1/3),  n(2, 10, dur=1/3),  n(2, 8, dur=1/3),             # triplet on B string
]


def section_card(num, title, role, bars, labels, caption, bpm=110, bars_per_line=4, width=900,
                 chords=None, strum=False):
    tab_svg = render_tab(bars, chord_labels=labels, bars_per_line=bars_per_line, width=width)
    strip = chord_strip(chords) if chords else ''
    return {
        "num": num, "title": title, "role": role,
        "body": strip + tab_svg, "caption": caption,
        "audio": audio_from_bars(bars, bpm=bpm, strum=strum),
    }


EXERCISE = {
    "slug": "shuffle",
    "order": 10,
    "section": "Rhythm",
    "title_one": "Shuffle",
    "title_em": "rhythm",
    "eyebrow": "The Engine of the Blues",
    "eyebrow_short": "Shuffle",
    "subtitle": "Three rhythmic feels: boogie, Texas shuffle, slow 12/8.",
    "intro_prose": """
      <p>The blues isn't just three chords. It's three chords played with
      a specific <em>feel</em> — a triplet-based swing called the
      shuffle. The shuffle is what makes blues sound like blues; without
      it, the same notes are just rock or pop.</p>
      <p>The eighth notes are unequal: a &ldquo;long-short, long-short&rdquo;
      pattern that fills triplet time. You'll hear this in any
      Chicago blues record (Muddy Waters, Howlin' Wolf), Texas blues
      (Stevie Ray, Albert Collins), or T-Bone Walker–style swing blues.
      The metronome above is your friend here — set it to <em>120</em>
      and let the eighth notes shuffle around the click.</p>
    """,
    "intro_pills": [
        ("Feel", "Long-short, long-short. Triplet subdivision."),
        ("Palm mute", "PM the bass-string parts. Lets the chords breathe."),
    ],
    "sections": [
        {
            "heading": "Boogie shuffle — the bass-line pattern",
            "blurb": "Eight notes per bar, walking pedal pattern. The Chuck Berry / Stones / Status Quo / John Lee Hooker sound. Palm-muted, every note even.",
            "layout": "full",
            "cards": [
                section_card(
                    "Pattern", "12-bar boogie shuffle — full chorus",
                    "Two-string pattern walking R-5-R-6 through the whole form",
                    BOOGIE_FULL, BOOGIE_LABELS,
                    "The whole 12-bar form in boogie style. On E7, low E + B (string 5 fret 2, the 5) walking to C♯ (fret 4, the 6). On A7, the same pattern shifted to strings 5 and 4. <em>Palm-mute every note</em> — that's the engine sound.",
                    bpm=120, bars_per_line=4, width=900,
                    chords=[('E7 — open', E7_OPEN, E7_OPEN_ROLES),
                            ('A7 — open', A7_OPEN, A7_OPEN_ROLES),
                            ('B7 — open', B7_OPEN, B7_OPEN_ROLES)]),
            ],
        },
        {
            "heading": "Texas shuffle — chord stabs and double-stops",
            "blurb": "SRV / Albert Collins style. Big chord on the down-beats, tight double-stop comes on the off-beat. Palm-mute throughout.",
            "layout": "full",
            "cards": [
                section_card(
                    "Pattern", "Texas shuffle — two bars of E7",
                    "Chord on 1 & 3 · double-stop on the off-beat",
                    TEXAS, TEXAS_LABELS,
                    "Three-string E7 stab (A-shape barre, fret 7), then a high double-stop on strings 1 &amp; 2 in the gap. PM the chord; let the double-stop ring. <strong>Accent</strong> beats 1 &amp; 3.",
                    bpm=110, bars_per_line=2, width=720, strum=True,
                    chords=[('E7 — A barre, fret 7', E7_BARRE_7, E7_BARRE_ROLES)]),
            ],
        },
        {
            "heading": "Slow 12/8 blues — triplet feel",
            "blurb": "The triplets are the rhythm. Big chord, then a 3-note fill, then chord, then fill. The slow-burn ballad blues feel — \"Stormy Monday\", \"The Thrill Is Gone\".",
            "layout": "full",
            "cards": [
                section_card(
                    "Pattern", "Slow 12/8 — one bar of E7",
                    "Chord + triplet filler · 4 beats per bar in compound time",
                    [SLOW_BLUES_E], ['E7'],
                    "Each &ldquo;beat&rdquo; is actually a <em>triplet</em> in 12/8. Chord on beat 1, then three quick notes filling that beat. Slow it down to <em>70 bpm</em> and let it breathe — this is heartbreak music.",
                    bpm=70, bars_per_line=1, width=720, strum=True,
                    chords=[('E7 — A barre, fret 7', E7_BARRE_7, E7_BARRE_ROLES)]),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Picking the ",
        "heading_em": "feel",
        "heading_two": "",
        "body": "<p>The three shuffles aren't ranked — they're tools. Boogie for upbeat rocking blues. Texas for hard, biting blues. 12/8 for slow ballads. Most blues players have all three under their fingers and switch as the tune asks. Practice them <em>against a backing track</em> — the metronome alone won't teach you to swing.</p>",
        "items": [
            ("Daily", "Pick one shuffle, play the whole form. Loop it twice. Mistakes are fine; <em>feel</em> is the goal."),
            ("Slowdown", "Practise the boogie at <em>60 bpm</em>. Slow enough that every note is intentional. Then double-time to 120."),
            ("Mix it up", "Play 12 bars of boogie, then 12 bars of Texas, then 12 bars of slow 12/8 — without stopping. That's a complete blues set."),
        ],
    },
    "closing": "Three chords plus a feel. The feel is everything.",
}
