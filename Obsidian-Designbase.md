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

**Folders are for browsing, metadata is for finding.** Retrieval depends on tags/properties/links, not folder placement — so reorganizing folders later is cosmetic, never structural. You should never need to "get the folders right."

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
As few as possible, fixed by Note Type — never invented ad hoc per note.

| Property    | Applies to  | Definition                                                                                                                                                      |
| ----------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Note Type` | Every note  | Working / Reference / MOC. Single value.                                                                                                                        |
| `Parent`    | Every note  | A single link to the nearest MOC this note belongs to. Determines the note's folder. Blank on a Concept. A note relevant elsewhere links there inline — not a second Parent. |
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

- **Working** — you're thinking, not documenting. Expected to go stale and get archived once done.
- **Reference** — the thing itself is the point. Meant to be found again and trusted later. Maintained, not just written once.
- **MOC** — a hub. Can be an empty stub or fully written out — what matters is that other notes point to it.

### Routing

| Note Type                     | Lives in                                       |
| ----------------------------- | ---------------------------------------------- |
| Working (active)              | Inbox                                          |
| Working (done)                | Archive                                        |
| Reference                     | The folder of the Concept its `Parent` chain leads to |
| MOC, no `Parent` (a Concept)  | Its own folder, named after it                 |
| MOC, has a `Parent` (nested)  | The folder of the Concept its `Parent` chain leads to — no folder of its own |

---

# Folder Structure

### CIAA — the only top-level structure

- **Concepts** — every top-level folder that isn't one of the other three.
- **Inbox** — landing folder for everything new.
- **Archive** — finished Working notes. Global by default, local by exception (only if a Concept is big enough to want its own).
- **Admin** — templates, system configuration.

### MOCs and folders

- **Concepts are MOC stubs.** Start minimal. Backlinks surface related content — organize only as needed.
- **Only a Concept (a MOC with no `Parent`) gets its own folder.**
- **Hierarchy is expressed through `Parent`, not nested folders.** If "Contracts" emerges as a hub inside Disney, it's just a note with `Parent: [[Disney]]` living in the Disney folder.
- **A note lives in the folder at the end of its `Parent` chain**, not necessarily its immediate Parent. A note under "Contracts" still lives in the Disney folder.
- A top-level folder can be one Concept (e.g. Career Map) or a group of Concepts (e.g. Analysis holds Obsidian, Designbase, …). Either is fine — it's browsing only.

###  Folders In This Vault 

| Folder              | CIAA role | What's in it                                                         |
| ------------------- | --------- | -------------------------------------------------------------------- |
| `99. Inbox`         | Inbox     | Default location for new notes                                       |
| `01. Career Map`    | Concept   | The Career Map project. Its internal structure is the project's own business, not the vault system's |
| `02. LABs`          | Concept   | Empty for now                                                        |
| `03. Everyday`      | Concept   | Daily notes                                                          |
| `04. Analysis`      | Concept   | Research and general-knowledge topics (Obsidian, Designbase, Website Hosting) |
| `05. Record Keeping`| Admin     | Templates, attachments, data backups                                 |
| `999. Archive`      | Archive   | Finished Working notes                                               |

---

# Note Creation Workflow

1. **Start in Inbox** from a template (`05. Record Keeping/Templates`) so properties are never typed from memory.
2. **Add a tag** — what IS this?
3. **Set properties** — `Note Type`, and `Parent` (the nearest MOC it belongs to).
4. **Link as you write.**
5. **Move when ready** — per the Routing table above. MOCs skip the Inbox and are created where they live.

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
