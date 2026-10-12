"""
Generates assets/features.svg (OFFGRID feature grid) and assets/quests.svg
(animated quest board) in the same galaxy style as the header.

Edit FEATURES / QUESTS below, then run:  python scripts/build_cards.py
No dependencies. Pure SVG + SMIL, so it animates inside GitHub READMEs.
"""
import random
from html import escape

from build_galaxy import ASSETS, C, FONT, defs, stars

# ── OFFGRID feature grid: (icon, title, line 1, line 2) ───────────────
FEATURES = [
    ("pin", "Offline map", "1,758 facilities across Batangas", "evacuation centers, hospitals, rescue"),
    ("chip", "Local AI, no cloud", "Qwen 2.5 (3B) via Ollama", "every summary fact-checked by code"),
    ("chat", "Speaks typo & Taglish", "“how do i stop bleding”", "“saan ang pinakamalapit na ospital”"),
    ("compass", "Offline directions", "A* routing on the device", "steers around flooded roads"),
    ("phone", "Hub off? Still works", "phones keep a ~46 MB copy", "map, guides, search & router"),
    ("shield", "Tested, not hoped", "Python ↔ JS parity tests", "offline e2e + 220-question bank"),
]

# ── Quest board: (quest, percent done, status) ────────────────────────
QUESTS = [
    ("OFFGRID: demo → real-world ready for Batangas", 80, "polishing"),
    ("Ship Pabrews Cafe's QR ordering system", 30, "building"),
    ("Java roadmap: basics ✔ → loops ✔ → OOP ◉ → DSA ○", 50, "levelling up"),
    ("Become a Full-Stack & AI Engineer", 20, "the long game"),
]

# ── about.me code card: (key, string or list of strings) ─────────────
ABOUT = [
    ("name", "Lyle Daniel"),
    ("school", "Batangas State University — The NEU"),
    ("studying", "Computer Science"),
    ("aimingFor", "Full-Stack & AI Engineer"),
    ("building", "OFFGRID — an offline AI emergency map"),
    ("learning", ["Java OOP", "Data Structures", "FastAPI", "local LLMs"]),
    ("speaks", ["Java", "Python", "C++", "React", "JavaScript"]),
    ("approach", "understand it → test it → improve it, step by step"),
]

W = 900
MONO = "'Fira Code','JetBrains Mono','Cascadia Code',Consolas,Menlo,monospace"
PANEL = "#120a24"
DIM = "#8c7aa9"

# 24×24 line icons.
ICONS = {
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "chip": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6" rx="1"/>'
            '<path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12z"/>'
            '<path d="M8.5 12h.01M12 12h.01M15.5 12h.01" stroke-width="2.6"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2.2"/><path d="M11 18h2"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
}


def sparkle(x, y, s, color, dur, begin):
    return (f'<path transform="translate({x} {y})" d="M0 {-s} Q{s * .16:.2f} {-s * .16:.2f} {s} 0 Q{s * .16:.2f} {s * .16:.2f} 0 {s} '
            f'Q{-s * .16:.2f} {s * .16:.2f} {-s} 0 Q{-s * .16:.2f} {-s * .16:.2f} 0 {-s}Z" fill="{color}">'
            f'<animate attributeName="opacity" values="1;0.25;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>')


def frame(w, h, uid, seed, n_stars, inner, star_opacity=1.0):
    rng = random.Random(seed)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
  <defs>{defs(uid)}
    <clipPath id="{uid}card"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#{uid}card)">
    <rect width="{w}" height="{h}" fill="url(#{uid}sky)"/>
    <g opacity="{star_opacity}">{stars(w, h, n_stars, rng, uid)}</g>
    {inner}
  </g>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="17.5" fill="none" stroke="{C["violet"]}" stroke-opacity="0.55" stroke-width="1.5"/>
