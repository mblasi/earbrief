# earbrief

Your personal daily audio briefing, generated and narrated by AI. No servers, no app, no code to run — the whole system is this repo plus GitHub's infrastructure: GitHub Actions workflows write the episodes, a GitHub Pages site plays them in your browser with text-to-speech, and git is the only database.

- **Fronts**: N independent topic areas — IT, politics, sports, whatever you follow — each with its own sources, curriculum, and episodes.
- **Daily**: one spoken news digest per front, researched from that front's source list.
- **Weekly** (~20 min): a deep-dive lesson following a front's curriculum, rotating across fronts.
- **Player**: one URL bookmarked on your phone — switch fronts with a tap, play/pause, progress, listened tracking, optional Spanish rendition.

The template ships with one AI/ML engineering front as a worked example; your fronts, sources, and curricula are yours to define — any fields work.

## Requirements

- An AI coding assistant (OpenCode, Claude, Cursor, etc.) for interactive repo management.
- A GitHub account with GitHub Actions enabled.
- GitHub Pages enabled on your repository.

## Quickstart

1. Click **Use this template** → create your own repo (can be public or private).
2. Clone it, open a terminal in it, run your AI coding assistant (e.g., `opencode`).
3. Type `/setup`. The agent interviews you (schedule, language, listener profile, topic domain), personalizes the sources and curriculum, sets up GitHub Pages and GitHub Actions workflows.
4. Enable GitHub Pages in your repo settings (Settings → Pages → Source: GitHub Actions).
5. Bookmark the GitHub Pages URL. Your first episode arrives on the next daily workflow run.

## Commands & use cases

Everything is driven from an AI agent session in your repo — two slash commands plus plain-language chat ops.

### Slash commands

| Command | What it does |
|---|---|
| `/setup` | First-run initialization: interviews you, writes `config.md`, creates your fronts (each with its own sources and optional curriculum), sets up GitHub Pages deployment, creates the two GitHub Actions workflows. |
| `/update` | Pulls the latest template improvements (player features, prompt fixes) without touching your fronts, digests, log, or config. Pre-fronts instances are migrated to the multi-front layout automatically. |

### Chat ops

Say these in any AI agent session opened in the repo — no exact syntax required:

| You say | What happens |
|---|---|
| "mark <episode> listened" | Checks the episode's line in `log.md`, commits, pushes. |
| paste `mark listened: <id>, <id>` | The string the player's **sync** pill copies; checks the matching `log.md` lines. Devices see the update after the next rebuild (the daily workflow suffices). |
| "rate <episode> 4" / paste `rate: <id>=<n>` | Appends a ` — ★n` rating to the episode's `log.md` line (the sync pill includes pending ratings too). Workflows read ratings as an interest signal. |
| "add source X" / "disable source Y" | Edits the relevant front's `sources.md` (disable = prefix the line with `x`); takes effect on the next workflow run. |
| "add front X" | Opens a new front: creates `fronts/<slug>/` with researched sources (and a curriculum if you want deep-dives there); its tab appears in the player. "disable front X" mothballs one. |
| "promote <topic>" | Adds the topic to that front's `curriculum.md` Track E (max 3 items), queued for an upcoming deep-dive. |
| "rebuild and republish the player" | Regenerates `player/player.html` from the digests and log, commits and pushes to trigger GitHub Pages deployment. |
| "update from upstream" | Same as `/update`. |

### Use cases

The full contract lives in `USECASES.md`; in short:

- **Stay current** — the daily workflow writes one news digest per front from that front's sources; you hit play.
- **Work N fronts** — every mechanism (sources, curriculum, ratings, digests) runs per front; the player switches between them with a tap and an All view interleaves everything.
- **Close the knowledge gap** — the weekly workflow writes a deep-dive from the next unchecked curriculum item, rotating across fronts that have a curriculum.
- **Track listened vs pending** — the player tracks on-device; `log.md` is the durable record, synced both ways through git (rebuild bakes it in, the sync pill pastes it back).
- **Rate to steer** — star an episode after listening (1–5); workflows weight future stories and deep-dives toward what you rated high, away from what you rated low.
- **Manage sources** — edit `sources.md` directly or via chat.
- **Spark** — a button on any episode opens a fresh AI chat session prefilled with that episode's context, for when a briefing wakes up an idea.
- **Choose the listening language** — optional secondary-language rendition per episode, with AUTO/EN/ES modes and per-episode pinning.
- **Promote news to curriculum** — digests flag deep-dive candidates; one chat op turns a headline into a future lesson.

## How it works

- A **front** is a directory under `fronts/` — metadata (`front.md`), its own `sources.md`, optional `curriculum.md`, and `digests/`. Fronts are independent editorial universes; nothing leaks between them.
- The **daily workflow** walks every enabled front: reads its `sources.md`, researches the last 24h, writes a spoken-prose digest into its `digests/`, commits, and triggers GitHub Pages deployment.
- The **weekly workflow** picks one front per run (round-robin across fronts with a curriculum) and writes a deep-dive episode from its next unchecked curriculum item.
- The **player page** (GitHub Pages) does browser TTS with play/pause and listened/pending tracking in localStorage. It never writes anywhere (static hosting) — its **sync** pill copies a `mark listened: ...` string you paste into any AI chat.
- `log.md` is the durable listened/pending record; all state changes travel through git commits.
- Day-to-day management is conversational: "mark yesterday listened", "add source X", "promote that topic to my curriculum" — see `AGENTS.md` for the chat ops any AI agent session in this repo understands.

Architecture contract: `USECASES.md`. Operating manual for AI agent sessions: `AGENTS.md`.

## Layout

```
config.md            instance settings, written by /setup (absent until then)
fronts/<id>/         one directory per front (topic area):
  front.md             metadata: label, hue, order, enabled, word overrides
  sources.md           tiered source list (tier 1 = daily, tier 2 = weekly scan)
  curriculum.md        learning syllabus (optional); next unchecked box = next deep-dive
  digests/             one markdown file per episode (+ optional .es.md rendition)
log.md               listened / pending record, all fronts (date — front — type — title)
routines/            the prompts the GitHub Actions workflows follow
player/              build.py + template → player.html (deployed to GitHub Pages)
.opencode/skills/    /setup (first run) and /update (pull template improvements)
.github/workflows/   GitHub Actions workflows for daily and weekly content generation
```

## Language

English is always canonical. Optionally, episodes also get a Spanish rendition (spoken register, technical terms kept in English) and the player offers AUTO/EN/ES listening modes with position mapping between languages. Other secondary languages need small edits to `player/template.html` (voice mapping is EN/ES in this version).

## Updating your instance

Template improvements (player features, prompt fixes) flow one way, on your command: run `/update` in your repo and your AI agent fetches the template's latest files without touching your digests, log, or config.

## Make it yours

If this sounds like your kind of morning: hit **Use this template** to create your own repo, run `/setup` to get your first briefing scheduled, and if earbrief earns a spot on your phone's home screen, a ⭐ on this repo helps others find it.

## License

MIT
