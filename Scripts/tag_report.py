"""Tag report: one row per tag, showing how much it's used and where.

Run:  python3 Scripts/tag_report.py            (writes Reports/Tag Report.md)
      python3 Scripts/tag_report.py --vault ~/MyVault --out report.md

Obsidian treats tags as case-insensitive, so `ToDo` and `todo` count as one tag.
Different spellings are listed under Flags so you can merge them.
"""

from collections import Counter, defaultdict

from vault_scan import find_vault, load_notes, parse_args, table, top, write_report


def build_report(notes) -> list[str]:
    stats = defaultdict(lambda: {"notes": set(), "props": 0, "inline": 0, "spellings": Counter(),
                                 "types": Counter(), "folders": Counter(), "last": None})
    for note in notes:
        in_props = set(note.property_tags)
        inline = set(note.inline_tags)
        for tag in in_props | inline:
            s = stats[tag.lower()]
            s["notes"].add(note.path)
            s["spellings"][tag] += 1
            s["props"] += tag in in_props
            s["inline"] += tag in inline
            s["types"][note.note_type] += 1
            s["folders"][note.folder] += 1
            s["last"] = max(filter(None, [s["last"], note.modified]))

    tagged = sum(1 for n in notes if n.property_tags or n.inline_tags)
    multi_spelling = {k: s for k, s in stats.items() if len(s["spellings"]) > 1}
    nested = sorted(k for k in stats if "/" in k)
    used_once = sorted(s["spellings"].most_common(1)[0][0] for s in stats.values() if len(s["notes"]) == 1)

    lines = [
        "## Summary", "",
        f"- **Notes scanned:** {len(notes)}",
        f"- **Notes with at least one tag:** {tagged} ({tagged * 100 // max(len(notes), 1)}%)",
        f"- **Distinct tags:** {len(stats)}",
        "",
        "## Flags", "",
        "**Same tag, different spellings** (consider merging):",
    ]
    lines += [f"- {', '.join(f'`{t}` ({c})' for t, c in s['spellings'].most_common())}"
              for s in multi_spelling.values()] or ["- None"]
    lines += ["", "**Nested tags** (the system doesn't use them; hierarchy comes from `Parent`):"]
    lines += [f"- `{t}`" for t in nested] or ["- None"]
    lines += ["", f"**Used in only one note** ({len(used_once)}): " + (", ".join(f"`{t}`" for t in used_once) or "None")]

    rows = []
    for s in sorted(stats.values(), key=lambda s: (-len(s["notes"]), s["spellings"].most_common(1)[0][0].lower())):
        rows.append([s["spellings"].most_common(1)[0][0], len(s["notes"]), s["props"], s["inline"],
                     top(s["types"]), top(s["folders"]), s["last"]])
    lines += ["", "## All tags", "",
              "*Properties / Inline: how many notes use the tag in their properties vs. in the note text.*", ""]
    lines += table(["Tag", "Notes", "Properties", "Inline", "Note Types", "Folders", "Last edited"], rows)
    return lines


def main():
    args = parse_args(__doc__.splitlines()[0], "Tag Report.md")
    vault = find_vault(args.vault)
    write_report(args.out, "Tag Report", vault, build_report(load_notes(vault)))


if __name__ == "__main__":
    main()
