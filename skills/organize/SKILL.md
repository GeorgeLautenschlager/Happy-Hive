---
name: organize
description: Use when processing inbox items that have been clarified
---

You will be given the full contents of inbox.md. Process each line item individually, top to bottom. Skip any line already annotated with ~~strikethrough~~. Skip any bolded line annotated with ❓ — it still needs clarification.
For each item, determine the correct destination:
- **Loose next action** — single concrete action, belongs to no project → append to `loose-actions.md`
- **Project next action** — action that belongs to an existing project → append to `<project>/next-actions.md`
- **Someday/Maybe** — not actionable now, worth revisiting → append to `someday-maybe.md`
- **New project** — outcome requiring multiple actions → follow the project template to create the project, append the first next action to `<project>/next-actions.md`
- **Reference** — no action, just information worth keeping → follow the reference template to create the item

Then apply the following transform to the inbox line:
1. Strikethrough the original item text
2. Append → followed by the destination
3. Append a timestamp in ISO format of when you made the clarification, wrapped in double tildes (~~) to indicate it's metadata and not part of the question.

Before: `- fix the login bug`
After: `- ~~fix the login bug~~ → projects/auth-overhaul/next-actions.md`

Rules:
- Write to the destination file before annotating the inbox line
- One destination per item — if it feels like two things, it probably is; process each separately if they're on separate lines, flag it if they're not
- Do not process lines annotated with ❓
- Do not re-process lines already struck through
- Update the file in place, emitting the full file contents as output — modified lines changed, untouched lines verbatim.
