"""30-minute daily blues practice routine.

A structured walk through the app's content — what to play, in what
order, for what duration.
"""

EXERCISE = {
    "slug": "routine",
    "order": 99,
    "section": "Practice",
    "title_one": "Daily",
    "title_em": "routine",
    "eyebrow": "30 Minutes · One Lap of the Blues",
    "eyebrow_short": "Routine",
    "subtitle": "A complete daily practice — form, chords, scales, vocabulary, rhythm.",
    "intro_prose": """
      <p>Knowing what to practise is harder than practising. This is a
      30-minute lap through the app — designed so that one cycle hits
      every essential element: the form, the chord shapes, the scale
      positions, a piece of vocabulary, and a rhythm pattern.</p>
      <p>Pick a tempo (start at <em>70 bpm</em>) and stay there for the
      whole session. Use the metronome. When something feels comfortable,
      bump the tempo up 5 bpm next session. Repeat for life.</p>
    """,
    "intro_pills": [
        ("Tempo discipline", "Pick one tempo. Hold it. Don't speed up when you get bored."),
        ("Daily over long", "30 minutes every day &gt;&gt; 3 hours on Sunday. Always."),
    ],
    "sections": [
        {
            "heading": "The 30-minute lap",
            "blurb": "Each block is timed. Do them in order — the warm-up earns you the chord changes; the chord changes earn you the soloing.",
            "layout": "wide",
            "cards": [
                {
                    "num": "0:00 → 3:00", "title": "Warm-up — E minor pentatonic Box 1",
                    "role": "3 min · ascending and descending, metronome at quarter notes",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p>Open the <a href="./pentatonic.html" style="color:var(--accent-dark);font-weight:600;">Pentatonic</a> page, hit play on Box 1. Match it. Play it three times, slow and clean. Land hard on every root.</p>'
                            '<p style="margin:0;"><strong>Goal:</strong> every note clean, no buzz, perfect time. Don\'t skip this for the &ldquo;fun stuff&rdquo;.</p>'
                            '</div>',
                    "caption": "Tone &amp; time first. If you don't earn this, you don't get to the licks.",
                },
                {
                    "num": "3:00 → 8:00", "title": "Chord shapes — E7, A7, B7",
                    "role": "5 min · cycle the three chords in one position",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p>Pick one position family — say, the A-shape barre. Play E7 (fret 7), A7 (open), B7 (fret 2). Land each chord on beat 1.</p>'
                            '<p>Then the same three chords in a <em>different</em> position. Then the third position.</p>'
                            '<p style="margin:0;"><strong>Bonus:</strong> swap any of these for the matching 9th chord. Hear the colour shift.</p>'
                            '</div>',
                    "caption": "Three positions × three chords. After a week, all 18 shapes are second nature.",
                },
                {
                    "num": "8:00 → 13:00", "title": "Play the form",
                    "role": "5 min · full 12-bar, quick-change",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p>Loop the <a href="./form.html" style="color:var(--accent-dark);font-weight:600;">Form</a> page in quick-change. Play one chorus with just whole notes — chord on beat 1, hold for four beats. Hit every chord change.</p>'
                            '<p>Then a chorus of the Charleston comping rhythm.</p>'
                            '<p>Then a chorus with no clicking — just hold each chord and hear the changes in your head before they happen.</p>'
                            '</div>',
                    "caption": "Three choruses. Each one teaches a different thing.",
                },
                {
                    "num": "13:00 → 20:00", "title": "Soloing — one box at a time",
                    "role": "7 min · improvise over a chorus, each chorus in a different box",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p>Loop the form. First chorus: <em>Box 1</em> only — don\'t leave it. Use rests. Bend the b3.</p>'
                            '<p>Second chorus: <em>Box 4</em> only (the BB box). Slow bends. Vibrato.</p>'
                            '<p>Third chorus: free. Move between boxes. Slide between them.</p>'
                            '<p style="margin:0;"><strong>Rule:</strong> no fast playing. Every note is a choice.</p>'
                            '</div>',
                    "caption": "Soloing is editing. Play half as many notes as you think you should.",
                },
                {
                    "num": "20:00 → 25:00", "title": "Steal a lick",
                    "role": "5 min · one lick, learned slowly, then dropped into a chorus",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p>Open the <a href="./licks.html" style="color:var(--accent-dark);font-weight:600;">Licks</a> page. Pick ONE. Just one. Loop the audio. Memorise it cold — at half-speed if needed.</p>'
                            '<p>Then play it once at the start of a chorus over the form. Then once in the middle. Then end on it.</p>'
                            '<p style="margin:0;">After a week of one lick a day, you have seven phrases in your toolkit.</p>'
                            '</div>',
                    "caption": "Steal directly. Originality comes from accumulation.",
                },
                {
                    "num": "25:00 → 28:00", "title": "Rhythm — pick one shuffle",
                    "role": "3 min · groove discipline",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p><a href="./shuffle.html" style="color:var(--accent-dark);font-weight:600;">Shuffle</a> page. Pick one feel today (boogie / Texas / 12&frasl;8). Two full choruses, no soloing.</p>'
                            '<p>Tomorrow, a different feel. Rotate the three across the week.</p>'
                            '<p style="margin:0;"><strong>This is rhythm guitar practice.</strong> It\'s its own skill. Don\'t skimp.</p>'
                            '</div>',
                    "caption": "Half of every blues set is rhythm guitar. Treat it that way.",
                },
                {
                    "num": "28:00 → 30:00", "title": "Cool-down — play a turnaround",
                    "role": "2 min · end on something good",
                    "body": '<div style="font-size:0.95rem;line-height:1.6;color:var(--card-ink-soft);">'
                            '<p>Play <em>Turn 1</em> from the Licks page, four times. Then play <em>Turn 2</em>, four times.</p>'
                            '<p style="margin:0;">End the session with a phrase that resolves. You\'ll walk away from the guitar feeling like the practice meant something.</p>'
                            '</div>',
                    "caption": "Always end on a phrase you can play well. Memory is built at the end of the session.",
                },
            ],
        },
    ],
    "next_step": {
        "heading_one": "Weekly ",
        "heading_em": "rotation",
        "heading_two": "",
        "body": "<p>The lap above is one day. The week looks like:</p><ul style=\"color:var(--ink-soft);margin:0.5rem 0;padding-left:1.2rem;\"><li><strong>Mon/Wed/Fri</strong> — full lap as above</li><li><strong>Tue/Thu</strong> — half lap, double the soloing time</li><li><strong>Sat</strong> — open practice: free play, learn a tune by ear, jam</li><li><strong>Sun</strong> — listen, not play. Find one record you've never heard.</li></ul>",
        "items": [
            ("Track tempo", "Write down your starting bpm each week. After a month, look back."),
            ("Pick repertoire", "Once you can play the form, pick two real tunes — <em>Pride and Joy</em>, <em>Sweet Home Chicago</em>, <em>The Thrill Is Gone</em>. Learn them properly."),
            ("Record yourself", "Phone audio is enough. Listen back. Your playing will surprise you (in both directions)."),
        ],
    },
    "closing": "Twelve bars, three chords, every day, for life.",
}
