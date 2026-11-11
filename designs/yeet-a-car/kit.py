"""SVG drawing kit for the Yeet a Car concept art (thumbnails 1920x1080, icons 1024x1024).

Flat-shaded cartoon style with heavy outlines: it reads at 150 px and matches the bright,
saturated look of top Roblox thumbnails. These are composition comps - final uploads should
be rendered from the real in-game car and avatar (Studio freecam) following the same layout.
"""

from __future__ import annotations

import math
import random

INK = "#14121a"
FONT = "'Inter Display', 'Inter', 'DejaVu Sans', sans-serif"

# Brand palette: complementary blue sky vs orange blast, cherry-red hero car.
SKY_TOP, SKY_MID, SKY_LOW = "#061f86", "#1f6fe8", "#7cc8ff"
CAR = ("#ff5a4f", "#e01e2b", "#9c0f19")  # light, base, shadow
SKIN = "#ffd23f"
SUIT = "#1f6fff"

_uid = 0


def uid(prefix: str) -> str:
    global _uid
    _uid += 1
    return f"{prefix}{_uid}"


DEFS = f"""
<linearGradient id="skyDay" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{SKY_TOP}"/><stop offset=".55" stop-color="{SKY_MID}"/><stop offset="1" stop-color="{SKY_LOW}"/>
</linearGradient>
<linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1c0f5c"/><stop offset=".45" stop-color="#6a2cf5"/><stop offset=".8" stop-color="#ff5e3a"/><stop offset="1" stop-color="#ffb347"/>
</linearGradient>
<linearGradient id="skyGrey" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#6d7480"/><stop offset="1" stop-color="#a9afb8"/>
</linearGradient>
<linearGradient id="skySpace" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#050716"/><stop offset=".6" stop-color="#14206b"/><stop offset="1" stop-color="#2f6bff"/>
</linearGradient>
<radialGradient id="blast" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#fffbe6"/><stop offset=".22" stop-color="#ffe94d"/><stop offset=".55" stop-color="#ff9a1f"/>
  <stop offset=".82" stop-color="#ff4a1c"/><stop offset="1" stop-color="#d0151c"/>
</radialGradient>
<radialGradient id="blastGlow" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#ffd23f" stop-opacity=".95"/><stop offset=".5" stop-color="#ff7a1a" stop-opacity=".45"/>
  <stop offset="1" stop-color="#ff5a00" stop-opacity="0"/>
</radialGradient>
<radialGradient id="sunGlow" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#fff6c8" stop-opacity="1"/><stop offset=".4" stop-color="#ffd66b" stop-opacity=".55"/>
  <stop offset="1" stop-color="#ffb347" stop-opacity="0"/>
</radialGradient>
<linearGradient id="carBody" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{CAR[0]}"/><stop offset=".55" stop-color="{CAR[1]}"/><stop offset="1" stop-color="{CAR[2]}"/>
</linearGradient>
<linearGradient id="rustBody" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#b08a6a"/><stop offset="1" stop-color="#6e5644"/>
</linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#e6f7ff"/><stop offset=".5" stop-color="#8fd0ff"/><stop offset="1" stop-color="#3b8be6"/>
</linearGradient>
<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#f4f7fb"/><stop offset="1" stop-color="#9aa6b4"/>
</linearGradient>
<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#5ee05a"/><stop offset="1" stop-color="#1f9a3a"/>
</linearGradient>
<linearGradient id="dirt" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#f0b45c"/><stop offset="1" stop-color="#b8692d"/>
</linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff3a0"/><stop offset=".5" stop-color="#ffd21f"/><stop offset="1" stop-color="#ff9d00"/>
</linearGradient>
<linearGradient id="flame" x1="1" y1="0" x2="0" y2="0">
  <stop offset="0" stop-color="#fffbe6"/><stop offset=".25" stop-color="#ffe14d"/><stop offset=".6" stop-color="#ff7a1a"/>
  <stop offset="1" stop-color="#ff3d1f" stop-opacity="0"/>
</linearGradient>
<pattern id="hazard" width="56" height="56" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="56" height="56" fill="{INK}"/><rect width="28" height="56" fill="#ffd000"/>
</pattern>
<radialGradient id="vignette" cx=".5" cy=".5" r=".75">
  <stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/>
</radialGradient>
<radialGradient id="halo" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/><stop offset=".6" stop-color="#ffffff" stop-opacity=".18"/>
  <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</radialGradient>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
  <feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#000" flood-opacity=".45"/>
</filter>
<filter id="textShadow" x="-20%" y="-20%" width="140%" height="160%">
  <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000" flood-opacity=".55"/>
</filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="22" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="blurX" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="14 2"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="haze" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>
"""


