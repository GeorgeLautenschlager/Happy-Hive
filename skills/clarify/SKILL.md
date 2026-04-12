---
name: clarify
description: Use when processing raw inbox items
---
You will be given the raw contents of `inbox.md` as input. Process each line item individually, top to bottom. For each item, ask yourself: *do I have enough information to determine what this means and whether it's actionable? If yes, leave the line unchanged If no, apply the following transform:
1. Bold the original item text
2. Append a single ❓ followed by your clarifying question
3. Append a timestamp in ISO format of when you made the clarification, wrapped in double tildes (~~) to indicate it's metadata and not part of the question.

Before: `- deal with the server thing`
After: `- **deal with the server thing** ❓ Which server, and what does "dealt with" mean — is it broken, or just needs attention? ~~2023-10-05T14:48:00Z~~`

Rules:
- One question per line. Pick the most load-bearing unknown.
- Do not alter lines that are already clear enough to process.
- Do not add questions to lines that are already annotated with ❓.
- update the file in place, emitting the full file contents as output — modified lines changed, untouched lines verbatim.
