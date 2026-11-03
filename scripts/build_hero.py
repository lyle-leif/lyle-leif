"""Builds assets/hero.svg: a lone ronin on a windswept hill before a red sun.

Every 9 seconds he draws and cuts: one stroke splits the sun, sparks fly, the camera shakes.

Pure SVG + SMIL so it animates inside GitHub's <img>. Seeded, so rebuilds are identical.
Run:  python scripts/build_hero.py
"""
import math
import random

from theme import ASSETS, EMBER, INK, MONO, PAPER, RED, SERIF, embers, f, grass, group, quad_ground

NAME = "LYLE DANIEL"
ROLE = "Aspiring Full-Stack & AI Engineer"
SUB = "CS STUDENT  ·  BATANGAS STATE UNIVERSITY"
SEAL = "LD"

W, H = 1200, 420
SUN = (885, 200, 172)            # cx, cy, r
HILL = ((200, 430), (700, 330), (1200, 212))   # quadratic bezier: start, control, end
RONIN_X = 838

BLADES = 300
EMBERS = 90
SHARDS = 30
LEAVES = 14
STREAKS = 6

LOOP = 9.0                          # the slash cycle, seconds
SLASH_AT = 5.6                      # blade leaves the scabbard
CUT = ((735, 345), (1050, 60))      # the cut line across the sun
HAND = (30, -94)                    # sword hand, in the ronin's own coordinates

rng = random.Random(7)
hill_y = quad_ground(*HILL)


def in_sun(x, y):
    cx, cy, r = SUN
    return (x - cx) ** 2 + (y - cy) ** 2 < r * r


# ── the slash timeline ─────────────────────────────────────────────────────
def at(sec):
    return f"{sec / LOOP:.4f}"


def keyframes(attr, frames, kind=None, mode=None):
    """One SMIL element on the shared slash loop. frames: [(seconds, value), ...]."""
    frames = list(frames)
    if frames[0][0] > 0:
        frames.insert(0, (0, frames[0][1]))
    if frames[-1][0] < LOOP:
        frames.append((LOOP, frames[-1][1]))
    values = ";".join(str(v) for _, v in frames)
    times = ";".join(at(t) for t, _ in frames)
    tag = f'animateTransform attributeName="transform" type="{kind}"' if kind else f'animate attributeName="{attr}"'
    calc = f' calcMode="{mode}"' if mode else ""
    return f'<{tag} values="{values}" keyTimes="{times}"{calc} dur="{LOOP:g}s" repeatCount="indefinite"/>'


def show(frames):
    """Discrete visibility switch: [(seconds, 0|1), ...]."""
    return keyframes("opacity", frames, mode="discrete")


def cut_frame():
    """Unit direction along the cut (P1 → P2) and the normal pointing to its upper-left side."""
    (x1, y1), (x2, y2) = CUT
    length = math.hypot(x2 - x1, y2 - y1)
    d = ((x2 - x1) / length, (y2 - y1) / length)
    return d, (d[1], -d[0])


def half_plane(sign):
    (x1, y1), (x2, y2) = CUT
    (dx, dy), (nx, ny) = cut_frame()
    a = (x1 - dx * 600, y1 - dy * 600)
    b = (x2 + dx * 600, y2 + dy * 600)
    far = 1200 * sign
    pts = [a, b, (b[0] + nx * far, b[1] + ny * far), (a[0] + nx * far, a[1] + ny * far)]
    return " ".join(f"{f(px)},{f(py)}" for px, py in pts)


