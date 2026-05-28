"""SVG fretboard / chord-box rendering.

Two flavours:
- chord_box(shape): vertical-orientation chord diagram (6 strings × ~5 frets)
- scale_box(notes, fret_range): horizontal scale-position diagram (5–6 frets wide)

Each returns an inline SVG string sized to drop into a card.
"""

# Note name lookup. Index = semitones from C.
SEMITONE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# Open string pitches in semitones from C (E2 = 4, A2 = 9, D3 = 2, G3 = 7, B3 = 11, E4 = 4)
# We just need pitch class, not octave.
OPEN_STRING_PC = {6: 4, 5: 9, 4: 2, 3: 7, 2: 11, 1: 4}


def note_at(string, fret):
    """Return the note name (pitch class only) at string `string` (1=high E, 6=low E), fret `fret`."""
    return SEMITONE_NAMES[(OPEN_STRING_PC[string] + fret) % 12]


def chord_box(shape, title=None, base_fret=None, role_labels=None, width=200, height=240):
    """Render a vertical chord box.

    Args:
      shape: list of 6 ints/None, ordered from 6th string (low E) to 1st string (high E).
             0 = open, -1 or None = muted, n>0 = fretted at fret n.
      title: optional title shown above the box (e.g. "E7 — open")
      base_fret: if shape uses frets all relative to a nut, leave None and we autodetect.
                 Otherwise force a specific base fret label on the side.
      role_labels: optional dict mapping string number (6..1) → role like "R", "3", "5", "b7"
                   to display below the box.
    """
    # Decide base_fret.
    played = [(s + 1, f) for s, f in enumerate(shape) if f and f > 0]  # NOTE: s+1 here is wrong order; rework below.
    # Rebuild properly.
    played = []
    for i, f in enumerate(shape):
        # i=0 corresponds to 6th string (low E)
        string_num = 6 - i
        if f is not None and f > 0:
            played.append((string_num, f))
    if base_fret is None:
        if played:
            min_fret = min(f for _, f in played)
            max_fret = max(f for _, f in played)
            if max_fret <= 5:
                base_fret = 0  # show nut
            else:
                base_fret = min_fret
        else:
            base_fret = 0

    frets_shown = 5  # 5 frets in the diagram

    # SVG geometry
    pad_top = 32
    pad_bottom = 24
    pad_left = 28
    pad_right = 28
    grid_w = width - pad_left - pad_right
    grid_h = height - pad_top - pad_bottom
    string_step = grid_w / 5  # 6 strings, 5 gaps
    fret_step = grid_h / frets_shown

    out = []
    out.append(f'<svg class="fretboard chord-box" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title or "chord diagram"}">')

    # Optional title (drawn outside the grid area, in CSS we let the parent caption handle it,
    # but we render a title element for accessibility).
    if title:
        out.append(f'<title>{title}</title>')

    # Nut: thick horizontal line on top if base_fret == 0, otherwise just a normal fret line + fret number label on side
    if base_fret == 0:
        out.append(f'<rect x="{pad_left - 1}" y="{pad_top - 5}" width="{grid_w + 2}" height="5" fill="currentColor"/>')
    else:
        out.append(f'<text x="{pad_left - 8}" y="{pad_top + fret_step * 0.65}" font-size="13" fill="currentColor" text-anchor="end" font-style="italic">{base_fret}fr</text>')

    # Frets (horizontal lines)
    for fi in range(frets_shown + 1):
        y = pad_top + fi * fret_step
        out.append(f'<line x1="{pad_left}" y1="{y}" x2="{pad_left + grid_w}" y2="{y}" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>')

    # Strings (vertical lines)
    for si in range(6):
        x = pad_left + si * string_step
        out.append(f'<line x1="{x}" y1="{pad_top}" x2="{x}" y2="{pad_top + grid_h}" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>')

    # Top markers (O for open, X for muted)
    for i, f in enumerate(shape):
        string_num = 6 - i
        x = pad_left + i * string_step
        if f is None or (isinstance(f, int) and f < 0):
            out.append(f'<text x="{x}" y="{pad_top - 10}" font-size="14" fill="currentColor" text-anchor="middle" font-style="italic">×</text>')
        elif f == 0:
            # Open-string marker — tagged so the playback animation can light it up too.
            out.append(f'<circle class="fret-dot open-dot" cx="{x}" cy="{pad_top - 13}" r="5" fill="none" stroke="currentColor" stroke-width="1.5" data-s="{string_num}" data-f="0"/>')

    # Detect barres: a barre is multiple strings at the same fret that's > 0
    # (we draw the lowest such row as a barre). Heuristic: if 2 or more strings
    # are at the same fret AND the fret is > 0 AND the leftmost muted/lower
    # fret is to the right of one of them — just draw a barre at the minimum fret.
    fret_counts = {}
    for i, f in enumerate(shape):
        if f is not None and f > 0:
            fret_counts.setdefault(f, []).append(i)
    for f, idxs in fret_counts.items():
        if len(idxs) >= 3:  # require ≥3 strings to count as a barre to avoid false positives
            # Need to make sure no lower-fret played note lies between them; otherwise it can't be barred there.
            lo, hi = min(idxs), max(idxs)
            barre_ok = True
            for j in range(lo, hi + 1):
                fv = shape[j]
                if fv is not None and fv >= 0 and fv != 0 and fv < f:
                    barre_ok = False
                    break
            if barre_ok:
                y_rel = f if base_fret == 0 else f - base_fret + 1
                if 0 < y_rel <= frets_shown:
                    y = pad_top + (y_rel - 0.5) * fret_step
                    x1 = pad_left + lo * string_step
                    x2 = pad_left + hi * string_step
                    out.append(f'<rect x="{x1 - 9}" y="{y - 9}" width="{x2 - x1 + 18}" height="18" rx="9" fill="currentColor" opacity="0.85"/>')

    # Dots
    for i, f in enumerate(shape):
        if f is None or f <= 0:
            continue
        y_rel = f if base_fret == 0 else f - base_fret + 1
        if y_rel <= 0 or y_rel > frets_shown:
            continue
        x = pad_left + i * string_step
        y = pad_top + (y_rel - 0.5) * fret_step
        role = role_labels.get(6 - i) if role_labels else None
        is_root = role == 'R'
        string_num = 6 - i
        if is_root:
            out.append(f'<circle class="fret-dot root-dot" cx="{x}" cy="{y}" r="10" fill="var(--accent-dark)" stroke="currentColor" stroke-width="1.2" data-s="{string_num}" data-f="{f}"/>')
            out.append(f'<text x="{x}" y="{y + 4}" font-size="10" fill="var(--card)" text-anchor="middle" font-weight="700" pointer-events="none">R</text>')
        else:
            out.append(f'<circle class="fret-dot" cx="{x}" cy="{y}" r="9" fill="currentColor" data-s="{string_num}" data-f="{f}"/>')
            if role:
                out.append(f'<text x="{x}" y="{y + 4}" font-size="10" fill="var(--card)" text-anchor="middle" font-weight="600" pointer-events="none">{role}</text>')

    # Bottom note-name labels under each string (note at that string and fret)
    for i, f in enumerate(shape):
        string_num = 6 - i
        x = pad_left + i * string_step
        if f is None or f < 0:
            continue
        name = note_at(string_num, f)
        y_label = pad_top + grid_h + 14
        out.append(f'<text x="{x}" y="{y_label}" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">{name}</text>')

    out.append('</svg>')
    return ''.join(out)


