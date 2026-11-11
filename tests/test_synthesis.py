from pathlib import Path

from blueprint_engine.config import load_config
from blueprint_engine.models import Document, Insight, Segment, Source
from blueprint_engine.prompts import load_templates, parse_template, render
from blueprint_engine.synthesis.blueprint import build_blueprint, excerpt
from blueprint_engine.synthesis.framework import write_framework
from blueprint_engine.synthesis.report import render_report

ROOT = Path(__file__).resolve().parents[1]


def _fixture():
    cfg = load_config(ROOT / "config" / "research.toml")
    sources = {
        "yt:a": Source("yt:a", "youtube", "https://www.youtube.com/watch?v=a", "Retention A", "Chan A", score=0.8, pillars=["retention"]),
        "yt:b": Source("yt:b", "youtube", "https://www.youtube.com/watch?v=b", "Retention B", "Chan B", score=0.5, pillars=["retention"]),
        "yt:c": Source("yt:c", "youtube", "https://www.youtube.com/watch?v=c", "Monetize C", "Chan C", score=0.6, pillars=["monetization"]),
        "doc:r": Source("doc:r", "doc", "https://create.roblox.com/docs/r", "Retention", "Roblox Creator Docs", score=0.75, pillars=["retention"]),
        "doc:p": Source("doc:p", "doc", "https://create.roblox.com/docs/p", "Engagement-based payouts", "Roblox Creator Docs", score=0.75, pillars=["monetization"]),
    }

    def ins(sid, pillar, mech, text, start=12.0, a=0.8):
        return Insight(sid, pillar, [mech], text, start, a, [])

    insights = [
        ins("yt:a", "retention", "daily_rewards", "Add a daily reward streak so players come back."),
        ins("yt:a", "retention", "daily_rewards", "Show tomorrow's reward to build intent.", 40.0),
        ins("yt:b", "retention", "daily_rewards", "Daily login rewards are the easiest retention win."),
        ins("doc:r", "retention", "daily_rewards", "Track D1 retention by cohort.", None, 0.5),
        ins("yt:b", "retention", "social", "Reward playing with friends."),
        ins("yt:c", "monetization", "premium_payouts", "Make money from premium payouts by keeping Premium players longer."),
    ]
    documents = {
        "doc:p": Document("doc:p", "html", "en", [Segment("Effective July 24, 2025, the Engagement-Based Payouts program is deprecated and has been replaced by the Creator Rewards program.")]),
    }
    return cfg, sources, insights, documents


def test_blueprint_consensus_priority_and_stale_flags():
    cfg, sources, insights, documents = _fixture()
    bp = build_blueprint(cfg, sources, insights, documents, extractor="heuristic")
    ret = bp.pillar("retention")
    daily = next(m for m in ret.mechanics if m.mechanic == "daily_rewards")
    assert daily.support == 3 and daily.media_support == 2 and daily.doc_support == ["Retention"]
    assert daily.priority == "P0"
    assert ret.mechanics[0].mechanic == "daily_rewards"  # highest weight first
    assert daily.playbook and daily.playbook["apis"]
    # Evidence is diverse: one quote per source before repeats.
    assert len({e.source_id for e in daily.evidence}) == len(daily.evidence)
    assert daily.evidence[0].link.endswith("&t=12s")

    mon = bp.pillar("monetization")
    payouts = next(m for m in mon.mechanics if m.mechanic == "premium_payouts")
    assert payouts.stale_flags and "Creator Rewards" in payouts.stale_flags[0]
    assert any("deprecated" in n["text"] for n in bp.platform_notices)


def test_report_and_framework_render(tmp_path):
    cfg, sources, insights, documents = _fixture()
    bp = build_blueprint(cfg, sources, insights, documents, extractor="heuristic")
    md = render_report(bp)
    assert "# Game Design Research — Evidence Report" in md
    assert "Daily rewards & streaks" in md and "⚠️" in md

    written = write_framework(bp, tmp_path / "pf")
    names = {p.name for p in written}
    assert "README.md" in names and "31-retention-systems.md" in names
    retention_prompt = (tmp_path / "pf" / "31-retention-systems.md").read_text()
    assert "Add a daily reward streak" in retention_prompt  # evidence injected
    assert "{{game_concept}}" in retention_prompt  # designer slots preserved
    assert "{{evidence_retention}}" not in retention_prompt


def test_template_parsing_and_render_reports_missing():
    t = parse_template("---\nname: x\ntitle: X\ninputs: a, b\n---\nHello {{a}} and {{ b }}.\n")
    text, missing = render(t, {"a": "A"})
    assert text.strip() == "Hello A and {{ b }}." and missing == ["b"] and t.inputs == ["a", "b"]


def test_all_templates_have_metadata():
    templates = load_templates()
    assert {"architect-system", "extract-insights", "core-loop-designer", "retention-systems", "onboarding-ftue",
            "monetization-design", "luau-implementation-spec", "design-review-redteam"} <= set(templates)
    for t in templates.values():
        assert t.title and t.description and t.stage


def test_excerpt_truncates():
    assert excerpt("word " * 100).endswith("…")
    assert excerpt("short quote") == "short quote"
