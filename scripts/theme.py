"""Shared look for every README card: palette, type, and the wind-blown grass + embers.

Everything takes the caller's own random.Random, so each card stays seeded and reproducible.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG = "#0c0d11"
INK = "#08080a"
PAPER = "#ece6dc"
DIM = "#8f8a84"
RED = "#ff2f1f"
EMBER = ("#ff3b22", "#ff5a2c", "#ff7a3a", "#ffb070")
SERIF = "'Cormorant Garamond', 'Garamond', 'Georgia', 'Times New Roman', serif"
MONO = "'JetBrains Mono', 'Consolas', 'SFMono-Regular', 'Menlo', monospace"
EASE = ".45 0 .55 1"


def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def group(items):
    return "\n  <g>" + "\n    ".join([""] + items) + "\n  </g>"


def quad_ground(p0, p1, p2):
    """y(x) along a quadratic bezier ground line."""
    def point(t):
        u = 1 - t
        return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])

    def y_at(x):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if point(mid)[0] < x:
                lo = mid
            else:
                hi = mid
        return point(lo)[1]
    return y_at


# ── grass ──────────────────────────────────────────────────────────────────
def blade(rng, x, y, h, lean, w, lit):
    tip_x, tip_y = x + lean, y - h
    path = (f'<path d="M{f(x - w)},{f(y)} Q{f(x + lean * .25)},{f(y - h * .55)} {f(tip_x)},{f(tip_y)} '
            f'Q{f(x + lean * .3 + w * .6)},{f(y - h * .45)} {f(x + w)},{f(y)}Z"/>')
    if lit(tip_x, tip_y) and rng.random() < 0.5:   # sun-lit edge on the upper half only
        path += (f'<path d="M{f(x + lean * .12)},{f(y - h * .4)} Q{f(x + lean * .3)},{f(y - h * .6)} {f(tip_x)},{f(tip_y)}" '
                 f'fill="none" stroke="{RED}" stroke-opacity="{rng.uniform(.3, .6):.2f}" stroke-width=".8"/>')
    return path


def grass(rng, count, pick_x, pick_base, pick_height, ground_y, x_range,
          lit=lambda x, y: False, sway=(1.8, 3.2), amp=(10, 18), cluster=70):
    """Blades in x-clusters; each cluster sways (skewX) around its own base line, leaning right → left."""
    clusters = {}
    for _ in range(count):
        x = pick_x()
        y = ground_y(x) + pick_base()
        h = pick_height(x)
        lean = -rng.uniform(.12, .45) * h
        clusters.setdefault(int(x // cluster), []).append(blade(rng, x, y, h, lean, rng.uniform(.9, 2.1), lit))

    out = []
    for key, blades in sorted(clusters.items()):
        bx = key * cluster + cluster // 2
        by = ground_y(min(max(bx, x_range[0]), x_range[1]))
        dur = rng.uniform(*sway)
        a = rng.uniform(*amp)
        out.append(
            f'<g transform="translate({bx},{f(by)})"><g>'
            f'<animateTransform attributeName="transform" type="skewX" '
            f'values="0;{f(a)};{f(a * .3)};{f(a * 1.6)};{f(a * .5)};0" keyTimes="0;.25;.45;.7;.85;1" calcMode="spline" '
            f'keySplines="{";".join([EASE] * 5)}" '
            f'dur="{dur:.1f}s" begin="-{rng.uniform(0, dur):.1f}s" repeatCount="indefinite"/>'
            f'<g transform="translate({-bx},{f(-by)})">{"".join(blades)}</g></g></g>')
    return f'\n  <g fill="{INK}">' + "\n    ".join([""] + out) + "\n  </g>"


# ── embers ─────────────────────────────────────────────────────────────────
def embers(rng, n, pick_start, front, travel=((450, 1000), (30, 220)), life=(4, 9),
           size_front=(1.6, 4), size_back=(1, 2)):
    """Sparks drifting right → left and upward, fading in and out on staggered loops."""
    out = []
    for _ in range(n):
        x, y = pick_start()
        dx, dy = -rng.uniform(*travel[0]), -rng.uniform(*travel[1])
        c1 = (dx * .3, dy * .2 + rng.uniform(-40, 40))
        c2 = (dx * .7, dy * .8 + rng.uniform(-40, 40))
        dur = rng.uniform(*life)
        begin = -rng.uniform(0, dur)
        r = rng.uniform(*size_front) if front else rng.uniform(*size_back)
        peak = rng.uniform(.75, 1) if front else rng.uniform(.4, .7)
        colour = rng.choice(EMBER)
        glow = (f'<circle r="{r * 2.4:.1f}" fill="{RED}" opacity=".18"/>'   # halo only on the big ones
                if front and r > 3 else "")
        out.append(
            f'<g transform="translate({f(x)},{f(y)})"><g opacity="0">'
            f'<animateMotion path="M0,0 C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(dx)},{f(dy)}" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{peak:.2f};{peak * .8:.2f};0" keyTimes="0;.12;.7;1" '
            f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/>'
            f'{glow}<circle r="{r:.1f}" fill="{colour}">'
            f'<animate attributeName="opacity" values="1;.45;1;.7;1" dur="{rng.uniform(.5, 1.1):.2f}s" repeatCount="indefinite"/>'
            f'</circle></g></g>')
    return group(out)


# ── card chrome ────────────────────────────────────────────────────────────
def chapter(x, y, number, title):
    """'01 ── THE PATH' style heading used by every section card."""
    return (f'\n  <text x="{x}" y="{y}" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{RED}">{number}</text>'
            f'\n  <text x="{x + 44}" y="{y + 1}" font-family="{SERIF}" font-size="30" font-weight="600" '
            f'letter-spacing="7" fill="{PAPER}">{esc(title)}</text>')


def card(w, h, uid, body, label):
    """Rounded dark panel with a faint warm glow, matching the hero's frame."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}">'
            f'\n  <defs>'
            f'\n    <linearGradient id="{uid}bg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#0a0b0e"/><stop offset="1" stop-color="#16141a"/></linearGradient>'
            f'\n    <radialGradient id="{uid}vg" cx=".5" cy=".5" r=".75">'
            f'<stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>'
            f'\n    <clipPath id="{uid}clip"><rect width="{w}" height="{h}" rx="14"/></clipPath>'
            f'\n  </defs>'
            f'\n  <g clip-path="url(#{uid}clip)">'
            f'\n  <rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>'
            f'{body}'
            f'\n  </g>'
            f'\n  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="#2a1614" stroke-width="1"/>'
            f'\n</svg>\n')