# ── sky, sun, hill ─────────────────────────────────────────────────────────
def backdrop():
    cx, cy, r = SUN
    (x0, y0), (x1, y1), (x2, y2) = HILL
    cut, heal = SLASH_AT + .1, SLASH_AT + 2.65
    (dx, dy), _ = cut_frame()
    slide = f"{f(-dx * 13)} {f(-dy * 13)}"          # top half slips down along the cut
    return f"""
  <rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="url(#sky)"/>
  <ellipse cx="{cx}" cy="{cy + 40}" rx="520" ry="260" fill="url(#haze)"/>
  <circle cx="{cx}" cy="{cy}" r="{r * 1.75:.0f}" fill="url(#halo)">
    <animate attributeName="opacity" values=".6;1;.6" dur="5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)">{show([(0, 1), (cut, 0), (heal, 1)])}</circle>
  <g opacity="0">{show([(0, 0), (cut, 1), (heal, 0)])}
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)" clip-path="url(#sunLow)"/>
    <g>{keyframes("", [(cut, "0 0"), (cut + .25, slide), (cut + 1, slide), (heal - .05, "0 0")], kind="translate")}
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)" clip-path="url(#sunHigh)"/>
    </g>
  </g>
  <path d="M-20,{H + 20} L-20,388 Q260,350 560,372 T{W + 20},338 L{W + 20},{H + 20} Z" fill="#100e12"/>
  <path d="M{x0},{y0} Q{x1},{y1} {x2},{y2} L{W + 20},{y2} L{W + 20},{H + 20} L{x0},{H + 20} Z" fill="{INK}"/>"""


# ── grass ──────────────────────────────────────────────────────────────────
def hill_grass(front=False):
    def pick_x():
        return rng.uniform(RONIN_X - 70, RONIN_X + 90) if front else rng.uniform(HILL[0][0] + 30, W + 10)

    def pick_height(x):
        reach = (x - HILL[0][0]) / (W - HILL[0][0])          # taller grass up the hill
        return rng.uniform(14, 34 + 46 * reach) * (1.15 if front else 1)

    return grass(rng, BLADES // 4 if front else BLADES, pick_x,
                 lambda: rng.uniform(-2, 22 if not front else 10), pick_height,
                 hill_y, (HILL[0][0], W), lit=in_sun)


# ── the ronin ──────────────────────────────────────────────────────────────
CLOAK = [   # same command structure in every frame so SMIL can morph between them
    "M-13,-124 C-28,-116 -42,-106 -60,-103 L-49,-94 C-57,-86 -64,-80 -74,-77 C-57,-67 -42,-59 -24,-57 L-19,-88 Z",
    "M-13,-124 C-32,-124 -50,-120 -76,-122 L-60,-106 C-70,-100 -80,-98 -94,-98 C-66,-78 -45,-63 -25,-58 L-19,-88 Z",
    "M-13,-124 C-27,-114 -40,-102 -56,-96 L-46,-89 C-53,-80 -60,-73 -68,-68 C-54,-62 -40,-57 -23,-56 L-19,-88 Z",
]
TAIL = [
    "M-4,-133 Q-22,-128 -40,-136 Q-50,-140 -60,-134",
    "M-4,-133 Q-26,-138 -44,-152 Q-56,-158 -70,-156",
    "M-4,-133 Q-20,-124 -38,-128 Q-48,-130 -56,-122",
]


