---
name: update
description: Pull earbrief template improvements from the upstream remote into this instance without touching personal state (fronts, digests, log, config). Auto-migrates pre-fronts instances to the multi-front layout.
---

# earbrief /update

Bring template files up to date from the upstream earbrief repo. Personal state is never touched (but see the one-time fronts migration below, which MOVES personal files without editing their content).

## Files owned by the template (updatable)

- `player/build.py`, `player/template.html`
- `routines/daily.md`, `routines/weekly.md`
- `.claude/` (skills, including this one)
- `USECASES.md`, `README.md`, `CLAUDE.md`, `.gitignore`

## Files owned by the instance (NEVER updated)

- `config.md`, `log.md`, `fronts/` (each front's `front.md`, `sources.md`, `curriculum.md`, `digests/`)
- legacy pre-migration locations: root `sources.md`, `curriculum.md`, `digests/`

## Procedure

1. `git remote get-url upstream` — if missing, add it: `git remote add upstream https://github.com/mblasi/earbrief.git`.
2. `git fetch upstream`.
3. `git diff HEAD upstream/master -- <template-owned paths>` — show the user a short summary of what changed. If nothing changed and the instance already has a `fronts/` directory, say so and stop.
4. If the instance has local edits to template-owned files (check `git log --oneline origin/master -- <paths>` vs upstream), point them out — a plain checkout would overwrite them; merge those by hand.
5. `git checkout upstream/master -- <template-owned paths that changed>`. The template's example front (`fronts/ai/`) is seed content, not an update target — never check it out into an instance.
6. **Fronts migration (one-time, automatic).** If there is no `fronts/` directory but a root `sources.md` exists (pre-fronts layout), migrate the instance:
   1. Episode ids change in this migration, so unsynced on-device player state won't carry over. Tell the user: if any listened episodes or ratings are not yet in `log.md`, tap the player's sync pill and paste it first, then re-run `/update`. Offer to continue anyway.
   2. Choose the front id: a short kebab slug for the instance's domain, inferred from `config.md`'s listener profile and `sources.md`'s content (e.g. `ai`, `politics`, `sports`). Confirm id and label with the user when the session is interactive; otherwise pick sensibly.
   3. `mkdir -p fronts/<id>`, then `git mv sources.md fronts/<id>/sources.md`, `git mv curriculum.md fronts/<id>/curriculum.md` (if present), `git mv digests fronts/<id>/digests`.
   4. Write `fronts/<id>/front.md` following the shape of the template's `fronts/ai/front.md`: `- id:`, `- label:`, `- hue:` (0–360, pick one that fits the domain), `- order: 1`, `- enabled: true`, plus an `## Editorial identity` paragraph distilled from the moved sources.md's editorial rules.
   5. Rewrite the episode lines in `log.md` from `- [ ] date — type — title` to `- [ ] date — <id> — type — title` (preserve `[x]` checkboxes and ` — ★n` suffixes; touch nothing else in the file).
   6. Tell the user they can now open more fronts: "add front <name>" in any Claude session in this repo.
7. If `player/template.html` or `player/build.py` changed, or a migration ran: rebuild (`python3 player/build.py` — the episode count must survive a migration unchanged, all episodes attributed to the new front), syntax-check the embedded script (see CLAUDE.md rebuild procedure), and republish the artifact with the `url` from config.md.
8. Commit `update from upstream template` (append ` + fronts migration` if step 6 ran), push.
