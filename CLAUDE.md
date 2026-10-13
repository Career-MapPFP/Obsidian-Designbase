---
tags:
  - AIContext
Note Type:
  - Reference
Parent: "[[Obsidian-Designbase]]"
---

# CLAUDE.md — Obsidian-Designbase

This folder holds the design for how the user organizes their Obsidian vault. Read this file before you review, change, or apply that system.

## Files here

- **[[Obsidian-Designbase]]** — the system itself and the source of truth. Read it before you touch notes anywhere in the vault.
- **[[Obsidian Reference Guide - Backlog]]** — work that's done, planned or undecided, in order. Struck-through steps are done. The "Parked", "Decided" and "Out of scope" lines are deliberate decisions.
- Other notes in this folder are the user's personal notes (see "Git repo" below).

## Git repo

This folder is a git repo that will eventually be published on GitHub, so anyone can use it to set up a vault with this system (Note Type, CIAA, and so on).

- **What's tracked:** the shareable system, meaning `Obsidian-Designbase.md`, the core templates in `Templates/` (one per Note Type), `Scripts/`, `Bases/`, the `/clean-inbox` skill in `.claude/skills/`, the Backlog (a public roadmap), this file, and `.gitignore`.
- **What moves to another vault:** the whole repo folder, not single pieces. The tools find the vault by walking up to its `.obsidian` folder, and the skill's helper reuses `Scripts/vault_scan.py`.
- **Scripts** (`Scripts/`, tracked): `tag_report.py` and `property_report.py` write `Reports/Tag Report.md` and `Reports/Property Report.md`. They use only the Python standard library, and `vault_scan.py` holds the code both share. `Reports/` is in `.gitignore`, because a report describes one specific vault. Re-run the scripts before cleanup work so the numbers are current.
- **Inbox cleanup** (tracked): everything is in `.claude/skills/clean-inbox/`. `SKILL.md` does the judgment, and `clean_inbox.py` does the mechanics (`context`, `apply plan.json [--preview]`, `undo`), reusing `Scripts/vault_scan.py`. Undo data is kept in `Reports/.undo/`. Vault-specific and not tracked: `Inbox Cleanup Settings.md`, one note holding the folder names and the rules learned from the user's Review answers. It's created on the first run. Routing follows the design note's Routing table. Keep the settings note out of `.claude`, because Obsidian hides dot-folders.
- **Bases** (`Bases/`, tracked): `Vault Health.base`, `Vault Overview.base`, and `MOC Contents.base` (embedded in MOCs through the MOC template; it uses `this`, meaning the MOC it's embedded in). Keep them working in any vault: find the Inbox and Archive by name, skip `/Templates/` and `/Reports/`, and read `Note Type` with `list(note["Note Type"])` because it may be stored as a list. Obsidian rewrites a `.base` file in its own format whenever the user changes a view, and drops `#` comments. That's expected, so keep explanations in the design note instead of in comments.
- **Templates:** this folder is the vault's template folder, set in Obsidian's settings. Core templates (part of the system) sit in `Templates/`. Templates for this vault only (Daily, Career Map MOCs) sit in `Templates/Custom/`, which is in `.gitignore`. Custom templates add properties for a particular kind of Concept. Don't put them in the core templates.
- **What's excluded on purpose (listed in `.gitignore`):** `Career Map in Obsidian.md` and `Obsidian vs Notion.md`. They're about the user's own vault, and some of their links point to notes outside this folder, which would be broken for anyone else. They still exist in the folder and in Obsidian. Git just ignores them.
- **For new files:** if a note is tied to the user's own vault, add it to `.gitignore`. If it's part of the shareable system, track it. If you're not sure, ask before committing. Anything committed stays in the git history after a push, even if it's deleted later.
- **Before publishing:** the "Folders In This Vault" section of the design note describes the user's specific vault. Consider labeling it as an example for a public audience.
- **Writing style:** keep the design note as simple and clear as possible. Prefer plain wording over clever wording.

## These are shared working files

The user and Claude both edit these files. The user often changes them directly without saying so. That's expected, and those edits are deliberate.

- **The file as it is now is the current version.** If it differs from what you wrote earlier, the user changed it on purpose. Don't treat it as a mistake.
- **Re-read a file before editing it.** Change only what you were asked to change, and never rewrite a file from memory or overwrite the user's wording.
- **If something looks accidental, ask.** Don't fix it yourself.

## What this system is for

The goal is to use Obsidian well **with as little admin as possible**. Organization comes from links and properties, not folders. Folders are only for browsing. The system is deliberately small: 4 native features with one job each, plus 1 invented property (`Note Type`).

## How to review or advise on it

- **Look at the big picture.** The question that matters is whether the system reliably gets the user the benefits of Obsidian (links and backlinks, structure that grows over time, quick capture, notes that are easy to find) without much admin overhead. Any system can be nitpicked. Don't send lists of small inconsistencies or arguments about wording.
- **The user has decided:** the tags-vs-Note-Type overlap is accepted as-is ("no perfect way to describe it").
- **`Status` is not how a note gets marked "done".** It's optional and only for long-term projects. Don't propose making it required.
- **Don't add new properties, Note Types, or processes.** Every rule has to fit in Layer 1 or Layer 2. Check "Retired ideas" in the design note before suggesting something, because it may already have been rejected.
- **The thing that most affects whether this works is that the Inbox gets processed.** That's `/clean-inbox`'s job, so the user doesn't have to triage by hand.
- **Say "MOC", not "hub".** That's the user's term.

## Key decisions (the design note has the full rules)

- **Route by where a note belongs, not by whether it's finished.** The user never marks notes done. Working notes go to the Archive (meaning "out of the way", not "finished") and stay visible on their MOC through `Parent` and the MOC Contents embed.
- **Every note gets a Parent.** Blank MOCs are fine: a MOC's minimum job is to collect backlinks. Exceptions: Concept MOCs and daily notes.
- **A Concept gets its own folder only once a Reference note or sub-MOC lands under it.** Working notes never trigger a folder.
- **The Inbox is temporary.** Unclear notes go to its Review folder with a question, and the user's answers become rules in `Inbox Cleanup Settings.md`.
- **Never lose content.** Changing or merging content is allowed if nothing is lost. Deleted notes go to Obsidian's trash.

## Scope

- The system applies to the whole `01. Career Map` vault, including the `01. Career Map` project folder. That folder was converted on 2026-10-13 (Backlog step 6). **Read `Career Map in Obsidian.md` before touching it.** It sets out the fixed hierarchy (Goal → Outcomes → Buckets → Sub-Buckets → Actions, with Airtable as the source of truth), the MOC chain, the folder layout, and the Action MOC properties. Its exceptions apply to this vault only, never to the system.
- **Outcomes are not Domains.** Outcomes come from the Career Map's backward design. Domains is a separate, later idea that lives under CM System Design (Domains-MOC). Don't merge them.
- `03. Everyday` (daily notes) stays where it is. Daily notes are `Note Type: Working` with no `Parent` (see the Daily template in `Templates/Custom/`).
- The one-time cleanups are done (2026-10-13). Almost every note has `Note Type`, `Parent` and a tag. What's left (Admin notes, retired templates) is on the Backlog's Parked list and shows in `Bases/Vault Health.base`. Backups from before each big change are in `01. Obsidian Vaults/_Backups/`.

## Before you change notes

- `/clean-inbox` may move and edit Inbox notes without asking. That's its job, and it can be undone.
- Anything else: ask before moving, renaming, or bulk-editing notes.
- Links use note names, not folder paths, so moving a note doesn't break its links. The exception is two notes with the same name, so check for that first.
- Keep modified dates when you edit properties in bulk (restore the file's mtime), so sorting by date in Obsidian still works.