def ronin():
    x = RONIN_X
    y = hill_y(x) + 8
    cloak = ";".join(CLOAK + CLOAK[:1])
    tail = ";".join(TAIL + TAIL[:1])
    sheathed = SLASH_AT + 2.72
    # blade angle (deg, clockwise from pointing right): rising cut, overshoot, chiburi, back into the scabbard
    blade_arc = [(SLASH_AT, 30), (SLASH_AT + .07, -75), (SLASH_AT + .14, -98), (SLASH_AT + .6, -88),
                 (SLASH_AT + 1, 32), (SLASH_AT + 2.6, 32), (sheathed, 150)]
    return f"""
  <g transform="translate({x},{f(y)}) scale(1.08)" fill="{INK}">
   <g>{keyframes("", [(SLASH_AT, "0 0"), (SLASH_AT + .06, "9 0"), (SLASH_AT + 2.6, "9 0"), (SLASH_AT + 3, "0 0")], kind="translate")}
   <g>{keyframes("", [(SLASH_AT - .4, "1 1"), (SLASH_AT - .15, "1.025 .97"), (SLASH_AT, "1.025 .97"), (SLASH_AT + .08, "1 1.01"), (SLASH_AT + .3, "1 1")], kind="scale")}
    <path d="{CLOAK[0]}"><animate attributeName="d" values="{cloak}" dur="1.4s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></path>
    <path d="{TAIL[0]}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"><animate attributeName="d" values="{tail}" dur="1.1s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></path>
    <path d="M-14,-129 C-22,-118 -22,-100 -19,-86 L-27,-22 L-23,0 L-7,0 L0,-32 L8,0 L27,0 L31,-18 L22,-86 C25,-101 23,-121 16,-129 Z"/>
    <rect x="-6" y="-138" width="13" height="12" rx="3"/>
    <path d="M-38,-134 L3,-163 L42,-134 Q3,-128 -38,-134 Z"/>
    <path d="M-44,-60 L21,-86.2" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>
    <path d="M-24,-67 L30,-88" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>
    <g>{show([(0, 1), (SLASH_AT, 0), (sheathed, 1)])}
      <path d="M21,-86.2 L38,-93" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>
      <path d="M19,-95 L23,-81" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
    </g>
    <path d="M-2,-118 C8,-112 14,-100 16,-90" fill="none" stroke="#1a0606" stroke-width="1.2" opacity=".6"/>
    <g opacity="0">{show([(0, 0), (SLASH_AT, 1), (sheathed, 0)])}
      <path d="M4,-120 Q20,-110 {HAND[0]},{HAND[1]}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
      <g transform="translate({HAND[0]},{HAND[1]})"><g>{keyframes("", blade_arc, kind="rotate")}
        <path d="M-15,0 L0,0" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>
        <path d="M1,-5 L1,5" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
        <path d="M2,-1.8 Q50,-4.5 97,-8.5 Q52,-.5 2,1.8 Z"/>
        <path d="M4,1.2 Q52,-1.4 96,-8" fill="none" stroke="#ffe6d6" stroke-width=".9" stroke-opacity=".85"/>
        <circle r="4.2"/>
      </g></g>
    </g>
    {glint(37, -93, SLASH_AT - .45, 1.4)}
    {glint(21, -86, sheathed, 1)}
   </g>
   </g>
  </g>"""


def glint(x, y, sec, size):
    """A four-point star that flashes for a split second."""
    return (f'<g transform="translate({x},{y})"><g>'
            f'{keyframes("", [(sec - .01, "0"), (sec + .12, f(size)), (sec + .3, "0")], kind="scale")}'
            f'<path d="M0,-8 L1.3,-1.3 L8,0 L1.3,1.3 L0,8 L-1.3,1.3 L-8,0 L-1.3,-1.3Z" fill="#fff"/></g></g>')


