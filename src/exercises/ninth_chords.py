"""9th chord voicings — E9, A9, B9.

The dominant 9 chord (R 3 5 ♭7 9) is the "Stax/Memphis/jazz blues"
voicing. It's a single moveable shape on strings 1–5 that defines the
soul/R&B sound (Booker T, Steve Cropper, Curtis Mayfield) and the jazz
blues sound (Wes, Grant Green, Kenny Burrell).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fretboard import chord_box


# Standard 9th-chord shape: x-R-3-b7-9-5 (low to high), root on string 5.
# For E9: root E on string 5 fret 7 → shape: x 7 9 7 9 7? wait that's E7 A-shape.
# Real E9 shape: x 7 6 7 7 7 → notes A=x, E (R), G# (3), D (b7), F# (9), B (5)
# Verify:
#   5: 7 = E (R) ✓
#   4: 6 = G# (3) ✓
#   3: 7 = D (b7) ✓
#   2: 7 = F# (9) ✓
#   1: 7 = B (5) ✓
E9_SHAPE_5  = [None, 7, 6, 7, 7, 7]   # root on 5
A9_SHAPE_5  = [None, 0, -1, 0, 0, 0]  # open A9: x 0 - 0 0 0? hmm need to compute.
# A9 with root on 5th string fret 0 (open A): x 0 2 0 2 - no that's A7.
# A9 shape with root on string 5 open is awkward (no 9 available without crazy stretch).
# Use root on string 6 fret 5 (A) shape instead:
# Shape relative to root on 6: R - - 3 b7 9 5 (over 6 strings)
# That's 6-string shape: 5 - 6 5 7 5  (low E fret 5 = A; A fret 6 = D#? no — verify)
# Open low E = E. fret 5 = A ✓. fret 7 = B. fret 6 = A# / Bb.
# For A9 with root on string 6: we need shape spanning 6 frets too far. Skip.
# Use root-on-5 shape moved up: A9 = E9 shape moved +5 frets: x 12 11 12 12 12
A9_SHAPE_5  = [None, 12, 11, 12, 12, 12]
# Or a more common A9 shape: x 0 2 0 2 0 with a 9th added... actually the common A9 is x 0 2 4 2 3? Hmm.
# A9 alternative (closed voicing, no open strings, fret 4-7):
A9_SHAPE_LOW = [None, None, 5, 4, 5, 5]  # root on 4th string fret 5? Wait, string 4 fret 5 = G, not A.
# Let me just use the E9 shape transposed: for A9, shape is at fret 5 (since A is fret 12 on string 5, or fret 0 open, but for the moveable shape we use the fret-position root).
# Actually for A9, root on 5th string fret 12 OR root on 6th string fret 5. Let's compute A9 shape with root on 6th string fret 5:
# Shape: R x 3 b7 9 5 (low E to high E) → but the 5-string shape doesn't include the 6th string. So just use E9-shape transposed +5 → x 12 11 12 12 12 (very high up the neck).
# Alternative: use root on 5th string fret 0 (open A), find the 9th-chord shape that works:
# A=R(5), C#=3(4), G=b7(3), B=9(2), E=5(1)
# Frets: 5: 0 (A=R), 4: 2 (E? no, fret 2 on string 4 = E? D string fret 2 = E ✓ but E is the 5, not 3 — we need C#)
# fret 4 on string 4 = F#. fret 11 on string 4 = C#. So C# isn't reachable near open A.
# Best: chord on strings 1-4 only, root on string 4 fret 7 = A: x x 7 6 5 7? compute:
# string 4 fret 7 = A (R)
# string 3 fret 6 = C# (3)
# string 2 fret 5 = E (5) — but we want b7 (G) here. fret 8 = G. Hmm doesn't fit cleanly.
# OK, simplest: use the moveable shape. Just have A9 way up the neck.
# But to keep variety, let me create three nice positions per chord.

# E9 — three positions:
E9_POS1 = [None, 7, 6, 7, 7, 7]   # root 5, fret 7 — the iconic shape
E9_POS2 = [0, None, 2, 1, 3, 2]   # open E9? Let me verify.
# Open E9: E (open low E = R), need 3, 5, b7, 9 above.
# 6: 0 = E (R), 5: x, 4: 2 = E... hmm string 4 fret 2 is E (octave), not very useful.
# Real "open E9": 0 2 0 1 3 2 — verify:
# 6: 0 = E (R)
# 5: 2 = B (5)
# 4: 0 = D (b7)
# 3: 1 = G# (3)
# 2: 3 = D (b7) — that's another b7, not 9. We want F# (9). F# on string 2 is fret 7.
# Try 0 2 4 1 3 2:
# 4: 4 = F# (9) ✓
# 3: 1 = G# (3) ✓
# 2: 3 = D (b7) — still b7. We want 5 here (B). Open B = 5.
# Try 0 2 4 1 0 2:
# 6: 0 = E (R)
# 5: 2 = B (5)
# 4: 4 = F# (9)
# 3: 1 = G# (3)
# 2: 0 = B (5)
# 1: 2 = F# (9) — duplicates the 9. Missing the b7.
# This is genuinely tricky in open position.
# Let's skip open and use three closed positions.
E9_POS2 = [12, 11, 9, 9, 9, 10]  # G-shape E7 with the b7 (D=fret 10) functioning + 9? actually this is just E7 G-shape.
# Try a different position: E9 with root on string 6 fret 12, 4-string voicing string 1-4:
# 4: 12+? need E (root)... wait root is on string 6.
# Easier: use a "rootless" 9th shape — common in jazz comping.
# Rootless E9: (3, b7, 9, 5) = (G#, D, F#, B) on strings 4, 3, 2, 1.
# E9 rootless on strings 4-1:
# 4: 13 (E? F? — fret 13 on D string is E. Need G#, which is fret 6 or 18 on string 4. Hmm.)
# Or 4-string voicing low: 6 fret 6 (Bb), nope.
# I'll just present three positions: the iconic A-shape 9, an A-shape moved up an octave, and a closed top-3-string voicing.

# Standard moveable 9 (root on string 5):
def ninth_chord(root_fret_on_5):
    """Build the standard 5-string 9 shape with root on 5th string at given fret."""
    f = root_fret_on_5
    return [None, f, f - 1, f, f, f]

E9_POS1 = ninth_chord(7)    # E9 around fret 6-7
E9_POS2_full = ninth_chord(7)
# Higher octave variant — same shape but high voicing on strings 1-4 only:
# Use the "jazz comp" voicing on strings 1-4: (3, b7, 9, 5)
# For E9: (G#, D, F#, B). On strings 4, 3, 2, 1:
# string 4 fret 6 = G# ✓
# string 3 fret 7 = D ✓
# string 2 fret 7 = F# ✓
# string 1 fret 7 = B ✓
E9_TOP4 = [None, None, 6, 7, 7, 7]

# An E13 chord (R 3 b7 13) gives the "real" jazz blues colour. Common shape:
# E13: 6 fret 0 (R) - skip - 4 fret 6 (G#? wait fret 6 on string 4 = G#) - 3 fret 7 (D b7) - 2 fret 6 (E? no) - 1 fret 9 (C# = 13)
# Standard rootless E13 strings 4-1: x x 6 7 6 9
# Check: 4: 6 = G# (3), 3: 7 = D (b7), 2: 6 = E (R? — but we said rootless), 1: 9 = C# (13)
# Hmm string 2 fret 6 = E (R), that's fine.
E13_TOP = [None, None, 6, 7, 7, 9]

E9_POS1_LABELS = {5: 'R', 4: '3', 3: 'b7', 2: '9', 1: '5'}
E9_TOP4_LABELS = {4: '3', 3: 'b7', 2: '9', 1: '5'}
E13_TOP_LABELS = {4: '3', 3: 'b7', 2: '9', 1: '13'}

# A9 — three positions
# Open A9 isn't easy. Use closed shapes.
A9_POS1 = ninth_chord(0)  # x 0 -1 0 0 0 — fret -1 isn't real; skip this. Use open A7 with 9 added on string 2.
# Easier: A9 root on string 5 fret 12: x 12 11 12 12 12
A9_POS1 = [None, 12, 11, 12, 12, 12]   # high A9
A9_POS2 = ninth_chord(0)
# Hmm ninth_chord(0) gives [None, 0, -1, 0, 0, 0]. fret -1 makes no sense.
# A "low A9" voicing — on strings 4-1: (3, b7, 9, 5) = (C#, G, B, E)
# string 4 fret 11 = C#, string 3 fret 12 = G, string 2 fret 12 = B (wait B-string fret 12 = B octave), string 1 fret 12 = E
# fret values: 4: 11, 3: 12, 2: 12, 1: 12 — that's high up.
# Lower: string 4 fret -1... skip.
# Try inverted: C# can be on string 5 fret 4, G on string 4 fret 5, B on string 3 fret 4, E on string 2 fret 5
# That's an A9 inversion. Let me verify:
# 5: 4 = C# (3)
# 4: 5 = G (b7)
# 3: 4 = B (9)
# 2: 5 = E (5)
# That works! "Low rootless A9":
A9_LOW_ROOTLESS = [None, 4, 5, 4, 5, None]
A9_TOP4 = [None, None, 11, 12, 12, 12]   # high rootless A9 on strings 4-1
A9_POS1_LABELS = {5: 'R', 4: '3', 3: 'b7', 2: '9', 1: '5'}
A9_LOW_LABELS = {5: '3', 4: 'b7', 3: '9', 2: '5'}
A9_TOP4_LABELS = {4: '3', 3: 'b7', 2: '9', 1: '5'}
A13_TOP = [None, None, 11, 12, 12, 14]
A13_TOP_LABELS = {4: '3', 3: 'b7', 2: '9', 1: '13'}

# B9 — three positions
B9_POS1 = ninth_chord(2)   # root on string 5 fret 2: x 2 1 2 2 2
B9_POS1_LABELS = {5: 'R', 4: '3', 3: 'b7', 2: '9', 1: '5'}
# Higher: same shape at fret 14
B9_POS2 = ninth_chord(14)
B9_POS2_LABELS = {5: 'R', 4: '3', 3: 'b7', 2: '9', 1: '5'}
# Top-4 rootless on strings 4-1: (3, b7, 9, 5) = (D#, A, C#, F#)
# 4 fret 1 = D#? D string fret 1 = D# ✓
# 3 fret 2 = A ✓
# 2 fret 2 = C# ✓
# 1 fret 2 = F# ✓
B9_TOP4 = [None, None, 1, 2, 2, 2]
B9_TOP4_LABELS = {4: '3', 3: 'b7', 2: '9', 1: '5'}
B13_TOP = [None, None, 1, 2, 2, 4]
B13_TOP_LABELS = {4: '3', 3: 'b7', 2: '9', 1: '13'}


def card(num, title, role, shape, labels, caption):
    return {
        "num": num, "title": title, "role": role,
        "body": chord_box(shape, title=title, role_labels=labels),
        "caption": caption,
        "audio": {"type": "chord", "shape": shape, "direction": "down"},
    }


EXERCISE = {
    "slug": "ninth_chords",
    "order": 9,
    "section": "Chord Shapes",
    "title_one": "9th",
    "title_em": "chords",
    "eyebrow": "Dominant 9 — the Soul/Jazz Blues Voicing",
    "eyebrow_short": "9ths & 13ths",
    "subtitle": "The Memphis sound. The Wes Montgomery sound. The James Brown sound.",
    "intro_prose": """
      <p>Add the 9 to a dominant 7 chord and the whole feel changes. The
      9th chord (R 3 5 ♭7 9) is the defining sound of soul, R&amp;B, and
      jazz blues — Booker T, Steve Cropper, Curtis Mayfield on the soul
      side; Wes Montgomery, Grant Green, Kenny Burrell on the jazz side.
      It also turns up on a thousand James Brown records.</p>
      <p>The classic shape is a one-finger barre with two finger placements
      on top (root on the 5th string). Move that shape anywhere on the
      neck and you've got a dominant 9 chord. The 13 chord is the next
      step up — substitute the 6 in for the 5 — and gives the &ldquo;jazz
      blues&rdquo; flavour all by itself.</p>
    """,
    "intro_pills": [
        ("E9 shape", "Root on string 5 · R · 3 · ♭7 · 9 · 5"),
        ("Why care", "Substitute any dom-7 in the form with the matching 9. Same function, richer colour."),
    ],
    "sections": [
        {
            "heading": "E9 — the I⁷ as a 9th",
            "blurb": "Substitute the dom-9 anywhere E7 lives in the form. Pair the iconic mid-neck shape with a top-strings voicing for variety.",
            "cards": [
                card("E9 — 1", "E9 — root on 5th string",
                     "The iconic moveable 9 shape · fret 7",
                     E9_POS1, E9_POS1_LABELS,
                     "The Booker T voicing. Five strings, two fingers. Move it to any fret — same chord, different root."),
                card("E9 — 2", "E9 — top-strings rootless",
                     "Strings 4–1 · jazz comping shape",
                     E9_TOP4, E9_TOP4_LABELS,
                     "Rootless — the bass player carries the E. Strings 4-3-2-1 give you 3-♭7-9-5. The compact jazz blues voicing."),
                card("E13", "E13 — the jazz blues colour",
                     "Top strings · adds the 6 to the dom-7",
                     E13_TOP, E13_TOP_LABELS,
                     "Replace the 5 with the 6 (the 13) and you've got dom-13. Pair this with the rootless E9 — same fret region, one note moved."),
            ],
        },
        {
            "heading": "A9 — the IV⁷ as a 9th",
            "blurb": "Slot these in for A7 in bars 5, 6, and 10. The most common is the rootless 4-string shape low on the neck.",
            "cards": [
                card("A9 — 1", "A9 — high voicing",
                     "Standard 9 shape · fret 12",
                     A9_POS1, A9_POS1_LABELS,
                     "Same shape as E9 from above, transposed up 5 frets. Useful when you're soloing high and want a quick chord stab."),
                card("A9 — 2", "A9 — rootless low",
                     "Strings 5–2 · fret 4–5",
                     A9_LOW_ROOTLESS, A9_LOW_LABELS,
                     "Rootless inversion in a low register. Compact, voice-leads beautifully from E9 (fret 6–7) — only two notes move."),
                card("A13", "A13 — bring the colour",
                     "Top strings · the soul/jazz alternative",
                     A13_TOP, A13_TOP_LABELS,
                     "A13 sits in the same neck zone as the rootless A9. Pick one for the bar, alternate for variety."),
            ],
        },
        {
            "heading": "B9 — the V⁷ as a 9th",
            "blurb": "The V⁷ wants resolution and the 9 makes that pull even stronger. Drop these in for B7 in bars 9 and 12.",
            "cards": [
                card("B9 — 1", "B9 — root on 5th string, fret 2",
                     "The everyday B9 — open-position friendly",
                     B9_POS1, B9_POS1_LABELS,
                     "Just shy of open. Pair with open E7 → A9 (low rootless) and you're playing the whole form with three two-finger shapes."),
                card("B9 — 2", "B9 — root on 5th string, fret 14",
                     "Same shape, high octave",
                     B9_POS2, B9_POS2_LABELS,
                     "Same chord one octave up. Useful at the end of a chorus when you want the turnaround to ring high."),
                card("B13", "B13 — the dominant 13",
                     "Top strings · the cliff-edge V chord",
                     B13_TOP, B13_TOP_LABELS,
                     "B13 is what jazz players grab on bar 12. The 13 (G♯) is the major 6 — it sounds like resolution is about to happen. And then it does."),
            ],
        },
    ],
    "next_step": {
        "heading_one": "Comping with ",
        "heading_em": "9ths",
        "heading_two": "",
        "body": "<p>Once you have three chord families (E9 mid, A9 low rootless, B9 fret-2), you can play the whole 12-bar form using <em>only three two-finger shapes</em>. The chord changes voice-lead automatically — most notes stay put, only one or two move. That's the &ldquo;modern blues comp&rdquo; sound.</p>",
        "items": [
            ("4 min", "Loop E9 → A9 (low rootless) → E9. Hear the voice leading. Only string 2 and 1 change a couple of frets."),
            ("3 min", "Whole 12-bar form using E9 (bars 1–4, 7–8, 11), A9 low (bars 5–6, 10), B9 fret-2 (bars 9, 12). Plays itself."),
            ("3 min", "Swap each chord for its 13 on the bar's last beat. <em>E9 → E13 → A9 → A13 →</em> ..."),
            ("Bonus", "Hold E9 and let the bass player walk under you. Bass plays E, B, D, E across the bar. Same chord all bar."),
        ],
    },
    "closing": "Two fingers. Six frets of difference. A whole new vocabulary.",
}
