---
name: thumbnail-icon-brief
title: Thumbnail & icon art-direction brief
stage: design
inputs: game_concept, core_hook, brand_character, key_findings_thumbnails, key_findings_discovery
description: Turns the thumbnail research into 5 testable 16:9 thumbnail concepts and 3 icon concepts for a Roblox game.
---
Write the art-direction brief for this Roblox game's Home thumbnails and icon.

- **Game & core loop:** {{game_concept}}
- **The single most exciting thing a player does or sees (the hook):** {{core_hook}}
- **Recurring character / mascot / brand colours (if any):** {{brand_character}}

## Research: what makes thumbnails work (MrBeast study + attention science)
{{key_findings_thumbnails}}

## Research: Roblox discovery
{{key_findings_discovery}}

## Deliver
1. **The one-sentence promise** the thumbnail must make (what the player will *do and feel*),
   and the one thing it must never imply that the game does not deliver.
2. **Five thumbnail concepts** (16:9, 1920×1080), each a different *idea* so personalisation can
   learn which hook works for whom. Use these archetypes, adapted to the game:
   - Progression contrast (level 1 vs level 100, small vs giant, poor vs rich base)
   - Stakes moment (the hero one second before the threat lands)
   - Scale spectacle (one hero against something enormous)
   - Progress counter (the number that tells the story: day, level, size, count)
   - Signature mechanic close-up (the verb nobody else has)
   For each: focal subject, the hero's expression and **gaze direction (toward the hook)**,
   background (simple, contrasting value), palette (2–3 saturated hues + one accent), overlay
   text (0–2 tokens, a number where possible, no claims), what sits in the bottom 15% (nothing
   important), and why it should beat the others.
3. **Three icon concepts** (512×512, read at 150 px): one centred subject filling ~60% of the
   frame, a one-colour background with strong value contrast to the subject, no text or one
   short word, and consistency with the thumbnails' hero and palette.
4. **Capture plan in Studio:** freecam angles, lighting (rim light to separate the hero), avatar
   expression via dynamic heads, render resolution, and post-processing that stays faithful to
   the real game.
5. **Test plan:** which 2–5 thumbnails to activate first in thumbnail personalisation, what
   qualified play-through rate would retire one, and when to refresh (each update; CTR decay).
6. **QA checklist** to run with `bpe thumbs score <file> [--kind icon]` before upload.
