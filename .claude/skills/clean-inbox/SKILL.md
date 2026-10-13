---
name: clean-inbox
description: Clean up the Obsidian vault's Inbox using the Obsidian-Designbase system. For each Inbox note, decide its Note Type, Parent (MOC) and tag, create blank MOCs where needed, file it (Working → Archive, Reference/MOC → Concept folder), delete blank notes, send unclear ones to Review, and write the Inbox Cleanup Report. Learns from the user's Review answers. Use when the user says "clean up my inbox", "/clean-inbox", "/clean-inbox preview" or "/clean-inbox undo".
---

# Clean Inbox

You're the judgment half of the inbox cleanup. `clean_inbox.py`, in this skill's folder, is the mechanical half: it reads the vault, applies your plan, saves undo data and writes the report. In the commands below, `clean_inbox.py` means the full path to that file.

The rules come from `Obsidian-Designbase.md` (Routing table). Read it if you're unsure about anything.

**Arguments:** none (normal run) · `preview` (report only, change nothing) · `undo` (reverse the last run: run `python3 clean_inbox.py undo` and stop).

## 1. Get the context

```
python3 clean_inbox.py context > /tmp/inbox_context.json
```

On the very first run in a vault, the script creates `Inbox Cleanup Settings.md` (in the repo folder, three levels above this file) with guessed folder names and stops. Help the user check the Folders section (Inbox, Review, Archive, Admin, Skip), then start again.

The JSON has: `inbox` and `review` notes (path, word count, properties, start of the text), every MOC in `mocs` (name, path, Parent, start of the text), the `tags` in use, the vault's `routing_rules` (the Rules section of the settings note), `concept_folders`, and `last_run_review`. Read a note in full whenever the preview isn't enough to decide.

## 2. Learn from the user's Review answers

For each item in `last_run_review`:
- **The user answered it** (`parent_now` is set, or `now_at` is outside the Review folder): write a short, general rule in plain English that would have filed it correctly, and add it to `rules_learned`. Example: "Investing and stock-research notes → Parent: PFP Financial Analysis". Don't write a rule that only fits that one note. If the note is still in Review with a Parent now set, file it with the user's Parent and Note Type.
- **No answer yet** (`now_at` missing means the user deleted it, which also counts as an answer: "notes like this are deleted"): if nothing changed, give it `"action": "leave"`.

## 3. Decide each Inbox note

Apply the routing rules first. They're the user's own decisions and override your judgment. Then:

1. **Blank?** It's empty, only template headings, or a few words with no real idea → `"action": "trash"`. Don't assign properties.
2. **Note Type:**
   - **Working:** thinking, not documenting. Ideas, questions, drafts, logs of a problem. This is most notes. They don't need to be finished.
   - **Reference:** the thing itself is the point, meant to be found and trusted later (a how-to, guidelines, a resource list someone maintains, a data dictionary).
   - **MOC:** a note whose job is to collect other notes.
3. **Parent** (required, except for a new Concept MOC):
   - Prefer an existing MOC. Strong signals: the note links to it, an old property (`Action`, `Concept`, `Project`, `Domain`, `Reference`) names it, or the topic clearly matches its name or text.
   - **Nothing fits → create a blank MOC** in `new_mocs`. Name it after the topic in plain words (e.g. `Git`). Several notes on one theme share one new MOC. Give the new MOC a Parent if it sits under an existing MOC. Otherwise it's a new Concept with no Parent, placed as a single file in the most fitting `concept_folders` folder. Never create a new top-level folder.
4. **Tag:** at least one. Reuse a tag from `tags` when one fits. CamelCase, no `/` nesting.
5. **Destination** (Reference and MOC only. Working notes always go to the Archive, and the script handles that):
   - Follow the Parent chain up to its Concept (a MOC with no Parent). The note goes in **that Concept's folder**.
   - The Concept has a folder if its MOC sits in a subfolder of its own (e.g. `Viva Pinata/Viva Pinata-MOC.md`, `Obsidian-Designbase/Obsidian-Designbase.md`).
   - If the Concept MOC is a single file directly in a top-level folder (e.g. `04. Analysis/Designbase.md`), it needs a folder now. Add `{"path": <MOC path>, "destination": "<top-level folder>/<Concept name>"}` to `move_existing` and use that folder as the destination. Create a folder **only** for a Reference note or a sub-MOC, never for Working notes.
6. **Review only if you genuinely can't tell**, for example two equally good homes, or you can't tell whether it's worth keeping. Ask one short, specific question. Aim for very few.

**New MOCs** automatically end with `![[MOC Contents.base]]` (a live list of the notes in that MOC), so don't add it to `body` yourself.

**Content:** never lose content. When you create a MOC, you may fold short notes into it if they belong in the MOC itself: put their full text in the MOC's `body` and list them in `merged_from` (the script then deletes them). Otherwise don't edit note text. The script only changes properties, adds a `Related:` line for links from old properties, and moves files.

**Scope:** only notes in the Inbox and the Review folder. Never touch anything else. Daily notes and the Skip folders are never processed.

**Wording:** the user calls these notes MOCs. Say "MOC" in the report and in what you tell them, not "hub".

## 4. Write the plan and apply it

Write `/tmp/inbox_plan.json`:

```json
{
  "notes": [
    {"path": "99. Inbox/Note.md", "action": "file", "note_type": "Working", "parent": "Some MOC",
     "tags": ["Idea"], "reason": "short why", "rule": "rule applied, if any"},
    {"path": "99. Inbox/Ref.md", "action": "file", "note_type": "Reference", "parent": "Git",
     "tags": ["Tool"], "destination": "04. Analysis/Git"},
    {"path": "99. Inbox/Empty.md", "action": "trash", "reason": "empty"},
    {"path": "99. Inbox/Unclear.md", "action": "review", "question": "Is this part of X or Y?"},
    {"path": "99. Inbox/Review/Old.md", "action": "leave", "reason": "waiting for your answer"}
  ],
  "new_mocs": [{"name": "Git", "folder": "04. Analysis", "parent": null, "tags": ["Tool"],
                "body": "optional text", "merged_from": []}],
  "move_existing": [{"path": "04. Analysis/Designbase.md", "destination": "04. Analysis/Designbase"}],
  "rules_learned": ["Plain-English rule"],
  "notes_for_user": "Optional: anything worth flagging (e.g. a possible new Concept)."
}
```

`parent` is the MOC's note name, without brackets. Then run:

```
python3 clean_inbox.py apply /tmp/inbox_plan.json            # normal run
python3 clean_inbox.py apply /tmp/inbox_plan.json --preview  # preview
```

Use preview if the user asked for it, or if this is the first run ever (no `Reports/.undo/` folder yet).

## 5. Tell the user

Keep it short: the counts, the MOCs you created, any Review questions, and where the full report is (`Reports/Inbox Cleanup Report.md`). After a real run, mention that `/clean-inbox undo` reverses it. Check the report's Problems section and fix or explain anything listed there.
