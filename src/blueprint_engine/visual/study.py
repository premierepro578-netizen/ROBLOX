"""Study a channel's thumbnails: download, measure, relate to performance.

Performance is measured as an *outlier ratio*: a video's views divided by the median views
of its 20 chronological neighbours (10 before, 10 after). That controls for channel growth
over time, so a 2018 video and a 2025 video are judged against what the channel was doing
at the time. Videos younger than ``min_age_days`` are excluded (views still accruing).
"""

from __future__ import annotations

import json
import logging
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import requests

from blueprint_engine.net import RateLimiter, make_session
from blueprint_engine.pipeline import parallel
from blueprint_engine.store import Store
from blueprint_engine.visual.features import NUMERIC_FEATURES, extract, load_image

log = logging.getLogger(__name__)
THUMB_VARIANTS = ("maxresdefault.jpg", "hq720.jpg", "sddefault.jpg", "hqdefault.jpg")


def list_channel(url: str, limit: int) -> dict[str, Any]:
    """Uploads (newest first) via yt-dlp's channel listing, with approximate upload times.

    The listing uses YouTube's browse endpoint, which keeps working when per-video watch
    pages sit behind a bot check.
    """
    from yt_dlp import YoutubeDL

    opts = {"quiet": True, "no_warnings": True, "skip_download": True, "extract_flat": "in_playlist",
            "playlistend": limit, "extractor_args": {"youtubetab": {"approximate_date": [""]}}}
    with YoutubeDL(opts) as ydl:
        res = ydl.extract_info(url, download=False) or {}
    entries = [e for e in res.get("entries") or [] if e and e.get("id")]
    return {
        "channel": res.get("channel"), "followers": res.get("channel_follower_count"),
        "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "url": url,
        "entries": [{k: e.get(k) for k in ("id", "title", "view_count", "duration", "timestamp")} for e in entries],
    }


def download_thumbnail(video_id: str, out_dir: Path, session: requests.Session, limiter: RateLimiter) -> Path:
    out = out_dir / f"{video_id}.jpg"
    if out.is_file() and out.stat().st_size > 2000:
        return out
    for variant in THUMB_VARIANTS:
        limiter.wait()
        r = session.get(f"https://i.ytimg.com/vi/{video_id}/{variant}", timeout=30)
        # YouTube serves a 120x90 grey placeholder (HTTP 404) for missing variants.
        if r.status_code == 200 and len(r.content) > 2000:
            out.write_bytes(r.content)
            return out
    raise FileNotFoundError(f"no thumbnail for {video_id}")


def outlier_ratios(views: list[float], window: int = 10) -> list[float | None]:
    """views[i] / median(views of the ``window`` uploads on each side), in upload order."""
    out: list[float | None] = []
    for i, v in enumerate(views):
        nb = [views[j] for j in range(max(0, i - window), min(len(views), i + window + 1)) if j != i and views[j]]
        out.append(v / float(np.median(nb)) if v and nb else None)
    return out


