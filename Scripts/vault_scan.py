"""Shared helpers for the report scripts: find the vault, then read every note's properties and tags.

Standard library only, so anyone can run the scripts without installing anything.
"""

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_DIR / "Reports"

# Never scanned: Obsidian/system folders, the templates, and the reports themselves.
SKIP_DIR_NAMES = {".obsidian", ".trash", ".git"}
SKIP_DIRS = {REPO_DIR / "Templates", REPORTS_DIR}

# Matches an inline #tag. A tag must contain at least one non-digit (Obsidian rule).
INLINE_TAG = re.compile(r"(?:^|\s)#([^\s#.,;:!?()\[\]{}\"'`|]+)")
FENCED_CODE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")


@dataclass
class Note:
    path: Path              # relative to the vault root
    props: dict | None      # None = the note has no properties block at all
    body: str
    modified: date

    @property
    def folder(self) -> str:
        """Top-level folder (or "(vault root)")."""
        return self.path.parts[0] if len(self.path.parts) > 1 else "(vault root)"

    @property
    def note_type(self) -> str:
        value = (self.props or {}).get("Note Type")
        if isinstance(value, list):
            value = ", ".join(value)
        return value or "(none)"

    @property
    def property_tags(self) -> list[str]:
        props = self.props or {}
        value = props.get("tags", props.get("tag"))
        if value is None:
            return []
        items = value if isinstance(value, list) else re.split(r"[,\s]+", value)
        return [t.lstrip("#") for t in items if t.strip("# ")]

    @property
    def inline_tags(self) -> list[str]:
        text = INLINE_CODE.sub("", FENCED_CODE.sub("", self.body))
        return [t for t in INLINE_TAG.findall(text) if not t.isdigit()]


def parse_args(description: str, default_report: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--vault", type=Path, help="vault folder (default: the vault this repo sits in)")
    parser.add_argument("--out", type=Path, default=REPORTS_DIR / default_report,
                        help=f"report file to write (default: Reports/{default_report})")
    return parser.parse_args()


def find_vault(start: Path | None) -> Path:
    """Return the vault root: the given folder, or the nearest parent with a .obsidian folder."""
    if start:
        return start.resolve()
    for folder in [REPO_DIR, *REPO_DIR.parents]:
        if (folder / ".obsidian").is_dir():
            return folder
    raise SystemExit("Couldn't find the vault. Run with --vault <path to your vault>.")


def load_notes(vault: Path) -> list[Note]:
    notes = []
    for path in sorted(vault.rglob("*.md")):
        if any(part in SKIP_DIR_NAMES for part in path.parts) or any(path.is_relative_to(d) for d in SKIP_DIRS):
            continue
        props, body = parse_note(path.read_text(encoding="utf-8", errors="replace"))
        modified = datetime.fromtimestamp(path.stat().st_mtime).date()
        notes.append(Note(path.relative_to(vault), props, body, modified))
    return notes


def parse_note(text: str) -> tuple[dict | None, str]:
    """Split a note into (properties, body). Handles the YAML forms Obsidian writes:
    `key: value`, `key:` followed by `  - item` lines, and `key: [a, b]`."""
    match = re.match(r"---\r?\n(.*?)^---\s*$", text, re.S | re.M)
    if not match:
        return None, text
    props: dict = {}
    key = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"\s*-\s*(.*)", line)
        if item and key is not None:
            if not isinstance(props[key], list):
                props[key] = []
            if value := _clean(item.group(1)):
                props[key].append(value)
        elif not line[0].isspace() and ":" in line:
            key, _, raw = line.partition(":")
            key, raw = key.strip(), raw.strip()
            if raw.startswith("[") and raw.endswith("]") and not raw.startswith("[["):
                props[key] = [v for v in (_clean(x) for x in raw[1:-1].split(",")) if v]
            else:
                props[key] = _clean(raw) or None
    return props, text[match.end():]


def _clean(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


# --- Report writing -----------------------------------------------------------

def top(counter: Counter, n: int = 3) -> str:
    """'a 5, b 2, +3 more' — the most common entries in a counter."""
    parts = [f"{k} {v}" for k, v in counter.most_common(n)]
    if len(counter) > n:
        parts.append(f"+{len(counter) - n} more")
    return ", ".join(parts)


def cell(value) -> str:
    """Make a value safe inside a markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return lines


def write_report(out: Path, title: str, vault: Path, body: list[str]) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "---", "tags:", "  - VaultReport", "Note Type:", "  - Reference", "---", "",
        f"# {title}", "",
        f"*Generated {datetime.now():%Y-%m-%d %H:%M} from vault `{vault.name}`. "
        "Re-run the script to refresh. Don't edit by hand.*", "",
    ]
    out.write_text("\n".join(header + body) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