</svg>
'''


def features():
    pad, gap, cols, ch = 14, 14, 3, 120
    cw = (W - 2 * pad - (cols - 1) * gap) / cols
    rows = (len(FEATURES) + cols - 1) // cols
    h = 2 * pad + rows * ch + (rows - 1) * gap
    cards = []
    for i, (icon, title, l1, l2) in enumerate(FEATURES):
        x = pad + (i % cols) * (cw + gap)
        y = pad + (i // cols) * (ch + gap)
        t = 0.2 + i * 0.15
        cards.append(f'''
    <g opacity="0" transform="translate({x:.2f} {y})">
      <animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.6s" fill="freeze"/>
      <rect x="0.5" y="0.5" width="{cw - 1:.2f}" height="{ch - 1}" rx="14" fill="{PANEL}" fill-opacity="0.88" stroke="{C["violet"]}" stroke-opacity="0.6"/>
      <rect x="16" y="16" width="40" height="40" rx="11" fill="{C["violet"]}" fill-opacity="0.22" stroke="{C["lav"]}" stroke-opacity="0.35"/>
      <g transform="translate(24 24) scale(1)" fill="none" stroke="{C["lav"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
      <text x="70" y="42" font-size="17" font-weight="700" fill="{C["star"]}">{escape(title)}</text>
      <text x="18" y="84" font-size="12.5" fill="{C["text"]}">{escape(l1)}</text>
      <text x="18" y="103" font-size="12.5" fill="{C["text"]}" fill-opacity="0.75">{escape(l2)}</text>
      {sparkle(cw - 16, 16, 4, C["star"], round(2.4 + i * 0.4, 1), round(i * 0.3, 1))}
    </g>''')
    inner = f'<g font-family="{FONT}">{"".join(cards)}</g>'
    return frame(W, h, "ft", 21, 60, inner, 0.6).replace(
        'role="img">', 'role="img" aria-label="OFFGRID features">', 1)


def quests():
    left, bar_x, bar_w, right = 28, 470, 230, W - 28
    top, step = 92, 50
    h = top + (len(QUESTS) - 1) * step + 38
    rows = []
    for i, (name, pct, status) in enumerate(QUESTS):
        y = top + i * step
        fill_w = bar_w * pct / 100
        t = 0.5 + i * 0.25
        sep = (f'<line x1="{left}" y1="{y + 25}" x2="{right}" y2="{y + 25}" stroke="{C["violet"]}" stroke-opacity="0.22"/>'
               if i < len(QUESTS) - 1 else "")
        rows.append(f'''
    <g>
      <text x="{left}" y="{y}" font-size="13" fill="{C["pink"]}">◆</text>
      <text x="{left + 20}" y="{y}" font-size="15" fill="{C["text"]}">{escape(name)}</text>
      <rect x="{bar_x}" y="{y - 10}" width="{bar_w}" height="10" rx="5" fill="{C["deep"]}" fill-opacity="0.7"/>
      <clipPath id="qfill{i}"><rect x="{bar_x}" y="{y - 10}" width="0" height="10" rx="5">
        <animate attributeName="width" from="0" to="{fill_w:.1f}" begin="{t:.2f}s" dur="1.4s" fill="freeze"
          calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/></rect></clipPath>
      <g clip-path="url(#qfill{i})">
        <rect x="{bar_x}" y="{y - 10}" width="{bar_w}" height="10" fill="url(#qbar)" filter="url(#qglow)"/>
        <rect x="{bar_x - 40}" y="{y - 10}" width="34" height="10" fill="#ffffff" fill-opacity="0.35">
          <animate attributeName="x" values="{bar_x - 40};{bar_x + fill_w + 10:.1f}" dur="2.6s" begin="{t + 1.6:.2f}s" repeatCount="indefinite"/>
        </rect>
      </g>
      <text x="{bar_x + bar_w + 14}" y="{y}" font-size="13" font-weight="700" fill="{C["lav"]}">{pct}%</text>
      <text x="{right}" y="{y}" text-anchor="end" font-size="13" fill="{C["star"]}" fill-opacity="0.75">{escape(status)}</text>
      {sep}
    </g>''')
    labels = f'''
    <g font-size="11" font-weight="700" letter-spacing="2" fill="{DIM}">
      <text x="{left}" y="40">QUEST</text>
      <text x="{bar_x}" y="40">PROGRESS</text>
      <text x="{right}" y="40" text-anchor="end">STATUS</text>
    </g>
    <line x1="{left}" y1="54" x2="{right}" y2="54" stroke="{C["lav"]}" stroke-opacity="0.3"/>'''
    grad = f'''
    <linearGradient id="qbar" gradientUnits="userSpaceOnUse" x1="{bar_x}" y1="0" x2="{bar_x + bar_w}" y2="0">
      <stop offset="0" stop-color="{C["violet"]}"/><stop offset="0.6" stop-color="{C["lav"]}"/><stop offset="1" stop-color="{C["pink"]}"/>
    </linearGradient>
    <filter id="qglow" x="-10%" y="-150%" width="120%" height="400%">
      <feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>'''
    inner = f'<g font-family="{FONT}">{grad}{labels}{"".join(rows)}</g>'
    return frame(W, h, "qb", 33, 45, inner, 0.45).replace(
        'role="img">', 'role="img" aria-label="Quest log">', 1)


def about():
    pad, ed_w, bar_h, line_h, fs = 16, 590, 34, 21, 12.5
    code_top = pad + bar_h + 28
    # Tokens are (text, colour) or (text, colour, column). A column pins the token to a
    # character position, so indentation and alignment don't depend on preserved spaces.
    lines = [[("const", "pink"), (" lyle ", "text"), ("= {", "dim")]]
    for key, value in ABOUT:
        toks = [(key, "lav", 2), (":", "dim")]
        if isinstance(value, list):
            toks.append(("[", "dim", 14))
            for j, item in enumerate(value):
                toks += [(f'"{item}"', "star")] + ([(", ", "dim")] if j < len(value) - 1 else [])
            toks.append(("]", "dim"))
        else:
            toks.append((f'"{value}"', "star", 14))
        lines.append(toks + [(",", "dim")])
    lines.append([("}", "dim"), (" as const", "pink"), (";", "dim")])

    colors = {"pink": C["pink"], "lav": C["lav"], "star": C["star"], "text": C["text"], "dim": DIM}
    ed_h = code_top + (len(lines) - 1) * line_h + 22 - pad
    h = ed_h + 2 * pad
    char_w = fs * 0.6
    code_x = pad + 46

    def tspan(text, colour, column=None):
        x = f' x="{code_x + column * char_w:.1f}"' if column is not None else ""
        return f'<tspan{x} fill="{colors[colour]}">{escape(text)}</tspan>'

    code = []
    for i, toks in enumerate(lines):
        y = code_top + i * line_h
        spans = "".join(tspan(*tok) for tok in toks)
        code.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.3 + i * 0.12:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<text x="{pad + 34}" y="{y}" text-anchor="end" fill="{DIM}" fill-opacity="0.6">{i + 1}</text>'
            f'<text x="{code_x}" y="{y}">{spans}</text></g>'
        )
    last = lines[-1]
    cursor_x = code_x + sum(len(tok[0]) for tok in last) * char_w + 3
    cursor_y = code_top + (len(lines) - 1) * line_h
    cursor_t = 0.3 + len(lines) * 0.12

    editor = f'''
    <rect x="{pad}" y="{pad}" width="{ed_w}" height="{ed_h}" rx="12" fill="{PANEL}" fill-opacity="0.9" stroke="{C["violet"]}" stroke-opacity="0.6"/>
    <path d="M{pad + 12} {pad} h{ed_w - 24} a12 12 0 0 1 12 12 v{bar_h - 12} h-{ed_w} v-{bar_h - 12} a12 12 0 0 1 12 -12z" fill="#1a0d33"/>
    <circle cx="{pad + 18}" cy="{pad + 17}" r="5" fill="#ff5f57"/>
    <circle cx="{pad + 34}" cy="{pad + 17}" r="5" fill="#febc2e"/>
    <circle cx="{pad + 50}" cy="{pad + 17}" r="5" fill="#28c840"/>
    <text x="{pad + 76}" y="{pad + 21}" font-family="{MONO}" font-size="12" fill="{C["star"]}">about.ts</text>
    <line x1="{pad + 70}" y1="{pad + bar_h - 1}" x2="{pad + 140}" y2="{pad + bar_h - 1}" stroke="{C["lav"]}" stroke-width="2"/>
    <g font-family="{MONO}" font-size="{fs}" xml:space="preserve">{"".join(code)}</g>
    <rect x="{cursor_x:.1f}" y="{cursor_y - fs + 1}" width="7" height="{fs + 3}" fill="{C["lav"]}" opacity="0">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1" dur="1s" begin="{cursor_t:.2f}s" repeatCount="indefinite"/>
    </rect>'''

    # The spiral galaxy from assets/orbit.svg, centred in the right-hand column.
    orbit_src = (ASSETS / "orbit.svg").read_text(encoding="utf-8")
    orbit_body = orbit_src[orbit_src.index(">") + 1: orbit_src.rindex("</svg>")]
    col_x, col_w, size = pad + ed_w, W - pad - (pad + ed_w), 250
    galaxy = (f'<svg x="{col_x + (col_w - size) / 2:.1f}" y="{(h - size) / 2:.1f}" width="{size}" height="{size}" '
              f'viewBox="0 0 320 320">{orbit_body}</svg>')

    return frame(W, h, "ab", 45, 40, editor + galaxy, 0.5).replace(
        'role="img">', 'role="img" aria-label="about.me">', 1)


if __name__ == "__main__":
    for name, svg in (("features.svg", features()), ("quests.svg", quests()), ("about.svg", about())):
        (ASSETS / name).write_text(svg, encoding="utf-8")
        print(f"wrote {ASSETS / name}  ({len(svg) // 1024} KB)")
