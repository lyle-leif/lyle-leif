"""Builds assets/about.svg: chapter 01, "The Path", in the hero's red-sun style.

Run:  python scripts/build_about.py
"""
import random

from theme import (ASSETS, DIM, MONO, PAPER, RED, SERIF, card, chapter, embers, esc, f, grass,
                   low_sun, quad_ground, rule)

INTRO = [                                   # line breaks are placed by hand
    "A Computer Science student at",
    "Batangas State University, walking",
    "the long road to Full-Stack and",
    "AI engineering, one step at a time.",
]
MOTTO = "understand it  →  test it  →  improve it"
ABOUT = [                                   # label, value, optional second line
    ("ORIGIN", "Batangas, Philippines", None),
    ("TRAINING", "BS Computer Science", "Batangas State University"),
    ("MISSION", "Aspiring Full-Stack & AI Engineer", None),
]

W, H = 1000, 316
UID = "ab"
SUN = (972, 322, 68)
GROUND = quad_ground((820, 318), (900, 300), (1010, 304))
rng = random.Random(11)


def in_sun(x, y):
    cx, cy, r = SUN
    return (x - cx) ** 2 + (y - cy) ** 2 < r * r


def intro():
    lines = "".join(
        f'\n  <text x="56" y="{142 + i * 33}" font-family="{SERIF}" font-size="25" font-style="italic" '
        f'fill="{PAPER}" fill-opacity=".92">{esc(line)}</text>' for i, line in enumerate(INTRO))
    return lines + (f'\n  <text x="56" y="{142 + len(INTRO) * 33 + 10}" font-family="{MONO}" font-size="13" '
                    f'letter-spacing="1.5" fill="{DIM}">{esc(MOTTO)}</text>')


def scroll():
    """Right column: diamond, small label, value (and an optional softer second line)."""
    x, y, out = 540, 122, []
    out.append(f'\n  <path d="M{x - 30},112 V286" stroke="{PAPER}" stroke-opacity=".1"/>'
               f'\n  <path d="M{x - 30},{199 - 5} l5,5 l-5,5 l-5,-5 Z" fill="{RED}" opacity=".8"/>')
    for label, value, extra in ABOUT:
        out.append(
            f'\n  <path d="M{x},{y + 18} l4.5,-4.5 l4.5,4.5 l-4.5,4.5 Z" fill="{RED}"/>'
            f'\n  <text x="{x + 20}" y="{y}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">{label}</text>'
            f'\n  <text x="{x + 20}" y="{y + 26}" font-family="{SERIF}" font-size="23" font-weight="600" fill="{PAPER}">{esc(value)}</text>')
        if extra:
            out.append(f'\n  <text x="{x + 20}" y="{y + 50}" font-family="{SERIF}" font-size="18" font-style="italic" '
                       f'fill="{PAPER}" fill-opacity=".62">{esc(extra)}</text>')
        y += 82 if extra else 60
    return "".join(out)


def scenery():
    cx, cy, r = SUN
    field = grass(rng, 70, lambda: rng.uniform(840, W + 10), lambda: rng.uniform(0, 8),
                  lambda x: rng.uniform(8, 30), GROUND, (820, W), lit=in_sun, amp=(8, 14))

    def start():
        return rng.uniform(880, W + 10), rng.uniform(250, 300)
    sparks = embers(rng, 22, start, False, travel=((300, 850), (20, 200)), life=(5, 10), size_back=(.8, 1.8))
    ground = f'\n  <path d="M820,318 Q900,300 1010,304 L1010,{H + 4} L820,{H + 4} Z" fill="#08080a"/>'
    return low_sun(UID, cx, cy, r, .8) + ground + field + sparks


def about():
    body = "".join([
        scenery(),
        chapter(56, 62, "01", "THE PATH"),
        rule(56, 84, W - 112),
        intro(),
        scroll(),
    ])
    label = (f"01 · The Path. {' '.join(INTRO)} "
             + "; ".join(f"{k.title()}: {v}{', ' + e if e else ''}" for k, v, e in ABOUT))
    return card(W, H, UID, body, label)


if __name__ == "__main__":
    (ASSETS / "about.svg").write_text(about(), encoding="utf-8")
    print("wrote", ASSETS / "about.svg")
