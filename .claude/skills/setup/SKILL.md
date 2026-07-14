---
name: setup
description: First-run initialization of an earbrief instance — interview the owner, write config.md, personalize sources/curriculum, publish the player artifact, create the cloud routines. Run when config.md is missing.
---

# earbrief /setup

You are initializing a fresh earbrief instance (a repo created from the earbrief template). The outcome: a written `config.md`, personalized `sources.md`/`curriculum.md`, a published player artifact, two scheduled cloud routines, everything committed and pushed.

## 0. Guards

- If `config.md` exists, this instance is already initialized. Show its contents and ask what to change instead of re-running the flow (a re-run would mint a duplicate artifact and duplicate routines).
- Check `git remote -v`. If there is no `origin`, stop and tell the user to create their GitHub repo (private recommended — the repo will accumulate their personal listening log) and push first.
- Warn if the repo is public: `gh repo view --json visibility` (skip silently if `gh` is unavailable).

## 1. Interview

Ask (AskUserQuestion where it fits, free text otherwise):

1. **Timezone and schedule** — daily digest time (default 07:00 local) and weekly deep-dive day+time (default Saturday 08:00 local). Convert to UTC for scheduling.
2. **Secondary language** — Spanish or none. English is always canonical. Only Spanish is supported as secondary in this version (the player's voice mapping and AUTO mode are EN/ES); other languages require editing `player/template.html`.
3. **Listener profile** — who they are, what they already know, what depth they want. One short paragraph; this steers every episode's tone and level.
4. **Domain** — keep the default AI/engineering sources and curriculum, or describe their field. If they change domain, rewrite `sources.md` (research real, currently-active sources for that field; keep the tier structure and the `x`-prefix disable convention and the editorial rules section) and `curriculum.md` (build tracks from their stated gaps; keep the first-unchecked convention and Track E).
5. **Episode length** — daily words (default 2200 ≈ 15 min) and deep-dive words (default 3000 ≈ 20 min).

## 2. Write config.md

```markdown
# Config — instance settings

Written by /setup. Routines, CLAUDE.md, and chat ops read instance values from here.

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

Also update the profile line in `curriculum.md` with the same paragraph (condensed to one line).

## 3. Build and publish the player

1. `python3 player/build.py` — with zero episodes it prints `built player/player.html with 0 episodes`; that is correct for a fresh instance.
2. Publish with the Artifact tool: `file_path` player/player.html, **no `url` param** (first publish mints this instance's own address), favicon 📻, description 'Audio player for the daily AI briefing'.
3. Record the returned URL as `player_artifact_url` in config.md. Every later publish MUST pass this URL as `url` or the phone bookmark breaks.

## 4. Create the routines

Use the schedule skill (scheduled cloud agents). The user's repo must be connected to Claude's GitHub app — if scheduling fails on repo access, send them to claude.ai/code to connect the repo, then retry.

- **Daily digest** — cron from the interview's daily time (UTC). Prompt: `You are a scheduled routine of the earbrief pipeline. The repo is already cloned in your working directory. Read routines/daily.md in this repo and follow it exactly.` Suggested model: sonnet.
- **Weekly deep-dive** — cron from the weekly day+time (UTC). Same prompt with `routines/weekly.md`. Suggested model: opus.

Both routines need allowed tools beyond the defaults: `Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Artifact` (WebSearch/WebFetch for research, Artifact to republish the player).

Record both trigger IDs in config.md. If routine creation is unavailable in this environment, write `(create manually)` in config.md and print step-by-step instructions for claude.ai/code/routines instead — including both prompts verbatim.

## 5. Upstream remote

If `origin` is not the template repo itself, add the template as upstream for future updates (skip if it already exists):

```
git remote add upstream https://github.com/mblasi/earbrief.git
```

## 6. Commit and hand over

1. Commit everything: `initialize earbrief instance`, push.
2. Print, in this order: the player URL with "bookmark this on your phone"; when the first episode will appear (next daily run, or offer to trigger the daily routine once now); the chat-ops cheat sheet (mark listened, add/disable source, promote topic, rebuild player, update from upstream — see CLAUDE.md).
