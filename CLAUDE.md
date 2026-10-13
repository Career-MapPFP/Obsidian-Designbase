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
- **[[Obsidian Reference Guide - Backlog]]** — work that's planned or undecided, in priority order. The "Parked" and "Out of scope" lines are deliberate decisions.
- Other notes in this folder are the user's personal notes (see "Git repo" below).

## Git repo

This folder is a git repo that will eventually be published on GitHub, so anyone can use it to set up a vault with this system (Note Type, CIAA, and so on).

- **What's tracked:** the shareable system, meaning `Obsidian-Designbase.md`, the core templates in `Templates/` (one per Note Type), the Backlog (a public roadmap), this file, and `.gitignore`.
- **Scripts** (`Scripts/`, tracked): `tag_report.py` and `property_report.py` write `Reports/Tag Report.md` and `Reports/Property Report.md`. They use only the Python standard library, and `vault_scan.py` holds the code both share. `Reports/` is in `.gitignore`, because a report describes one specific vault. Re-run the scripts before cleanup work so the numbers are current.
- **Inbox cleanup** (tracked): the `/clean-inbox` skill (`.claude/skills/clean-inbox/SKILL.md`) does the judgment, and `Scripts/clean_inbox.py` does the mechanics (`context`, `apply plan.json [--preview]`, `undo`). Undo data is kept in `Reports/.undo/`. Vault-specific and not tracked: `vault_settings.json` (folder names; `vault_settings.example.json` is the tracked example) and `Routing Rules.md` (rules learned from the user's Review answers). Routing follows the design note's Routing table.
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
- **The thing that most affects whether this works is that the Inbox gets processed.** Out-of-date templates come second, because every new note starts from one.

## Scope

- The system applies to the whole `01. Career Map` vault, including the `01. Career Map` project folder. Bringing that folder into the system is backlog item 3. It was built top-down before the system existed, so it may need exceptions. Those exceptions apply only to this vault, never to the system, and they're written down in `Career Map in Obsidian.md`. Don't restructure the folder until item 3 has been planned with the user.
- `03. Everyday` (daily notes) stays where it is. Daily notes are `Note Type: Working` with no `Parent` (see the Daily template in `Templates/Custom/`).
- Most of the vault was written before this system existed. Many notes have no properties or still use old ones (`Action`, `Concept`, `Reference`, `Draft`). That's expected. Fixing it is backlog item 2, so don't treat it as a design flaw.

## Before you change notes

Ask before moving, renaming, or bulk-editing notes. Moving or renaming files outside Obsidian can break links, because Obsidian only updates links for changes made inside the app.
