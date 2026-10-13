"""Inbox cleanup helper for the /clean-inbox skill (SKILL.md, in this folder).

The skill (AI) makes the judgment calls and writes a plan. This script handles the mechanics:
  python3 clean_inbox.py context                      JSON snapshot for the AI: Inbox notes, MOCs, tags, rules
  python3 clean_inbox.py apply plan.json              carry out the plan, save undo data, write the report
  python3 clean_inbox.py apply plan.json --preview    write the report only, change nothing
  python3 clean_inbox.py undo                         reverse the last run

Vault-specific settings (folder names) and learned rules live in one note, "Inbox Cleanup Settings.md",
in the repo folder. It's created on the first run.
"""

import json
import os
import re
import shutil
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Scripts"))  # shared note-reading code
from vault_scan import REPO_DIR, REPORTS_DIR, find_vault, load_notes, parse_note, table, write_report

SETTINGS_FILE = REPO_DIR / "Inbox Cleanup Settings.md"
UNDO_DIR = REPORTS_DIR / ".undo"
REPORT = REPORTS_DIR / "Inbox Cleanup Report.md"
NOTE_TYPES = {"Working", "Reference", "MOC"}
# Old linking properties (retired by the system). Their links are kept as a "Related:" line.
OLD_LINK_PROPS = {"Action", "Concept", "Reference", "Parent MOC", "Project", "Domain", "Analysis"}


# --- Setup ----------------------------------------------------------------------

SETTING_KEYS = {"Inbox": "inbox", "Review": "review", "Archive": "archive", "Admin": "admin", "Skip": "skip"}


