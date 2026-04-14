# Project Template

Use this template whenever you need to create a new project during the Organize step.

---

## What a project looks like on disk

A project is a **directory** named after the project (lowercase, hyphenated) inside `projects/`.
It contains at least one markdown file.

```
projects/
  <project-name>/
    overview.md
    next-actions.md
```

---

## Step-by-step: how to create a new project

1. **Choose a name.** Lowercase, hyphenated, describes the outcome. Example: `bathroom-fan-repair`, `onboarding-redesign`.

2. **Create `projects/<project-name>/overview.md`** using the structure below.

3. **Create `projects/<project-name>/next-actions.md`** using the structure below.

4. **Append the first next action** (the one from the inbox item) to `next-actions.md`.

---

## overview.md structure

```markdown
# <Project Name>

## Description
<One or two sentences. What does "done" look like for this project?>

## Next Actions
(see next-actions.md)
```

**Example:**

```markdown
# Bathroom Fan Repair

## Description
The bathroom exhaust fan is broken and needs to be repaired or replaced. Done when the fan is working and the bathroom ventilates properly.

## Next Actions
(see next-actions.md)
```

---

## next-actions.md structure

```markdown
# Next Actions — <Project Name>

- [ ] <first next action>
```

**Example:**

```markdown
# Next Actions — Bathroom Fan Repair

- [ ] Inspect bathroom fan to determine if it needs repair or full replacement
```

---

## Rules

- Use **one directory per project**. Do not nest projects inside each other.
- The first next action must be **concrete and physical** — something you could do in a single sitting without further planning.
- If the inbox item is vague (e.g. "fix bathroom fan"), derive a reasonable first next action from it. Do not leave the list empty.
- Do not create a project for something that is a single action. Single actions go to `loose-actions.md`.
