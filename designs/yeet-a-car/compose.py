"""Yeet a Car: five thumbnail + icon iterations, each a different archetype from
reports/thumbnails/MRBEAST_THUMBNAIL_STUDY.md (section 7.2).

    python3 compose.py && NODE_PATH=$(npm root -g) node render.cjs v1 v2 v3 v4 v5
"""

from __future__ import annotations

import math
import random
from pathlib import Path

from kit import (INK, avatar, broken_car, car, cloud, crates, doc, explosion, g, halo, hills, ramp, speed_lines,
                 text, vignette)

W, H = 1920, 1080
ICON = 1024
OUT = Path(__file__).parent


def stars(n: int, w: int, h: int, seed: int = 1) -> str:
    rnd = random.Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(0, w):.0f}" cy="{rnd.uniform(0, h):.0f}" r="{rnd.uniform(1.5, 4.5):.1f}" '
                   f'fill="#fff" opacity="{rnd.uniform(.4, 1):.2f}"/>' for _ in range(n))


def rays(cx: float, cy: float, n: int = 16, r0: float = 200, r1: float = 1400, opacity: float = 0.18) -> str:
    out = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + math.pi / n * 0.55
        out.append(f'<polygon points="{cx + r0 * math.cos(a0):.0f},{cy + r0 * math.sin(a0):.0f} '
                   f'{cx + r1 * math.cos(a0):.0f},{cy + r1 * math.sin(a0):.0f} '
                   f'{cx + r1 * math.cos(a1):.0f},{cy + r1 * math.sin(a1):.0f} '
                   f'{cx + r0 * math.cos(a1):.0f},{cy + r0 * math.sin(a1):.0f}" fill="#fff" opacity="{opacity}"/>')
    return "".join(out)


def barrels(n: int = 3) -> str:
    out = []
    for i in range(n):
        x = i * 110 - (n - 1) * 55
        out.append(f'<g transform="translate({x} 0)"><rect x="-48" y="-150" width="96" height="150" rx="14" fill="#e8262f" '
                   f'stroke="{INK}" stroke-width="8"/><rect x="-48" y="-112" width="96" height="16" fill="#ffd000" stroke="{INK}" '
                   f'stroke-width="5"/><rect x="-48" y="-56" width="96" height="16" fill="#ffd000" stroke="{INK}" stroke-width="5"/>'
                   f'<path d="M -14,-90 L 6,-90 L -6,-66 L 14,-66 L -10,-32 L -2,-58 L -18,-58 Z" fill="#fff" stroke="{INK}" stroke-width="3"/></g>')
    return "".join(out)


def planet(cx: float, cy: float, r: float) -> str:
    return (f'<circle cx="{cx}" cy="{cy}" r="{r + 60}" fill="#7fd8ff" opacity=".25"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 25}" fill="#7fd8ff" opacity=".35"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2f8bff" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M {cx - r * .7},{cy - r * .55} q {r * .25},{-r * .15} {r * .45},0 t {r * .3},{r * .12} '
            f'l {-r * .1},{r * .2} q {-r * .3},{r * .05} {-r * .6},{-r * .05} z" fill="#3fd06a" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {cx + r * .15},{cy - r * .78} q {r * .2},{-r * .05} {r * .4},{r * .05} l {-r * .05},{r * .1} '
            f'q {-r * .2},{r * .02} {-r * .35},{-r * .03} z" fill="#3fd06a" stroke="{INK}" stroke-width="6"/>')


# ----------------------------------------------------------------------- v1
def thumb_v1() -> str:
    """'The Launch' - the verb, shown straight, with the destruction target waiting."""
    b = '<rect width="1920" height="1080" fill="url(#skyDay)"/>'
    b += g(cloud(), 330, 170, 0.8) + g(cloud(opacity=0.8), 1650, 140, 0.55)
    b += hills(W, 905)
    b += g(crates(3), 1700, 905, 0.9)
    b += ramp(-260, 960, 820, 500)
    b += halo(1200, 330, 420)
    b += speed_lines(16, angle=-18, cx=1200, cy=330)
    b += g(car(driver=True, flames=True), 1200, 330, 1.45, -18, extra='filter="url(#shadow)"')
    b += vignette(W, H)
    b += text(430, 250, 220, "YEET!", rot=-6)
    return doc(W, H, b)


