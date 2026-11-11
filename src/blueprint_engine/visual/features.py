"""Image features for thumbnails and icons.

Every feature maps to a claim in the research on what makes a thumbnail work:

=====================  =====================================================================
brightness, contrast   mean / RMS of CIELAB L* (0-100): luminance contrast drives pre-attentive
                       pop-out and survives downscaling
saturation, vivid      HSV saturation; share of vivid pixels (S>0.35, V>0.25)
colorfulness           Hasler & Suesstrunk (2003) colourfulness metric
warm_share             share of vivid pixels that are red/orange/yellow
palette_top2           share of the frame covered by the two largest k-means colour clusters
                       (colour simplicity)
edge_density           Canny edge pixels / frame (clutter)
jpeg_kb                JPEG size at a fixed size and quality: a "feature complexity" proxy
                       (as used in advertising research on visual complexity)
saliency_*             attention map = mean of spectral-residual (Hou & Zhang 2007) and
                       frequency-tuned (Achanta et al. 2009) saliency: how concentrated the
                       attention map is, how many separate focal blobs it has, where it sits
faces_*                OpenCV Haar frontal-face detector: count, largest face size, position
text_*                 Tesseract OCR: large, confident words only (thumbnail-scale text)
squint_contrast        L* contrast after a heavy blur: does the value structure still read
                       when the image is tiny (a 150 px icon, a phone feed)?
bottom_saliency        attention mass in the bottom 15% (covered by player counts on Roblox)
=====================  =====================================================================
"""

from __future__ import annotations

import math
import re
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import cv2
import numpy as np

STD_THUMB = (640, 360)
STD_ICON = (360, 360)
_CASCADE: cv2.CascadeClassifier | None = None


def _cascade() -> cv2.CascadeClassifier:
    global _CASCADE
    if _CASCADE is None:
        _CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    return _CASCADE


def load_image(path: str | Path, kind: str = "thumbnail") -> np.ndarray:
    """Read as BGR; crop letterboxed 4:3 YouTube fallbacks back to their 16:9 content."""
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"cannot read image: {path}")
    h, w = img.shape[:2]
    if kind == "thumbnail" and abs(w / h - 4 / 3) < 0.02:
        nh = int(round(w * 9 / 16))
        y0 = (h - nh) // 2
        img = img[y0: y0 + nh]
    return img


def colorfulness(img: np.ndarray) -> float:
    b, g, r = (img[..., i].astype(np.float64) for i in range(3))
    rg = r - g
    yb = 0.5 * (r + g) - b
    return float(math.hypot(rg.std(), yb.std()) + 0.3 * math.hypot(rg.mean(), yb.mean()))


def spectral_residual_saliency(gray: np.ndarray, out_size: tuple[int, int]) -> np.ndarray:
    """Hou & Zhang (2007): saliency from the residual of the log amplitude spectrum."""
    small = cv2.resize(gray, (96, max(1, int(96 * gray.shape[0] / gray.shape[1]))), interpolation=cv2.INTER_AREA)
    f = np.fft.fft2(small.astype(np.float64))
    log_amp = np.log(np.abs(f) + 1e-8)
    residual = log_amp - cv2.blur(log_amp, (3, 3))
    sal = np.abs(np.fft.ifft2(np.exp(residual + 1j * np.angle(f)))) ** 2
    sal = cv2.GaussianBlur(sal, (0, 0), 2.5)
    sal = cv2.resize(sal, out_size, interpolation=cv2.INTER_LINEAR)
    sal -= sal.min()
    return sal / (sal.max() + 1e-12)


def frequency_tuned_saliency(img: np.ndarray) -> np.ndarray:
    """Achanta et al. (2009): distance of each (slightly blurred) Lab pixel from the image's mean
    Lab colour. Highlights whole uniform objects, where spectral residual only traces their edges,
    which matters for flat-shaded game renders."""
    lab = cv2.cvtColor(cv2.GaussianBlur(img, (5, 5), 0), cv2.COLOR_BGR2LAB).astype(np.float64)
    sal = np.linalg.norm(lab - lab.reshape(-1, 3).mean(axis=0), axis=2)
    sal -= sal.min()
    return sal / (sal.max() + 1e-12)


