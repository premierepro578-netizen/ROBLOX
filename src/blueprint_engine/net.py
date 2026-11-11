"""HTTP session + polite, thread-safe rate limiting shared by every adapter."""

from __future__ import annotations

import logging
import random
import threading
import time
from typing import Callable, TypeVar

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

log = logging.getLogger(__name__)
T = TypeVar("T")

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0 Safari/537.36 blueprint-engine/0.1"
)


class RateLimiter:
    """Enforce a minimum interval between calls across all threads (with small jitter)."""

    def __init__(self, min_interval_s: float):
        self.min_interval = max(0.0, min_interval_s)
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        if self.min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            delay = self._next - now
            self._next = max(now, self._next) + self.min_interval * random.uniform(0.85, 1.25)
        if delay > 0:
            time.sleep(delay)


def make_session(total_retries: int = 4) -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=total_retries,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "HEAD"),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=16, pool_maxsize=16)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    s.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.8"})
    return s


def with_backoff(fn: Callable[[], T], *, attempts: int = 4, base_delay: float = 2.0,
                 retry_on: tuple[type[BaseException], ...] = (Exception,), what: str = "") -> T:
    """Run ``fn`` with exponential backoff; re-raise the last error."""
    for i in range(attempts):
        try:
            return fn()
        except retry_on as exc:  # noqa: PERF203 - clarity over micro-optimisation
            if i == attempts - 1:
                raise
            delay = base_delay * (2**i) * random.uniform(0.8, 1.2)
            log.debug("retry %s after %s (%.1fs): %s", what, type(exc).__name__, delay, exc)
            time.sleep(delay)
    raise AssertionError("unreachable")
