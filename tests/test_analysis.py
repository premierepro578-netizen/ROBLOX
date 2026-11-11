from datetime import date

from blueprint_engine.analysis.extract import actionability, extract_insights, metric_mentions
from blueprint_engine.analysis.taxonomy import classify
from blueprint_engine.models import Document, Segment, Source
from blueprint_engine.ranking import score_sources


def test_classify_routes_to_expected_pillars():
    assert classify("add a daily login reward streak so players come back tomorrow")[0].pillar == "retention"
    assert classify("the tutorial should show new players where to go with an arrow")[0].pillar == "onboarding"
    assert classify("sell a vip game pass and a 2x coins developer product")[0].pillar == "monetization"
    assert classify("your core loop is action then reward then upgrade")[0].pillar == "core_loop"
    assert classify("I had pizza for lunch today") == []


def test_mechanics_are_identified():
    c = classify("add a daily reward streak and weekly quests")[0]
    keys = [k for k, _ in c.mechanics]
    assert "daily_rewards" in keys and "quests" in keys


def test_actionability_prefers_directives_with_reasons():
    advice = actionability("You need to give players a reward in the first minute because it hooks them.", 2.0)
    chatter = actionability("This game has a reward system and some players.", 2.0)
    assert advice > 0.6 > chatter


def test_metric_mentions_capture_context():
    ms = metric_mentions("we got 40% D1 retention after adding it")
    assert any("40%" in m for m in ms) and any("D1" in m for m in ms)


def _doc(texts, start_step=10.0):
    return Document("yt:x", "auto-captions", "en", [Segment(t, i * start_step) for i, t in enumerate(texts)])


def test_extract_filters_noise_and_merges_passages():
    doc = _doc([
        "Make sure you smash that like button and subscribe to my channel for more videos.",
        "Number one is daily rewards.",
        "You should give players a daily reward streak because it makes them come back tomorrow.",
        "I really like the color blue in this map, it looks nice.",
        "The tutorial should guide new players with an arrow so they never get confused in the first minute.",
    ])
    out = extract_insights(doc, kind="youtube")
    texts = [i.text for i in out]
    assert not any("subscribe" in t for t in texts)
    # The short lead-in sentence is merged with its explanation.
    assert any(t.startswith("Number one is daily rewards. You should give") for t in texts)
    pillars = {i.pillar for i in out}
    assert {"retention", "onboarding"} <= pillars
    retention = next(i for i in out if i.pillar == "retention")
    assert retention.start == 10.0 and "daily_rewards" in retention.mechanics


def test_extract_caps_insights_per_pillar():
    doc = _doc([f"You should add a daily reward streak number {i} so players come back tomorrow for item {i * 7}."
                for i in range(40)])
    from blueprint_engine.analysis.extract import ExtractConfig

    out = extract_insights(doc, kind="youtube", cfg=ExtractConfig(max_insights_per_pillar_per_source=5))
    assert sum(1 for i in out if i.pillar == "retention") <= 5


def test_ranking_rewards_velocity_and_relevance():
    fast = Source("yt:a", "youtube", "u", "Roblox retention tips: daily rewards and streaks", published="2026-10-01",
                  views=500_000, likes=20_000, followers=200_000, pillars=["retention"])
    slow = Source("yt:b", "youtube", "u", "My vlog", published="2019-01-01",
                  views=500_000, likes=2_000, followers=1_000, pillars=["retention"])
    doc = Source("doc:x", "doc", "u", "Retention")
    score_sources([fast, slow, doc], today=date(2026, 11, 10))
    assert fast.score > slow.score
    assert doc.score == 0.75
    assert set(fast.score_breakdown) == {"velocity", "like_rate", "authority", "relevance"}


def test_viral_gameplay_video_cannot_outrank_design_content():
    # Same audience numbers; the gameplay video's tags match "ranked/competitive" keywords.
    gameplay = Source("yt:g", "youtube", "u", "BRONZE to NEMESIS RANK in Rivals!!", published="2026-10-01",
                      views=2_000_000, likes=60_000, followers=900_000, pillars=["retention"],
                      description="ranked competitive pvp leaderboard grind #roblox #rivals")
    talk = Source("yt:t", "youtube", "u", "How to improve your Roblox game's retention", published="2026-10-01",
                  views=2_000_000, likes=60_000, followers=900_000, pillars=["retention"],
                  description="D1 and D7 retention tips: daily rewards, streaks and quests")
    # A third, smaller video keeps min-max normalisation from degenerating.
    other = Source("yt:o", "youtube", "u", "Roblox retention tips", published="2026-01-01",
                   views=5_000, likes=100, followers=1_000, pillars=["retention"])
    score_sources([gameplay, talk, other], today=date(2026, 11, 10))
    assert talk.score > gameplay.score * 2
    assert gameplay.score_breakdown["relevance"] < 0.3


def test_boilerplate_and_tags_do_not_create_dev_intent():
    from blueprint_engine.ranking import relevance

    desc = "Use Code: TanqR when purchasing Robux!\nClick The Bell and Turn on All Post Notifications!"
    assert relevance("BRONZE to NEMESIS RANK", desc, ["retention"], tags=["how to rank up", "rivals tips"]) < 0.2