def doc(w: int, h: int, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f"<defs>{DEFS}</defs>{body}</svg>")


def g(content: str, x: float = 0, y: float = 0, s: float = 1, rot: float = 0, flip: bool = False,
      extra: str = "") -> str:
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({sx:.3f} {s:.3f})" {extra}>{content}</g>'


# --------------------------------------------------------------------------- car
CAR_BODY = ("M -255,30 C -262,0 -255,-30 -230,-40 L -150,-52 C -120,-58 -100,-62 -85,-75 L -40,-118 "
            "C -30,-127 -18,-130 -5,-130 L 95,-130 C 115,-130 128,-124 140,-112 L 185,-62 L 238,-50 "
            "C 258,-46 268,-30 268,-10 L 268,22 C 268,34 260,40 248,40 L -240,40 C -250,40 -255,36 -255,30 Z")


def wheel(x: float, y: float, r: float = 54, spin: float = 0) -> str:
    spokes = "".join(
        f'<line x1="0" y1="0" x2="{r * 0.5 * math.cos(math.radians(a + spin)):.1f}" '
        f'y2="{r * 0.5 * math.sin(math.radians(a + spin)):.1f}" stroke="#7d8896" stroke-width="7" stroke-linecap="round"/>'
        for a in range(0, 360, 72))
    return (f'<g transform="translate({x} {y})"><circle r="{r}" fill="#22232a" stroke="{INK}" stroke-width="9"/>'
            f'<circle r="{r * 0.58}" fill="#d9e0e7" stroke="{INK}" stroke-width="6"/>{spokes}'
            f'<circle r="{r * 0.16}" fill="#5c6775"/></g>')


