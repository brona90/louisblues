"""Rich SVG tablature rendering.

Supports the full blues vocabulary:
  - variable-duration notes (whole..32nd)
  - bends (full, half, pre-bend, release)
  - hammer-ons / pull-offs (slurs labelled h / p)
  - slides (up / down / into)
  - vibrato (squiggle above the note)
  - palm mute (PM bracket above)
  - ghost notes (parens around fret number)
  - ties between bars
  - chord-name labels above the staff
  - bar numbers
  - bar lines and double-bar end repeats

Event format (use the helper constructors below):
  ('note', string, fret, opts)
  ('chord', [(string, fret), ...], opts)
  ('rest', opts)
  ('bar',)         — drawn automatically when bars are passed as a list of bars
  ('rep_start',)
  ('rep_end',)

opts is a dict with any of:
  dur (beats), bend_to, pre_bend, release_to, slide_up, slide_down,
  slide_into_from, slide_into_dir ('up'|'down'),
  hammer_to, pull_to, vibrato, pm, ghost, tie_next, accent, audio_note
"""

import html


# ────────────────────────────────────────────────────────────────────
# Helpers — build events in a readable way
# ────────────────────────────────────────────────────────────────────

def n(string, fret, dur=1.0, **opts):
    opts['dur'] = dur
    return ('note', string, fret, opts)


def c(notes, dur=1.0, **opts):
    opts['dur'] = dur
    return ('chord', list(notes), opts)


def r(dur=1.0, **opts):
    opts['dur'] = dur
    return ('rest', opts)


def br():
    return ('bar',)


def rep_start():
    return ('rep_start',)


def rep_end():
    return ('rep_end',)


# ────────────────────────────────────────────────────────────────────
# Layout
# ────────────────────────────────────────────────────────────────────

def _event_dur(ev):
    if ev[0] in ('note', 'chord', 'rest'):
        return ev[-1].get('dur', 1.0)
    return 0.0


def _split_into_bars(events):
    """If events contain ('bar',) markers, split into bars. Otherwise yield single bar."""
    bars = []
    cur = []
    for ev in events:
        if ev[0] == 'bar':
            bars.append(cur)
            cur = []
        else:
            cur.append(ev)
    if cur:
        bars.append(cur)
    return bars


def _layout_lines(bars, bars_per_line):
    """Group bars into lines of `bars_per_line` bars each."""
    lines = []
    for i in range(0, len(bars), bars_per_line):
        lines.append(bars[i:i + bars_per_line])
    return lines


# ────────────────────────────────────────────────────────────────────
# Drawing
# ────────────────────────────────────────────────────────────────────

STEM_H = 18

def _stem(out, x, y_top, dur, fill='currentColor'):
    """Draw a stem line only — flags / beams are added later by _beam_bar."""
    out.append(f'<line x1="{x:.2f}" y1="{y_top:.2f}" x2="{x:.2f}" y2="{y_top + STEM_H:.2f}" stroke="{fill}" stroke-width="1.1"/>')


def _flag_count(dur):
    if dur <= 0.0625: return 4    # 64th
    if dur <= 0.125: return 3     # 32nd
    if dur <= 0.25: return 2      # 16th
    if dur <= 0.5: return 1       # 8th
    return 0                      # quarter+


