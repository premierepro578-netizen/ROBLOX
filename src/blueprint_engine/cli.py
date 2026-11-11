"""``bpe`` command line.

    bpe run                         # discover -> fetch -> analyze -> synthesize
    bpe discover | fetch | analyze | synthesize
    bpe analyze --extractor claude  # higher-quality extraction (needs Anthropic credentials)
    bpe status
    bpe prompts list
    bpe prompts render core-loop-designer --var game_concept="pet battler"
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from blueprint_engine import __version__
from blueprint_engine.config import load_config

DEFAULT_CONFIG = "config/research.toml"


def _pipeline(args):
    from blueprint_engine.pipeline import Pipeline

    return Pipeline(load_config(args.config), args.data, workers=args.workers, refresh=args.refresh)


def _print(rep) -> None:
    print(rep.summary())
    for note in rep.notes[:12]:
        print(f"    note: {note}")
    if len(rep.notes) > 12:
        print(f"    ... {len(rep.notes) - 12} more notes")


def cmd_discover(args) -> int:
    _print(_pipeline(args).discover())
    return 0


def cmd_fetch(args) -> int:
    _print(_pipeline(args).fetch())
    return 0


def cmd_analyze(args) -> int:
    _print(_pipeline(args).analyze(args.extractor, model=args.model, effort=args.effort))
    return 0


def cmd_synthesize(args) -> int:
    _print(_pipeline(args).synthesize(args.reports, extractor=args.use))
    print(f"wrote {args.reports}/evidence-report.md, blueprint.json, prompt-framework/")
    return 0


def cmd_run(args) -> int:
    p = _pipeline(args)
    for rep in (p.discover(), p.fetch()):
        _print(rep)
    _print(p.analyze("heuristic"))
    if args.extractor == "claude":
        _print(p.analyze("claude", model=args.model, effort=args.effort))
    _print(p.synthesize(args.reports, extractor="best"))
    print(f"done -> {args.reports}/evidence-report.md")
    return 0


def cmd_status(args) -> int:
    from blueprint_engine.store import Store

    s = Store(args.data)
    cands = s.get("state", "candidates", {}) or {}
    print(f"candidates: youtube={len(cands.get('youtube', {}))} tiktok={len(cands.get('tiktok', []))} "
          f"devforum={len(cands.get('devforum', {}))}")
    for col in ("yt_info", "documents", "sources", "insights", "doc_cache", "tt_cache"):
        print(f"{col:>10}: {s.count(col)}")
    return 0


def cmd_prompts(args) -> int:
    from blueprint_engine.prompts import load_templates
    from blueprint_engine.synthesis.framework import render_one, write_framework

    templates = load_templates()
    if args.prompts_cmd == "list":
        for t in sorted(templates.values(), key=lambda t: t.order):
            print(f"{t.order:02d}  {t.name:<28} [{t.stage}] {t.description}")
            print(f"    slots: {', '.join(t.variables) or '-'}")
        return 0

    bp = None
    bp_path = Path(args.reports) / "blueprint.json"
    if bp_path.is_file():
        bp = _load_blueprint(bp_path)
    extra = dict(v.split("=", 1) for v in args.var or [])
    kf = Path(args.config).parent / "key-findings.md"
    if args.all:
        if bp is None:
            print("no blueprint.json yet - run `bpe synthesize` first", file=sys.stderr)
            return 1
        out = Path(args.out or Path(args.reports) / "prompt-framework")
        for p in write_framework(bp, out, extra, key_findings_path=kf):
            print(p)
        return 0
    if not args.name or args.name not in templates:
        print(f"unknown prompt {args.name!r}; try `bpe prompts list`", file=sys.stderr)
        return 1
    text, missing = render_one(templates[args.name], bp, extra, key_findings_path=kf)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    if missing:
        print(f"\n[unfilled slots: {', '.join(missing)} - pass --var name=value]", file=sys.stderr)
    return 0


def _load_blueprint(path: Path):
    from blueprint_engine.synthesis.blueprint import Blueprint, Evidence, MechanicFinding, PillarFinding

    d = json.loads(path.read_text(encoding="utf-8"))
    pillars = []
    for p in d["pillars"]:
        mechs = [MechanicFinding(**{**m, "evidence": [Evidence(**e) for e in m["evidence"]]}) for m in p["mechanics"]]
        pillars.append(PillarFinding(**{**p, "mechanics": mechs}))
    return Blueprint(**{**d, "pillars": pillars})


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="bpe", description="Game-design research -> implementation blueprints")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--data", default="data", help="cache directory (raw transcripts live here)")
    ap.add_argument("--reports", default="reports", help="output directory for reports and prompts")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--refresh", action="store_true", help="ignore caches and re-fetch")
    ap.add_argument("-v", "--verbose", action="count", default=0)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("discover", help="search for candidate sources").set_defaults(fn=cmd_discover)
    sub.add_parser("fetch", help="metadata, ranking, transcripts, docs").set_defaults(fn=cmd_fetch)

    def llm_opts(p):
        p.add_argument("--extractor", choices=("heuristic", "claude"), default="heuristic")
        p.add_argument("--model", default=None, help="Claude model id (default claude-opus-5-5)")
        p.add_argument("--effort", default="medium", choices=("low", "medium", "high", "xhigh", "max"))

    a = sub.add_parser("analyze", help="extract insights from fetched sources")
    llm_opts(a)
    a.set_defaults(fn=cmd_analyze)

    s = sub.add_parser("synthesize", help="blueprint + evidence report + prompt framework")
    s.add_argument("--use", choices=("best", "heuristic", "claude"), default="best")
    s.set_defaults(fn=cmd_synthesize)

    r = sub.add_parser("run", help="all stages")
    llm_opts(r)
    r.set_defaults(fn=cmd_run)

    sub.add_parser("status", help="cache counts").set_defaults(fn=cmd_status)

    pr = sub.add_parser("prompts", help="list or render prompt templates")
    pr.add_argument("prompts_cmd", choices=("list", "render"))
    pr.add_argument("name", nargs="?")
    pr.add_argument("--all", action="store_true", help="render every template into the framework folder")
    pr.add_argument("--var", action="append", help="fill a slot: --var game_concept='...'")
    pr.add_argument("--out", default=None)
    pr.set_defaults(fn=cmd_prompts)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    level = logging.WARNING - 10 * min(args.verbose, 2)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")
    try:
        return args.fn(args)
    except KeyboardInterrupt:
        return 130
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
