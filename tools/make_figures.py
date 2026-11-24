"""Generate abstract schematic figures (SVG) for the personal site.

Run from the repo root:  python tools/make_figures.py
Figures are schematics, not data. Replace any of them with a real figure by
adding a PNG/JPG to assets/img/ and pointing the matching entry in _data/ at it.
"""
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'img')

TEAL = '#1f6f78'
GREY = '#9aa3a7'
LIGHT = '#dcebed'
PALE = '#f1f3f4'
INK = '#2b2f33'
MONO = 'Menlo, Consolas, monospace'


def wrap(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{label}"><rect width="{w}" height="{h}" fill="#ffffff"/>{body}</svg>')


def line_path(pts, color=TEAL, width=1.4, extra=''):
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round" {extra}/>')


def label(x, y, s, color=INK, size=11, anchor='start', weight='normal', italic=False):
    st = ' font-style="italic"' if italic else ''
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO}" font-size="{size}" '
            f'text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')


def circle(x, y, r, fill='none', stroke=TEAL, sw=1.2, opacity=1):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{opacity}"/>')


def frange(a, b, step):
    n = int((b - a) / step)
    return [a + i * step for i in range(n + 1)]


def save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', name)


def fig_oscillations():
    W, H = 640, 300
    x0, x1, P = 60, 610, 275.0
    base = [70, 160, 244]

    def slow(x):
        return math.sin(2 * math.pi * (x - x0) / P - math.pi / 2)

    centers = [x0 + P / 2 + k * P for k in range(2)]
    body = []
    for c in centers:
        body.append(f'<line x1="{c}" y1="34" x2="{c}" y2="272" stroke="{GREY}" '
                    f'stroke-width="1" stroke-dasharray="3 4"/>')
    body.append(line_path([(x, base[0] - 28 * slow(x)) for x in frange(x0, x1, 1.0)]))

    body.append(f'<line x1="{x0}" y1="{base[1]}" x2="{x1}" y2="{base[1]}" stroke="{GREY}" stroke-width="0.8"/>')
    for c in centers:
        pts = []
        for x in frange(c - 70, c + 70, 0.5):
            env = max(0.0, (slow(x) - 0.35) / 0.65) ** 1.3
            pts.append((x, base[1] - 17 * env * math.sin(2 * math.pi * x / 10.0)))
        body.append(line_path(pts, width=1.2))

    body.append(f'<line x1="{x0}" y1="{base[2]}" x2="{x1}" y2="{base[2]}" stroke="{GREY}" stroke-width="0.8"/>')
    for c in centers:
        pts = []
        for x in frange(c - 30, c + 30, 0.4):
            env = math.exp(-((x - c) / 9.0) ** 2)
            pts.append((x, base[2] - 20 * env * math.sin(2 * math.pi * x / 3.4)))
        body.append(line_path(pts, width=1.1))

    body.append(label(x0, 24, 'slow oscillation', weight='bold'))
    body.append(label(x0, 112, 'spindle  (11-16 Hz)', weight='bold'))
    body.append(label(x0, 198, 'hippocampal ripple  (150-250 Hz)', weight='bold'))
    body.append(label(W - 14, H - 10, 'schematic: nested oscillations during sleep', GREY, 10, 'end', italic=True))
    save('oscillations.svg', wrap(W, H, ''.join(body), 'Schematic of nested slow oscillation, spindle and ripple rhythms'))


