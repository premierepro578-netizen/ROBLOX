"""Prompt framework: Markdown templates with front matter and ``{{variable}}`` slots.

Front matter (between ``---`` lines) is ``key: value``; ``inputs`` is a comma list.
Variables the caller does not supply are left as ``{{name}}`` so a designer can fill
them in by hand - rendering never silently drops a slot.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "templates"
_VAR = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


@dataclass
class PromptTemplate:
    name: str
    title: str
    stage: str
    description: str
    inputs: list[str] = field(default_factory=list)
    body: str = ""
    path: Path | None = None
    order: int = 0

    @property
    def variables(self) -> list[str]:
        return list(dict.fromkeys(_VAR.findall(self.body)))


def parse_template(text: str, path: Path | None = None) -> PromptTemplate:
    meta: dict[str, str] = {}
    body = text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    stem = path.stem if path else meta.get("name", "template")
    order = int(stem.split("-", 1)[0]) if stem[:2].isdigit() else 0
    return PromptTemplate(
        name=meta.get("name", stem),
        title=meta.get("title", stem),
        stage=meta.get("stage", "design"),
        description=meta.get("description", ""),
        inputs=[x.strip() for x in meta.get("inputs", "").split(",") if x.strip()],
        body=body.strip() + "\n",
        path=path,
        order=order,
    )


def load_templates(directory: Path = TEMPLATE_DIR) -> dict[str, PromptTemplate]:
    out = {}
    for p in sorted(directory.glob("*.md")):
        t = parse_template(p.read_text(encoding="utf-8"), p)
        out[t.name] = t
    return out


def render(template: PromptTemplate, variables: dict[str, str]) -> tuple[str, list[str]]:
    """Return (rendered text, names of variables left unfilled)."""
    missing: list[str] = []

    def sub(m: re.Match[str]) -> str:
        key = m.group(1)
        if key in variables and variables[key] is not None:
            return str(variables[key])
        missing.append(key)
        return m.group(0)

    return _VAR.sub(sub, template.body), list(dict.fromkeys(missing))
