"""Blueprint Engine: mine top-performing game-design content into implementation blueprints.

Pipeline stages (each cached and idempotent):

    discover  -> find candidate videos/pages for every design pillar
    fetch     -> pull metadata, score performance, download transcripts / page text
    analyze   -> segment text and extract actionable, timestamped insights
    synthesize-> aggregate cross-source consensus into a blueprint, report and prompt pack
"""

__version__ = "0.1.0"
