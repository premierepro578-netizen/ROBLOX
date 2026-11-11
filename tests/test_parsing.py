from blueprint_engine.analysis.segment import is_punctuated, segments_from_paragraphs, segments_from_tokens
from blueprint_engine.sources.captions import parse_json3, parse_vtt
from blueprint_engine.sources.devforum import topic_to_document
from blueprint_engine.sources.roblox_docs import parse_article
from blueprint_engine.sources.youtube import pick_track, slim_info


def test_parse_json3_word_level_offsets():
    data = {"events": [
        {"tStartMs": 1000, "segs": [{"utf8": "make"}, {"utf8": " sure", "tOffsetMs": 300}]},
        {"tStartMs": 1500, "aAppend": 1, "segs": [{"utf8": "\n"}]},
        {"tStartMs": 2000, "segs": [{"utf8": "players", "tOffsetMs": 0}]},
    ]}
    assert parse_json3(data) == [(1.0, "make"), (1.3, "sure"), (2.0, "players")]


def test_parse_vtt_dedupes_rolling_lines():
    vtt = """WEBVTT
Kind: captions

00:00:01.000 --> 00:00:03.000
add a daily reward

00:00:03.000 --> 00:00:05.000
add a daily reward
so players come back
"""
    assert parse_vtt(vtt) == [(1.0, "add a daily reward"), (3.0, "so players come back")]


def test_unpunctuated_asr_split_on_pauses():
    words = "the core loop is the most important thing in your game".split()
    tokens = [(i * 0.3, w) for i, w in enumerate(words)]
    more = "next you need a daily reward so players return".split()
    tokens += [(10.0 + i * 0.3, w) for i, w in enumerate(more)]
    assert not is_punctuated(tokens)
    segs = segments_from_tokens(tokens)
    assert [s.start for s in segs] == [0.0, 10.0]
    assert segs[1].text.startswith("next you need")


def test_punctuated_captions_split_on_terminals():
    tokens = [(0.0, "Give players a goal."), (2.0, "Then reward them!"), (4.0, "[Music]")]
    segs = segments_from_tokens(tokens)
    assert [s.text for s in segs] == ["Give players a goal.", "Then reward them!"]


def test_paragraph_sentence_split():
    segs = segments_from_paragraphs(["Retention measures returns. D1 is next day. Keep it high."])
    assert [s.text for s in segs] == ["Retention measures returns.", "D1 is next day.", "Keep it high."]


def _info(subs=None, auto=None):
    return slim_info({"id": "abc", "title": "t", "subtitles": subs or {}, "automatic_captions": auto or {}}, ["en"])


def test_pick_track_prefers_manual_then_original_asr():
    fmt = [{"ext": "vtt", "url": "u-vtt"}, {"ext": "json3", "url": "u-json3"}]
    assert pick_track(_info(subs={"en-US": fmt}, auto={"en-orig": fmt}), ["en"])[2] == "manual-captions"
    url, ext, origin, lang = pick_track(_info(auto={"en": fmt, "en-orig": fmt}), ["en"])
    assert (ext, origin, lang) == ("json3", "auto-captions", "en-orig")


def test_pick_track_rejects_machine_translation():
    fmt = [{"ext": "json3", "url": "u"}]
    # Original ASR is Portuguese; the "en" auto track is a translation, not a transcript.
    assert pick_track(_info(auto={"pt-orig": fmt, "en": fmt}), ["en"]) is None


def test_docs_article_parser_keeps_prose_and_inline_code():
    html = """<html><head><meta name="description" content="About passes"></head><body><article>
      <h1>Passes</h1>
      <p>Use <code>UserOwnsGamePassAsync</code> to check ownership on join.</p>
      <pre><code>local x = 1 -- code blocks are dropped</code></pre>
      <ul><li><p>Grant the perk immediately after purchase.</p></li><li>Show the pass where it helps the player.</li></ul>
    </article></body></html>"""
    title, desc, paras = parse_article(html)
    assert title == "Passes" and desc == "About passes"
    assert "Use UserOwnsGamePassAsync to check ownership on join." in paras
    assert "Grant the perk immediately after purchase." in paras
    assert not any("code blocks" in p for p in paras)
    assert len(paras) == 3


def test_discourse_topic_to_document():
    topic = {"id": 42, "slug": "retention-tips", "title": "Retention tips", "views": 900, "like_count": 30,
             "posts_count": 3, "created_at": "2024-05-01T00:00:00Z",
             "post_stream": {"posts": [{"username": "dev", "cooked": "<p>Add a daily reward so players return.</p>"}]}}
    src, doc = topic_to_document(topic, "https://devforum.roblox.com")
    assert src.id == "df:42" and src.url.endswith("/t/retention-tips/42") and src.published == "2024-05-01"
    assert doc.segments[0].text == "Add a daily reward so players return."
    assert not src.first_party


def test_discourse_staff_announcement_is_first_party_and_skips_replies():
    topic = {"id": 7, "slug": "launch", "title": "Launch", "post_stream": {"posts": [
        {"username": "staffer", "primary_group_name": "Roblox_Staff", "cooked": "<p>Discounts on subscriptions are not eligible.</p>"},
        {"username": "dev", "cooked": "<p>This is awesome, thank you so much for this!</p>"},
    ]}}
    src, doc = topic_to_document(topic, "https://devforum.roblox.com")
    assert src.first_party and [s.text for s in doc.segments] == ["Discounts on subscriptions are not eligible."]