def attention_map(img: np.ndarray) -> np.ndarray:
    """Average of spectral-residual (detail/edges) and frequency-tuned (colour regions) saliency."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sr = spectral_residual_saliency(gray, (img.shape[1], img.shape[0]))
    return 0.5 * sr + 0.5 * frequency_tuned_saliency(img)


def palette(img: np.ndarray, k: int = 5, samples: int = 12000, seed: int = 7) -> list[tuple[str, float]]:
    """k-means palette in Lab: [(hex, share), ...] largest first."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
    rng = np.random.default_rng(seed)
    pts = lab[rng.choice(len(lab), size=min(samples, len(lab)), replace=False)]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    cv2.setRNGSeed(seed)
    _, labels, centers = cv2.kmeans(pts, k, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    shares = np.bincount(labels.ravel(), minlength=k) / len(labels)
    bgr = cv2.cvtColor(centers.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_LAB2BGR).reshape(-1, 3)
    out = [("#%02x%02x%02x" % (int(c[2]), int(c[1]), int(c[0])), float(s)) for c, s in zip(bgr, shares)]
    return sorted(out, key=lambda x: -x[1])


_WORD = re.compile(r"^(?:[A-Za-z]{3,}|[A-Za-z]*\d[\w$%.,]*|\$[\d.,]+[kKmMbB]?|[A-Z]{2})$")


def detect_text(img: np.ndarray, min_height_frac: float = 0.035, min_conf: float = 70.0,
                timeout_s: float = 8.0) -> list[dict[str, Any]]:
    """Large, confident words (thumbnail text is big; small OCR hits are usually texture noise)."""
    if shutil.which("tesseract") is None:
        return []
    import os

    import pytesseract

    # One OpenMP thread per tesseract process: we already parallelise across images, and
    # oversubscribed OpenMP makes each call orders of magnitude slower.
    os.environ.setdefault("OMP_THREAD_LIMIT", "1")
    h, w = img.shape[:2]
    scale = 1280 / w if w < 1280 else 1.0
    big = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC) if scale != 1.0 else img
    gray = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
    # Thumbnail text is usually heavy white (or yellow) lettering with a dark outline. A mask
    # of bright, low-saturation pixels isolates it far better than OCR on the raw photo.
    hsv = cv2.cvtColor(big, cv2.COLOR_BGR2HSV)
    white = ((hsv[..., 2] > 215) & (hsv[..., 1] < 45)).astype(np.uint8) * 255
    yellow = ((hsv[..., 0] >= 20) & (hsv[..., 0] <= 35) & (hsv[..., 1] > 120) & (hsv[..., 2] > 200)).astype(np.uint8) * 255
    kernel = np.ones((3, 3), np.uint8)
    variants = [(gray, min_conf), (255 - gray, min_conf)]
    for mask in (white, yellow):
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # drop speckle highlights
        if 0.002 < mask.mean() / 255 < 0.35:  # a mask covering a third of the frame is sky/snow, not text
            variants.append((255 - mask, min_conf - 15))
    words = []
    for variant, floor in variants:
        try:
            d = pytesseract.image_to_data(variant, config="--psm 11", output_type=pytesseract.Output.DICT,
                                          timeout=timeout_s)
        except RuntimeError:  # pytesseract raises RuntimeError on timeout
            continue
        for i, txt in enumerate(d["text"]):
            txt = (txt or "").strip()
            conf = float(d["conf"][i])
            hh = d["height"][i] / big.shape[0]
            if conf >= floor and hh >= min_height_frac and _WORD.match(txt):
                words.append({"text": txt, "conf": conf, "x": d["left"][i] / big.shape[1], "y": d["top"][i] / big.shape[0],
                              "w": d["width"][i] / big.shape[1], "h": hh})
    # de-duplicate the two passes by position
    out: list[dict[str, Any]] = []
    for wd in sorted(words, key=lambda x: -x["conf"]):
        if not any(abs(wd["x"] - o["x"]) < 0.02 and abs(wd["y"] - o["y"]) < 0.02 for o in out):
            out.append(wd)
    return out


@dataclass
class Features:
    width: int
    height: int
    brightness: float
    contrast: float
    saturation: float
    vivid_share: float
    colorfulness: float
    warm_share: float
    hue_entropy: float
    palette_top2: float
    palette: list[tuple[str, float]]
    edge_density: float
    jpeg_kb: float
    saliency_concentration: float
    focal_points: int
    saliency_cx: float
    saliency_cy: float
    bottom_saliency: float
    squint_contrast: float
    faces: int
    face_area_max: float
    face_area_total: float
    face_cx: float | None
    text_words: int
    text_area: float
    text_has_number: bool
    text: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