def chord_strip(chords, mini=True):
    """Render a row of small chord boxes labelled by chord name.

    Each item carries data-shape (a JSON-encoded shape array) so JS can
    match a played chord to its corresponding chord-box for the lit animation.
    """
    import json
    items = []
    for entry in chords:
        if len(entry) == 3:
            label, shape, roles = entry
        else:
            label, shape = entry
            roles = None
        w, h = (140, 175) if mini else (200, 240)
        box = chord_box(shape, role_labels=roles, width=w, height=h)
        shape_json = json.dumps(shape, separators=(',', ':'))
        items.append(
            f'<div class="chord-strip-item" data-shape=\'{shape_json}\'>'
            f'<div class="chord-strip-label">{label}</div>'
            f'{box}'
            f'</div>'
        )
    return '<div class="chord-strip">' + ''.join(items) + '</div>'


def scale_box(positions, fret_range, title=None, root_pitch_class=None, width=560, height=200):
    """Render a horizontal scale-position box.

    Args:
      positions: list of (string_num, fret, role) tuples. role is e.g. "R", "b3", "4", "b5", "5", "b7".
                 If role is "R" the dot is filled with a distinct accent.
      fret_range: (start_fret, end_fret) inclusive, e.g. (0, 4) for an open-position scale.
      title: optional title.
      root_pitch_class: if set, dots whose note matches the root pitch class get the "R" treatment
                        regardless of role argument.
    """
    start, end = fret_range
    # number of cells (= fret positions visible)
    # for start==0, cell i represents fret i (with open strings to the left of the nut)
    # for start>0, cell i represents fret (start + i - 1)
    if start == 0:
        n_frets = end  # cells 1..end, plus the open-string area outside
    else:
        n_frets = end - start + 1

    pad_top = 22
    pad_bottom = 26
    pad_left = 38
    pad_right = 16
    grid_w = width - pad_left - pad_right
    grid_h = height - pad_top - pad_bottom
    string_step = grid_h / 5  # 6 strings, 5 gaps
    fret_step = grid_w / n_frets  # n_frets cells

    out = []
    out.append(f'<svg class="fretboard scale-box" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title or "scale diagram"}">')
    if title:
        out.append(f'<title>{title}</title>')

    # Nut on left if start == 0
    if start == 0:
        out.append(f'<rect x="{pad_left - 4}" y="{pad_top - 1}" width="4" height="{grid_h + 2}" fill="currentColor"/>')

    # Fret lines (vertical)
    for fi in range(n_frets + 1):
        x = pad_left + fi * fret_step
        out.append(f'<line x1="{x}" y1="{pad_top}" x2="{x}" y2="{pad_top + grid_h}" stroke="currentColor" stroke-width="1.1" opacity="0.6"/>')

    # String lines (horizontal); string 1 (high E) is at top? Convention varies. Most guitar diagrams put 6=low E at bottom, 1=high E at top. We follow that.
    for si in range(6):
        # si=0 → string 1 (high E) at top
        string_num = si + 1
        y = pad_top + si * string_step
        # vary stroke weight slightly so low strings look thicker
        sw = 0.9 + (string_num / 12) * 1.0
        out.append(f'<line x1="{pad_left}" y1="{y}" x2="{pad_left + grid_w}" y2="{y}" stroke="currentColor" stroke-width="{sw:.2f}" opacity="0.6"/>')

    # Fret number markers below
    # cell fi (1-indexed) represents fret: fi when start==0, else (start + fi - 1)
    def cell_fret(fi):
        return fi if start == 0 else start + fi - 1
    for fi in range(n_frets + 1):
        actual_fret = cell_fret(fi) if fi > 0 else start
        if actual_fret in (3, 5, 7, 9, 15, 17, 19, 21) and fi > 0:
            # single-dot inlay between strings 3 and 4
            x = pad_left + (fi - 0.5) * fret_step
            y = pad_top + 2.5 * string_step
            out.append(f'<circle cx="{x}" cy="{y}" r="3" fill="currentColor" opacity="0.18"/>')
        if actual_fret == 12 and fi > 0:
            # double-dot
            x = pad_left + (fi - 0.5) * fret_step
            y1 = pad_top + 1.5 * string_step
            y2 = pad_top + 3.5 * string_step
            out.append(f'<circle cx="{x}" cy="{y1}" r="3" fill="currentColor" opacity="0.18"/>')
            out.append(f'<circle cx="{x}" cy="{y2}" r="3" fill="currentColor" opacity="0.18"/>')

    # Fret numbers along the bottom + side-label for non-zero start
    if start > 0:
        x = pad_left - 14
        y_label = pad_top + grid_h / 2 + 4
        out.append(f'<text x="{x}" y="{y_label}" font-size="12" fill="currentColor" text-anchor="middle" font-style="italic" opacity="0.85">{start}fr</text>')
    for fi in range(1, n_frets + 1):
        actual_fret = cell_fret(fi)
        x = pad_left + (fi - 0.5) * fret_step
        y_label = pad_top + grid_h + 14
        out.append(f'<text x="{x}" y="{y_label}" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.55">{actual_fret}</text>')

    # Dots
    for entry in positions:
        if len(entry) == 3:
            string_num, fret, role = entry
        else:
            string_num, fret = entry
            role = ''
        if fret == 0:
            # open string — draw to the left of the nut as a small circle
            x = pad_left - 16
        else:
            fi = fret if start == 0 else fret - start + 1
            x = pad_left + (fi - 0.5) * fret_step
        y = pad_top + (string_num - 1) * string_step  # string 1 at top
        is_root = (role == 'R') or (root_pitch_class is not None and note_at(string_num, fret) == root_pitch_class)
        if is_root:
            out.append(f'<circle class="fret-dot root-dot" cx="{x}" cy="{y}" r="11" fill="var(--accent)" stroke="currentColor" stroke-width="1.4" data-s="{string_num}" data-f="{fret}"/>')
            out.append(f'<text x="{x}" y="{y + 4}" font-size="10" fill="var(--paper)" text-anchor="middle" font-weight="700" pointer-events="none">R</text>')
        else:
            out.append(f'<circle class="fret-dot" cx="{x}" cy="{y}" r="10" fill="currentColor" data-s="{string_num}" data-f="{fret}"/>')
            if role:
                out.append(f'<text x="{x}" y="{y + 3.5}" font-size="9" fill="var(--card)" text-anchor="middle" font-weight="600" pointer-events="none">{role}</text>')

    out.append('</svg>')
    return ''.join(out)
