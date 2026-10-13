"""Property report: one row per property, showing how much it's used and whether it's part of the system.

Run:  python3 Scripts/property_report.py       (writes Reports/Property Report.md)
      python3 Scripts/property_report.py --vault ~/MyVault --out report.md

Properties outside the system aren't automatically wrong. A vault can add some through
custom templates. The report shows them so you can decide what to keep.
"""

import re
from collections import Counter, defaultdict

from vault_scan import find_vault, load_notes, parse_args, table, top, write_report

# What each property is, per the system design (Obsidian-Designbase.md).
KINDS = {
    "tags": "Obsidian built-in", "aliases": "Obsidian built-in", "cssclasses": "Obsidian built-in",
    "Note Type": "System: required", "Parent": "System: required",
    "Status": "System: optional", "As of Date": "System: optional",
}
KIND_ORDER = ["System: required", "System: optional", "Obsidian built-in", "Other"]
NOTE_TYPES = {"Working", "Reference", "MOC"}
MAX_DISTINCT_TO_LIST = 8  # show common values only for properties with few distinct values


def value_type(value) -> str:
    if value is None or value == []:
        return "empty"
    if isinstance(value, list):
        return "list"
    if re.fullmatch(r"\[\[.*\]\]", value):
        return "link"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", value):
        return "date"
    if re.fullmatch(r"-?\d+(\.\d+)?", value):
        return "number"
    return "text"


def build_report(notes) -> list[str]:
    stats = defaultdict(lambda: {"notes": 0, "filled": 0, "types": Counter(), "values": Counter(), "folders": Counter()})
    for note in notes:
        for key, value in (note.props or {}).items():
            s = stats[key]
            s["notes"] += 1
            s["filled"] += value not in (None, [])
            s["types"][value_type(value)] += 1
            s["folders"][note.folder] += 1
            for v in value if isinstance(value, list) else [value] if value else []:
                s["values"][v] += 1

    with_props = [n for n in notes if n.props]
    no_type = [n for n in notes if n.note_type == "(none)"]
    bad_types = Counter(n.note_type for n in notes if n.note_type != "(none)" and n.note_type not in NOTE_TYPES)
    # A MOC with no Parent is a Concept, so MOCs are left out of the "missing Parent" count.
    no_parent = [n for n in notes if n.note_type != "MOC" and not (n.props or {}).get("Parent")]
    by_lower = defaultdict(list)
    for key in stats:
        by_lower[key.lower()].append(key)

    lines = [
        "## Summary", "",
        f"- **Notes scanned:** {len(notes)}",
        f"- **Notes with any properties:** {len(with_props)}. **With none:** {len(notes) - len(with_props)}",
        f"- **Distinct properties:** {len(stats)}",
        "",
        "## System check", "",
        f"- **Missing `Note Type`:** {len(no_type)} notes ({top(Counter(n.folder for n in no_type), 5) or 'none'})",
        f"- **`Note Type` not Working / Reference / MOC:** "
        + (", ".join(f"`{t}` ({c})" for t, c in bad_types.most_common()) or "None"),
        f"- **Missing `Parent`** (MOCs not counted): {len(no_parent)} notes",
        "",
        "## Flags", "",
        "**Same property, different capitalization** (Obsidian treats these as one property):",
    ]
    lines += [f"- {', '.join(f'`{k}`' for k in keys)}" for keys in by_lower.values() if len(keys) > 1] or ["- None"]
    lines += ["", "**Defined but always empty:** "
              + (", ".join(f"`{k}`" for k, s in stats.items() if s["filled"] == 0) or "None")]

    rows = []
    for key, s in sorted(stats.items(), key=lambda kv: (KIND_ORDER.index(KINDS.get(kv[0], "Other")), -kv[1]["notes"])):
        values = top(s["values"], 3) if len(s["values"]) <= MAX_DISTINCT_TO_LIST else f"{len(s['values'])} distinct"
        rows.append([key, KINDS.get(key, "Other"), s["notes"], s["filled"], top(s["types"]), values, top(s["folders"])])
    lines += ["", "## All properties", "",
              "*Notes: how many notes have the property. Filled: how many of those have a value.*", ""]
    lines += table(["Property", "Kind", "Notes", "Filled", "Value types", "Common values", "Folders"], rows)
    return lines


def main():
    args = parse_args(__doc__.splitlines()[0], "Property Report.md")
    vault = find_vault(args.vault)
    write_report(args.out, "Property Report", vault, build_report(load_notes(vault)))


if __name__ == "__main__":
    main()
