"""Generate the faint neuroscience background SVGs.

Run from the repo root:  python tools/make_decor.py
"""
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets', 'img')
TEAL = '#1f6f78'


def save(name, svg):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(svg)
    print('wrote', name)


def decor_wave():
    """Tiling oscillation used as the divider under section headings."""
    W, H = 96, 12
    pts = []
    for i in range(0, W + 1, 2):
        t = i / W
        y = 6 - 3.2 * math.sin(2 * math.pi * t * 2) * (0.35 + 0.65 * math.sin(math.pi * t) ** 2)
        pts.append((i, y))
    d = 'M' + ' L'.join(f'{x},{y:.2f}' for x, y in pts)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<path d="{d}" fill="none" stroke="{TEAL}" stroke-width="1.2" stroke-linecap="round" opacity="0.55"/></svg>')
    save('decor-wave.svg', svg)


def decor_network():
    """Faint branching dendrite-and-soma motif for the page background (top right)."""
    W, H = 520, 420
    rnd = random.Random(7)
    body = []
    somas = []

    def branch(x, y, ang, length, depth, width):
        if depth == 0 or length < 9:
            return
        x2 = x + length * math.cos(ang)
        y2 = y + length * math.sin(ang)
        bend = rnd.uniform(-0.35, 0.35)
        cx = (x + x2) / 2 + 10 * math.sin(ang + bend)
        cy = (y + y2) / 2 - 10 * math.cos(ang + bend)
        body.append(f'<path d="M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" '
                    f'stroke="{TEAL}" stroke-width="{width:.2f}" stroke-linecap="round"/>')
        if depth <= 2 and rnd.random() < 0.6:
            body.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="1.8" fill="{TEAL}"/>')
        n = 2 if rnd.random() < 0.8 else 3
        for k in range(n):
            branch(x2, y2, ang + rnd.uniform(-0.75, 0.75), length * rnd.uniform(0.62, 0.8), depth - 1, max(width * 0.75, 0.5))

    for sx, sy, base in [(500, 40, 2.3), (440, 150, 2.7), (510, 250, 2.9)]:
        somas.append((sx, sy))
        for k in range(4):
            branch(sx, sy, base + rnd.uniform(-0.9, 0.9), rnd.uniform(46, 66), 5, 1.4)
    for sx, sy in somas:
        body.append(f'<circle cx="{sx}" cy="{sy}" r="7" fill="{TEAL}" opacity="0.9"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" aria-hidden="true">'
           f'<g opacity="0.14">{"".join(body)}</g></svg>')
    save('decor-network.svg', svg)


def decor_traces():
    """Faint stacked EEG-like traces for the lower-left page background."""
    W, H = 520, 300
    rnd = random.Random(11)
    body = []
    for row in range(6):
        y0 = 30 + row * 46
        f1, f2 = rnd.uniform(0.018, 0.03), rnd.uniform(0.07, 0.11)
        a1, a2 = rnd.uniform(6, 10), rnd.uniform(2, 4)
        ph = rnd.uniform(0, 6)
        pts = [(x, y0 + a1 * math.sin(x * f1 * 2 * math.pi + ph) + a2 * math.sin(x * f2 * 2 * math.pi) + rnd.uniform(-0.8, 0.8))
               for x in range(0, W + 1, 4)]
        d = 'M' + ' L'.join(f'{x},{y:.1f}' for x, y in pts)
        body.append(f'<path d="{d}" fill="none" stroke="{TEAL}" stroke-width="1" stroke-linejoin="round"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(body)}</svg>')
    save('decor-traces.svg', svg)


if __name__ == '__main__':
    decor_wave()
    decor_network()
    decor_traces()