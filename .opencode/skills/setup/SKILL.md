---
name: setup
description: First-run initialization of an earbrief instance — interview the owner, write config.md, define the fronts (topic areas) with their sources/curricula, set up GitHub Pages deployment, configure GitHub Actions workflows. Run when config.md is missing.
---

# earbrief /setup

You are initializing a fresh earbrief instance (a repo created from the earbrief template). The outcome: a written `config.md`, one or more personalized fronts under `fronts/`, GitHub Pages configured, two scheduled GitHub Actions workflows, everything committed and pushed.

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

Written by /setup. GitHub Actions workflows, AGENTS.md, and chat ops read instance values from here.
Per-front settings (label, hue, word overrides, enabled) live in fronts/<id>/front.md.

- player_pages_url: (pending first deployment - will be https://<username>.github.io/<repo>/)
- daily_workflow_id: daily-digest.yml
- weekly_workflow_id: weekly-deepdive.yml
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

## 4. Build the player and prepare GitHub Pages

1. `python3 player/build.py` — with zero episodes it prints the front list with 0 episodes each; that is correct for a fresh instance.
2. Determine the GitHub Pages URL (format: `https://<username>.github.io/<repo>/` or custom domain if configured).
3. Record it as `player_pages_url` in config.md.
4. The player will be deployed automatically by GitHub Actions when `player/player.html` is pushed to the main branch.

## 5. Configure GitHub Actions workflows

The workflows are already created in `.github/workflows/`:
- `daily-digest.yml` — scheduled for the daily time from the interview
- `weekly-deepdive.yml` — scheduled for the weekly day+time from the interview

Update their cron schedules to match the UTC times from the interview:

1. Edit `.github/workflows/daily-digest.yml` — update the cron line to the daily UTC time.
2. Edit `.github/workflows/weekly-deepdive.yml` — update the cron line to the weekly UTC time (day of week: 0=Sunday, 6=Saturday).

**IMPORTANT NOTE:** These workflows are currently placeholders that require AI agent API integration. To make them functional, you need to:
- Choose an AI provider (OpenAI, Anthropic, etc.)
- Add the API key as a GitHub secret (Settings → Secrets and variables → Actions)
- Implement the workflow steps to call the AI API with the instructions from `routines/daily.md` and `routines/weekly.md`
- Have the AI agent execute the content generation, commit, and push

For now, the workflows are configured but will need manual triggering and AI API integration to work automatically.

## 6. Upstream remote

If `origin` is not the template repo itself, add the template as upstream for future updates (skip if it already exists):

```
git remote add upstream https://github.com/mblasi/earbrief.git
```

## 7. Commit and hand over

1. Commit everything: `initialize earbrief instance`, push.
2. Print setup completion instructions:
   - Enable GitHub Pages: Settings → Pages → Source: GitHub Actions
   - The player URL (once Pages is enabled): the `player_pages_url` from config.md
   - Note that workflows require AI API integration to run automatically (see step 5)
   - Manual workflow triggers available at: Actions tab → workflow name → Run workflow
   - Chat-ops cheat sheet: mark listened, add/disable source, add front, promote topic, rebuild player, update from upstream (see AGENTS.md)