def _beam_bar(out, event_info_list, stem_y_top):
    """Add flags / beams to the bar after the stems have been drawn.
    Groups runs of adjacent flagged notes (dur <= 0.5) into a single beam group.
    """
    bottom = stem_y_top + STEM_H
    i = 0
    while i < len(event_info_list):
        info = event_info_list[i]
        ev = info['ev']
        if ev[0] not in ('note', 'chord'):
            i += 1
            continue
        dur = ev[-1].get('dur', 1.0)
        if _flag_count(dur) == 0:
            i += 1
            continue
        # Find run end — consecutive flagged events with no rest/long-note in between
        j = i
        while (j < len(event_info_list)
               and event_info_list[j]['ev'][0] in ('note', 'chord')
               and _flag_count(event_info_list[j]['ev'][-1].get('dur', 1.0)) > 0):
            j += 1
        group = event_info_list[i:j]
        if len(group) == 1:
            # Isolated → curved flag
            g = group[0]
            x = g['note_x']
            n_flags = _flag_count(g['ev'][-1].get('dur', 1.0))
            for k in range(n_flags):
                yy = bottom - k * 4
                out.append(f'<path d="M{x:.2f} {yy:.2f} Q{x + 7:.2f} {yy + 3:.2f} {x + 6:.2f} {yy + 8:.2f}" '
                           f'fill="none" stroke="currentColor" stroke-width="1.2"/>')
        else:
            # Beam group — primary (8th) beam across whole run
            xs = [g['note_x'] for g in group]
            x1, x2 = xs[0], xs[-1]
            out.append(f'<rect x="{x1 - 0.5:.2f}" y="{bottom - 3:.2f}" width="{x2 - x1 + 1:.2f}" '
                       f'height="3.5" fill="currentColor"/>')
            # Secondary (16th) beam — only between adjacent 16ths.
            # Find sub-runs of 2+ adjacent 16ths.
            k = 0
            while k < len(group):
                d = group[k]['ev'][-1].get('dur', 1.0)
                if _flag_count(d) >= 2:
                    m = k
                    while m < len(group) and _flag_count(group[m]['ev'][-1].get('dur', 1.0)) >= 2:
                        m += 1
                    if m - k >= 2:
                        sx1 = group[k]['note_x']
                        sx2 = group[m - 1]['note_x']
                        out.append(f'<rect x="{sx1 - 0.5:.2f}" y="{bottom - 8:.2f}" '
                                   f'width="{sx2 - sx1 + 1:.2f}" height="3" fill="currentColor"/>')
                    elif m - k == 1:
                        # single 16th in a beam group — partial beam stub
                        sx = group[k]['note_x']
                        # decide direction: stub to the right if first/middle, left if last
                        if k == 0 or _flag_count(group[k - 1]['ev'][-1].get('dur', 1.0)) < 2:
                            out.append(f'<rect x="{sx:.2f}" y="{bottom - 8:.2f}" width="6" height="3" fill="currentColor"/>')
                        else:
                            out.append(f'<rect x="{sx - 6:.2f}" y="{bottom - 8:.2f}" width="6" height="3" fill="currentColor"/>')
                    k = m
                else:
                    k += 1
        i = j


def _draw_note_text(out, x, y, fret_text, fill='currentColor', bg='var(--card)', accent=False, ghost=False):
    label = fret_text
    if ghost:
        label = f'({fret_text})'
    w = max(11, 7 * len(label))
    bg_color = bg
    out.append(f'<rect x="{x - w/2:.2f}" y="{y - 7:.2f}" width="{w}" height="14" fill="{bg_color}" rx="2"/>')
    weight = '700' if accent else '600'
    out.append(f'<text x="{x:.2f}" y="{y + 4:.2f}" font-size="11.5" fill="{fill}" text-anchor="middle" font-weight="{weight}">{html.escape(label)}</text>')


def _bend_arrow(out, x, y, target_text):
    """Draw a curved bend arrow upward from (x, y) with label `target_text`."""
    # Arrow rises up-and-right ~16px, points at the target text
    ax = x + 14
    ay = y - 22
    out.append(f'<path d="M{x:.2f} {y - 8:.2f} Q{x + 4:.2f} {y - 18:.2f} {ax:.2f} {ay:.2f}" fill="none" stroke="currentColor" stroke-width="1.2"/>')
    # arrowhead
    out.append(f'<path d="M{ax - 3:.2f} {ay + 4:.2f} L{ax:.2f} {ay:.2f} L{ax + 3:.2f} {ay + 4:.2f}" fill="none" stroke="currentColor" stroke-width="1.2"/>')
    out.append(f'<text x="{ax + 5:.2f}" y="{ay + 4:.2f}" font-size="9.5" fill="currentColor" font-style="italic">{html.escape(str(target_text))}</text>')


