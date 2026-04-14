# Reference Template

Use this template whenever you need to file a reference item during the Organize step.

---

## What a reference item looks like on disk

A reference item is a **single markdown file** inside `reference/` (no subdirectories).

```
reference/
  <item-name>.md
```

---

## Step-by-step: how to create a reference item

1. **Choose a filename.** Lowercase, hyphenated, describes the subject. Example: `deep-work-cal-newport.md`, `wifi-router-admin-password.md`.

2. **Create `reference/<item-name>.md`** using the structure below.

---

## File structure

```markdown
# <Title>

Filed: <ISO 8601 timestamp>

## Notes
<Everything worth keeping about this item. Write as much or as little as the inbox item gives you.
If the item includes a URL or source, include it here.>
```

**Example (article):**

```markdown
# Deep Work — Cal Newport

Filed: 2024-03-15T09:30:00Z

## Notes
Book arguing that the ability to focus without distraction is the most valuable skill in the modern economy.
Useful framework: shallow work vs deep work. Newport recommends scheduling deep work blocks and eliminating
social media during work hours.
```

**Example (credential/fact):**

```markdown
# WiFi Router Admin Password

Filed: 2024-03-15T09:31:00Z

## Notes
Router admin panel: 192.168.1.1
Username: admin
Password: (check the sticker on the bottom of the router)
```

---

## Rules

- One file per reference item. Do not combine multiple unrelated items into one file.
- Derive the title and notes from whatever the inbox item says. Do not leave the Notes section empty.
- If the inbox item is just a title (e.g. "article about deep work"), use that as the title and write what you can infer in the Notes section.
- Do not create a reference item for something that has an action attached to it. Those belong in projects or loose-actions.md.
