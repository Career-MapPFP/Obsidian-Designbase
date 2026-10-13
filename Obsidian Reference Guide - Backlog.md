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

### 1. Update the templates
Do this first. Every new note starts from a template, so this stops more notes getting old properties.
- Replace the 6 old templates with 3 (Working, Reference, MOC), each with only `tags`, `Note Type` and `Parent`.
- Keep the Daily template as it is.
- Old properties to remove: `Action`, `Concept`, `Reference`, `LEAP`, `Bucket`, `Sub-Bucket`, `Semester`, `Resource Type`, `Parent MOC`.
- Retire the `Draft` template (Draft was folded into Working).

### 2. Tag report
Each tag is one row, with stats: how many notes use it, which folders, which Note Types, and first and last used.
- **Python script, no AI.** It writes a `Tag Report.md` that you read in Obsidian.
- Why not Bases: every row in Bases is a note, so it can't make each tag a row.
- Lives in this repo, as part of the system's maintenance tools.
- It shows how tags are actually used, which step 3 needs before merging tags.

### 3. Clean up properties on pre-system notes
Most of the vault was written before the system existed. One catch-up pass, not perfection.
- **Scope:** every note **except** Career Map (step 6), `03. Everyday` (daily notes stay as they are) and `99. Inbox` (step 4).
- Give each note `Note Type` + `Parent`, and remove old properties.
- **Process:** Claude proposes properties in batches, the user approves, then Claude applies them.
- Merge tags, using the tag report.
- Flatten `999. Archive`: move the 10 files up out of the `Drafts` and `Working Notes` subfolders.

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
- Step 2: is a Python report for tag stats plus Bases for note lists the right split?
- Step 4: Claude Code skill or Python with the API? Should the first version ask the user to approve every note?

**Parked:** Status/As of Date as standard? · MOC tag vs `Note Type: MOC` · `Designbase.md` has no folder · finish `Obsidian-Background`?

**Decided:** Daily notes stay as they are in `03. Everyday`, and the cleanup doesn't touch them.

**Out of scope:** Idea promotion system