def car(body_fill: str = "url(#carBody)", driver: bool = False, rusty: bool = False, flames: bool = False,
        number: str | None = "7") -> str:
    """Side view, facing right, ~525 x 225, origin at body centre."""
    clip = uid("cb")
    stripe = "#ffffff" if not rusty else "#8a7a6a"
    rust = ""
    if rusty:
        rnd = random.Random(4)
        rust = "".join(f'<circle cx="{rnd.randint(-230, 240)}" cy="{rnd.randint(-40, 30)}" r="{rnd.randint(8, 22)}" '
                       f'fill="#5a3b22" opacity=".55"/>' for _ in range(14))
    flame = ""
    if flames:
        flame = ('<path d="M -255,-5 C -330,-40 -420,-20 -520,0 C -420,20 -330,40 -255,15 Z" fill="url(#flame)" '
                 'filter="url(#glow)"/>')
    driver_svg = ""
    if driver:
        driver_svg = (f'<g transform="translate(78 -92)"><rect x="-26" y="-28" width="52" height="50" rx="10" fill="{SKIN}" '
                      f'stroke="{INK}" stroke-width="5"/><path d="M -30,-8 C -30,-40 30,-40 30,-8 Z" fill="#e8262f" '
                      f'stroke="{INK}" stroke-width="5"/><circle cx="10" cy="2" r="5" fill="{INK}"/>'
                      f'<path d="M 0,14 Q 12,20 24,10" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/></g>')
    num = ""
    if number:
        num = (f'<circle cx="-20" cy="-5" r="30" fill="#fff" stroke="{INK}" stroke-width="6"/>'
               f'<text x="-20" y="8" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="38" '
               f'fill="{INK}">{number}</text>')
    return (
        flame +
        f'<clipPath id="{clip}"><path d="{CAR_BODY}"/></clipPath>'
        # spoiler
        f'<path d="M -238,-40 L -262,-84 L -196,-84 L -200,-50 Z" fill="{body_fill}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        f'<path d="{CAR_BODY}" fill="{body_fill}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
        f'<g clip-path="url(#{clip})">'
        f'<rect x="-270" y="-14" width="560" height="18" fill="{stripe}" opacity=".95"/>'
        f'<path d="M -230,-40 L -150,-52 L 238,-50 L 238,-40 L -230,-28 Z" fill="#fff" opacity=".25"/>{rust}'
        f'<rect x="-270" y="22" width="560" height="30" fill="#000" opacity=".18"/></g>'
        f'<path d="M -72,-66 L -32,-112 C -26,-118 -20,-120 -12,-120 L 40,-120 L 40,-66 Z" fill="url(#glass)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f'<path d="M 54,-66 L 54,-120 L 92,-120 C 104,-120 112,-116 120,-108 L 162,-66 Z" fill="url(#glass)" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        + driver_svg + num +
        f'<path d="M 250,-38 L 268,-34 L 268,-18 L 246,-22 Z" fill="#fff6a8" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="-258" y="-30" width="16" height="18" rx="4" fill="#ff2a2a" stroke="{INK}" stroke-width="5"/>'
        f'<circle cx="-160" cy="40" r="66" fill="{INK}"/><circle cx="170" cy="40" r="66" fill="{INK}"/>'
        + wheel(-160, 40) + wheel(170, 40, spin=30)
    )


def broken_car(gap: float = 90, tilt: float = 22, debris_seed: int = 3, shards_n: int = 16, loose_wheel: bool = True) -> str:
    """The hero car snapping in half mid-air, with flying parts."""
    jag = "M 5,-170 L -22,-95 L 22,-55 L -18,-5 L 18,35 L -6,120"
    rear_clip, front_clip = uid("rc"), uid("fc")
    whole = car(driver=False)
    rnd = random.Random(debris_seed)
    shards = []
    for _ in range(shards_n):
        x, y = rnd.uniform(-60, 60), rnd.uniform(-160, 40)
        r = rnd.uniform(10, 28)
        pts = " ".join(f"{x + r * math.cos(a):.0f},{y + r * 0.7 * math.sin(a):.0f}"
                       for a in sorted(rnd.uniform(0, 2 * math.pi) for _ in range(4)))
        col = rnd.choice(["#8fd0ff", CAR[1], CAR[0], "#d9e0e7", INK])
        dx, dy = rnd.uniform(-1, 1) * 260, rnd.uniform(-1.2, 0.4) * 220
        shards.append(f'<polygon points="{pts}" transform="translate({dx:.0f} {dy:.0f}) rotate({rnd.uniform(0, 90):.0f})" '
                      f'fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    return (
        f'<clipPath id="{rear_clip}"><path d="M -600,-300 L 5,-300 {jag[jag.index("L"):]} L -6,300 L -600,300 Z"/></clipPath>'
        f'<clipPath id="{front_clip}"><path d="M 600,-300 L 5,-300 {jag[jag.index("L"):]} L -6,300 L 600,300 Z"/></clipPath>'
        f'<g transform="translate({-gap / 2} 10) rotate({-tilt})"><g clip-path="url(#{rear_clip})">{whole}</g>'
        f'<path d="{jag}" stroke="#ffb020" stroke-width="10" fill="none" stroke-linejoin="round" filter="url(#glow)"/></g>'
        f'<g transform="translate({gap / 2} -10) rotate({tilt * 0.6})"><g clip-path="url(#{front_clip})">{car(driver=False, number=None)}</g>'
        f'<path d="{jag}" stroke="#ffb020" stroke-width="10" fill="none" stroke-linejoin="round" filter="url(#glow)"/></g>'
        + "".join(shards)
        + (g(wheel(0, 0, 54, spin=20), 330, -170, 0.9, 25) if loose_wheel else "")
    )


