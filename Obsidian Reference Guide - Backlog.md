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

### ~~3. Clean up properties on pre-system notes~~ ✅ Done 2026-10-13 (open questions in `99. Inbox/Review/00. Cleanup Review`)
- **Result:** 184 notes updated across the whole vault (Career Map included, Everyday left as is). Every note now has `Note Type` + `Parent`, old linking properties were turned into `Parent` or a `Related:` line, and Archive was flattened. Backup: `01. Obsidian Vaults/_Backups/`.
- **Left for step 6:** about 110 Career Map notes have no Parent, because their folders have no hub yet.

**Original plan:**
Most of the vault was written before the system existed. One catch-up pass, not perfection.
- **Scope:** every note **except** Career Map (step 6), `03. Everyday` (daily notes stay as they are) and `99. Inbox` (step 4).
- Give each note `Note Type` + `Parent`, and remove old properties.
- **Process:** Claude proposes properties in batches, the user approves, then Claude applies them.
- Merge tags, using the tag report.
- Flatten `999. Archive`: move the 10 files up out of the `Drafts` and `Working Notes` subfolders.
- **Decide first:** MOC tag vs `Note Type: MOC`. 7 notes are tagged `MOC` but have no `Note Type`.

### 4. Inbox cleanup tool
A tool kept in the repo that the user runs about once a week to clean up `99. Inbox`.
- **Its first real run is the current Inbox (about 25 notes)**, which finishes the cleanup and tests the tool at the same time.
- **Weekly procedure:**
  1. Scan every note in the Inbox.
  2. AI proposes Note Type, tags, Parent and destination (stays in Inbox, a Concept folder, or Archive), and flags Working notes that look finished.
  3. The user approves, edits or skips each row in one table.
  4. Apply: set the properties and move the files. Skipped notes stay in the Inbox for next week.
  5. Log what moved where.
- Keyword matching in plain Python was dropped. Routing needs judgment, so AI does it.
- **Leading option: a Claude Code skill** (`/clean-inbox`): one markdown file in the repo, included in the subscription, review step built in, and the file itself documents the procedure. Alternative: Python that calls the Claude API (needs an API key, costs per run).
- Moving files is safe: links use note names, not folder paths. Watch for the few duplicate note names (for example, `Idea Promotion System.md`, `00. Intro.md`).
- **Vault settings:** the tool moves files, so each vault states its folder names once (Inbox, Archive, Concept folders) in a short settings section. Nothing is hard-coded. The report scripts don't need this, because they only read the vault.

### 5. Property Base
A `.base` file in the repo for ongoing maintenance. It catches notes that drift from the system after the cleanup.
- Rows are notes. Saved views for: missing Note Type, missing Parent, old properties, retired `Draft` type.

### 6. Career Map
Built with a deliberate top-down structure before the system existed (about 150 notes, 130 of them with no properties).
- **First: check that Claude can map the full structure (the hierarchy) of Career Map accurately.** Claude needs the full list of Actions to do that.
- Then connect it to the system. A likely approach: each Action becomes a MOC, and Career Map–specific properties (LEAP, Bucket…) go only on the Action MOCs.
- Any exceptions apply to **this vault only, not the system**, and get written down in `Career Map in Obsidian.md`.

---

**Open decisions**
- Step 4: Claude Code skill or Python with the API? Should the first version ask the user to approve every note?

**Parked:** Status/As of Date as standard? · `Designbase.md` has no folder · finish `Obsidian-Background`?

**Decided:**
- Daily notes stay as they are in `03. Everyday`, and the cleanup doesn't touch them.
- ~~Step 2: Python reports for stats vs. Bases~~: Python reports for tag and property stats. Bases is saved for note lists (step 5).

**Out of scope:** Idea promotion system
