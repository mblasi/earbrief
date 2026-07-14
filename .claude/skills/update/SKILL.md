---
name: update
description: Pull earbrief template improvements from the upstream remote into this instance without touching personal state (digests, log, config, sources, curriculum).
---

# earbrief /update

Bring template files up to date from the upstream earbrief repo. Personal state is never touched.

## Files owned by the template (updatable)

- `player/build.py`, `player/template.html`
- `routines/daily.md`, `routines/weekly.md`
- `.claude/` (skills, including this one)
- `USECASES.md`, `README.md`, `CLAUDE.md`, `.gitignore`

## Files owned by the instance (NEVER updated)

- `config.md`, `sources.md`, `curriculum.md`, `log.md`, `digests/`

## Procedure

1. `git remote get-url upstream` — if missing, add it: `git remote add upstream https://github.com/mblasi/earbrief.git`.
2. `git fetch upstream`.
3. `git diff HEAD upstream/master -- <template-owned paths>` — show the user a short summary of what changed. If nothing changed, say so and stop.
4. If the instance has local edits to template-owned files (check `git log --oneline origin/master -- <paths>` vs upstream), point them out — a plain checkout would overwrite them; merge those by hand.
5. `git checkout upstream/master -- <template-owned paths that changed>`.
6. If `player/template.html` or `player/build.py` changed: rebuild (`python3 player/build.py`), syntax-check the embedded script (see CLAUDE.md rebuild procedure), and republish the artifact with the `url` from config.md.
7. Commit `update from upstream template`, push.