# -------------------------------------------------------------------------- ramp
def ramp(x0: float, y0: float, x1: float, y1: float, ribs: int = 6) -> str:
    """Solid kicker ramp: ground at (x0,y0), curving up to the lip at (x1,y1), back wall at x1."""
    cx, cy = x1 - (x1 - x0) * 0.22, y0
    surface = f"M {x0},{y0} Q {cx},{cy} {x1},{y1}"
    body = f"{surface} L {x1},{y0} Z"
    clip = uid("rp")
    rib_lines = []
    for i in range(1, ribs + 1):
        t = i / (ribs + 1)
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1
        rib_lines.append(f'<line x1="{px:.0f}" y1="{y1 - 50}" x2="{px:.0f}" y2="{y0}" stroke="#7b8796" stroke-width="10"/>')
    braces = []
    for i in range(1, ribs):
        t0, t1 = i / (ribs + 1), (i + 1) / (ribs + 1)
        a = (1 - t0) ** 2 * x0 + 2 * (1 - t0) * t0 * cx + t0 ** 2 * x1
        b = (1 - t1) ** 2 * x0 + 2 * (1 - t1) * t1 * cx + t1 ** 2 * x1
        braces.append(f'<line x1="{a:.0f}" y1="{y0}" x2="{b:.0f}" y2="{y1 - 50}" stroke="#7b8796" stroke-width="7"/>')
    return (
        f'<clipPath id="{clip}"><path d="{body}"/></clipPath>'
        f'<path d="{body}" fill="#c9d2dc" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
        f'<g clip-path="url(#{clip})">{"".join(rib_lines)}{"".join(braces)}'
        f'<rect x="{x1 - 40}" y="{y1}" width="40" height="{y0 - y1}" fill="#8d99a8"/></g>'
        f'<path d="{surface}" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/>'
        f'<path d="{surface}" stroke="url(#hazard)" stroke-width="26" fill="none" stroke-linecap="round"/>'
        f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
    )