def fig_state_space():
    W, H = 640, 300
    cx, cy, rx, ry = 340, 150, 150, 82
    body = [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GREY}" '
            f'stroke-width="1" stroke-dasharray="4 5"/>']
    for k, (ph, op) in enumerate([(0.0, 0.9), (1.7, 0.55), (3.1, 0.4)]):
        pts = []
        for t in frange(0, 2 * math.pi * 1.2, 0.04):
            wob = 1 + 0.09 * math.sin(3 * t + ph) + 0.05 * math.sin(7 * t + 2 * ph)
            pts.append((cx + rx * wob * math.cos(t + ph * 0.1), cy + ry * wob * math.sin(t + ph * 0.1)))
        body.append(line_path(pts, TEAL, 1.5, f'opacity="{op}"'))
    pts = []
    for t in frange(0, 2 * math.pi * 1.75, 0.04):
        r = 1.0 if t < 4.2 else max(0.12, 1.0 - 0.17 * (t - 4.2))
        pts.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    body.append(line_path(pts, INK, 1.8))
    ex, ey = pts[-1]
    body.append(circle(ex, ey, 4, INK, INK))
    body.append(circle(pts[0][0], pts[0][1], 4, '#ffffff', INK, 1.4))
    body.append(label(cx + rx - 4, cy - ry - 14, 'attractor ring', GREY, 11, 'end'))
    body.append(label(ex + 12, ey + 4, 'perturbed trajectory', INK, 11))
    body.append('<path d="M40,270 L120,270 M40,270 L40,196" stroke="#2b2f33" stroke-width="1.2" fill="none"/>')
    body.append(label(124, 274, 'PC1'))
    body.append(label(34, 188, 'PC2', anchor='start'))
    body.append(label(W - 14, H - 10, 'schematic: population state space', GREY, 10, 'end', italic=True))
    save('state-space.svg', wrap(W, H, ''.join(body), 'Schematic of neural population trajectories around an attractor'))


def fig_memory_states():
    W, H = 640, 300
    rnd = random.Random(7)
    body = []
    cols, rows, sp, ox, oy = 6, 5, 40, 50, 62
    left = [(ox + c * sp, oy + r * sp) for r in range(rows) for c in range(cols)]
    for r in range(rows):
        for c in range(cols):
            x, y = ox + c * sp, oy + r * sp
            if c < cols - 1:
                body.append(f'<line x1="{x}" y1="{y}" x2="{x + sp}" y2="{y}" stroke="{GREY}" stroke-width="1"/>')
            if r < rows - 1:
                body.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + sp}" stroke="{GREY}" stroke-width="1"/>')
    for x, y in left:
        body.append(circle(x, y, 6, LIGHT, TEAL, 1.3))

    pts = []
    tries = 0
    while len(pts) < 30 and tries < 4000:
        tries += 1
        p = (rnd.uniform(385, 610), rnd.uniform(60, 250))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 30 ** 2 for q in pts):
            pts.append(p)
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            if (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 < 60 ** 2:
                body.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                            f'stroke="{GREY}" stroke-width="1"/>')
    for i, (x, y) in enumerate(pts):
        active = (x - 500) ** 2 + (y - 150) ** 2 < 70 ** 2
        body.append(circle(x, y, 6, TEAL if active else '#ffffff', TEAL, 1.3))

    body.append('<path d="M278,160 L350,160" stroke="#2b2f33" stroke-width="1.4" fill="none"/>')
    body.append('<path d="M343,154 L351,160 L343,166" stroke="#2b2f33" stroke-width="1.4" fill="none"/>')
    body.append(label(314, 140, 'local rules', INK, 10, 'middle'))
    body.append(label(314, 182, 'propagate', INK, 10, 'middle'))
    body.append(label(ox, 30, 'periodic substrate', weight='bold'))
    body.append(label(385, 30, 'aperiodic substrate', weight='bold'))
    body.append(label(W - 14, H - 10, 'schematic: periodic rules, aperiodic networks', GREY, 10, 'end', italic=True))
    save('memory-states.svg', wrap(W, H, ''.join(body), 'Schematic of a periodic lattice and an aperiodic network'))


