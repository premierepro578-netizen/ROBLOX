"""A small, thread-safe JSON file store. One file per object keeps caches diffable and resumable."""

from __future__ import annotations

import json
import os
import re
import tempfile
import threading
from pathlib import Path
from typing import Any, Iterator

_SAFE = re.compile(r"[^A-Za-z0-9._-]+")


def safe_key(key: str) -> str:
    return _SAFE.sub("_", key).strip("_")[:180] or "_"


class Store:
    def __init__(self, root: str | os.PathLike[str]):
        self.root = Path(root)
        self._lock = threading.Lock()

    def path(self, collection: str, key: str) -> Path:
        return self.root / collection / f"{safe_key(key)}.json"

    def exists(self, collection: str, key: str) -> bool:
        return self.path(collection, key).is_file()

    def get(self, collection: str, key: str, default: Any = None) -> Any:
        p = self.path(collection, key)
        if not p.is_file():
            return default
        with p.open(encoding="utf-8") as fh:
            return json.load(fh)

    def put(self, collection: str, key: str, obj: Any) -> Path:
        p = self.path(collection, key)
        p.parent.mkdir(parents=True, exist_ok=True)
        # Atomic replace so a crash mid-write never leaves a truncated cache entry.
        fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=".tmp-", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=False)
            os.replace(tmp, p)
        except BaseException:
            Path(tmp).unlink(missing_ok=True)
            raise
        return p

    def items(self, collection: str) -> Iterator[tuple[str, Any]]:
        d = self.root / collection
        if not d.is_dir():
            return
        for p in sorted(d.glob("*.json")):
            with p.open(encoding="utf-8") as fh:
                yield p.stem, json.load(fh)

    def clear(self, collection: str) -> int:
        d = self.root / collection
        n = 0
        if d.is_dir():
            for p in d.glob("*.json"):
                p.unlink()
                n += 1
        return n

    def count(self, collection: str) -> int:
        d = self.root / collection
        return len(list(d.glob("*.json"))) if d.is_dir() else 0