def rankdata(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(len(x), dtype=np.float64)
    ranks[order] = np.arange(1, len(x) + 1)
    # average ties
    vals, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
    sums = np.bincount(inv, weights=ranks)
    return (sums / counts)[inv]


def spearman(x: np.ndarray, y: np.ndarray, permutations: int = 2000, seed: int = 11) -> tuple[float, float]:
    """Spearman rho and a two-sided permutation p-value."""
    rx, ry = rankdata(x), rankdata(y)
    rx, ry = rx - rx.mean(), ry - ry.mean()
    denom = math.sqrt((rx ** 2).sum() * (ry ** 2).sum()) or 1.0
    rho = float((rx * ry).sum() / denom)
    rng = np.random.default_rng(seed)
    hits = sum(1 for _ in range(permutations) if abs(float((rx * rng.permutation(ry)).sum() / denom)) >= abs(rho))
    return rho, (hits + 1) / (permutations + 1)


def run_study(channel_url: str, data_dir: str | Path, *, limit: int = 400, workers: int = 6,
              min_age_days: int = 30, refresh_listing: bool = False) -> dict[str, Any]:
    root = Path(data_dir)
    store = Store(root)
    img_dir = root / "img"
    img_dir.mkdir(parents=True, exist_ok=True)

    listing = None if refresh_listing else store.get("state", "listing")
    if not listing or listing.get("url") != channel_url:
        listing = list_channel(channel_url, limit)
        store.put("state", "listing", listing)
    entries = listing["entries"][:limit]

    session, limiter = make_session(), RateLimiter(0.05)
    paths: dict[str, Path] = {}
    for vid, path, err in parallel(lambda e: (e["id"], download_thumbnail(e["id"], img_dir, session, limiter)),
                                   entries, workers):
        if err is None:
            paths[path[0]] = path[1]

    def feat(e: dict[str, Any]) -> dict[str, Any]:
        hit = store.get("features", e["id"])
        if hit:
            return hit
        f = extract(load_image(paths[e["id"]]), "thumbnail").to_dict()
        store.put("features", e["id"], f)
        return f

    feats: dict[str, dict[str, Any]] = {}
    for e, f, err in parallel(feat, [e for e in entries if e["id"] in paths], workers):
        if err is None:
            feats[e["id"]] = f
        else:
            log.debug("features failed for %s: %s", e["id"], err)

    # chronological order (oldest first) for the neighbour baseline
    chron = list(reversed(entries))
    ratios = outlier_ratios([float(e.get("view_count") or 0) for e in chron])
    now = time.time()
    rows = []
    for e, ratio in zip(chron, ratios):
        if e["id"] not in feats or ratio is None:
            continue
        ts = e.get("timestamp")
        age = (now - ts) / 86400 if ts else None
        rows.append({
            "id": e["id"], "title": e.get("title"), "views": e.get("view_count"), "duration": e.get("duration"),
            "year": datetime.fromtimestamp(ts, timezone.utc).year if ts else None,
            "age_days": round(age) if age is not None else None, "outlier": round(ratio, 3),
            "eligible": age is None or age >= min_age_days, **feats[e["id"]],
        })
    return {"channel": listing.get("channel"), "followers": listing.get("followers"), "fetched": listing.get("fetched"),
            "url": channel_url, "rows": rows, "analysed": len(rows)}


def summarize(study: dict[str, Any], recent_from_year: int = 2022, permutations: int = 10000) -> dict[str, Any]:
    rows = [r for r in study["rows"] if r["eligible"]]
    y = np.log2(np.array([r["outlier"] for r in rows]))
    corr = {}
    for f in NUMERIC_FEATURES:
        x = np.array([float(r[f]) for r in rows])
        if np.ptp(x) == 0:
            continue
        rho, p = spearman(x, y, permutations=permutations)
        q = np.quantile(y, [0.25, 0.75])
        top = x[y >= q[1]]
        bottom = x[y <= q[0]]
        corr[f] = {"rho": round(rho, 3), "p": round(p, 4), "top_quartile_median": round(float(np.median(top)), 4),
                   "bottom_quartile_median": round(float(np.median(bottom)), 4)}

    def pct(sub: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
        out = {}
        for f in NUMERIC_FEATURES:
            x = np.array([float(r[f]) for r in sub])
            if len(x):
                out[f] = {k: round(float(np.quantile(x, q)), 4) for k, q in
                          (("p10", .1), ("p25", .25), ("p50", .5), ("p75", .75), ("p90", .9))}
        return out

    years = sorted({r["year"] for r in study["rows"] if r["year"]})
    by_year = {}
    for yr in years:
        sub = [r for r in study["rows"] if r["year"] == yr]
        by_year[yr] = {"n": len(sub), **{f: round(float(np.median([float(r[f]) for r in sub])), 4) for f in NUMERIC_FEATURES},
                       "share_with_face": round(sum(1 for r in sub if r["faces"]) / len(sub), 3),
                       "share_with_text": round(sum(1 for r in sub if r["text_words"]) / len(sub), 3)}
    recent = [r for r in study["rows"] if (r["year"] or 0) >= recent_from_year]
    recent_eligible = [r for r in recent if r["eligible"]]
    yr = np.log2(np.array([r["outlier"] for r in recent_eligible]))
    corr_recent = {}
    for f in NUMERIC_FEATURES:
        x = np.array([float(r[f]) for r in recent_eligible])
        if len(x) > 10 and np.ptp(x) > 0:
            rho, p = spearman(x, yr, permutations=permutations)
            corr_recent[f] = {"rho": round(rho, 3), "p": round(p, 4)}
    return {
        "channel": study["channel"], "followers": study["followers"], "fetched": study["fetched"],
        "n_analysed": study["analysed"], "n_eligible": len(rows), "recent_from_year": recent_from_year,
        "correlations_with_log2_outlier": corr, "correlations_recent": corr_recent, "by_year": by_year,
        "benchmark_all": pct(study["rows"]), "benchmark_recent": pct(recent),
        "n_recent": len(recent),
    }


def save(study: dict[str, Any], summary: dict[str, Any], out_dir: str | Path) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    slim = [{k: r[k] for k in ("id", "title", "views", "year", "outlier", *NUMERIC_FEATURES, "text", "palette")}
            for r in study["rows"]]
    (out / "dataset.json").write_text(json.dumps({**{k: study[k] for k in ("channel", "followers", "fetched", "url")},
                                                  "rows": slim}, indent=1), encoding="utf-8")
    (out / "benchmark.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
