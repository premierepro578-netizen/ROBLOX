"""Contact sheets and small-size previews (for human review and for design QA)."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def _font(size: int) -> ImageFont.ImageFont:
    for name in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _to_pil(img_bgr: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))


def contact_sheet(items: Iterable[tuple[np.ndarray, str]], out: str | Path, cols: int = 4,
                  tile: tuple[int, int] = (384, 216), caption_h: int = 22) -> Path:
    """Grid of images with one-line captions."""
    items = list(items)
    rows = max(1, (len(items) + cols - 1) // cols)
    W, H = tile
    sheet = Image.new("RGB", (cols * W, rows * (H + caption_h)), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    font = _font(14)
    for i, (img, cap) in enumerate(items):
        x, y = (i % cols) * W, (i // cols) * (H + caption_h)
        sheet.paste(_to_pil(cv2.resize(img, tile, interpolation=cv2.INTER_AREA)), (x, y))
        draw.text((x + 4, y + H + 3), cap[:52], fill=(235, 235, 235), font=font)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, optimize=True)
    return out


def preview_sheet(img: np.ndarray, kind: str, out: str | Path) -> Path:
    """How a design reads in practice: real display sizes, a squint (blur) test and a value
    (greyscale) test. Roblox: icons drop to ~150 px; thumbnails show as small Home tiles and
    the bottom strip can be covered by the player count."""
    if kind == "icon":
        sizes = [(512, 512), (150, 150), (100, 100), (64, 64)]
    else:
        sizes = [(640, 360), (320, 180), (240, 135), (160, 90)]
    blur = cv2.GaussianBlur(cv2.resize(img, sizes[0]), (0, 0), 10 if kind != "icon" else 12)
    gray = cv2.cvtColor(cv2.cvtColor(cv2.resize(img, sizes[0]), cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    if kind != "icon":
        # mark the bottom 15% band that Roblox overlays with metadata
        h = gray.shape[0]
        cv2.rectangle(gray, (0, int(h * 0.85)), (gray.shape[1] - 1, h - 1), (0, 0, 255), 2)
    panels = [(cv2.resize(img, s, interpolation=cv2.INTER_AREA), f"{s[0]}x{s[1]}") for s in sizes]
    panels += [(blur, "squint test (blurred)"), (gray, "value test (greyscale)")]
    pad, lab = 16, 26
    width = sum(p.shape[1] for p, _ in panels[:len(sizes)]) + pad * (len(sizes) + 1)
    height = sizes[0][1] * 2 + lab * 2 + pad * 3
    canvas = Image.new("RGB", (max(width, sizes[0][0] * 2 + pad * 3), height), (32, 32, 32))
    draw = ImageDraw.Draw(canvas)
    font = _font(15)
    x = pad
    for p, cap in panels[:len(sizes)]:
        canvas.paste(_to_pil(p), (x, pad + lab))
        draw.text((x, pad + 4), cap, fill=(230, 230, 230), font=font)
        x += p.shape[1] + pad
    y2 = pad * 2 + lab + sizes[0][1]
    x = pad
    for p, cap in panels[len(sizes):]:
        canvas.paste(_to_pil(p), (x, y2 + lab))
        draw.text((x, y2 + 4), cap, fill=(230, 230, 230), font=font)
        x += p.shape[1] + pad
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, optimize=True)
    return out
