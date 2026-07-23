---
name: setup
description: First-run initialization of an earbrief instance — interview the owner, write config.md, define the fronts (topic areas) with their sources/curricula, publish the player artifact, create the cloud routines. Run when config.md is missing.
---

# earbrief /setup

You are initializing a fresh earbrief instance (a repo created from the earbrief template). The outcome: a written `config.md`, one or more personalized fronts under `fronts/`, a published player artifact, two scheduled cloud routines, everything committed and pushed.

## 0. Guards

- If `config.md` exists, this instance is already initialized. Show its contents and ask what to change instead of re-running the flow (a re-run would mint a duplicate artifact and duplicate routines).
- Check `git remote -v`. If there is no `origin`, stop and tell the user to create their GitHub repo (private recommended — the repo will accumulate their personal listening log) and push first.
- Warn if the repo is public: `gh repo view --json visibility` (skip silently if `gh` is unavailable).

## 1. Interview

Ask (AskUserQuestion where it fits, free text otherwise):

1. **Timezone and schedule** — daily digest time (default 07:00 local) and weekly deep-dive day+time (default Saturday 08:00 local). Convert to UTC for scheduling.
2. **Secondary language** — Spanish or none. English is always canonical. Only Spanish is supported as secondary in this version (the player's voice mapping and AUTO mode are EN/ES); other languages require editing `player/template.html`.
3. **Listener profile** — who they are, what they already know, what depth they want. One short paragraph; this steers every episode's tone and level.
4. **Fronts** — the topic areas they want briefings on (e.g. AI engineering, national politics, football). One front is a fine start; each additional front adds a daily digest (time and tokens), so suggest starting with 1–3. For each front collect: a short label, what to cover and from what angle, and whether they want a learning curriculum for it (deep-dives) or news only.
5. **Episode length** — daily words per front (default 2200 ≈ 15 min) and deep-dive words (default 3000 ≈ 20 min). With several fronts, suggest smaller daily targets (e.g. 1200–1500 each) so the morning queue stays listenable.

## 2. Build the fronts

The template ships `fronts/ai/` as a worked example. For each front from the interview:

- Create `fronts/<id>/` (id = short kebab slug) with:
  - `front.md` — follow the shape of `fronts/ai/front.md`: `- id:`, `- label:`, `- hue:` (0–360; give every front a visually distinct hue — the player tints itself with it), `- order:` (interview order), `- enabled: true`, optional `- daily_words:`/`- deepdive_words:` overrides, and an `## Editorial identity` paragraph capturing the angle the user described.
  - `sources.md` — research real, currently-active sources for that front (keep the tier structure, the `x`-prefix disable convention, and an editorial-rules section adapted to the front).
  - `curriculum.md` — only if they wanted deep-dives on this front: build tracks from their stated gaps; keep the first-unchecked convention and Track E. News-only fronts get no curriculum.md.
  - `digests/.gitkeep`.
- If the user keeps the default AI front, personalize `fronts/ai/` in place; otherwise delete it.

## 3. Write config.md

```markdown
# Config — instance settings

Written by /setup. Routines, CLAUDE.md, and chat ops read instance values from here.
Per-front settings (label, hue, word overrides, enabled) live in fronts/<id>/front.md.

- player_artifact_url: (pending first publish)
- daily_routine_id: (pending)
- weekly_routine_id: (pending)
- timezone: <IANA tz>
- daily_schedule: <HH:MM local / HH:MM UTC>
- weekly_schedule: <Day HH:MM local / HH:MM UTC>
- secondary_language: es | none
- daily_words: 2200
- deepdive_words: 3000

## Listener profile

<the paragraph from the interview>
```

Also update the profile line in each front's `curriculum.md` with the same paragraph (condensed to one line, angled to that front).

## 4. Build and publish the player

1. `python3 player/build.py` — with zero episodes it prints the front list with 0 episodes each; that is correct for a fresh instance.
2. Publish with the Artifact tool: `file_path` player/player.html, **no `url` param** (first publish mints this instance's own address), favicon 📻, description 'Audio player for the daily briefing'.
3. Record the returned URL as `player_artifact_url` in config.md. Every later publish MUST pass this URL as `url` or the phone bookmark breaks.

## 5. Create the routines

Use the schedule skill (scheduled cloud agents). The user's repo must be connected to Claude's GitHub app — if scheduling fails on repo access, send them to claude.ai/code to connect the repo, then retry.

- **Daily digest** — cron from the interview's daily time (UTC). Prompt: `You are a scheduled routine of the earbrief pipeline. The repo is already cloned in your working directory. Read routines/daily.md in this repo and follow it exactly.` Suggested model: sonnet. It processes every enabled front in one run.
- **Weekly deep-dive** — cron from the weekly day+time (UTC). Same prompt with `routines/weekly.md`. Suggested model: opus. It picks one front per run, round-robin across fronts that have a curriculum.

Both routines need allowed tools beyond the defaults: `Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Artifact` (WebSearch/WebFetch for research, Artifact to republish the player).

Record both trigger IDs in config.md. If routine creation is unavailable in this environment, write `(create manually)` in config.md and print step-by-step instructions for claude.ai/code/routines instead — including both prompts verbatim.

## 6. Upstream remote

If `origin` is not the template repo itself, add the template as upstream for future updates (skip if it already exists):

```
git remote add upstream https://github.com/mblasi/earbrief.git
```

## 7. Commit and hand over

1. Commit everything: `initialize earbrief instance`, push.
2. Print, in this order: the player URL with "bookmark this on your phone"; when the first episodes will appear (next daily run, or offer to trigger the daily routine once now); the chat-ops cheat sheet (mark listened, add/disable source, add front, promote topic, rebuild player, update from upstream — see CLAUDE.md).