def _release_arrow(out, x, y, target_text):
    """Bend-release: arrow curving down."""
    ax = x + 14
    ay = y + 22
    out.append(f'<path d="M{x:.2f} {y + 8:.2f} Q{x + 4:.2f} {y + 18:.2f} {ax:.2f} {ay:.2f}" fill="none" stroke="currentColor" stroke-width="1.2"/>')
    out.append(f'<path d="M{ax - 3:.2f} {ay - 4:.2f} L{ax:.2f} {ay:.2f} L{ax + 3:.2f} {ay - 4:.2f}" fill="none" stroke="currentColor" stroke-width="1.2"/>')
    out.append(f'<text x="{ax + 5:.2f}" y="{ay + 4:.2f}" font-size="9.5" fill="currentColor" font-style="italic">{html.escape(str(target_text))}</text>')


def _slur(out, x1, y1, x2, y2, label):
    """Curved slur (hammer-on / pull-off) above the strings, with text label."""
    cx = (x1 + x2) / 2
    cy = min(y1, y2) - 13
    out.append(f'<path d="M{x1:.2f} {y1 - 5:.2f} Q{cx:.2f} {cy:.2f} {x2:.2f} {y2 - 5:.2f}" fill="none" stroke="currentColor" stroke-width="1.1"/>')
    out.append(f'<text x="{cx:.2f}" y="{cy + 2:.2f}" font-size="10" fill="currentColor" text-anchor="middle" font-style="italic" opacity="0.8">{html.escape(str(label))}</text>')


def _vibrato(out, x, y, width=22):
    """Squiggle above the note."""
    yy = y - 16
    d = f'M{x - 2:.2f} {yy:.2f}'
    n_waves = 4
    step = width / n_waves
    for i in range(n_waves):
        x1 = x - 2 + (i + 0.5) * step
        ydir = -3 if i % 2 == 0 else 3
        d += f' Q{x1:.2f} {yy + ydir:.2f} {x - 2 + (i + 1) * step:.2f} {yy:.2f}'
    out.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.1"/>')


def _palm_mute(out, x1, x2, y):
    """PM bracket above a passage."""
    yy = y - 22
    out.append(f'<text x="{x1 - 2:.2f}" y="{yy + 3:.2f}" font-size="9.5" fill="currentColor" font-style="italic" font-weight="600">PM</text>')
    out.append(f'<line x1="{x1 + 18:.2f}" y1="{yy:.2f}" x2="{x2:.2f}" y2="{yy:.2f}" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>')


def _slide_line(out, x1, y1, x2, y2):
    out.append(f'<line x1="{x1 + 6:.2f}" y1="{y1:.2f}" x2="{x2 - 6:.2f}" y2="{y2:.2f}" stroke="currentColor" stroke-width="1.2"/>')


