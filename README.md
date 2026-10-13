# Obsidian-Designbase

A small system for organizing an Obsidian vault with as little admin as possible, plus the tools that keep it maintained.

Organization comes from links and properties, not folders. Every note gets one `Note Type` (Working, Reference or MOC) and one `Parent` (the MOC it belongs to). New notes land in an Inbox, and a Claude Code skill files them for you.

The full system is in **[Obsidian-Designbase.md](Obsidian-Designbase.md)**. Read that first.

## What's in this folder

| Path | What it is |
| --- | --- |
| `Obsidian-Designbase.md` | The system: the rules, the Note Types, routing, and folders |
| `Templates/` | One template per Note Type |
| `Bases/` | Live views of the vault: Vault Health, Vault Overview, and MOC Contents (embedded in every MOC) |
| `Scripts/` | Tag and property reports, to spot notes that drift from the system |
| `.claude/skills/clean-inbox/` | The `/clean-inbox` Claude Code skill, which empties the Inbox |
| `Obsidian Reference Guide - Backlog.md` | What's done and planned. It describes the author's own vault as a worked example |

## Requirements

- **Obsidian 1.9 or later**, with the **Bases** and **Templates** core plugins turned on.
- **Python 3.10 or later** for the scripts. They use only the standard library, so there's nothing to install.
- **[Claude Code](https://claude.com/claude-code)** for `/clean-inbox`. Everything else works without it.

## Setup

1. **Copy this whole folder into your vault.** It can go anywhere, for example in an Admin folder. Keep it together: the tools find your vault by walking up to its `.obsidian` folder, and the skill reuses code in `Scripts/`.
2. **Create the core folders** at the top level of your vault: an Inbox, an Archive, and an Admin folder (see "Folder Structure" in the design note). Every other top-level folder is a Concept folder, and those are up to you.
3. **Point Obsidian at the templates.** In Settings → Templates, set the template folder to this folder's `Templates/`.
4. **Make your Inbox the default location for new notes.** Settings → Files and links → Default location for new notes.
5. **Run `/clean-inbox` once.** Open a terminal in this folder, start Claude Code, and type `/clean-inbox`. On the first run it creates `Inbox Cleanup Settings.md` with its best guess at your folder names, then stops. Check the folder names, then run it again. Use `/clean-inbox preview` to see what it would do without changing anything, and `/clean-inbox undo` to reverse the last run.

## Names the tools rely on

You can rename most things, but these names are read by the tools:

- **Properties:** `Note Type` (values `Working`, `Reference` or `MOC`), `Parent` (a link to a MOC), and `tags`.
- **Inbox and Archive folders:** their names must contain the words `Inbox` and `Archive`, because the Bases find them by name. Numbered names like `99. Inbox` are fine. `/clean-inbox` reads the exact folder names from `Inbox Cleanup Settings.md`.
- **`Templates/` and `Reports/`** inside this folder: the Bases and scripts skip them, so templates and reports don't show up as notes.
- **`MOC Contents.base`:** MOCs embed it by name (`![[MOC Contents.base]]`), so don't rename it.

## Reports

```
python3 Scripts/tag_report.py
python3 Scripts/property_report.py
```

These write `Reports/Tag Report.md` and `Reports/Property Report.md`. Run them before any cleanup so the numbers are current. Use `--vault <path>` if your vault isn't found automatically.
