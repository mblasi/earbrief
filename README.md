# earbrief

Your personal daily audio briefing, generated and narrated by Claude. No servers, no app, no code to run — the whole system is this repo plus Claude's own machinery: scheduled cloud agents write the episodes, a Claude artifact plays them in your browser with text-to-speech, and git is the only database.

- **Fronts**: N independent topic areas — IT, politics, sports, whatever you follow — each with its own sources, curriculum, and episodes.
- **Daily**: one spoken news digest per front, researched from that front's source list.
- **Weekly** (~20 min): a deep-dive lesson following a front's curriculum, rotating across fronts.
- **Player**: one URL bookmarked on your phone — switch fronts with a tap, play/pause, progress, listened tracking, optional Spanish rendition.

The template ships with one AI/ML engineering front as a worked example; your fronts, sources, and curricula are yours to define — any fields work.

**[▶ Try the demo player](https://claude.ai/code/artifact/4c1db192-1d52-41a9-8cfb-6d31f9204e7d)** — three sample fronts, front switching, TTS playback, EN/ES, ratings. Sample state lives in `demo/`.

## Requirements

- A Claude plan with **Claude Code**, **scheduled cloud agents (routines)**, and **artifacts**.
- A GitHub account; the repo you create must be connected to Claude's GitHub app so routines can commit to it.

## Quickstart

1. Click **Use this template** → create your own repo (**private recommended** — it will accumulate your personal listening log).
2. Clone it, open a terminal in it, run `claude`.
3. Type `/setup`. Claude interviews you (schedule, language, listener profile, topic domain), personalizes the sources and curriculum, publishes your player, and creates the two routines.
4. Bookmark the player URL it prints. Your first episode arrives on the next daily run.

## Commands & use cases

Everything is driven from a Claude Code session in your repo — two slash commands plus plain-language chat ops.

### Slash commands

| Command | What it does |
|---|---|
| `/setup` | First-run initialization: interviews you, writes `config.md`, creates your fronts (each with its own sources and optional curriculum), publishes the player artifact, creates the two routines. |
| `/update` | Pulls the latest template improvements (player features, prompt fixes) without touching your fronts, digests, log, or config. Pre-fronts instances are migrated to the multi-front layout automatically. |

### Chat ops

Say these in any Claude session opened in the repo — no exact syntax required:

| You say | What happens |
|---|---|
| "mark <episode> listened" | Checks the episode's line in `log.md`, commits, pushes. |
| paste `mark listened: <id>, <id>` | The string the player's **sync** pill copies; checks the matching `log.md` lines. Devices see the update after the next rebuild (the daily routine's suffices). |
| "rate <episode> 4" / paste `rate: <id>=<n>` | Appends a ` — ★n` rating to the episode's `log.md` line (the sync pill includes pending ratings too). Routines read ratings as an interest signal. |
| "add source X" / "disable source Y" | Edits the relevant front's `sources.md` (disable = prefix the line with `x`); takes effect on the next routine run. |
| "add front X" | Opens a new front: creates `fronts/<slug>/` with researched sources (and a curriculum if you want deep-dives there); its tab appears in the player. "disable front X" mothballs one. |
| "promote <topic>" | Adds the topic to that front's `curriculum.md` Track E (max 3 items), queued for an upcoming deep-dive. |
| "rebuild and republish the player" | Regenerates `player/player.html` from the digests and log, republishes the artifact at the same URL. |
| "update from upstream" | Same as `/update`. |

### Use cases

The full contract lives in `USECASES.md`; in short:

- **Stay current** — the daily routine writes one news digest per front from that front's sources; you hit play.
- **Work N fronts** — every mechanism (sources, curriculum, ratings, digests) runs per front; the player switches between them with a tap and an All view interleaves everything.
- **Close the knowledge gap** — the weekly routine writes a deep-dive from the next unchecked curriculum item, rotating across fronts that have a curriculum.
- **Track listened vs pending** — the player tracks on-device; `log.md` is the durable record, synced both ways through git (rebuild bakes it in, the sync pill pastes it back).
- **Rate to steer** — star an episode after listening (1–5); routines weight future stories and deep-dives toward what you rated high, away from what you rated low.
- **Manage sources** — edit `sources.md` directly or via chat.
- **Spark** — a button on any episode opens a fresh Claude session prefilled with that episode's context, for when a briefing wakes up an idea.
- **Choose the listening language** — optional secondary-language rendition per episode, with AUTO/EN/ES modes and per-episode pinning.
- **Promote news to curriculum** — digests flag deep-dive candidates; one chat op turns a headline into a future lesson.

## How it works

- A **front** is a directory under `fronts/` — metadata (`front.md`), its own `sources.md`, optional `curriculum.md`, and `digests/`. Fronts are independent editorial universes; nothing leaks between them.
- The **daily routine** walks every enabled front: reads its `sources.md`, researches the last 24h, writes a spoken-prose digest into its `digests/`, commits, and refreshes the player artifact.
- The **weekly routine** picks one front per run (round-robin across fronts with a curriculum) and writes a deep-dive episode from its next unchecked curriculum item.
- The **player artifact** does browser TTS with play/pause and listened/pending tracking in localStorage. It never writes anywhere (artifact pages can't make network calls) — its **sync** pill copies a `mark listened: ...` string you paste into any Claude chat.
- `log.md` is the durable listened/pending record; all state changes travel through git commits.
- Day-to-day management is conversational: "mark yesterday listened", "add source X", "promote that topic to my curriculum" — see `CLAUDE.md` for the chat ops any Claude session in this repo understands.

Architecture contract: `USECASES.md`. Operating manual for Claude sessions: `CLAUDE.md`.

## Layout

```
config.md            instance settings, written by /setup (absent until then)
fronts/<id>/         one directory per front (topic area):
  front.md             metadata: label, hue, order, enabled, word overrides
  sources.md           tiered source list (tier 1 = daily, tier 2 = weekly scan)
  curriculum.md        learning syllabus (optional); next unchecked box = next deep-dive
  digests/             one markdown file per episode (+ optional .es.md rendition)
log.md               listened / pending record, all fronts (date — front — type — title)
routines/            the prompts the scheduled agents follow
player/              build.py + template → player.html (published as the artifact)
.claude/skills/      /setup (first run) and /update (pull template improvements)
```

## Language

English is always canonical. Optionally, episodes also get a Spanish rendition (spoken register, technical terms kept in English) and the player offers AUTO/EN/ES listening modes with position mapping between languages. Other secondary languages need small edits to `player/template.html` (voice mapping is EN/ES in this version).

## Updating your instance

Template improvements (player features, prompt fixes) flow one way, on your command: run `/update` in your repo and Claude fetches the template's latest files without touching your digests, log, or config.

## Make it yours

If this sounds like your kind of morning: hit **Use this template** to create your own repo, run `/setup` to get your first briefing scheduled, and if earbrief earns a spot on your phone's home screen, a ⭐ on this repo helps others find it.

## License

MIT
