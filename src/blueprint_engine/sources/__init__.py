"""Source adapters. Each one turns a platform into ``Source`` + ``Document`` objects."""


class SourceUnavailable(RuntimeError):
    """The platform cannot be reached right now (policy block, maintenance, bot wall)."""


class NoTranscript(RuntimeError):
    """The item exists but has no usable text in the requested languages."""