def _draw_event(out, ev, x_left, x_right, string_step, pad_top):
    """Draw one event in the slot x_left..x_right. Returns dict of post-render info (e.g. note positions)."""
    info = {}
    kind = ev[0]
    x_center = (x_left + x_right) / 2

    if kind == 'rest':
        opts = ev[1]
        dur = opts.get('dur', 1.0)
        # Rest glyph: simple text. position rest in the vertical centre of staff
        y = pad_top + 2.5 * string_step
        sym = '𝄽' if dur >= 1.0 else '𝄾' if dur >= 0.5 else '𝄿'
        out.append(f'<text x="{x_center:.2f}" y="{y + 6:.2f}" font-size="20" fill="currentColor" text-anchor="middle" opacity="0.55">{sym}</text>')
        return info

    if kind == 'note':
        _, sn, fr, opts = ev
        y = pad_top + (sn - 1) * string_step
        accent = opts.get('accent', False)
        ghost = opts.get('ghost', False)
        seq_idx = opts.get('_seq_idx')
        # Open a wrapper so the playhead can light this one note up.
        attrs = f' data-s="{sn}" data-f="{fr}"'
        if seq_idx is not None:
            attrs += f' data-i="{seq_idx}"'
        out.append(f'<g class="tab-note"{attrs}>')
        if opts.get('pre_bend') is not None:
            _draw_note_text(out, x_center, y, str(opts['pre_bend']), accent=accent, ghost=ghost)
            _release_arrow(out, x_center, y, str(fr))
            info['note_x'] = x_center
            info['note_y'] = y
            out.append('</g>')
            return info
        _draw_note_text(out, x_center, y, str(fr), accent=accent, ghost=ghost)
        info['note_x'] = x_center
        info['note_y'] = y
        if opts.get('bend_to') is not None:
            target = opts['bend_to']
            label = '½' if target - fr == 1 else 'full' if target - fr == 2 else f'+{target - fr}'
            _bend_arrow(out, x_center, y, label)
        if opts.get('release_to') is not None:
            _release_arrow(out, x_center, y, str(opts['release_to']))
        if opts.get('vibrato'):
            _vibrato(out, x_center, y)
        if opts.get('slide_into_dir') == 'up':
            out.append(f'<line x1="{x_center - 14:.2f}" y1="{y + 6:.2f}" x2="{x_center - 6:.2f}" y2="{y:.2f}" stroke="currentColor" stroke-width="1.1"/>')
        elif opts.get('slide_into_dir') == 'down':
            out.append(f'<line x1="{x_center - 14:.2f}" y1="{y - 6:.2f}" x2="{x_center - 6:.2f}" y2="{y:.2f}" stroke="currentColor" stroke-width="1.1"/>')
        dur = opts.get('dur', 1.0)
        if dur < 1.5:
            _stem(out, x_center, pad_top + 5 * string_step + 6, dur)
        out.append('</g>')
        return info

    if kind == 'chord':
        _, notes, opts = ev
        accent = opts.get('accent', False)
        seq_idx = opts.get('_seq_idx')
        attrs = ''
        if seq_idx is not None:
            attrs += f' data-i="{seq_idx}"'
        out.append(f'<g class="tab-note tab-chord"{attrs}>')
        for sn, fr in notes:
            y = pad_top + (sn - 1) * string_step
            _draw_note_text(out, x_center, y, str(fr), accent=accent)
        info['notes'] = [(sn, fr) for sn, fr in notes]
        info['note_x'] = x_center
        dur = opts.get('dur', 1.0)
        if dur < 1.5:
            _stem(out, x_center, pad_top + 5 * string_step + 6, dur)
        out.append('</g>')
        return info

    return info


