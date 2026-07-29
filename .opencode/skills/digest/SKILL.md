---
name: digest
description: Generate daily news digest episodes for all enabled fronts. Run this on-demand when the backlog is empty or when you want fresh content. Follows routines/daily.md instructions.
---

# earbrief /digest

Generate daily news digest episodes for all enabled fronts. This is an on-demand operation — run it when you want new content, typically when the pending queue is empty.

## Pre-check

1. Check `log.md` for unchecked episodes. If there are 5+ pending across all fronts, ask if the user wants to proceed anyway (generating more will grow the backlog).
2. Get today's date: `date +%F` (call it TODAY).

## Execution

Read and follow `routines/daily.md` exactly. That file contains the complete instructions for:
- Discovering enabled fronts
- Reading sources and researching news
- Writing digest markdown files (English + optional secondary language)
- Updating log.md
- Rebuilding the player
- Committing and pushing

The routine is self-contained and thoroughly documented. Execute it step by step.

## Post-execution

After the routine completes successfully:
1. Report the episodes generated (which fronts, word counts)
2. Remind the user that the push triggered GitHub Pages deployment
3. Suggest they can reload the player page in a minute to see the new episodes