def icon_v1() -> str:
    b = '<rect width="1024" height="1024" fill="url(#skyDay)"/>'
    b += ramp(-160, 1060, 430, 690)
    b += halo(600, 430, 380)
    b += speed_lines(10, 1024, 1024, angle=-22, cx=600, cy=420)
    b += g(car(driver=True, flames=True), 610, 430, 1.2, -22, extra='filter="url(#shadow)"')
    b += vignette(1024, 1024)
    return doc(ICON, ICON, b)


# ----------------------------------------------------------------------- v2
def thumb_v2() -> str:
    """Stakes moment: the beat before impact, big hero face whose gaze points at it."""
    b = '<rect width="1920" height="1080" fill="url(#skyDusk)"/>'
    b += '<circle cx="1560" cy="720" r="460" fill="url(#sunGlow)"/>'
    b += hills(W, 900, fill="#2b1a5e", amp=80)
    b += g(barrels(3), 1620, 900, 1.35) + g(crates(3), 1330, 900, 1.25)
    b += speed_lines(12, angle=26, cx=1130, cy=300)
    b += g(car(driver=True, flames=True), 1110, 300, 1.15, 26, extra='filter="url(#shadow)"')
    b += vignette(W, H)
    b += g(avatar("grin", look=(1, -0.5)), 420, 905, 1.7)
    return doc(W, H, b)


def icon_v2() -> str:
    b = '<rect width="1024" height="1024" fill="#1c0f5c"/>'
    b += g(explosion(380, seed=4, smoke=False), 512, 430)
    b += vignette(1024, 1024)
    b += g(avatar("grin", look=(0.5, -0.2)), 512, 1000, 2.2)
    return doc(ICON, ICON, b)


# ----------------------------------------------------------------------- v3
def thumb_v3() -> str:
    """Progression contrast: LVL 1 vs LVL 999 (the '$1 vs $1M' pattern)."""
    left = ('<rect width="960" height="1080" fill="#2a2e36"/>'
            '<rect width="960" height="1080" fill="url(#skyGrey)" opacity=".35"/>'
            '<rect y="860" width="960" height="220" fill="#7a6e62" stroke="#14121a" stroke-width="6"/>'
            + g(ramp(0, 0, 300, -130), 200, 862)
            + g(car(body_fill="url(#rustBody)", rusty=True, number=None), 560, 700, 0.85, -6)
            + '<circle cx="300" cy="820" r="44" fill="#d8d2c8" opacity=".85"/><circle cx="240" cy="840" r="30" fill="#d8d2c8" opacity=".7"/>'
            + '<rect width="960" height="1080" fill="#000" opacity=".18"/>'
            + text(300, 240, 170, "LVL 1"))
    right = ('<rect x="960" width="960" height="1080" fill="url(#skyDay)"/>'
             '<circle cx="1500" cy="420" r="460" fill="url(#sunGlow)"/>'
             + hills(W, 905).replace('M 0,', 'M 960,')
             + ramp(900, 960, 1330, 640)
             + speed_lines(10, angle=-28, cx=1560, cy=470)
             + g(car(driver=True, flames=True), 1560, 470, 1.0, -28, extra='filter="url(#shadow)"')
             + text(1440, 240, 170, "LVL 999", fill="url(#gold)"))
    clip_l = '<clipPath id="leftHalf"><polygon points="0,0 1000,0 920,1080 0,1080"/></clipPath>'
    clip_r = '<clipPath id="rightHalf"><polygon points="1000,0 1920,0 1920,1080 920,1080"/></clipPath>'
    divider = f'<polygon points="990,0 1014,0 934,1080 910,1080" fill="#fff" stroke="{INK}" stroke-width="8"/>'
    return doc(W, H, clip_l + clip_r + f'<g clip-path="url(#leftHalf)">{left}</g>'
               f'<g clip-path="url(#rightHalf)">{right}</g>' + vignette(W, H) + divider)