def render_tab(bars,
               chord_labels=None,
               width=900,
               bars_per_line=4,
               line_h=140,
               beat_unit=4,
               title=None,
               show_bar_numbers=True,
               start_bar=1):
    """Render a multi-line tab.

    Args:
      bars: list of bars. Each bar is a list of events built with n/c/r/...
      chord_labels: optional list (one chord-name per bar; '' for blank)
      width: SVG width in px
      bars_per_line: how many bars per staff line
      beat_unit: total beats per bar (4 for 4/4)
      title: optional title
      show_bar_numbers: small bar number above each bar
      start_bar: bar number for the first bar
    """
    lines = _layout_lines(bars, bars_per_line)
    n_lines = len(lines)

    total_height = n_lines * line_h + 30
    pad_left = 22
    pad_right = 22
    pad_top = 36
    pad_bottom = 26
    grid_w = width - pad_left - pad_right
    string_step = 13
    grid_h = 5 * string_step

    # Sequential note counter — increments for every note/chord event across
    # all bars so each rendered tab-note gets a unique data-i.
    note_seq = 0

    out = [f'<svg class="tab tab-rich" viewBox="0 0 {width} {total_height}" xmlns="http://www.w3.org/2000/svg">']
    if title:
        out.append(f'<text x="{width/2:.2f}" y="14" font-size="13" fill="currentColor" text-anchor="middle" font-style="italic" opacity="0.75">{html.escape(title)}</text>')

    # Every bar takes a uniform amount of horizontal space — one "bar unit"
    # equals `beat_unit` beats and is `grid_w / bars_per_line` pixels wide.
    # This way a partial last line (fewer bars than bars_per_line) doesn't
    # stretch its bars to fill the whole width.
    width_per_beat = grid_w / (bars_per_line * beat_unit)
    for line_idx, line_bars in enumerate(lines):
        line_y_top = 30 + line_idx * line_h
        durs = []
        for bar in line_bars:
            d = sum(_event_dur(e) for e in bar)
            durs.append(d if d > 0 else beat_unit)
        bar_x_starts = [pad_left]
        cum = 0.0
        for d in durs:
            cum += d
            bar_x_starts.append(pad_left + cum * width_per_beat)

        # Staff lines stop at the last bar of THIS line (so partial last lines
        # don't have ghost rules hanging off to the right).
        line_end_x = bar_x_starts[-1]
        for si in range(6):
            y = line_y_top + pad_top + si * string_step
            sw = 0.85 + (si / 12) * 0.6
            out.append(f'<line x1="{pad_left}" y1="{y:.2f}" x2="{line_end_x:.2f}" y2="{y:.2f}" stroke="currentColor" stroke-width="{sw:.2f}" opacity="0.55"/>')

        # T A B letters on left
        for i, ch in enumerate(['T', 'A', 'B']):
            y = line_y_top + pad_top + (1.0 + i * 1.5) * string_step + 4
            out.append(f'<text x="{pad_left - 8}" y="{y:.2f}" font-size="13" fill="currentColor" text-anchor="end" font-style="italic" opacity="0.5">{ch}</text>')

        # Bar lines
        for x in bar_x_starts:
            out.append(f'<line x1="{x:.2f}" y1="{line_y_top + pad_top - 4}" x2="{x:.2f}" y2="{line_y_top + pad_top + grid_h + 4}" stroke="currentColor" stroke-width="1.1" opacity="0.6"/>')

        # Final double bar at end of last line
        if line_idx == n_lines - 1:
            x_end = bar_x_starts[-1]
            out.append(f'<line x1="{x_end - 3:.2f}" y1="{line_y_top + pad_top - 4}" x2="{x_end - 3:.2f}" y2="{line_y_top + pad_top + grid_h + 4}" stroke="currentColor" stroke-width="1.4" opacity="0.7"/>')

        # Per-bar drawing
        first_bar_in_line = line_idx * bars_per_line
        for bi, bar in enumerate(line_bars):
            bar_x_left = bar_x_starts[bi]
            bar_x_right = bar_x_starts[bi + 1]
            bar_w = bar_x_right - bar_x_left
            global_bar_idx = first_bar_in_line + bi

            # Chord label above
            if chord_labels and global_bar_idx < len(chord_labels) and chord_labels[global_bar_idx]:
                out.append(f'<text x="{bar_x_left + 4:.2f}" y="{line_y_top + pad_top - 14}" font-size="13" fill="var(--accent)" font-weight="700" font-style="italic">{html.escape(str(chord_labels[global_bar_idx]))}</text>')

            # Bar number
            if show_bar_numbers:
                out.append(f'<text x="{bar_x_left + 2:.2f}" y="{line_y_top + pad_top - 26}" font-size="9" fill="currentColor" opacity="0.4">{start_bar + global_bar_idx}</text>')

            # Layout events within the bar by duration
            bar_total_dur = sum(_event_dur(e) for e in bar)
            if bar_total_dur <= 0:
                continue
            ev_x_start = bar_x_left + 4
            slot_w_unit = (bar_w - 12) / bar_total_dur

            cur_x = ev_x_start
            event_info_list = []
            for ev in bar:
                d = _event_dur(ev)
                slot_w = d * slot_w_unit
                # Inject the sequential note index into note/chord events
                # so the playhead can light up each tab-note in order.
                if ev[0] in ('note', 'chord'):
                    new_opts = dict(ev[-1])
                    new_opts['_seq_idx'] = note_seq
                    note_seq += 1
                    ev = ev[:-1] + (new_opts,)
                info = _draw_event(out, ev, cur_x, cur_x + slot_w,
                                    string_step, line_y_top + pad_top)
                info['x_left'] = cur_x
                info['x_right'] = cur_x + slot_w
                info['ev'] = ev
                event_info_list.append(info)
                cur_x += slot_w

            # Post-pass: connect hammer-ons / pull-offs / slides to NEXT event's note position
            for i, info in enumerate(event_info_list):
                ev = info['ev']
                if ev[0] != 'note':
                    continue
                opts = ev[-1]
                if i + 1 >= len(event_info_list):
                    continue
                next_info = event_info_list[i + 1]
                if 'note_x' not in next_info:
                    continue
                y_now = info['note_y']
                x_now = info['note_x']
                x_next = next_info['note_x']
                y_next = next_info.get('note_y', y_now)
                if opts.get('hammer_to') is not None:
                    _slur(out, x_now, y_now, x_next, y_next, 'H')
                if opts.get('pull_to') is not None:
                    _slur(out, x_now, y_now, x_next, y_next, 'P')
                if opts.get('slide_up'):
                    _slide_line(out, x_now, y_now, x_next, y_next)
                if opts.get('slide_down'):
                    _slide_line(out, x_now, y_now, x_next, y_next)

            # Beam pass — replace per-note flags with proper beams across runs of 8ths/16ths
            stem_y_top = line_y_top + pad_top + 5 * string_step + 6
            _beam_bar(out, event_info_list, stem_y_top)

            # Palm-mute bracket spanning consecutive pm events
            pm_runs = []
            i = 0
            while i < len(event_info_list):
                if event_info_list[i]['ev'][0] == 'note' and event_info_list[i]['ev'][-1].get('pm'):
                    j = i
                    while j < len(event_info_list) and event_info_list[j]['ev'][0] == 'note' and event_info_list[j]['ev'][-1].get('pm'):
                        j += 1
                    pm_runs.append((i, j - 1))
                    i = j
                else:
                    i += 1
            for a, b in pm_runs:
                x1 = event_info_list[a]['note_x']
                x2 = event_info_list[b]['note_x']
                y0 = event_info_list[a].get('note_y', line_y_top + pad_top + 2 * string_step)
                _palm_mute(out, x1, x2 + 14, y0)

    out.append('</svg>')
    # Wrap in a horizontally-scrollable container so the tab stays legible
    # on narrow (mobile) screens.
    return '<div class="tab-scroll">' + ''.join(out) + '</div>'