# ── the cut ────────────────────────────────────────────────────────────────
def slash():
    (x1, y1), (x2, y2) = CUT
    (dx, dy), (nx, ny) = cut_frame()
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    hit = SLASH_AT + .1

    def bow(amount):                                      # control point bulging to the lower-right
        return f"{f(mx - nx * amount)},{f(my - ny * amount)}"

    line = f"M{x1},{y1} Q{bow(120)} {x2},{y2}"
    trail_vis = [(SLASH_AT - .01, 0), (SLASH_AT, 1), (SLASH_AT + .25, 1), (SLASH_AT + .9, 0)]
    draw = [(SLASH_AT, 1), (SLASH_AT + .09, 0)]
    out = [
        # crescent flare that blooms behind the stroke, then cools
        f'<path d="M{x1},{y1} Q{bow(185)} {x2},{y2} Q{bow(70)} {x1},{y1}Z" fill="{RED}" filter="url(#blur)" opacity="0">'
        f'{keyframes("opacity", [(hit - .02, 0), (hit + .02, .75), (SLASH_AT + 1.4, 0)])}</path>',
        f'<path d="M{x1},{y1} Q{bow(150)} {x2},{y2} Q{bow(100)} {x1},{y1}Z" fill="#fff3ea" opacity="0">'
        f'{keyframes("opacity", [(hit - .02, 0), (hit, .95), (hit + .3, .4), (SLASH_AT + 1.2, 0)])}</path>',
        # the stroke itself rips across in 90 ms
        f'<path d="{line}" fill="none" stroke="{RED}" stroke-width="12" filter="url(#blur)" pathLength="1" '
        f'stroke-dasharray="1 1" stroke-dashoffset="1" opacity="0">'
        f'{keyframes("stroke-dashoffset", draw)}{keyframes("opacity", trail_vis)}</path>',
        f'<path d="{line}" fill="none" stroke="#fff8f2" stroke-width="3.2" stroke-linecap="round" pathLength="1" '
        f'stroke-dasharray="1 1" stroke-dashoffset="1" opacity="0">'
        f'{keyframes("stroke-dashoffset", draw)}{keyframes("opacity", trail_vis)}</path>',
        # glowing seam where the sun was split
        f'<g clip-path="url(#sunDisc)" opacity="0">{keyframes("opacity", [(hit, 0), (hit + .04, 1), (SLASH_AT + 1, .8), (SLASH_AT + 2.6, 0)])}'
        f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{RED}" stroke-width="9" filter="url(#blur)"/>'
        f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#ffd9c6" stroke-width="2"/></g>',
    ]
    # sparks thrown off along the cut
    for _ in range(16):
        t = rng.uniform(.2, .85)
        sx, sy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        side = rng.choice((-1, 1))
        reach = rng.uniform(50, 150)
        along = rng.uniform(-70, 70)
        ex, ey = nx * side * reach + dx * along, ny * side * reach + dy * along + rng.uniform(0, 40)
        out.append(
            f'<path d="M-9,0 L1,0" stroke="{rng.choice(EMBER[:3] + ("#fff1e0",))}" stroke-width="{rng.uniform(1.4, 2.6):.1f}" '
            f'stroke-linecap="round" opacity="0">'
            f'<animateMotion path="M{f(sx)},{f(sy)} l{f(ex)},{f(ey)}" rotate="auto" keyPoints="0;0;1;1" '
            f'keyTimes="0;{at(hit)};{at(hit + rng.uniform(.4, .7))};1" calcMode="linear" dur="{LOOP:g}s" repeatCount="indefinite"/>'
            f'{keyframes("opacity", [(hit - .01, 0), (hit + .01, 1), (hit + .3, .8), (hit + .7, 0)])}</path>')
    # grass tips cut loose near his feet
    for _ in range(9):
        gx = rng.uniform(RONIN_X - 50, RONIN_X + 80)
        gy = hill_y(gx) - rng.uniform(18, 45)
        fx, fy = -rng.uniform(40, 170), rng.uniform(-40, 30)
        lift = rng.uniform(60, 120)
        s = rng.uniform(.8, 1.3)
        out.append(
            f'<g opacity="0"><animateMotion path="M{f(gx)},{f(gy)} q{f(fx * .4)},{f(-lift)} {f(fx)},{f(fy)}" '
            f'keyPoints="0;0;1;1" keyTimes="0;{at(hit + .02)};{at(hit + 1.3)};1" calcMode="linear" dur="{LOOP:g}s" repeatCount="indefinite"/>'
            f'{keyframes("opacity", [(hit, 0), (hit + .03, 1), (hit + .9, 1), (hit + 1.3, 0)])}'
            f'<g><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{rng.uniform(.4, .8):.2f}s" repeatCount="indefinite"/>'
            f'<path d="M0,0 L{f(16 * s)},{f(-2.5 * s)} L0,{f(3 * s)}Z" fill="{INK}"/></g></g>')
    # white flash on impact
    out.append(f'<rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="#ffe4d8" opacity="0">'
               f'{keyframes("opacity", [(hit - .01, 0), (hit + .02, .26), (hit + .25, 0)])}</rect>')
    return group(out)


def shake():
    hit = SLASH_AT + .1
    jolts = ["0 0", "7 -4", "-6 4", "4 -3", "-3 2", "1 -1", "0 0"]
    return keyframes("", [(hit + i * .04, j) for i, j in enumerate(jolts)], kind="translate")


# ── wind: embers + grass shards ────────────────────────────────────────────
def hill_embers(n, front):
    def start():
        x = rng.uniform(470, W + 20)
        return x, hill_y(min(x, W)) - rng.uniform(0, 70)
    return embers(rng, n, start, front)


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


def leaves():
    """Red leaves tumbling on the wind."""
    out = []
    for _ in range(LEAVES):
        x = rng.uniform(700, W + 40)
        y = hill_y(min(x, W)) - rng.uniform(0, 160)
        dx, dy = -rng.uniform(600, 1150), -rng.uniform(-20, 200)
        dur = rng.uniform(5, 9)
        begin = -rng.uniform(0, dur)
        s = rng.uniform(.8, 1.4)
        spin = rng.uniform(.8, 1.8)
        out.append(
            f'<g opacity="0">'
            f'<animateMotion path="M{f(x)},{f(y)} c{f(dx * .3)},{f(rng.uniform(-60, 40))} {f(dx * .6)},{f(dy * .5 + rng.uniform(-50, 50))} {f(dx)},{f(dy)}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.95;.85;0" keyTimes="0;.1;.8;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<g><animateTransform attributeName="transform" type="rotate" values="0;360" dur="{spin:.1f}s" repeatCount="indefinite"/>'
            f'<path d="M{f(-5 * s)},0 C{f(-2 * s)},{f(-3.5 * s)} {f(3 * s)},{f(-3.5 * s)} {f(6 * s)},0 C{f(3 * s)},{f(3 * s)} {f(-2 * s)},{f(3 * s)} {f(-5 * s)},0Z" '
            f'fill="{rng.choice(EMBER[:3])}"/></g></g>')
    return "\n  <g>" + "\n    ".join([""] + out) + "\n  </g>"


def streaks():
    """Faint wind lines that whip across the sky every few seconds."""
    out = []
    for _ in range(STREAKS):
        x = rng.uniform(700, 1150)
        y = rng.uniform(40, 260)
        length = rng.uniform(90, 200)
        dur = rng.uniform(4, 7)
        begin = -rng.uniform(0, dur)
        out.append(
            f'<path d="M0,0 h{f(length)}" stroke="{PAPER}" stroke-width="1" stroke-linecap="round" opacity="0">'
            f'<animateMotion path="M{f(x)},{f(y)} q-250,-14 -560,6" keyPoints="0;1;1" keyTimes="0;.3;1" calcMode="linear" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.22;0;0" keyTimes="0;.12;.3;1" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></path>')
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
    <clipPath id="sunHigh"><polygon points="{half_plane(1)}"/></clipPath>
    <clipPath id="sunLow"><polygon points="{half_plane(-1)}"/></clipPath>
    <clipPath id="sunDisc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
    <filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
  </defs>"""


def hero():
    scene = "".join([
        backdrop(),
        streaks(),
        hill_embers(EMBERS // 3, front=False),
        hill_grass(),
        ronin(),
        hill_grass(front=True),
        shards(),
        leaves(),
        hill_embers(EMBERS - EMBERS // 3, front=True),
        slash(),
    ])
    body = (f'\n  <g>{shake()}{scene}\n  </g>'
            f'\n  <rect width="{W}" height="{H}" fill="url(#vignette)"/>' + title())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{NAME.title()}, {ROLE.replace("&", "&amp;")}">'
            f'{defs()}\n  <g clip-path="url(#frame)">{body}\n  </g>\n</svg>\n')


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(hero(), encoding="utf-8")
    print("wrote", ASSETS / "hero.svg")