# ------------------------------------------------------------------------ avatar
def avatar(expression: str = "grin", look: tuple[float, float] = (1, -0.4), helmet: bool = True,
           arm: str | None = None) -> str:
    """Blocky hero, front view. Origin = bottom-centre of the head (neck). Head is 240x240."""
    lx, ly = look
    eyes = ""
    for ex in (-58, 58):
        eyes += (f'<ellipse cx="{ex}" cy="-112" rx="30" ry="34" fill="#fff" stroke="{INK}" stroke-width="7"/>'
                 f'<circle cx="{ex + lx * 13:.0f}" cy="{-112 + ly * 14:.0f}" r="16" fill="{INK}"/>'
                 f'<circle cx="{ex + lx * 13 + 5:.0f}" cy="{-112 + ly * 14 - 6:.0f}" r="5" fill="#fff"/>')
    brows = {
        "grin": f'<path d="M -92,-160 L -30,-150" /><path d="M 30,-150 L 92,-160"/>',
        "determined": f'<path d="M -92,-168 L -28,-146"/><path d="M 28,-146 L 92,-168"/>',
        "awe": f'<path d="M -88,-170 Q -58,-186 -28,-170"/><path d="M 28,-170 Q 58,-186 88,-170"/>',
        "sad": f'<path d="M -92,-150 L -30,-166"/><path d="M 30,-166 L 92,-150"/>',
    }[expression]
    mouth = {
        "grin": f'<path d="M -62,-58 Q 0,-14 66,-64" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
                f'<path d="M 58,-74 Q 72,-66 70,-52" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>',
        "determined": f'<path d="M -50,-52 Q 10,-34 62,-66" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>',
        "awe": f'<ellipse cx="0" cy="-50" rx="18" ry="22" fill="{INK}"/>',
        "sad": f'<path d="M -46,-44 Q 0,-70 46,-44" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>',
    }[expression]
    helmet_svg = ""
    if helmet:
        helmet_svg = (f'<path d="M -136,-176 L -136,-210 C -136,-300 -76,-322 0,-322 C 76,-322 136,-300 136,-210 L 136,-176 '
                      f'C 80,-196 -80,-196 -136,-176 Z" fill="#e8262f" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
                      f'<path d="M -22,-320 L 22,-320 L 22,-190 L -22,-190 Z" fill="#fff" opacity=".95"/>'
                      f'<path d="M -136,-176 C -80,-196 80,-196 136,-176" fill="none" stroke="{INK}" stroke-width="10"/>'
                      f'<path d="M -100,-290 C -70,-312 -30,-318 -8,-318" fill="none" stroke="#fff" stroke-width="10" opacity=".6" stroke-linecap="round"/>')
    arm_svg = ""
    if arm == "fist":
        arm_svg = (f'<g transform="translate(178 70) rotate(26)"><rect x="-42" y="-200" width="84" height="230" rx="20" fill="{SUIT}" '
                   f'stroke="{INK}" stroke-width="9"/><rect x="-50" y="-270" width="100" height="90" rx="22" fill="{SKIN}" '
                   f'stroke="{INK}" stroke-width="9"/></g>')
    elif arm == "point":
        arm_svg = (f'<g transform="translate(190 40) rotate(-60)"><rect x="-40" y="-220" width="80" height="250" rx="20" fill="{SUIT}" '
                   f'stroke="{INK}" stroke-width="9"/><rect x="-36" y="-292" width="72" height="80" rx="18" fill="{SKIN}" '
                   f'stroke="{INK}" stroke-width="9"/><rect x="-10" y="-352" width="26" height="70" rx="12" fill="{SKIN}" '
                   f'stroke="{INK}" stroke-width="8"/></g>')
    return (
        f'<rect x="-170" y="-14" width="340" height="320" rx="34" fill="{SUIT}" stroke="{INK}" stroke-width="10"/>'
        f'<rect x="-22" y="-14" width="44" height="320" fill="#fff" opacity=".9"/>'
        f'<circle cx="-92" cy="70" r="26" fill="#ffd000" stroke="{INK}" stroke-width="7"/>'
        + arm_svg +
        f'<rect x="-124" y="-250" width="248" height="250" rx="46" fill="{SKIN}" stroke="{INK}" stroke-width="10"/>'
        + eyes + f'<g stroke="{INK}" stroke-width="18" stroke-linecap="round" fill="none">{brows}</g>' + mouth + helmet_svg
    )


# ------------------------------------------------------------------- effects/env
def explosion(r: float = 220, seed: int = 1, smoke: bool = True) -> str:
    rnd = random.Random(seed)
    pts = []
    n = 22
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1.0 if i % 2 == 0 else rnd.uniform(0.55, 0.7)) * rnd.uniform(0.9, 1.1)
        pts.append(f"{rr * math.cos(a):.0f},{rr * math.sin(a):.0f}")
    inner = []
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        rr = r * 0.62 * (1.0 if i % 2 == 0 else 0.6)
        inner.append(f"{rr * math.cos(a):.0f},{rr * math.sin(a):.0f}")
    puffs = ""
    if smoke:
        for _ in range(9):
            a = rnd.uniform(0, 2 * math.pi)
            d = r * rnd.uniform(0.85, 1.15)
            puffs += (f'<circle cx="{d * math.cos(a):.0f}" cy="{d * math.sin(a):.0f}" r="{r * rnd.uniform(0.28, 0.42):.0f}" '
                      f'fill="#3c3a44" opacity=".55"/>')
    return (f'<circle r="{r * 1.9:.0f}" fill="url(#blastGlow)"/>' + puffs +
            f'<polygon points="{" ".join(pts)}" fill="url(#blast)" stroke="#c4161c" stroke-width="8" stroke-linejoin="round"/>'
            f'<polygon points="{" ".join(inner)}" fill="#fff4a8" opacity=".9"/>'
            f'<circle r="{r * 0.22:.0f}" fill="#ffffff" filter="url(#haze)"/>')