def fig_silent_recall():
    W, H = 640, 300
    rnd = random.Random(11)
    wx0, wx1 = 320, 440
    body = [f'<rect x="{wx0}" y="38" width="{wx1 - wx0}" height="232" fill="{LIGHT}" opacity="0.65"/>']
    body.append(label((wx0 + wx1) / 2, 30, 'recall window', TEAL, 11, 'middle', 'bold'))
    xs0, xs1 = 70, 610
    pup = []
    for x in frange(xs0, xs1, 2):
        bump = 20 * math.exp(-((x - 380) / 38.0) ** 2)
        pup.append((x, 86 - bump + 4 * math.sin(x / 23.0) + 2 * math.sin(x / 7.0)))
    body.append(line_path(pup))
    body.append(label(xs0, 56, 'pupil', weight='bold'))
    body.append(f'<line x1="{xs0}" y1="168" x2="{xs1}" y2="168" stroke="{GREY}" stroke-width="0.8"/>')
    x = xs0
    while x < xs1:
        inside = wx0 <= x <= wx1
        x += rnd.expovariate(1 / (9 if inside else 32))
        if x < xs1:
            body.append(f'<line x1="{x:.1f}" y1="158" x2="{x:.1f}" y2="178" stroke="{TEAL}" stroke-width="1.6"/>')
    body.append(label(xs0, 142, 'micro-saccades', weight='bold'))
    clf = []
    for x in frange(xs0, xs1, 2):
        s = 1 / (1 + math.exp(-(x - 330) / 7.0)) * (1 - 1 / (1 + math.exp(-(x - 440) / 7.0)))
        clf.append((x, 254 - 34 * s + rnd.uniform(-1.0, 1.0)))
    body.append(line_path(clf, INK, 1.6))
    body.append(label(xs0, 212, 'classifier output', weight='bold'))
    body.append(label(W - 14, H - 10, 'schematic: decoding covert recall', GREY, 10, 'end', italic=True))
    save('silent-recall.svg', wrap(W, H, ''.join(body), 'Schematic of pupil, micro-saccade and classifier signals around a recall window'))


def fig_neuronal_substrates():
    W, H = 640, 300
    rnd = random.Random(5)
    sw, n = 40, 16
    ox = (W - sw * n) / 2
    body = []
    for i in range(n):
        body.append(f'<rect x="{ox + i * sw}" y="40" width="{sw}" height="230" fill="{LIGHT if i % 2 == 0 else PALE}"/>')
    body.append(f'<rect x="{ox}" y="12" width="10" height="10" fill="{LIGHT}" stroke="{TEAL}" stroke-width="0.8"/>')
    body.append(label(ox + 16, 21, 'PEDOT:PSS', INK, 10))
    body.append(f'<rect x="{ox + 112}" y="12" width="10" height="10" fill="{PALE}" stroke="{GREY}" stroke-width="0.8"/>')
    body.append(label(ox + 128, 21, 'PVDF-TrFE', INK, 10))
    for k, s in enumerate(rnd.sample([1, 3, 5, 7, 9, 11, 13], 7)):
        cx = ox + s * sw + sw / 2
        cy = rnd.uniform(90, 220)
        up, dn = rnd.uniform(40, 62), rnd.uniform(40, 62)
        pts = [(cx + 2 * math.sin(i / 6.0), cy - i) for i in range(0, int(up))]
        body.append(line_path(pts, TEAL, 1.5))
        pts = [(cx + 2 * math.sin(i / 6.0), cy + i) for i in range(0, int(dn))]
        body.append(line_path(pts, TEAL, 1.5))
        if k % 3 == 0:
            side = 1 if rnd.random() < 0.5 else -1
            bend = [(cx + side * (j * 0.9), cy - up + 1 - j * 0.35) for j in range(0, 22)]
            body.append(line_path(bend, TEAL, 1.5))
            gx, gy = bend[-1]
            body.append(circle(gx, gy, 3, TEAL, TEAL))
        body.append(circle(cx, cy, 7, TEAL, TEAL))
    body.append(label(W - 14, H - 10, 'schematic: neurites aligning to patterned stripes', GREY, 10, 'end', italic=True))
    save('neuronal-substrates.svg', wrap(W, H, ''.join(body), 'Schematic of neurons growing along patterned polymer stripes'))


