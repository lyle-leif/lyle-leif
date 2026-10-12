"""
Generates assets/header.svg and assets/footer.svg — animated galaxy banners
(nebula clouds, twinkling stars, shooting stars) behind your name.

Edit the text below, then run:  python scripts/build_galaxy.py
No dependencies. Pure SVG + SMIL, so it animates inside GitHub READMEs.
"""
import math
import random
from pathlib import Path
from html import escape

# ── What the banners say ──────────────────────────────────────────────
NAME = "Lyle Daniel"
TAGLINE = "CS Student · Aspiring Full-Stack and AI Engineer"
FOOTER = "thanks for stopping by · stay offline-ready"

# ── Galaxy palette ────────────────────────────────────────────────────
C = {
    "space": "#07020f", "deep": "#3c096c", "plum": "#5a189a", "violet": "#7b2cbf",
    "purple": "#9d4edd", "lav": "#c77dff", "star": "#e0aaff", "text": "#e6dcf5",
    "pink": "#ff5ccf", "blue": "#7aa2ff",
}
FONT = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
STAR_TINTS = ["#ffffff"] * 6 + [C["star"], C["star"], C["lav"], C["blue"], C["pink"]]


def defs(uid):
    return f'''
    <linearGradient id="{uid}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0a0318"/><stop offset="1" stop-color="{C["space"]}"/>
    </linearGradient>
    <linearGradient id="{uid}title" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.55" stop-color="{C["star"]}"/>
      <stop offset="1" stop-color="{C["lav"]}"/>
    </linearGradient>
    <filter id="{uid}cloud" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="38"/></filter>
    <filter id="{uid}glow" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feFlood flood-color="{C["violet"]}" flood-opacity="0.9"/><feComposite in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="{uid}spark" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="1.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <radialGradient id="{uid}planet" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="{C["lav"]}"/><stop offset="0.6" stop-color="{C["plum"]}"/><stop offset="1" stop-color="#1a0633"/>
    </radialGradient>'''


def nebula(w, h, rng, uid):
    clouds = [
        (0.32, 0.58, 0.28, 0.45, C["violet"], 0.42),
        (0.10, 0.85, 0.20, 0.40, C["deep"], 0.70),
        (0.70, 0.28, 0.20, 0.35, C["pink"], 0.20),
        (0.88, 0.78, 0.18, 0.35, C["blue"], 0.20),
        (0.58, 0.72, 0.22, 0.30, C["purple"], 0.22),
    ]
    out = []
    for fx, fy, frx, fry, col, op in clouds:
        dx, dy = rng.uniform(-40, 40), rng.uniform(-12, 12)
        dur = rng.uniform(16, 26)
        out.append(
            f'<ellipse cx="{fx * w:.0f}" cy="{fy * h:.0f}" rx="{frx * w:.0f}" ry="{fry * h:.0f}" fill="{col}" '
            f'opacity="{op}" filter="url(#{uid}cloud)">'
            f'<animate attributeName="opacity" values="{op};{op * 0.55:.2f};{op}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx:.0f} {dy:.0f};0 0" '
            f'dur="{dur * 1.4:.1f}s" repeatCount="indefinite"/></ellipse>'
        )
    return "".join(out)


def milky_way(w, h, rng):
    """A faint diagonal band of tiny, densely packed stars."""
    out = []
    angle = math.radians(-14)
    for _ in range(int(w * 0.18)):
        t = rng.uniform(-0.1, 1.1) * w
        spread = rng.gauss(0, h * 0.11)
        x = t * math.cos(angle) - spread * math.sin(angle)
        y = h * 0.62 + t * math.sin(angle) + spread * math.cos(angle)
        if 0 <= x <= w and 0 <= y <= h:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(0.25, 0.7):.2f}" fill="#ffffff" '
                       f'opacity="{rng.uniform(0.15, 0.5):.2f}"/>')
    return "".join(out)


def stars(w, h, n, rng, uid):
    out = []
    for _ in range(n):
        x, y = rng.uniform(4, w - 4), rng.uniform(4, h - 4)
        r = rng.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.3, 1.6])
        tint = rng.choice(STAR_TINTS)
        lo, hi = rng.uniform(0.1, 0.4), rng.uniform(0.75, 1.0)
        dur, begin = rng.uniform(2.0, 6.5), rng.uniform(0, 6)
        twinkle = (f'<animate attributeName="opacity" values="{hi:.2f};{lo:.2f};{hi:.2f}" dur="{dur:.1f}s" '
                   f'begin="{begin:.1f}s" repeatCount="indefinite"/>')
        if r >= 1.3:
            # Bright star: four-point sparkle with a soft glow.
            s = r * 4.2
            out.append(
                f'<g transform="translate({x:.1f} {y:.1f})" opacity="{hi:.2f}" filter="url(#{uid}spark)">{twinkle}'
                f'<path d="M0 {-s:.1f} Q0.9 -0.9 {s:.1f} 0 Q0.9 0.9 0 {s:.1f} Q-0.9 0.9 {-s:.1f} 0 Q-0.9 -0.9 0 {-s:.1f}Z" '
                f'fill="{tint}"/></g>'
            )
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{tint}" opacity="{hi:.2f}">{twinkle}</circle>')
    return "".join(out)


