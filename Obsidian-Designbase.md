---
tags:
  - MOC
  - SOP
Note Type:
  - MOC
Parent:
Status:
  - Active
As of Date: 2026-10-12
---

# Core Principle

This system has exactly two layers:

1. **4 native Obsidian features, each given exactly one job.**
2. **1 invented mechanism (Note Type)** layered on top, which does two things: routing, and deciding which properties a note carries.

If a rule doesn't obviously belong to Layer 1 or Layer 2, it doesn't belong in the system.

**Organization comes from links and properties, not folders.** Most computers train you to organize by folder; Obsidian is the opposite. Folders are just for browsing — so you never need to get them "right."

The system is the same in every vault. Only the set of Concept folders changes (see This Vault below).

---

# Layer 1: Native Features (each has one job)

| Feature    | Job                                            | Question it answers         |
| ---------- | ---------------------------------------------- | --------------------------- |
| Tags       | Discovery                                      | What IS this note?          |
| Properties | Structured attributes                          | What KIND of note is this?  |
| Links      | Relationships between notes                    | What is this note ABOUT?    |
| Folders    | Physical organization for browsing             | Where do I browse for this? |

### Tags
- **Freeform, no fixed vocabulary.** Any tag is valid. No approved list to check first.
- **Used in two places:** in the note's properties, and inline in the body wherever it's naturally relevant.
- **Not for routing** — that's Note Type's job.
- **Not for hierarchy** — that's `Parent`'s job. No nested tags (`#topic/subtopic`).

### Properties
As few as possible, fixed by Note Type — never invented ad hoc per note. A vault can add properties for a kind of Concept through a custom template (see Templates).