def fig_retinal_waves():
    W, H = 640, 300
    gx0, gy0, sp, cols, rows = 90, 52, 30, 16, 8
    ccx, ccy, R, th = 40, 290, 200, 30
    body = []
    for rr in (R, R - 70, R + 70):
        body.append(f'<path d="M{ccx},{ccy - rr} A{rr},{rr} 0 0 1 {ccx + rr},{ccy}" fill="none" '
                    f'stroke="{GREY}" stroke-width="1" stroke-dasharray="3 5"/>')
    for r in range(rows):
        for c in range(cols):
            x, y = gx0 + c * sp, gy0 + r * sp
            d = math.hypot(x - ccx, y - ccy)
            if R - th <= d <= R:
                body.append(circle(x, y, 6, TEAL, TEAL))
            elif d < R - th:
                body.append(circle(x, y, 4.5, LIGHT, TEAL, 1))
            else:
                body.append(circle(x, y, 4, '#ffffff', GREY, 1))
    body.append('<path d="M110,262 L190,214" stroke="#2b2f33" stroke-width="1.4" fill="none"/>')
    body.append('<path d="M180,212 L191,213.5 L186,223" stroke="#2b2f33" stroke-width="1.4" fill="none"/>')
    body.append(label(96, 282, 'propagation', INK, 10))
    body.append(label(gx0, 28, 'multi-electrode array', weight='bold'))
    body.append(label(W - 14, 28, 'active wave front', TEAL, 11, 'end', 'bold'))
    body.append(label(W - 14, H - 10, 'schematic: a retinal wave crossing an MEA', GREY, 10, 'end', italic=True))
    save('retinal-waves.svg', wrap(W, H, ''.join(body), 'Schematic of a retinal wave front crossing a multi-electrode array'))


def fig_toolkit():
    W, H = 640, 300
    body = [
        f'<circle cx="250" cy="150" r="104" fill="{TEAL}" fill-opacity="0.10" stroke="{TEAL}" stroke-width="1.4"/>',
        f'<circle cx="390" cy="150" r="104" fill="{GREY}" fill-opacity="0.14" stroke="{GREY}" stroke-width="1.4"/>',
        label(200, 62, 'experimental', INK, 13, 'middle', 'bold'),
        label(440, 62, 'computational', INK, 13, 'middle', 'bold'),
        label(190, 140, 'electrophysiology', INK, 11, 'middle'),
        label(190, 160, 'long-term recordings', INK, 11, 'middle'),
        label(190, 180, 'imaging', INK, 11, 'middle'),
        label(452, 140, 'dynamical systems', INK, 11, 'middle'),
        label(452, 160, 'signal processing', INK, 11, 'middle'),
        label(452, 180, 'machine learning', INK, 11, 'middle'),
        label(320, 146, 'systems', TEAL, 13, 'middle', 'bold'),
        label(320, 164, 'neuroscience', TEAL, 13, 'middle', 'bold'),
        label(W - 14, H - 10, 'a hybrid toolkit', GREY, 10, 'end', italic=True),
    ]
    save('toolkit.svg', wrap(W, H, ''.join(body), 'Venn diagram: experimental and computational approaches meet in systems neuroscience'))


def fig_scicomm():
    W, H = 640, 150
    rnd = random.Random(21)
    pts = []
    cols, rows = 16, 4
    for r in range(rows):
        for c in range(cols):
            pts.append((30 + c * 38 + rnd.uniform(-12, 12), 24 + r * 34 + rnd.uniform(-10, 10)))
    body = []
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            if d2 < 58 ** 2 and rnd.random() < 0.55:
                body.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                            f'stroke="{TEAL}" stroke-width="0.9" opacity="0.35"/>')
    for x, y in pts:
        hot = rnd.random() < 0.18
        body.append(circle(x, y, 3.6 if hot else 2.6, TEAL if hot else '#ffffff', TEAL, 1, 1 if hot else 0.7))
    save('scicomm.svg', wrap(W, H, ''.join(body), 'Abstract network of connected neurons'))


if __name__ == '__main__':
    fig_oscillations()
    fig_state_space()
    fig_memory_states()
    fig_silent_recall()
    fig_neuronal_substrates()
    fig_retinal_waves()
    fig_toolkit()
    fig_scicomm()