NUMERIC_FEATURES = (
    "brightness", "contrast", "saturation", "vivid_share", "colorfulness", "warm_share", "hue_entropy",
    "palette_top2", "edge_density", "jpeg_kb", "saliency_concentration", "focal_points", "bottom_saliency",
    "squint_contrast", "faces", "face_area_max", "text_words", "text_area",
)


def extract(img: np.ndarray, kind: str = "thumbnail", text: bool = True) -> Features:
    h0, w0 = img.shape[:2]
    std = cv2.resize(img, STD_THUMB if kind == "thumbnail" else STD_ICON, interpolation=cv2.INTER_AREA)
    sw, sh = std.shape[1], std.shape[0]

    lab = cv2.cvtColor(std, cv2.COLOR_BGR2LAB).astype(np.float64)
    L = lab[..., 0] * 100.0 / 255.0
    hsv = cv2.cvtColor(std, cv2.COLOR_BGR2HSV).astype(np.float64)
    H, S, V = hsv[..., 0] * 2.0, hsv[..., 1] / 255.0, hsv[..., 2] / 255.0
    vivid = (S > 0.35) & (V > 0.25)
    nviv = max(int(vivid.sum()), 1)
    warm = vivid & ((H < 50) | (H >= 330))
    hist = np.histogram(H[vivid], bins=12, range=(0, 360))[0].astype(np.float64)
    p = hist / max(hist.sum(), 1)
    entropy = float(-(p[p > 0] * np.log(p[p > 0])).sum() / math.log(12)) if hist.sum() else 0.0
    pal = palette(std)

    gray = cv2.cvtColor(std, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    ok, enc = cv2.imencode(".jpg", std, [cv2.IMWRITE_JPEG_QUALITY, 80])

    sal = attention_map(std)
    flat = np.sort(sal.ravel())[::-1]
    conc = float(flat[: len(flat) // 10].sum() / (flat.sum() + 1e-12))
    thr = sal.mean() + 2 * sal.std()
    # Spectral residual responds to edges, so one object can light up as several arcs along
    # its outline; closing merges fragments within ~6% of the frame width into one region.
    k = max(3, int(sw * 0.06)) | 1
    hot = cv2.morphologyEx((sal > thr).astype(np.uint8), cv2.MORPH_CLOSE,
                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    n, _, stats, _ = cv2.connectedComponentsWithStats(hot, 8)
    blobs = int(sum(1 for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= 0.005 * sw * sh))
    ys, xs = np.mgrid[0:sh, 0:sw]
    mass = sal.sum() + 1e-12
    cx, cy = float((sal * xs).sum() / mass / sw), float((sal * ys).sum() / mass / sh)
    bottom = float(sal[int(sh * 0.85):].sum() / mass)

    blurred = cv2.GaussianBlur(std, (0, 0), 10)
    squint = float((cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float64) * 100 / 255).std())

    faces = _cascade().detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(int(sh * 0.08),) * 2)
    areas = [fw * fh / (sw * sh) for (_, _, fw, fh) in faces] if len(faces) else []
    face_cx = None
    if len(faces):
        x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        face_cx = float((x + fw / 2) / sw)

    words = detect_text(img) if text else []
    return Features(
        width=w0, height=h0,
        brightness=round(float(L.mean()), 2), contrast=round(float(L.std()), 2),
        saturation=round(float(S.mean()), 3), vivid_share=round(float(vivid.mean()), 3),
        colorfulness=round(colorfulness(std), 2), warm_share=round(float(warm.sum() / nviv), 3),
        hue_entropy=round(entropy, 3), palette_top2=round(pal[0][1] + pal[1][1], 3), palette=pal,
        edge_density=round(float(edges.mean() / 255.0), 4), jpeg_kb=round(len(enc) / 1024, 1) if ok else 0.0,
        saliency_concentration=round(conc, 3), focal_points=blobs, saliency_cx=round(cx, 3), saliency_cy=round(cy, 3),
        bottom_saliency=round(bottom, 3), squint_contrast=round(squint, 2),
        faces=len(areas), face_area_max=round(max(areas, default=0.0), 4), face_area_total=round(sum(areas), 4),
        face_cx=round(face_cx, 3) if face_cx is not None else None,
        text_words=len(words), text_area=round(sum(w["w"] * w["h"] for w in words), 4),
        text_has_number=any(re.search(r"\d|\$", w["text"]) for w in words),
        text=[w["text"] for w in words],
    )
