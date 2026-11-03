"""Builds assets/hero.svg: a lone ronin on a windswept hill before a red sun.

Pure SVG + SMIL so it animates inside GitHub's <img>. Seeded, so rebuilds are identical.
Run:  python scripts/build_hero.py
"""
import math
import random
from pathlib import Path

NAME = "LYLE DANIEL"
ROLE = "Aspiring Full-Stack & AI Engineer"
SUB = "CS STUDENT  ·  BATANGAS STATE UNIVERSITY"
SEAL = "LD"

W, H = 1200, 420
SUN = (885, 200, 172)            # cx, cy, r
HILL = ((200, 430), (700, 330), (1200, 212))   # quadratic bezier: start, control, end
RONIN_X = 838

BLADES = 300
EMBERS = 60
SHARDS = 22

INK = "#08080a"
PAPER = "#ece6dc"
RED = "#ff2f1f"
EMBER = ("#ff3b22", "#ff5a2c", "#ff7a3a", "#ffb070")
SERIF = "'Cormorant Garamond', 'Garamond', 'Georgia', 'Times New Roman', serif"
MONO = "'JetBrains Mono', 'Consolas', 'SFMono-Regular', 'Menlo', monospace"

ASSETS = Path(__file__).resolve().parent.parent / "assets"
rng = random.Random(7)


def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def hill_point(t):
    (x0, y0), (x1, y1), (x2, y2) = HILL
    u = 1 - t
    return u * u * x0 + 2 * u * t * x1 + t * t * x2, u * u * y0 + 2 * u * t * y1 + t * t * y2


def hill_y(x):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if hill_point(mid)[0] < x:
            lo = mid
        else:
            hi = mid
    return hill_point(lo)[1]


def in_sun(x, y):
    cx, cy, r = SUN
    return (x - cx) ** 2 + (y - cy) ** 2 < r * r


# ── sky, sun, hill ─────────────────────────────────────────────────────────
def backdrop():
    cx, cy, r = SUN
    (x0, y0), (x1, y1), (x2, y2) = HILL
    return f"""
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <ellipse cx="{cx}" cy="{cy + 40}" rx="520" ry="260" fill="url(#haze)"/>
  <circle cx="{cx}" cy="{cy}" r="{r * 1.75:.0f}" fill="url(#halo)">
    <animate attributeName="opacity" values=".75;1;.75" dur="7s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)"/>
  <path d="M-20,{H} L-20,388 Q260,350 560,372 T{W + 20},338 L{W + 20},{H} Z" fill="#100e12"/>
  <path d="M{x0},{y0} Q{x1},{y1} {x2},{y2} L{W + 20},{y2} L{W + 20},{H + 10} L{x0},{H + 10} Z" fill="{INK}"/>"""


# ── grass ──────────────────────────────────────────────────────────────────
def blade(x, y, h, lean, w):
    tip_x, tip_y = x + lean, y - h
    path = (f'<path d="M{f(x - w)},{f(y)} Q{f(x + lean * .25)},{f(y - h * .55)} {f(tip_x)},{f(tip_y)} '
            f'Q{f(x + lean * .3 + w * .6)},{f(y - h * .45)} {f(x + w)},{f(y)}Z"/>')
    if in_sun(tip_x, tip_y) and rng.random() < 0.5:   # sun-lit edge on the upper half only
        path += (f'<path d="M{f(x + lean * .12)},{f(y - h * .4)} Q{f(x + lean * .3)},{f(y - h * .6)} {f(tip_x)},{f(tip_y)}" '
                 f'fill="none" stroke="{RED}" stroke-opacity="{rng.uniform(.3, .6):.2f}" stroke-width=".8"/>')
    return path