def load_settings(vault: Path) -> dict:
    """Read the "## Folders" section of the settings note (lines like "- Inbox: 99. Inbox")."""
    if not SETTINGS_FILE.exists():
        guess = lambda word, default: next((p.name for p in sorted(vault.iterdir())
                                            if p.is_dir() and word in p.name.lower()), default)
        inbox = guess("inbox", "Inbox")
        SETTINGS_FILE.write_text(SETTINGS_TEMPLATE.format(inbox=inbox, archive=guess("archive", "Archive")),
                                 encoding="utf-8")
        sys.exit(f"Created {SETTINGS_FILE.name} with guessed folder names. Check them, then run again.")
    text = SETTINGS_FILE.read_text(encoding="utf-8")
    folders = re.search(r"^## Folders\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    s = {"admin": [], "skip": []}
    for key, value in re.findall(r"^\s*-\s*(\w+):[ \t]*(.*)$", folders.group(1) if folders else "", re.M):
        if key in SETTING_KEYS:
            k = SETTING_KEYS[key]
            s[k] = [v.strip() for v in value.split(",") if v.strip()] if k in ("admin", "skip") else value.strip()
    for key in ("inbox", "review", "archive"):
        if not s.get(key):
            sys.exit(f"{SETTINGS_FILE.name} is missing the '{key.title()}' folder.")
    for key in ("inbox", "archive"):
        if not (vault / s[key]).is_dir():
            sys.exit(f"{SETTINGS_FILE.name}: the {key.title()} folder doesn't exist: {s[key]}")
    return s


SETTINGS_TEMPLATE = """---
tags:
  - SOP
Note Type:
  - Reference
Parent: "[[Obsidian-Designbase]]"
---

# Inbox Cleanup Settings

Settings and learned rules for `/clean-inbox` in this vault. Edit freely.

## Folders

Folder paths are relative to the vault. Admin and Skip take a comma-separated list.

- Inbox: {inbox}
- Review: {inbox}/Review
- Archive: {archive}
- Admin:
- Skip:

## Rules

How to file notes in this vault, in plain English, one per line. The skill adds a rule each time you
answer a Review question, and applies these before its own judgment. Edit or delete any rule.
"""


def words(text: str) -> int:
    return len(re.sub(r"[#*_>\-|`\[\]]", " ", text).split())


def preview(body: str, n: int) -> str:
    text = re.sub(r"\n{3,}", "\n\n", body.strip())
    return text[:n] + ("…" if len(text) > n else "")


# --- context --------------------------------------------------------------------

def context(vault: Path, s: dict) -> dict:
    notes = load_notes(vault)
    inbox, review = vault / s["inbox"], vault / s["review"]
    special = {s["inbox"], s["archive"], *s.get("admin", []), *s.get("skip", [])}
    tags = Counter(t for n in notes for t in {*n.property_tags, *n.inline_tags})

    def describe(n, chars):
        return {"path": n.path.as_posix(), "words": words(n.body), "properties": n.props or {},
                "text": preview(n.body, chars)}

    mocs = [{"name": n.path.stem, "path": n.path.as_posix(), "parent": (n.props or {}).get("Parent"),
             "text": preview(n.body, 300)} for n in notes if n.note_type == "MOC"]
    in_inbox = [n for n in notes if (vault / n.path).is_relative_to(inbox)]
    return {
        "vault": vault.name,
        "settings": s,
        "concept_folders": sorted(p.name for p in vault.iterdir()
                                  if p.is_dir() and not p.name.startswith(".") and p.name not in special),
        "routing_rules": SETTINGS_FILE.read_text(encoding="utf-8").split("## Rules", 1)[-1].strip(),
        "mocs": mocs,
        "tags": dict(tags.most_common()),
        "inbox": [describe(n, 800) for n in in_inbox if not (vault / n.path).is_relative_to(review)],
        "review": [describe(n, 800) for n in in_inbox if (vault / n.path).is_relative_to(review)],
        "last_run_review": last_run_review(vault, notes),
    }


def last_run_review(vault: Path, notes) -> list[dict]:
    """Review items from the last run and what the user has done with them since (for learning)."""
    manifest = latest_manifest()
    if not manifest or manifest.get("undone"):
        return []
    by_name = {n.path.name: n for n in notes}
    out = []
    for item in manifest.get("review", []):
        now = by_name.get(Path(item["path"]).name)
        out.append({**item, "now_at": now.path.as_posix() if now else None,
                    "parent_now": (now.props or {}).get("Parent") if now else None,
                    "note_type_now": now.note_type if now else None})
    return out


# --- Writing properties ----------------------------------------------------------

def blocks(fm: str) -> list[list]:
    """Split raw frontmatter into [key, raw_lines] blocks, keeping each property's exact text."""
    out = []
    for line in fm.splitlines():
        if line and not line[0].isspace() and not line.startswith("-") and ":" in line:
            out.append([line.split(":", 1)[0].strip(), [line]])
        elif out:
            out[-1][1].append(line)
    return out


def link_target(value) -> str | None:
    m = re.fullmatch(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]", str(value).strip())
    return m.group(1).strip() if m else None


def set_properties(text: str, note_type: str, parent: str | None, tags: list[str]) -> str:
    """Rewrite the properties block: tags, Note Type, Parent first, then any other filled-in properties.
    Old linking properties are removed and their links kept as a "Related:" line. Note text is unchanged."""
    m = re.match(r"---\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    fm, body = (m.group(1), text[m.end():]) if m else ("", text)
    props, _ = parse_note(text)
    props = props or {}
    related = []
    for key in OLD_LINK_PROPS:
        vals = props.get(key) or []
        for v in vals if isinstance(vals, list) else [vals]:
            t = link_target(v)
            if t and t != parent and f"[[{t}" not in body and t not in related:
                related.append(t)
    lines = ["tags:"] + [f"  - {t.lstrip('#')}" for t in tags]
    lines += ["Note Type:", f"  - {note_type}", f'Parent: "[[{parent}]]"' if parent else "Parent:"]
    for key, raw in blocks(fm):
        if key not in ("tags", "Note Type", "Parent") and key not in OLD_LINK_PROPS and props.get(key) not in (None, []):
            lines += raw
    if related:
        body = body.rstrip("\n") + "\n\nRelated: " + ", ".join(f"[[{t}]]" for t in sorted(related)) + "\n"
    return "---\n" + "\n".join(lines) + "\n---\n" + (body if m else "\n" + body.lstrip("\n"))


# --- apply -----------------------------------------------------------------------

class Run:
    """Carries out file operations, recording each one so the run can be undone."""

    def __init__(self, vault: Path, preview: bool):
        self.vault, self.preview = vault, preview
        self.id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        self.snap = UNDO_DIR / self.id
        self.ops: list[dict] = []
        self.renamed: list[str] = []
        self.planned: set[Path] = set()  # paths taken during a preview run

    def rel(self, p: Path) -> str:
        return p.relative_to(self.vault).as_posix()

    def free_path(self, folder: Path, name: str) -> Path:
        """A path in `folder` that isn't taken; adds " (2)", " (3)"… on a name collision."""
        stem, suffix, i = Path(name).stem, Path(name).suffix, 1
        target = folder / name
        while target.exists() or target in self.planned:
            i += 1
            target = folder / f"{stem} ({i}){suffix}"
        if i > 1:
            self.renamed.append(f"{name} → {target.name} (in {self.rel(folder)})")
        self.planned.add(target)
        return target

    def mkdir(self, folder: Path) -> None:
        if folder.exists() or folder in self.planned:
            return
        self.mkdir(folder.parent)
        self.planned.add(folder)
        self.ops.append({"op": "folder", "path": self.rel(folder)})
        if not self.preview:
            folder.mkdir()

    def snapshot(self, src: Path) -> None:
        if not self.preview:
            dst = self.snap / self.rel(src)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    def move(self, src: Path, folder: Path, new_text: str | None = None, op: str = "move") -> Path:
        self.mkdir(folder)
        dst = src if src.parent == folder and new_text is not None else self.free_path(folder, src.name)
        self.ops.append({"op": op, "from": self.rel(src), "to": self.rel(dst)})
        if not self.preview:
            self.snapshot(src)
            st = src.stat()
            if dst != src:
                shutil.move(src, dst)
            if new_text is not None:
                dst.write_text(new_text, encoding="utf-8")
                os.utime(dst, (st.st_atime, st.st_mtime))  # keep the original modified date
        return dst

    def create(self, folder: Path, name: str, text: str) -> Path:
        self.mkdir(folder)
        path = self.free_path(folder, name)
        self.ops.append({"op": "create", "path": self.rel(path)})
        if not self.preview:
            path.write_text(text, encoding="utf-8")
        return path


def moc_text(m: dict) -> str:
    tags = "".join(f"\n  - {t}" for t in m.get("tags", []))
    parent = f'"[[{m["parent"]}]]"' if m.get("parent") else ""
    body = m.get("body", "").strip()
    return f"---\ntags:{tags}\nNote Type:\n  - MOC\nParent: {parent}".rstrip() + "\n---\n" + (f"\n{body}\n" if body else "")


def apply(vault: Path, s: dict, plan: dict, preview_only: bool) -> None:
    run = Run(vault, preview_only)
    inbox, archive, trash = vault / s["inbox"], vault / s["archive"], vault / ".trash"  # Obsidian's trash
    results = {k: [] for k in ("trash", "Working", "Reference", "MOC", "review", "left", "moved_mocs", "new_mocs", "errors")}

    def safe(path_str: str) -> Path | None:
        p = (vault / path_str).resolve()
        if not p.is_relative_to(vault):
            results["errors"].append(f"Outside the vault, skipped: {path_str}")
            return None
        return p

    # 1. New MOCs (plus notes merged into them)
    merged = {}
    for m in plan.get("new_mocs", []):
        folder = safe(m["folder"])
        if folder is None:
            continue
        path = run.create(folder, f"{m['name']}.md", moc_text(m))
        results["new_mocs"].append([f"[[{path.stem}]]", f"[[{m['parent']}]]" if m.get("parent") else "(Concept)",
                                    run.rel(path.parent), ", ".join(Path(p).stem for p in m.get("merged_from", [])) or "—"])
        for p in m.get("merged_from", []):
            merged[p] = m["name"]

    # 2. Existing MOCs that get their own folder now
    for mv in plan.get("move_existing", []):
        src, dest = safe(mv["path"]), safe(mv["destination"])
        if src and dest and src.exists():
            run.move(src, dest)
            results["moved_mocs"].append([f"[[{src.stem}]]", run.rel(src.parent), run.rel(dest)])

    # 3. Inbox notes (notes merged into a new MOC are deleted even if the plan doesn't list them)
    listed = {n["path"] for n in plan.get("notes", [])}
    plan.setdefault("notes", []).extend({"path": p, "action": "trash"} for p in merged if p not in listed)
    review_dir = vault / s["review"]
    for n in plan["notes"]:
        src = safe(n["path"])
        if src is None:
            continue
        if not src.exists() or not (src.is_relative_to(inbox) or src.is_relative_to(review_dir)):
            results["errors"].append(f"Not found in the Inbox, skipped: {n['path']}")
            continue
        action = "trash" if n["path"] in merged else n["action"]
        reason = f"merged into [[{merged[n['path']]}]]" if n["path"] in merged else n.get("reason", "")
        if action == "trash":
            run.move(src, trash, op="trash")
            results["trash"].append([src.stem, reason])
        elif action == "review":
            dst = run.move(src, review_dir) if src.parent != review_dir else src
            results["review"].append([f"[[{src.stem}]]", n.get("question", "")])
            n["_review_path"] = run.rel(dst)
        elif action == "leave":
            results["left"].append([f"[[{src.stem}]]", reason])
        elif action == "file":
            nt = n["note_type"]
            if nt not in NOTE_TYPES:
                results["errors"].append(f"Invalid Note Type '{nt}', skipped: {n['path']}")
                continue
            if not n.get("parent") and nt != "MOC":
                results["errors"].append(f"No Parent given, skipped: {n['path']}")
                continue
            if nt != "Working" and not n.get("destination"):
                results["errors"].append(f"No destination folder given, skipped: {n['path']}")
                continue
            dest = archive if nt == "Working" else safe(n["destination"])
            if dest is None:
                continue
            text = set_properties(src.read_text(encoding="utf-8"), nt, n.get("parent"), n.get("tags", []))
            dst = run.move(src, dest, text)
            results[nt].append([f"[[{src.stem}]]", f"[[{n['parent']}]]" if n.get("parent") else "(Concept)",
                                ", ".join(n.get("tags", [])) or "—", run.rel(dst.parent), n.get("rule", "") or "—"])
        else:
            results["errors"].append(f"Unknown action '{action}': {n['path']}")

    rules = [r for r in plan.get("rules_learned", []) if r.strip()]
    if not preview_only:
        if rules:
            add_rules(rules, run.id)
        manifest = {"id": run.id, "ops": run.ops, "rules_learned": rules,
                    "review": [{"path": n["_review_path"], "question": n.get("question", "")}
                               for n in plan.get("notes", []) if "_review_path" in n]}
        run.snap.mkdir(parents=True, exist_ok=True)
        (run.snap / "manifest.json").write_text(json.dumps(manifest, indent=2))
    write_report(REPORT, "Inbox Cleanup Report", vault, report_body(run, results, rules, plan, preview_only))


def add_rules(rules: list[str], run_id: str) -> None:
    """Append rules to the end of the settings note (the Rules section is last)."""
    text = SETTINGS_FILE.read_text(encoding="utf-8").rstrip("\n")
    SETTINGS_FILE.write_text(text + "\n" + "".join(f"- {r} *(learned {run_id[:10]})*\n" for r in rules), encoding="utf-8")


def report_body(run: Run, r: dict, rules: list[str], plan: dict, preview_only: bool) -> list[str]:
    lines = []
    if preview_only:
        lines += ["> [!warning] PREVIEW: nothing has been changed. This is what the cleanup would do.", ""]
    else:
        lines += [f"Run `{run.id}`. To reverse it: `/clean-inbox undo`", ""]
    folders = [o["path"] for o in run.ops if o["op"] == "folder"]
    lines += ["## Summary", "",
              f"- **Blank notes deleted** (to Obsidian's trash): {len(r['trash'])}",
              f"- **Working notes archived:** {len(r['Working'])}",
              f"- **Reference notes filed:** {len(r['Reference'])}",
              f"- **MOCs created:** {len(r['new_mocs'])}. **Existing MOCs filed:** {len(r['MOC'])}",
              f"- **Folders created:** {len(folders)}",
              f"- **Sent to Review:** {len(r['review'])}. **Left in place:** {len(r['left'])}",
              f"- **Rules learned:** {len(rules)}. **Renamed (name already taken):** {len(run.renamed)}",
              f"- **Problems:** {len(r['errors'])}", ""]
    sections = [
        ("MOCs created", ["MOC", "Parent", "Folder", "Merged in"], r["new_mocs"]),
        ("MOCs moved into their own folder", ["MOC", "From", "To"], r["moved_mocs"]),
        ("Reference notes filed", ["Note", "Parent", "Tags", "Folder", "Rule applied"], r["Reference"]),
        ("MOCs filed", ["Note", "Parent", "Tags", "Folder", "Rule applied"], r["MOC"]),
        ("Working notes archived", ["Note", "Parent", "Tags", "Folder", "Rule applied"], r["Working"]),
        ("Blank notes deleted", ["Note", "Why"], r["trash"]),
        ("Review: needs your answer", ["Note", "Question"], r["review"]),
        ("Left in place", ["Note", "Why"], r["left"]),
    ]
    for title, headers, rows in sections:
        if rows:
            lines += [f"## {title}", ""] + table(headers, rows) + [""]
    if r["review"]:
        lines += ["*To answer a Review question, set the note's `Parent` (and `Note Type` if needed) or move it "
                  "where it belongs. The next run learns a rule from your answer.*", ""]
    for title, items in [("Folders created", folders), ("Rules learned", rules), ("Renamed", run.renamed),
                         ("Problems", r["errors"])]:
        if items:
            lines += [f"## {title}", ""] + [f"- {i}" for i in items] + [""]
    if plan.get("notes_for_user"):
        lines += ["## Notes from the AI", "", plan["notes_for_user"], ""]
    return lines


# --- undo ------------------------------------------------------------------------

def latest_manifest() -> dict | None:
    runs = sorted(UNDO_DIR.glob("*/manifest.json")) if UNDO_DIR.exists() else []
    return json.loads(runs[-1].read_text()) if runs else None


def undo(vault: Path) -> None:
    m = latest_manifest()
    if not m or m.get("undone"):
        sys.exit("Nothing to undo.")
    snap = UNDO_DIR / m["id"]
    for op in reversed(m["ops"]):
        if op["op"] in ("move", "trash"):
            src, dst = vault / op["from"], vault / op["to"]
            src.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst.unlink()
            shutil.copy2(snap / op["from"], src)  # original text and date
        elif op["op"] == "create":
            (vault / op["path"]).unlink(missing_ok=True)
        elif op["op"] == "folder":
            folder = vault / op["path"]
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
    m["undone"] = True
    (snap / "manifest.json").write_text(json.dumps(m, indent=2))
    note = f" Rules it learned are still in {SETTINGS_FILE.name}; delete them there if needed." if m.get("rules_learned") else ""
    print(f"Undid run {m['id']}: {len(m['ops'])} changes reversed.{note}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("context", "apply", "undo"):
        sys.exit(__doc__)
    vault = find_vault(None)
    s = load_settings(vault)
    if sys.argv[1] == "context":
        print(json.dumps(context(vault, s), indent=1, default=str))
    elif sys.argv[1] == "apply":
        plan = json.loads(Path(sys.argv[2]).read_text())
        apply(vault, s, plan, "--preview" in sys.argv)
    else:
        undo(vault)


if __name__ == "__main__":
    main()
