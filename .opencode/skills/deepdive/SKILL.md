---
name: deepdive
description: Generate a weekly deep-dive episode from one front's curriculum. Run this on-demand when you want a learning episode, rotating round-robin across fronts that have a curriculum.
---

# earbrief /deepdive

Generate a deep-dive episode from the next unchecked curriculum item, rotating round-robin across fronts that have a curriculum. This is an on-demand operation — run it when you want to learn something new.

## Pre-check

1. Get today's date: `date +%F` (call it TODAY).
2. Scan all fronts to see which ones have a `curriculum.md` with unchecked items. If none, tell the user there's nothing to deep-dive right now and suggest they can add curriculum items or say "promote <topic>".

## Execution

Read and follow `routines/weekly.md` exactly. That file contains the complete instructions for:
- Selecting which front to process (round-robin)
- Reading the curriculum and picking the next item
- Researching the topic
- Writing the deep-dive markdown file (English + optional secondary language)
- Marking the curriculum item as done
- Updating log.md
- Rebuilding the player
- Committing and pushing

The routine is self-contained and thoroughly documented. Execute it step by step.

## Post-execution

After the routine completes successfully:
1. Report which front and curriculum item was covered
2. Note the word count and duration (~150 wpm spoken)
3. Remind the user that the push triggered GitHub Pages deployment
4. Suggest they can reload the player page in a minute to see the new episode