# ────────────────────────────────────────────────────────────────────
# Compatibility shim — old API used by form.py
# ────────────────────────────────────────────────────────────────────

def tab_line(events, beats_per_line=16, width=900, height=130, bar_lines=None, labels=None):
    """Legacy single-line renderer used by form.py.
    Converts an old-style flat events list into the new format.
    """
    new_bars = [[]]
    bar_positions = set(bar_lines or [])
    chord_labels = []
    if labels:
        # labels are at positions; we need them per-bar
        cur_label = None
        for i in range(beats_per_line):
            for pos, txt in labels:
                if pos == i:
                    cur_label = txt
            chord_labels.append(cur_label)
    cur_bar_label = labels[0][1] if labels else None
    bar_labels = []
    for i, ev in enumerate(events):
        if i in bar_positions and i > 0:
            new_bars.append([])
            # determine label for this new bar
            for pos, txt in (labels or []):
                if pos == i:
                    cur_bar_label = txt
        old_kind = ev[0]
        if old_kind == 'rest':
            new_bars[-1].append(r(0.5))
        elif old_kind == 'note':
            new_bars[-1].append(n(ev[1], ev[2], dur=0.5))
        elif old_kind == 'chord':
            new_bars[-1].append(c(ev[1], dur=0.5))
    # bar labels: one per bar, from labels list
    if labels:
        # labels[(pos, txt)] — derive one per new_bar
        label_per_bar = []
        boundaries = [0] + [b for b in sorted(bar_positions) if b > 0]
        for bstart in boundaries:
            found = None
            for pos, txt in labels:
                if pos <= bstart:
                    found = txt
            label_per_bar.append(found or '')
        bar_labels = label_per_bar
    return render_tab(new_bars, chord_labels=bar_labels, width=width,
                       bars_per_line=len(new_bars), beat_unit=4, show_bar_numbers=False)