def grass(front=False):
    """Blades in x-clusters; each cluster sways (skewX) around its own base line."""
    clusters = {}
    count = BLADES // 4 if front else BLADES
    for _ in range(count):
        if front:
            x = rng.uniform(RONIN_X - 70, RONIN_X + 90)
        else:
            x = rng.uniform(HILL[0][0] + 30, W + 10)
        reach = (x - HILL[0][0]) / (W - HILL[0][0])          # taller grass up the hill
        y = hill_y(x) + rng.uniform(-2, 22 if not front else 10)
        h = rng.uniform(14, 34 + 46 * reach) * (1.15 if front else 1)
        lean = -rng.uniform(.12, .45) * h                     # wind blows right → left
        clusters.setdefault(int(x // 70), []).append(blade(x, y, h, lean, rng.uniform(.9, 2.1)))

    out = []
    for key, blades in sorted(clusters.items()):
        bx = key * 70 + 35
        by = hill_y(min(max(bx, HILL[0][0]), W))
        dur = rng.uniform(2.8, 4.6)
        amp = rng.uniform(5, 10)
        out.append(
            f'<g transform="translate({bx},{f(by)})"><g>'
            f'<animateTransform attributeName="transform" type="skewX" '
            f'values="0;{f(amp)};{f(amp * .3)};{f(amp * 1.2)};0" keyTimes="0;.3;.5;.8;1" calcMode="spline" '
            f'keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1;.45 0 .55 1" '
            f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<g transform="translate({-bx},{f(-by)})">{"".join(blades)}</g></g></g>')
    return f'\n  <g fill="{INK}">' + "\n    ".join([""] + out) + "\n  </g>"


# ── the ronin ──────────────────────────────────────────────────────────────
CLOAK = [   # same command structure in every frame so SMIL can morph between them
    "M-13,-124 C-28,-116 -42,-106 -60,-103 L-49,-94 C-57,-86 -64,-80 -74,-77 C-57,-67 -42,-59 -24,-57 L-19,-88 Z",
    "M-13,-124 C-30,-120 -46,-114 -68,-114 L-55,-101 C-63,-94 -72,-90 -84,-88 C-62,-74 -45,-63 -25,-58 L-19,-88 Z",
    "M-13,-124 C-27,-114 -40,-102 -56,-96 L-46,-89 C-53,-80 -60,-73 -68,-68 C-54,-62 -40,-57 -23,-56 L-19,-88 Z",
]
TAIL = [
    "M-4,-133 Q-22,-128 -40,-136 Q-50,-140 -60,-134",
    "M-4,-133 Q-24,-134 -42,-146 Q-52,-150 -64,-148",
    "M-4,-133 Q-20,-124 -38,-128 Q-48,-130 -56,-122",
]


def ronin():
    x = RONIN_X
    y = hill_y(x) + 8
    cloak = ";".join(CLOAK + CLOAK[:1])
    tail = ";".join(TAIL + TAIL[:1])
    return f"""
  <g transform="translate({x},{f(y)}) scale(1.08)" fill="{INK}">
    <path d="{CLOAK[0]}"><animate attributeName="d" values="{cloak}" dur="2.6s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></path>
    <path d="{TAIL[0]}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"><animate attributeName="d" values="{tail}" dur="1.9s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></path>
    <path d="M-14,-129 C-22,-118 -22,-100 -19,-86 L-27,-22 L-23,0 L-7,0 L0,-32 L8,0 L27,0 L31,-18 L22,-86 C25,-101 23,-121 16,-129 Z"/>
    <rect x="-6" y="-138" width="13" height="12" rx="3"/>
    <path d="M-38,-134 L3,-163 L42,-134 Q3,-128 -38,-134 Z"/>
    <path d="M-44,-60 L38,-93" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>
    <path d="M-24,-67 L30,-88" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
    <path d="M19,-95 L23,-81" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
    <path d="M-2,-118 C8,-112 14,-100 16,-90" fill="none" stroke="#1a0606" stroke-width="1.2" opacity=".6"/>
  </g>"""


# ── wind: embers + grass shards ────────────────────────────────────────────
def embers(n, front):
    out = []
    for _ in range(n):
        x = rng.uniform(470, W + 20)
        y = hill_y(min(x, W)) - rng.uniform(0, 70)
        dx, dy = -rng.uniform(450, 1000), -rng.uniform(30, 220)
        c1 = (dx * .3, dy * .2 + rng.uniform(-40, 40))
        c2 = (dx * .7, dy * .8 + rng.uniform(-40, 40))
        dur = rng.uniform(7, 14)
        begin = -rng.uniform(0, dur)
        r = rng.uniform(1.1, 2.8) if front else rng.uniform(.7, 1.6)
        peak = rng.uniform(.7, 1) if front else rng.uniform(.35, .65)
        out.append(
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{r:.1f}" fill="{rng.choice(EMBER)}" opacity="0">'
            f'<animateMotion path="M0,0 C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(dx)},{f(dy)}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{peak:.2f};{peak * .8:.2f};0" keyTimes="0;.12;.7;1" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>')
    return "\n  <g>" + "\n    ".join([""] + out) + "\n  </g>"


def shards():
    out = []
    for _ in range(SHARDS):
        x = rng.uniform(760, W + 30)
        y = hill_y(min(x, W)) - rng.uniform(10, 140)
        dx, dy = -rng.uniform(300, 650), -rng.uniform(-30, 160)
        dur = rng.uniform(4, 8)
        s = rng.uniform(.7, 1.5)
        out.append(
            f'<path d="M{f(-5 * s)},0 L{f(5 * s)},{f(-1.4 * s)} L{f(-5 * s)},{f(1.6 * s)}Z" fill="{INK}" opacity="0">'
            f'<animateMotion path="M{f(x)},{f(y)} q{f(dx * .5)},{f(dy * .2 - 40)} {f(dx)},{f(dy)}" rotate="auto" '
            f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.95;.9;0" keyTimes="0;.1;.75;1" '
            f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/></path>')
    return "\n  <g>" + "\n    ".join([""] + out) + "\n  </g>"


# ── type ───────────────────────────────────────────────────────────────────
def title():
    x = 72
    return f"""
  <g>
    <g transform="translate({x},86)">
      <rect width="40" height="40" rx="3" fill="{RED}" opacity=".92"/>
      <rect x="3" y="3" width="34" height="34" rx="2" fill="none" stroke="#0b0b0d" stroke-opacity=".55" stroke-width="1.2"/>
      <text x="20" y="27.5" text-anchor="middle" font-family="{SERIF}" font-size="20" font-weight="700" fill="#0b0b0d">{SEAL}</text>
    </g>
    <text x="{x}" y="206" font-family="{SERIF}" font-size="66" font-weight="600" letter-spacing="9" fill="{PAPER}">{NAME}</text>
    <path d="M{x},232 H{x + 132}" stroke="{RED}" stroke-width="2.4"/>
    <path d="M{x + 140},232 l5,-5 l5,5 l-5,5 Z" fill="{RED}"/>
    <path d="M{x + 158},232 H{x + 190}" stroke="{RED}" stroke-width="1" stroke-opacity=".6"/>
    <text x="{x}" y="280" font-family="{SERIF}" font-size="31" font-style="italic" fill="{PAPER}" fill-opacity=".92">{ROLE.replace("&", "&amp;")}</text>
    <text x="{x}" y="318" font-family="{MONO}" font-size="15" letter-spacing="2.5" fill="#8f8a84">{SUB}</text>
  </g>"""


def defs():
    cx, cy, r = SUN
    return f"""
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0a0b0e"/><stop offset=".7" stop-color="#15141a"/><stop offset="1" stop-color="#1b1418"/>
    </linearGradient>
    <radialGradient id="haze">
      <stop offset="0" stop-color="#5a0d08" stop-opacity=".45"/><stop offset="1" stop-color="#5a0d08" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="halo">
      <stop offset=".5" stop-color="#ff2a18" stop-opacity=".55"/>
      <stop offset=".62" stop-color="#e01a0e" stop-opacity=".22"/>
      <stop offset="1" stop-color="#a00c06" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sun" cx=".5" cy=".62" r=".6" fx=".5" fy=".78">
      <stop offset="0" stop-color="#ff5a2e"/><stop offset=".55" stop-color="#ff2a1a"/><stop offset="1" stop-color="#d9140b"/>
    </radialGradient>
    <radialGradient id="vignette" cx=".5" cy=".5" r=".75">
      <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/>
    </radialGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>"""


def hero():
    body = "".join([
        backdrop(),
        embers(EMBERS // 3, front=False),
        grass(),
        ronin(),
        grass(front=True),
        shards(),
        embers(EMBERS - EMBERS // 3, front=True),
        f'\n  <rect width="{W}" height="{H}" fill="url(#vignette)"/>',
        title(),
    ])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{NAME.title()}, {ROLE.replace("&", "&amp;")}">'
            f'{defs()}\n  <g clip-path="url(#frame)">{body}\n  </g>\n</svg>\n')


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    print("wrote", ASSETS / "hero.svg")
