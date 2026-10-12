"""
Generates assets/terminal.svg — an animated neon terminal that "types" itself.

Edit SCRIPT below, then run:  python scripts/build_terminal.py
No dependencies. Pure SVG + SMIL, so it animates inside GitHub READMEs.
"""
from pathlib import Path
from html import escape

# ── What the terminal says ─────────────────────────────────────────────
USER, HOST = "lyle", "lyle-leif"
SCRIPT = [
    ("cmd", "whoami"),
    ("out", [("Lyle Daniel", "pink"), ("  //  CS student @ BatStateU · aspiring full-stack & AI engineer", "text")]),
    ("cmd", "ls ~/projects"),
    ("out", [("OFFGRID/", "cyan"), ("  Cafe-Pabrew/  eMATINO/  SpartaFeast/  Cosmic-Quest/", "text")]),
    ("cmd", "ping internet.com"),
    ("out", [("✗ request timed out", "pink"), ("  ...  ", "dim"), ("OFFGRID: ", "cyan"),
             ("still mapping, routing & answering ", "text"), ("✓", "green")]),
    ("cmd", "echo $MOTTO"),
    ("out", [('"Build things that ', "text"), ("still work", "purple"), (' when everything else doesn\'t."', "text")]),
]

# ── Look & feel ───────────────────────────────────────────────────────
W = 900
FONT = 15
CHAR_W = 9.05          # approx. advance width of a 15px monospace glyph
LINE_H = 31
TOP = 84               # baseline of first line
LEFT = 32
TYPE_SPEED = 0.055     # seconds per typed character
PAUSE_AFTER_CMD = 0.35
PAUSE_AFTER_OUT = 0.45
START = 0.9

C = {
    "bg": "#0b0f17", "bar": "#121826", "text": "#c9d1d9", "dim": "#6e7681",
    "pink": "#ff2e97", "cyan": "#00f0ff", "purple": "#b388ff", "green": "#39ff88",
}

PROMPT = [(USER, "green"), ("@", "dim"), (HOST, "cyan"), (":", "dim"), ("~", "purple"), ("$ ", "pink")]
PROMPT_LEN = sum(len(t) for t, _ in PROMPT)


def tspans(parts):
    return "".join(f'<tspan fill="{C[c]}">{escape(t)}</tspan>' for t, c in parts)


lines_svg, clips = [], []
t = START
y = TOP
for i, (kind, payload) in enumerate(SCRIPT):
    if kind == "cmd":
        cmd_x = LEFT + PROMPT_LEN * CHAR_W
        n = len(payload)
        dur = max(n * TYPE_SPEED, 0.1)
        # Discrete widths → a real char-by-char typing feel.
        widths = ";".join(f"{k * CHAR_W:.2f}" for k in range(n + 1)) + f";{n * CHAR_W + 40:.2f}"
        clips.append(
            f'<clipPath id="c{i}"><rect x="{cmd_x:.2f}" y="{y - FONT - 4}" height="{LINE_H}" width="0">'
            f'<animate attributeName="width" values="{widths}" calcMode="discrete" '
            f'begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        lines_svg.append(
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
            f'<text x="{LEFT}" y="{y}">{tspans(PROMPT)}</text>'
            f'<text x="{cmd_x:.2f}" y="{y}" fill="{C["text"]}" clip-path="url(#c{i})">{escape(payload)}</text></g>'
        )
        t += dur + PAUSE_AFTER_CMD
    else:
        lines_svg.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.25s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" '
            f'begin="{t:.2f}s" dur="0.25s" fill="freeze"/>'
            f'<text x="{LEFT}" y="{y}">{tspans([("→ ", "pink")] + payload)}</text></g>'
        )
        t += PAUSE_AFTER_OUT
    y += LINE_H

# Final idle prompt with a blinking cursor.
cursor_x = LEFT + PROMPT_LEN * CHAR_W
lines_svg.append(
    f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
    f'<text x="{LEFT}" y="{y}">{tspans(PROMPT)}</text>'
    f'<rect x="{cursor_x:.2f}" y="{y - FONT + 1}" width="{CHAR_W:.2f}" height="{FONT + 3}" fill="{C["pink"]}" filter="url(#glow)">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect></g>'
)

H = y + 34

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated terminal introducing Lyle Daniel">
  <defs>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{C["pink"]}"/>
      <stop offset="0.5" stop-color="#7928ca"/>
      <stop offset="1" stop-color="{C["cyan"]}"/>
      <animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{C["cyan"]}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#ffffff" opacity="0.025"/>
    </pattern>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="0.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="win"><rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="14"/></clipPath>
    {"".join(clips)}
  </defs>

  <!-- window -->
  <rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="14" fill="{C["bg"]}"/>
  <g clip-path="url(#win)">
    <rect x="6" y="6" width="{W - 12}" height="38" fill="{C["bar"]}"/>
    <rect width="{W}" height="{H}" fill="url(#lines)"/>
    <rect x="0" y="-120" width="{W}" height="120" fill="url(#scan)">
      <animate attributeName="y" values="-120;{H}" dur="4.5s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="14" fill="none" stroke="url(#border)" stroke-width="2" filter="url(#glow)"/>

  <!-- title bar -->
  <circle cx="30" cy="25" r="6" fill="#ff5f57"/>
  <circle cx="50" cy="25" r="6" fill="#febc2e"/>
  <circle cx="70" cy="25" r="6" fill="#28c840"/>
  <text x="{W / 2}" y="30" text-anchor="middle" fill="{C["dim"]}" font-family="'Fira Code','JetBrains Mono',Consolas,Menlo,monospace" font-size="13">{USER}@{HOST}: ~ — zsh</text>

  <!-- content -->
  <g font-family="'Fira Code','JetBrains Mono','Cascadia Code',Consolas,Menlo,monospace" font-size="{FONT}" xml:space="preserve" filter="url(#soft)">
    {"".join(lines_svg)}
  </g>
</svg>
'''

out = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg, encoding="utf-8")
print(f"wrote {out}  ({W}x{H}, animation ends at {t:.1f}s)")