| Property    | Applies to  | Definition                                                                                                                                                      |
| ----------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Note Type` | Every note  | Working / Reference / MOC. Single value.                                                                                                                        |
| `Parent`    | Every note  | A single link to the nearest MOC this note belongs to. Determines the note's folder. Blank on a Concept and on daily notes. A note relevant elsewhere links there inline — not a second Parent. |
| `Status`    | Incidental  | Lifecycle state, e.g. `Active`. Not yet standard — see Backlog.                                                                                                 |
| `As of Date`| Incidental  | Date the content was last confirmed accurate. Not yet standard — see Backlog.                                                                                    |

### Links
Organic — happen naturally while writing, not planned.

---

# Layer 2: Note Type (the one invented mechanism)

| Note Type | Purpose                                 | Example Tags                                               |
| --------- | --------------------------------------- | ---------------------------------------------------------- |
| Working   | Temporary, ephemeral thinking artifacts | ToDo, Meeting, Commentary, Storyboard, CheckIn, Design, Idea |
| Reference | Permanent, maintained knowledge assets  | Guidelines, DataDictionary, SOP, Framework, Tool, Research |
| MOC       | Organizational hub, collects backlinks  | Project MOCs, Topic MOCs                                   |

Every note has exactly one Note Type.

- **Working** — you're thinking, not documenting. Expected to go stale — no need to mark it done. The inbox cleanup files it in the Archive.
- **Reference** — the thing itself is the point. Meant to be found again and trusted later. Maintained, not just written once.
- **MOC** — a hub. Can be an empty stub or fully written out — what matters is that other notes point to it.

### Routing

| Note                          | Lives in                                       |
| ----------------------------- | ---------------------------------------------- |
| New, not yet processed        | Inbox                                          |
| Working                       | Archive — still linked to its MOC through `Parent` |
| Reference                     | The folder of the Concept its `Parent` chain leads to |
| MOC, no `Parent` (a Concept)  | A single file in a top-level folder; gets its own folder once a Reference note or sub-MOC lands under it |
| MOC, has a `Parent` (nested)  | The folder of the Concept its `Parent` chain leads to — no folder of its own |
| Basically blank               | Deleted                                        |

- **Every note gets a `Parent`.** If nothing fits, create a blank MOC — a MOC's minimum job is to collect backlinks.
- **To keep a Working note out of the Archive**, file it in its Concept folder yourself (e.g. an active project). Older Working notes already in Concept folders can stay there.
- **The Inbox is temporary.** The inbox cleanup (`/clean-inbox`, see Tools) applies this table. Notes it can't place go to a Review folder in the Inbox with a question.

---

# Folder Structure

### CIAA — the only top-level structure

- **Concepts** — every top-level folder that isn't one of the other three.
- **Inbox** — landing folder for everything new. Temporary — emptied by the inbox cleanup.
- **Archive** — Working notes, out of the way (not necessarily finished). Global by default, local by exception (only if a Concept is big enough to want its own).
- **Admin** — templates, system configuration.

### MOCs and folders

- **Concepts are MOC stubs.** Start minimal. Backlinks surface related content — organize only as needed.
- **Only a Concept (a MOC with no `Parent`) gets its own folder** — and only once a Reference note or sub-MOC lands under it. Until then it's a single file in a top-level folder.
- **Hierarchy is expressed through `Parent`, not nested folders.** If "Contracts" emerges as a hub inside Disney, it's just a note with `Parent: [[Disney]]` living in the Disney folder.
- **A note lives in the folder at the end of its `Parent` chain**, not necessarily its immediate Parent. A note under "Contracts" still lives in the Disney folder.
- A top-level folder can be one Concept (e.g. Career Map) or a group of Concepts (e.g. Analysis holds Obsidian, Designbase, …). Either is fine — it's browsing only.

###  Folders In This Vault 

| Folder              | CIAA role | What's in it                                                         |
| ------------------- | --------- | -------------------------------------------------------------------- |
| `99. Inbox`         | Inbox     | Default location for new notes. Cleaned up with `/clean-inbox`       |
| `01. Career Map`    | Concept   | The Career Map project. Its older, top-down structure is being brought into the system (see Backlog) |
| `02. LABs`          | Concept   | Empty for now                                                        |
| `03. Everyday`      | Concept   | Daily notes                                                          |
| `04. Analysis`      | Concept   | Research and general-knowledge topics (Obsidian, Designbase, Website Hosting) |
| `05. Record Keeping`| Admin     | Attachments, data backups (templates live in `Obsidian-Designbase/Templates`) |
| `999. Archive`      | Archive   | Working notes, out of the way                                        |

---

# Note Creation Workflow

1. **Start in Inbox** from a template (see Templates) so properties are never typed from memory.
2. **Add a tag** — what IS this?
3. **Set properties** — `Note Type`, and `Parent` (the nearest MOC it belongs to).
4. **Link as you write.**
5. **Let the inbox cleanup file it** — run `/clean-inbox` whenever the Inbox needs clearing, or move a note yourself per the Routing table. MOCs skip the Inbox and are created where they live.

---

# Templates

- **Core templates** — one per Note Type (Working, Reference, MOC), in `Templates/`. Part of the system.
- **Custom templates** — a vault can add its own for a kind of Concept. Example: a Project MOC with `Start Date` and `Client`. They live in `Templates/Custom/` and belong to the vault, not the system.

---

# Tools

Kept in this repo so the system maintains itself with as little admin as possible.

- **`/clean-inbox`** — a Claude Code skill that empties the Inbox per the Routing table: decides each note's Note Type, Parent and tag, creates blank MOCs where needed, files everything, and writes a report. Learns from your answers to Review questions.
- **Tag and property reports** — `Scripts/tag_report.py` and `Scripts/property_report.py`. One row per tag / property, to spot drift from the system.
- **Bases** (`Bases/`) — live views of the vault in Obsidian:
  - **Vault Health** — what needs fixing: missing Note Type or Parent, untagged notes, old properties, Inbox backlog, MOCs nothing points to.
  - **Vault Overview** — the big picture: notes by Note Type and area, hubs ranked by size, recent activity, stale Working notes, Reference notes due for a re-check.
  - **MOC Contents** — embedded in every MOC (it's in the MOC template). Lists every note connected to that hub, grouped by Note Type — including archived Working notes.

---

# Related Notes

- [[Obsidian Reference Guide - Backlog]] — open decisions and planned cleanup

---

# Appendix

### Where this comes from
A synthesis, not something novel — worth knowing so you can borrow from any of them instead of reinventing:
- **Zettelkasten** — Working / Reference / MOC = fleeting / permanent / structure notes.
- **LYT (Nick Milo)** — MOCs, and "start as a stub, grow only as needed."
- **PARA** — CIAA is a compressed PARA.

### Retired ideas (from earlier versions — don't reintroduce without a reason)
- **Draft as a 4th Note Type** — folded into Working. Ideas, thoughts, questions are just Working notes with a tag.
- **Context-named concept properties** (`Project:`, `Network:`, `Topic:`, `Action:`, `Concept:`) — replaced by one `Parent` property.
- **`Reference` property** for secondary grouping — dropped; use an inline link.
- **Letting Career Map's structure drive the vault** — the vault has one system; Career Map is one Concept within it.
- **Idea Promotion System** — out of scope for this system.

![[MOC Contents.base]]
