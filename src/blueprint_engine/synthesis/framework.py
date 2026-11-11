"""Render the prompt framework with research evidence injected into every template."""

from __future__ import annotations

from pathlib import Path

from blueprint_engine.analysis.llm import taxonomy_text
from blueprint_engine.analysis.taxonomy import TAXONOMY
from blueprint_engine.prompts import PromptTemplate, load_templates, render
from blueprint_engine.synthesis.blueprint import Blueprint
from blueprint_engine.synthesis.report import fmt_ts


def _cite_short(e) -> str:
    where = f" @ {fmt_ts(e.start)}" if e.start is not None else ""
    who = f"{e.author}, " if e.author and e.kind != "doc" else ""
    return f"{who}“{e.title}”{where} <{e.link}>"


def evidence_digest(bp: Blueprint, pillar: str, mechanics: int = 6, quotes: int = 2) -> str:
    p = bp.pillar(pillar)
    if not p or not p.mechanics:
        return "(no research evidence collected for this pillar yet - run `bpe run`)"
    lines = []
    for f in [m for m in p.mechanics if m.priority in ("P0", "P1")][:mechanics]:
        docs = f", {len(f.doc_support)} first-party doc(s)" if f.doc_support else ""
        lines.append(f"- **{f.label}** — {f.priority}, taught by {f.support} source(s){docs}")
        for e in f.evidence[:quotes]:
            lines.append(f"  - \"{e.tactic or e.quote}\" — {_cite_short(e)}")
        if f.metrics:
            lines.append(f"  - Numbers cited: {'; '.join(f.metrics[:4])}")
        for s in f.stale_flags:
            lines.append(f"  - WARNING (platform change): {s}")
    return "\n".join(lines)


def playbook_digest(bp: Blueprint, pillar: str, mechanics: int = 6) -> str:
    p = bp.pillar(pillar)
    if not p:
        return "(none)"
    lines = []
    for f in [m for m in p.mechanics if m.priority in ("P0", "P1") and m.playbook][:mechanics]:
        lines.append(f"- **{f.label}**: " + " ".join(f.playbook["build"]))
        if f.playbook.get("apis"):
            lines.append(f"  - APIs: {', '.join(f.playbook['apis'])}")
        if f.playbook.get("kpis"):
            lines.append(f"  - Measure: {'; '.join(f.playbook['kpis'])}")
    return "\n".join(lines) or "(none)"


def research_summary(bp: Blueprint) -> str:
    t = bp.totals
    lines = [f"{t['sources']} sources ({', '.join(f'{n} {k}' for k, n in t['by_kind'].items())}), "
             f"{t['words_analyzed']:,} words, {t['insights']:,} extracted insights. Highest-consensus mechanics:"]
    for p in bp.pillars:
        top = [f.label for f in p.mechanics if f.priority == "P0"][:4]
        if top:
            lines.append(f"- {p.label}: {', '.join(top)}")
    return "\n".join(lines)


def notices_text(bp: Blueprint) -> str:
    if not bp.platform_notices:
        return "(none detected)"
    return "\n".join(f"- {n['text']} ({n['url']})" for n in bp.platform_notices)


def variables_from_blueprint(bp: Blueprint) -> dict[str, str]:
    v = {
        "research_summary": research_summary(bp),
        "platform_notices": notices_text(bp),
        "taxonomy": taxonomy_text(TAXONOMY),
    }
    for p in bp.pillars:
        v[f"evidence_{p.pillar}"] = evidence_digest(bp, p.pillar)
        v[f"playbook_{p.pillar}"] = playbook_digest(bp, p.pillar)
    return v


def write_framework(bp: Blueprint, out_dir: Path, extra: dict[str, str] | None = None) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    variables = {**variables_from_blueprint(bp), **(extra or {})}
    templates = sorted(load_templates().values(), key=lambda t: (t.order, t.name))
    written: list[Path] = []
    index = [
        "# Game Design Prompt Framework",
        "",
        f"Rendered from the research run of {bp.generated_at}. Each prompt below already contains the relevant",
        "research evidence (quotes with deep links) and the curated Roblox playbook. `{{slots}}` that remain are",
        "for you to fill in: your concept, metrics or spec.",
        "",
        "**How to use:** paste `00-architect-system.md` as the system prompt, then one task prompt as the user",
        "message. Chain them: concept → core loop → onboarding → retention → monetization → implementation spec",
        "→ analytics → red-team review. Re-render after every research run: `bpe prompts render --all`.",
        "",
        "| # | Prompt | Stage | You fill in |",
        "|---|---|---|---|",
    ]
    for t in templates:
        text, missing = render(t, variables)
        fname = f"{t.path.stem if t.path else t.name}.md"
        header = f"<!-- {t.title} · stage: {t.stage} · unfilled slots: {', '.join(missing) or 'none'} -->\n\n"
        (out_dir / fname).write_text(header + text, encoding="utf-8")
        written.append(out_dir / fname)
        index.append(f"| {t.order:02d} | [{t.title}]({fname}) — {t.description} | {t.stage} | "
                     f"{', '.join(f'`{m}`' for m in missing) or '–'} |")
    (out_dir / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    written.append(out_dir / "README.md")
    return written


def render_one(template: PromptTemplate, bp: Blueprint | None, extra: dict[str, str]) -> tuple[str, list[str]]:
    variables = variables_from_blueprint(bp) if bp else {}
    variables.update(extra)
    return render(template, variables)
