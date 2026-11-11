"""Score a Roblox thumbnail or icon draft against platform specs and a benchmark.

Checks come from three places, and each one says which:
  [Roblox]    create.roblox.com/docs: 16:9 at 1920x1080 (<3 MB) for thumbnails, square
              >=512 px for icons (shown down to ~150 px), keep the bottom strip clear,
              unambiguous imagery, no promotional claims.
  [Benchmark] where the draft sits among MrBeast's 2022+ thumbnails (reports/thumbnails/
              benchmark.json), plus the composition patterns that tracked performance there.
  [Research]  attention science: few focal points, legible at small size, faces/text draw gaze.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from blueprint_engine.visual.features import Features, extract, load_image
from blueprint_engine.visual.sheets import preview_sheet

# Promotional wording Roblox rejects in video thumbnails; risky in image thumbnails too.
_CLAIMS = re.compile(r"\b(?:free|robux|ugc|giveaway|%|off|sale|discount|promo|code|admin)\b", re.I)


@dataclass
class Check:
    level: str  # pass | warn | fail | info
    source: str  # Roblox | Benchmark | Research
    message: str


def _position(value: float, pct: dict[str, float]) -> str:
    if value < pct["p10"]:
        return "below p10"
    for lo, hi in (("p10", "p25"), ("p25", "p50"), ("p50", "p75"), ("p75", "p90")):
        if value < pct[hi]:
            return f"{lo}-{hi}"
    return "above p90"


def score(path: str | Path, kind: str = "thumbnail", benchmark: dict[str, Any] | None = None,
          preview: str | Path | None = None) -> dict[str, Any]:
    if kind not in ("thumbnail", "icon"):
        raise ValueError("kind must be 'thumbnail' or 'icon'")
    path = Path(path)
    img = load_image(path, kind="raw")
    h, w = img.shape[:2]
    f: Features = extract(img, kind)
    bench = (benchmark or {}).get("benchmark_recent", {})
    checks: list[Check] = []
    add = lambda level, source, msg: checks.append(Check(level, source, msg))  # noqa: E731

    # ---- platform format -------------------------------------------------------------
    size_mb = path.stat().st_size / 1_048_576
    if kind == "thumbnail":
        if abs(w / h - 16 / 9) > 0.01:
            add("fail", "Roblox", f"aspect {w}x{h} is not 16:9 - Roblox stretches thumbnails to 16:9")
        if w < 1920 or h < 1080:
            add("warn", "Roblox", f"{w}x{h} is below the recommended 1920x1080")
        else:
            add("pass", "Roblox", f"{w}x{h}, 16:9")
        if size_mb >= 3:
            add("fail", "Roblox", f"{size_mb:.1f} MB - thumbnail uploads must stay under 3 MB")
        if f.bottom_saliency > 0.2:
            add("warn", "Roblox", f"{f.bottom_saliency:.0%} of visual attention sits in the bottom 15%, "
                                   "which Roblox can cover with metadata such as the player count")
    else:
        if w != h:
            add("fail", "Roblox", f"icon is {w}x{h}; it must be square")
        if min(w, h) < 512:
            add("warn", "Roblox", f"icon is {min(w, h)} px; upload at least 512x512")
        else:
            add("pass", "Roblox", f"{w}x{h} square")
        off = max(abs(f.saliency_cx - 0.5), abs(f.saliency_cy - 0.5))
        if off > 0.18:
            add("warn", "Research", "the main subject sits off-centre; icons are cropped and shrunk to ~150 px, "
                                     "so centre one large subject")

    # ---- composition (what tracked performance) --------------------------------------
    if f.focal_points >= 4:
        add("warn", "Benchmark", f"{f.focal_points} separate focal regions. In MrBeast's 2022+ thumbnails, 4+ regions "
                                 "had a median outlier of x0.92 vs x1.14 for 0-1. Cut to one idea.")
    elif f.focal_points <= 1:
        add("pass", "Benchmark", "one dominant focal region")
    else:
        add("info", "Benchmark", f"{f.focal_points} focal regions - fine for a deliberate A-vs-B contrast, otherwise simplify")

    if f.faces >= 3:
        add("warn", "Benchmark", f"{f.faces} faces detected; crowded group shots underperformed (3+ faces median x0.83 "
                                 "vs x1.05 for one face). Feature one or two characters large.")
    add("info", "Research", "faces draw gaze far more than matched regions (Cerf et al. 2009). Roblox avatar faces "
                            "are not reliably detected here - judge by eye: is one character's expression "
                            "readable at 150 px?")

    if f.text_words > 3:
        add("warn", "Benchmark", f"~{f.text_words} words of overlay text detected ({' '.join(f.text[:6])}). MrBeast-style "
                                 "text is 1-2 tokens, usually a number ('DAY 97', '$1M'); Roblox asks for text sparingly.")
    elif 1 <= f.text_words <= 2:
        add("pass", "Benchmark", f"short overlay text ({' '.join(f.text)}): 1-2 tokens tracked x1.12 vs x0.92 with none")
    claims = [t for t in f.text if _CLAIMS.search(t)]
    if claims:
        add("fail", "Roblox", f"promotional wording detected ({', '.join(claims)}); Roblox rejects claims like "
                              "'50% off' or 'Free UGC!' in video thumbnails - keep images claim-free too")

    # ---- colour, contrast, legibility vs benchmark -----------------------------------
    for feat, label, low_msg in (
        ("colorfulness", "colourfulness", "flatter than most benchmark thumbnails; push saturated, contrasting hues"),
        ("saturation", "saturation", "muted; benchmark thumbnails are saturated"),
        ("squint_contrast", "squint contrast", "light/dark structure fades when small; separate subject and background by value"),
    ):
        if feat in bench:
            pos = _position(getattr(f, feat), bench[feat])
            if pos in ("below p10", "p10-p25"):
                add("warn", "Benchmark", f"{label} {getattr(f, feat)} is {pos} of MrBeast 2022+: {low_msg}")
            else:
                add("pass", "Benchmark", f"{label} {getattr(f, feat)} ({pos} of MrBeast 2022+)")
    if "edge_density" in bench and _position(f.edge_density, bench["edge_density"]) == "above p90":
        add("warn", "Research", "very busy detail (edge density above p90 of the benchmark): dense perceptual detail "
                                "lowers attention to the message (Pieters, Wedel & Batra 2010)")

    out_preview = None
    if preview:
        out_preview = str(preview_sheet(img, kind, preview))
    order = {"fail": 0, "warn": 1, "info": 2, "pass": 3}
    checks.sort(key=lambda c: order[c.level])
    return {
        "file": str(path), "kind": kind, "size": [w, h], "size_mb": round(size_mb, 2),
        "features": {k: v for k, v in f.to_dict().items() if k != "palette"}, "palette": f.palette,
        "checks": [asdict(c) for c in checks],
        "summary": {lvl: sum(1 for c in checks if c.level == lvl) for lvl in order},
        "preview": out_preview,
    }


def format_report(result: dict[str, Any]) -> str:
    icon = {"fail": "FAIL", "warn": "WARN", "info": "info", "pass": " ok "}
    lines = [f"{result['file']}  ({result['kind']}, {result['size'][0]}x{result['size'][1]}, {result['size_mb']} MB)", ""]
    for c in result["checks"]:
        lines.append(f"[{icon[c['level']]}] ({c['source']}) {c['message']}")
    pal = "  ".join(f"{hx} {share:.0%}" for hx, share in result["palette"])
    lines += ["", f"palette: {pal}"]
    if result["preview"]:
        lines.append(f"preview sheet: {result['preview']}  (real display sizes + squint + greyscale tests)")
    return "\n".join(lines)
