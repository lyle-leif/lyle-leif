"""Builds assets/stack.svg: chapter 02, "The Arsenal", wooden tags swinging on a rack before a red sun.

Run:  python scripts/build_stack.py
"""
import random

from theme import (ASSETS, DIM, EASE, INK, MONO, PAPER, RED, SERIF, card, chapter, embers, esc, f,
                   low_sun, rule)

STACK = [                                   # row label, tags
    ("LANGUAGES", ["Java", "Python", "C++", "JavaScript"]),
    ("WEB", ["React", "HTML", "CSS", "Node.js", "FastAPI"]),
    ("DATA", ["PostgreSQL", "SQLite"]),
    ("TOOLS", ["Git", "GitHub", "VS Code"]),
    ("AI TOOLS", ["Codex", "Claude Code"]),
]
HIGHLIGHT = "AI TOOLS"                      # this row's tags get a red glow

W = 1000
UID = "st"
ROW_TOP, ROW_GAP = 116, 60
RACK_X = (200, 944)
SUN = (872, 238, 92)
H = ROW_TOP + ROW_GAP * (len(STACK) - 1) + 70
rng = random.Random(23)


def katana(x, y, length):
    """Sheathed sword lying along the header: scabbard, guard, cord-wrapped grip."""
    grip = 66
    wraps = "".join(f'<path d="M{x + 9 + i * 10},{y - 3.5} l3.5,3.5 l-3.5,3.5 l-3.5,-3.5 Z" fill="#3a1412" '
                    f'stroke="{RED}" stroke-width=".9" stroke-opacity=".8"/>' for i in range(6))
    return (f'\n  <g>'
            f'<rect x="{x}" y="{y - 4.5}" width="{grip}" height="9" rx="3" fill="#1a1416" stroke="{PAPER}" stroke-opacity=".25"/>{wraps}'
            f'<ellipse cx="{x + grip + 4}" cy="{y}" rx="3.5" ry="10" fill="#1a1416" stroke="{PAPER}" stroke-opacity=".35"/>'
            f'<path d="M{x + grip + 9},{y - 4} H{x + length - 8} Q{x + length},{y - 4} {x + length + 2},{y + 1} '
            f'Q{x + length},{y + 4} {x + length - 8},{y + 4} H{x + grip + 9} Z" fill="#100d10" stroke="{PAPER}" stroke-opacity=".25"/>'
            f'<path d="M{x + grip + 30},{y - 4} v8 M{x + grip + 38},{y - 4} v8" stroke="{RED}" stroke-width="1.6" stroke-opacity=".8"/>'
            f'</g>')


def tag(x, y, name, hot):
    """One hanging tag; it swings around the peg at (x + width/2, y)."""
    width = round(len(name) * 10.2 + 34)
    peg = x + width / 2
    top = y + 12
    fill, stroke = ("#21100f", RED) if hot else ("#141218", PAPER)
    stroke_op = ".8" if hot else ".28"
    dur = rng.uniform(2.6, 4.2)
    swing = rng.uniform(2.5, 4.5)
    glow = (f'<rect x="{x - 4}" y="{top - 4}" width="{width + 8}" height="42" rx="8" fill="{RED}" opacity=".22" filter="url(#{UID}blur)"/>'
            if hot else "")
    return (f'\n  <g transform="translate({f(peg)},{y})"><g>'
            f'<animateTransform attributeName="transform" type="rotate" values="{f(-swing)};{f(swing)};{f(-swing)}" '
            f'keyTimes="0;.5;1" calcMode="spline" keySplines="{EASE};{EASE}" dur="{dur:.1f}s" '
            f'begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<g transform="translate({f(-peg)},{-y})">'
            f'<path d="M{f(peg)},{y} L{x + 10},{top} M{f(peg)},{y} L{x + width - 10},{top}" stroke="{RED}" stroke-width="1.2" stroke-opacity=".7"/>'
            f'{glow}<rect x="{x}" y="{top}" width="{width}" height="34" rx="5" fill="{fill}" stroke="{stroke}" stroke-opacity="{stroke_op}"/>'
            f'<text x="{f(peg)}" y="{top + 23}" text-anchor="middle" font-family="{SERIF}" font-size="19" font-weight="600" '
            f'fill="{PAPER}">{esc(name)}</text>'
            f'<circle cx="{f(peg)}" cy="{y}" r="2.4" fill="{PAPER}" opacity=".6"/>'
            f'</g></g></g>')


def rack():
    out = []
    for i, (label, names) in enumerate(STACK):
        y = ROW_TOP + i * ROW_GAP
        out.append(f'\n  <text x="56" y="{y + 34}" font-family="{MONO}" font-size="12" letter-spacing="3" '
                   f'fill="{RED if label == HIGHLIGHT else DIM}">{label}</text>'
                   f'\n  <path d="M{RACK_X[0]},{y} H{RACK_X[1]}" stroke="{INK}" stroke-width="3"/>'
                   f'\n  <path d="M{RACK_X[0]},{y - 1.5} H{RACK_X[1]}" stroke="{PAPER}" stroke-opacity=".14"/>')
        x = RACK_X[0] + 14
        for name in names:
            out.append(tag(x, y, name, label == HIGHLIGHT))
            x += round(len(name) * 10.2 + 34) + 14
    return "".join(out)


def stack():
    cx, cy, r = SUN

    def start():
        return rng.uniform(cx - 40, W + 10), rng.uniform(cy, H)
    sparks = embers(rng, 24, start, False, travel=((350, 900), (30, 220)), life=(5, 10), size_back=(.8, 1.9))
    body = "".join([
        f'\n  <defs><filter id="{UID}blur" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="5"/></filter></defs>',
        low_sun(UID, cx, cy, r, .8),
        sparks,
        chapter(56, 62, "02", "THE ARSENAL"),
        katana(640, 56, 304),
        rule(56, 84, W - 112),
        rack(),
    ])
    label = "02 · The Arsenal. " + "; ".join(f"{k.title()}: {', '.join(v)}" for k, v in STACK)
    return card(W, H, UID, body, label)


if __name__ == "__main__":
    (ASSETS / "stack.svg").write_text(stack(), encoding="utf-8")
    print("wrote", ASSETS / "stack.svg")