def cloud(s: float = 1.0, opacity: float = 0.95) -> str:
    return (f'<g opacity="{opacity}" transform="scale({s})"><ellipse cx="0" cy="0" rx="160" ry="60" fill="#fff"/>'
            f'<ellipse cx="-70" cy="-30" rx="80" ry="65" fill="#fff"/><ellipse cx="40" cy="-55" rx="95" ry="80" fill="#fff"/>'
            f'<ellipse cx="120" cy="-15" rx="70" ry="50" fill="#fff"/>'
            f'<ellipse cx="0" cy="25" rx="170" ry="30" fill="#d7ecff"/></g>')


def speed_lines(n: int = 14, w: int = 1920, h: int = 1080, seed: int = 9, angle: float = -18,
                cx: float = 0, cy: float = 0, opacity: float = 0.55) -> str:
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        L = rnd.uniform(160, 420)
        out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + L:.0f}" y2="{y:.0f}" stroke="#fff" '
                   f'stroke-width="{rnd.uniform(6, 14):.0f}" stroke-linecap="round" opacity="{rnd.uniform(.35, .8):.2f}"/>')
    return f'<g transform="rotate({angle} {cx} {cy})" opacity="{opacity}" filter="url(#blurX)">{"".join(out)}</g>'


def text(x: float, y: float, size: float, content: str, fill: str = "#ffffff", anchor: str = "middle",
         rot: float = 0, stroke: float = 0.17) -> str:
    sw = size * stroke
    common = (f'x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="900" font-size="{size}" '
              f'letter-spacing="{-size * 0.02:.1f}" transform="rotate({rot} {x} {y})"')
    return (f'<g filter="url(#textShadow)"><text {common} fill="{INK}" stroke="{INK}" stroke-width="{sw:.0f}" '
            f'stroke-linejoin="round" paint-order="stroke">{content}</text>'
            f'<text {common} fill="{fill}">{content}</text></g>')


def hills(w: int, y: int, fill: str = "url(#grass)", seed: int = 2, amp: int = 60) -> str:
    rnd = random.Random(seed)
    pts = [f"M 0,{y}"]
    x = 0
    while x < w:
        nx = x + rnd.randint(260, 420)
        pts.append(f"Q {x + (nx - x) / 2:.0f},{y - rnd.randint(amp // 2, amp)} {nx},{y}")
        x = nx
    return f'<path d="{" ".join(pts)} L {w},{y + 2000} L 0,{y + 2000} Z" fill="{fill}" stroke="{INK}" stroke-width="6"/>'


def crates(n: int = 3, seed: int = 5) -> str:
    """A small stack of wooden crates (destruction target)."""
    rnd = random.Random(seed)
    out = []
    pos = [(0, 0), (130, 0), (65, -120)][:n]
    for x, y in pos:
        out.append(f'<g transform="translate({x} {y}) rotate({rnd.uniform(-4, 4):.1f})">'
                   f'<rect x="-60" y="-120" width="120" height="120" fill="#e0a252" stroke="{INK}" stroke-width="8"/>'
                   f'<path d="M -60,-120 L 60,0 M 60,-120 L -60,0" stroke="#9a6326" stroke-width="10"/>'
                   f'<rect x="-60" y="-120" width="120" height="120" fill="none" stroke="{INK}" stroke-width="8"/></g>')
    return "".join(out)


def vignette(w: int, h: int) -> str:
    """Darkened edges: pushes the eye to the centre and raises subject/background value contrast."""
    return f'<rect width="{w}" height="{h}" fill="url(#vignette)"/>'


def halo(x: float, y: float, r: float) -> str:
    """Soft light behind a subject so it separates from the background when shrunk."""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#halo)"/>'