def icon_v3() -> str:
    b = '<rect width="1024" height="1024" fill="url(#skyDusk)"/>'
    b += '<circle cx="540" cy="520" r="470" fill="url(#sunGlow)" opacity=".7"/>'
    b += '<circle cx="540" cy="520" r="360" fill="#ffd23f" stroke="#14121a" stroke-width="10"/>'
    b += g(car(driver=True, flames=True), 560, 520, 1.25, -20, extra='filter="url(#shadow)"')
    b += vignette(1024, 1024)
    return doc(ICON, ICON, b)


# ----------------------------------------------------------------------- v4
def thumb_v4() -> str:
    """Progress counter + scale: the distance number tells the story. No face (tests the no-face hook)."""
    b = '<rect width="1920" height="1080" fill="url(#skySpace)"/>' + stars(90, W, 700)
    b += planet(960, 2350, 1500)
    b += ('<path d="M 160,960 C 500,420 900,300 1240,360" fill="none" stroke="#ffe14d" stroke-width="12" '
          'stroke-dasharray="30 26" stroke-linecap="round" opacity=".9"/>')
    b += g(ramp(0, 0, 150, -110), 70, 960, 1)
    b += halo(1400, 360, 420)
    b += g(car(driver=True, flames=True), 1400, 360, 1.35, -10, extra='filter="url(#shadow)"')
    b += vignette(W, H)
    b += text(540, 290, 230, "9,999m", fill="url(#gold)", rot=-4)
    return doc(W, H, b)


def icon_v4() -> str:
    b = '<rect width="1024" height="1024" fill="url(#skySpace)"/>' + stars(40, 1024, 600, seed=3)
    b += planet(512, 1650, 900)
    b += halo(540, 450, 360)
    b += g(car(driver=True, flames=True), 540, 450, 1.25, -14, extra='filter="url(#shadow)"')
    b += vignette(1024, 1024)
    return doc(ICON, ICON, b)


# ----------------------------------------------------------------------- v5
def thumb_v5() -> str:
    """Signature mechanic: the car snapping apart mid-air, hero reacting, damage number popping."""
    b = '<rect width="1920" height="1080" fill="url(#skyDay)"/>'
    b += rays(1300, 430, n=18, opacity=0.12)
    b += hills(W, 910, amp=50)
    b += g(explosion(320, seed=7), 1300, 450)
    b += g(broken_car(gap=120, tilt=24, shards_n=7, loose_wheel=True), 1300, 470, 1.2)
    b += vignette(W, H)
    b += g(avatar("grin", look=(1, -0.4)), 400, 912, 1.65)
    b += text(1330, 190, 150, "999,999", fill="#fff", rot=-5)
    return doc(W, H, b)


def icon_v5() -> str:
    b = '<rect width="1024" height="1024" fill="#061f86"/>'
    b += rays(512, 512, n=14, r0=120, r1=900, opacity=0.12)
    b += g(explosion(250, seed=7, smoke=False), 512, 500)
    b += g(broken_car(gap=120, tilt=24, shards_n=5, loose_wheel=False), 512, 530, 1.12)
    b += vignette(1024, 1024)
    return doc(ICON, ICON, b)


ITERATIONS = {
    "v1": (thumb_v1, icon_v1),
    "v2": (thumb_v2, icon_v2),
    "v3": (thumb_v3, icon_v3),
    "v4": (thumb_v4, icon_v4),
    "v5": (thumb_v5, icon_v5),
}

if __name__ == "__main__":
    for name, (thumb, icon) in ITERATIONS.items():
        d = OUT / name
        d.mkdir(exist_ok=True)
        (d / "thumbnail.svg").write_text(thumb(), encoding="utf-8")
        (d / "icon.svg").write_text(icon(), encoding="utf-8")
        print("wrote", d)
