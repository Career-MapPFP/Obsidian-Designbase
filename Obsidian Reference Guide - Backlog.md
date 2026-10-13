---
tags:
  - ToDo
Note Type:
  - Working
Parent: "[[Obsidian-Designbase]]"
---

# Backlog

One step at a time, in this order. Each step makes the next one easier.

**Goal:** bring the vault up to the system, then give it tools that keep it there. The tools (report, skill, Bases, templates) go in this repo so anyone can use them.

---

### ~~1. Update the templates~~ ✅ Done 2026-10-13
- Templates moved from `05. Record Keeping/Templates` into this repo's `Templates/` folder, and Obsidian's settings now point here.
- Core templates (in the repo): Working, Reference, MOC, each with only `tags`, `Note Type` and `Parent`.
- Custom templates (`Templates/Custom/`, left out of the repo): Daily (unchanged), plus `MOC CM` and `MOC Analysis` kept as-is as placeholders until step 6 decides on Career Map's customizations.
- Old Working and Reference templates deleted (replaced). The retired Draft template moved to `999. Archive`.

### ~~2. Tag and property reports~~ ✅ Done 2026-10-13
Two Python scripts in `Scripts/` (standard library only, no AI). Run them whenever you want an up-to-date picture of the vault.
- `python3 Scripts/tag_report.py` writes `Reports/Tag Report.md`. One row per tag: how many notes, used in properties vs. inline, Note Types, folders, last edited. It also flags the same tag spelled differently, nested tags, and tags used in only one note.
- `python3 Scripts/property_report.py` writes `Reports/Property Report.md`. One row per property: kind (system / Obsidian built-in / other), how many notes have it and how many fill it in, value types, common values, folders. It also has a system check (missing Note Type, invalid Note Types, missing Parent) and flags properties that are always empty.
- Why not Bases: every row in Bases is a note, so it can't make each tag or property a row.
- The scripts are in the repo. The reports aren't, because they describe one specific vault.
- **First run (2026-10-13):** 223 notes. 185 have no Note Type, 14 still use `Draft`, and 25 distinct properties are in use (17 of them outside the system). 31 tags, 15 of them used only once.

### ~~3. Clean up properties on pre-system notes~~ ✅ Done 2026-10-13 (its review note is archived; the open questions moved to Parked below)
- **Result:** 184 notes updated across the whole vault (Career Map included, Everyday left as is). Every note now has `Note Type` + `Parent`, old linking properties were turned into `Parent` or a `Related:` line, and Archive was flattened. Backup: `01. Obsidian Vaults/_Backups/`.
- **Left for step 6:** about 110 Career Map notes have no Parent, because their folders have no MOC yet.

**Original plan:**
Most of the vault was written before the system existed. One catch-up pass, not perfection.
- **Scope:** every note **except** Career Map (step 6), `03. Everyday` (daily notes stay as they are) and `99. Inbox` (step 4).
- Give each note `Note Type` + `Parent`, and remove old properties.
- **Process:** Claude proposes properties in batches, the user approves, then Claude applies them.
- Merge tags, using the tag report.
- Flatten `999. Archive`: move the 10 files up out of the `Drafts` and `Working Notes` subfolders.
- **Decide first:** MOC tag vs `Note Type: MOC`. 7 notes are tagged `MOC` but have no `Note Type`.

### ~~4. Inbox cleanup tool (`/clean-inbox`)~~ ✅ Done 2026-10-13
Run it whenever the Inbox needs clearing. No approvals, no marking notes done.
- **The skill** (`.claude/skills/clean-inbox/`) makes the judgment calls for each note: blank? → Note Type → Parent (an existing MOC, or create a blank one) → tag → destination. Only genuinely unclear notes go to Review, with one question.
- **The helper** (`clean_inbox.py`, in the same skill folder) applies the plan: sets properties, moves files (Working → Archive, Reference/MOC → Concept folder), creates folders only for Reference notes or sub-MOCs, deletes blank notes to Obsidian's trash, renames on name collisions, saves undo data, and writes `Reports/Inbox Cleanup Report.md`.
- **Learning:** answer a Review question by setting the note's Parent or moving it. The next run turns your answer into a rule in `Inbox Cleanup Settings.md` and applies it from then on.
- **Undo:** `/clean-inbox undo` reverses the last run. Tested on a copy of the vault: the copy came back identical.
- **Settings:** `Inbox Cleanup Settings.md`, one note per vault with the folder names and learned rules. It's created on the first run, so the tool works in any vault.
- **First run (2026-10-13):** 17 Working notes archived, 1 Reference filed, 8 MOCs created, 3 blank notes deleted, 0 problems. The Inbox is empty apart from 2 Review notes.
- Decisions made along the way: route by where a note belongs, not by whether it's finished; Archive means "out of the way"; every note gets a Parent (blank MOCs are fine); a skill, not an API script, so no extra setup or cost.
- **Portable:** the unit you move is the whole Obsidian-Designbase repo folder, not the skill alone (the helper reuses `Scripts/vault_scan.py` and finds the vault by walking up from the repo). To use it in another vault, clone the repo anywhere inside that vault. Each vault gets its own settings note.
- **Still to verify:**
  - [ ] Open a fresh Claude Code session in this folder and check that `/clean-inbox` appears and runs from start to finish. So far the skill's steps were followed by hand in the session that built it.
  - [ ] The learning loop: answer the 2 Review notes (the duplicates), run again, and check that a rule lands in the settings note.
  - [ ] Undo on a real run. It's only been tested on a copy of the vault.