def shooting_star(x, y, dx, dy, period, begin, uid, k):
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    tx, ty = -ux * 90, -uy * 90
    return f'''
    <linearGradient id="{uid}trail{k}" gradientUnits="userSpaceOnUse" x1="{tx:.1f}" y1="{ty:.1f}" x2="0" y2="0">
      <stop offset="0" stop-color="{C["lav"]}" stop-opacity="0"/><stop offset="1" stop-color="#ffffff"/>
    </linearGradient>
    <g transform="translate({x} {y})"><g opacity="0">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.02;0.09;0.12;1" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;{dx} {dy};{dx} {dy}" keyTimes="0;0.12;1"
        dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>
      <line x1="{tx:.1f}" y1="{ty:.1f}" x2="0" y2="0" stroke="url(#{uid}trail{k})" stroke-width="1.6" stroke-linecap="round"/>
      <circle r="1.8" fill="#ffffff" filter="url(#{uid}spark)"/>
    </g></g>'''


def planet(cx, cy, r, uid, bob):
    return f'''
    <g><animateTransform attributeName="transform" type="translate" values="0 0;0 {bob};0 0" dur="7s" repeatCount="indefinite"/>
      <ellipse cx="{cx}" cy="{cy}" rx="{r * 2.1:.1f}" ry="{r * 0.55:.1f}" fill="none" stroke="{C["lav"]}" stroke-opacity="0.35"
        stroke-width="1.4" transform="rotate(-18 {cx} {cy})"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{uid}planet)"/>
      <path d="M{cx - r * 2.1:.1f} {cy} A{r * 2.1:.1f} {r * 0.55:.1f} 0 0 0 {cx + r * 2.1:.1f} {cy}" fill="none"
        stroke="{C["star"]}" stroke-opacity="0.55" stroke-width="1.4" transform="rotate(-18 {cx} {cy})"/>
    </g>'''


def scene(w, h, uid, seed, n_stars, body, shooters, planets=""):
    rng = random.Random(seed)
    sky = nebula(w, h, rng, uid) + milky_way(w, h, rng) + stars(w, h, n_stars, rng, uid)
    shoot_defs = "".join(shooting_star(*s, uid, k) for k, s in enumerate(shooters))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(NAME)} — galaxy banner">
  <defs>{defs(uid)}
    <clipPath id="{uid}card"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#{uid}card)">
    <rect width="{w}" height="{h}" fill="url(#{uid}sky)"/>
    {sky}
    {planets}
    {shoot_defs}
    {body}
  </g>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="17.5" fill="none" stroke="{C["violet"]}" stroke-opacity="0.55" stroke-width="1.5"/>
</svg>
'''


def header():
    w, h, uid = 900, 260, "h"
    body = f'''
    <g text-anchor="middle" font-family="{FONT}">
      <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="1.4s" fill="freeze"/>
        <text x="{w / 2}" y="142" font-size="68" font-weight="800" letter-spacing="2" fill="url(#{uid}title)" filter="url(#{uid}glow)">{escape(NAME)}</text>
      </g>
      <g opacity="0"><animate attributeName="opacity" from="0" to="0.92" begin="1.1s" dur="1.2s" fill="freeze"/>
        <line x1="{w / 2 - 210}" y1="166" x2="{w / 2 + 210}" y2="166" stroke="{C["lav"]}" stroke-opacity="0.35"/>
        <text x="{w / 2}" y="194" font-size="18" font-weight="600" letter-spacing="3" fill="{C["text"]}">{escape(TAGLINE.upper())}</text>
      </g>
    </g>'''
    planets = planet(790, 62, 16, uid, 5) + planet(96, 214, 7, uid, -3)
    shooters = [(140, 18, 420, 190, 7, 1.5), (520, 10, 300, 140, 9, 5.5)]
    return scene(w, h, uid, 7, 150, body, shooters, planets)


def footer():
    w, h, uid = 900, 120, "f"
    body = f'''
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="1.2s" fill="freeze"/>
      <text x="{w / 2}" y="68" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" letter-spacing="2"
        fill="url(#{uid}title)" filter="url(#{uid}glow)">{escape(FOOTER)}</text>
    </g>'''
    return scene(w, h, uid, 11, 70, body, [(60, 8, 380, 110, 8, 2.5)])


ASSETS = Path(__file__).resolve().parent.parent / "assets"

if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, svg in (("header.svg", header()), ("footer.svg", footer())):
        (ASSETS / name).write_text(svg, encoding="utf-8")
        print(f"wrote {ASSETS / name}  ({len(svg) // 1024} KB)")