- **Idea:** also learn from corrections. If you move a note the tool filed, or change its Parent, the next run could spot it (each run's undo record lists where every note went) and turn it into a rule.

### ~~5. Bases~~ ✅ Done 2026-10-13
Three bases in `Bases/`, part of the system:
- **Vault Health:** one view per kind of drift (missing Note Type / invalid Note Type / missing Parent / untagged / old properties / Inbox backlog / lonely MOCs).
- **Vault Overview:** by Note Type, by area, MOCs ranked by how many notes point to them, active in the last 30 days, Working notes going stale (90+ days, outside Archive), Reference to re-check (180+ days untouched).
- **MOC Contents:** embedded in the MOC template, so every MOC lists its connected notes (archived ones included).
- [x] Vault Health checked in Obsidian: All issues shows one column per problem (140 notes, mostly Career Map waiting on step 6).
- [x] Vault Overview checked in Obsidian (the Note Type views fit the system well).
- [ ] Check a MOC's embedded table in Obsidian (e.g. Create a Website-MOC).
- [x] MOC Contents embed added to all 18 existing MOCs (2026-10-13). `/clean-inbox` adds it to every MOC it creates.

### ~~6. Career Map~~ ✅ Done 2026-10-13
- **Result:** the Career Map folder was restructured: `00. Design` plus one folder per Outcome (Technical / Communication / Leadership / Consulting), each holding its Actions. The LEAP folders are gone, because LEAP is a property now.
- **MOCs:** a new Career Map MOC, 4 Outcome MOCs, and 15 Action MOCs with Airtable properties (Action ID, Bucket, Sub-Bucket, LEAP, Semester, Resource Type). Every Career Map note has `Note Type`, `Parent` and a tag (124 notes tagged).
- **Moved in:** Journalling → Develop Daily Reflection-MOC; ConfusionWarfare → Confusion Warfare-MOC (an Action); Website Hosting → under Create a Website. Domains-MOC was created under CM System Design, with Non-Profit beneath it. The two Review duplicates were archived with their active version's Parent.
- **Checked:** no broken links (folder-path links rewritten), and every note's text matches the pre-change backup (`_Backups/career-map-vault-pre-step6-…`). The rules are written down in `Career Map in Obsidian.md`.
- [ ] Look it over in Obsidian: the Career Map MOC, an Outcome MOC's table, and an Action MOC's properties.
Built with a deliberate top-down structure before the system existed (about 150 notes, 130 of them with no properties).
- **First: check that Claude can map the full structure (the hierarchy) of Career Map accurately.** Claude needs the full list of Actions to do that.
- Then connect it to the system. A likely approach: each Action becomes a MOC, and Career Map–specific properties (LEAP, Bucket…) go only on the Action MOCs.
- Any exceptions apply to **this vault only, not the system**, and get written down in `Career Map in Obsidian.md`.

---

**Parked:** Status/As of Date as standard? · delete the retired `Template - Draft Note` in `999. Archive`? · `05. Record Keeping` (Admin) notes have no Parent. Fine, or give Admin a MOC? · finish `Obsidian-Background`?

**Decided:**
- A Concept MOC gets its own folder only once a Reference note or sub-MOC lands under it (this settles "`Designbase.md` has no folder").
- Daily notes stay in `03. Everyday`, with `Note Type: Working` and no `Parent`. All 28 existing daily notes were updated on 2026-10-13.
- ~~Step 2: Python reports for stats vs. Bases~~: Python reports for tag and property stats. Bases is saved for note lists (step 5).

**Out of scope:** Idea promotion system
