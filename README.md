# earbrief

Your personal daily audio briefing, generated and narrated by Claude. No servers, no app, no code to run — the whole system is this repo plus Claude's own machinery: scheduled cloud agents write the episodes, a Claude artifact plays them in your browser with text-to-speech, and git is the only database.

- **Daily** (~15 min): a spoken news digest researched from your source list.
- **Weekly** (~20 min): a deep-dive lesson following your personal curriculum.
- **Player**: one URL bookmarked on your phone — play/pause, progress, listened tracking, optional Spanish rendition.

The default configuration tracks AI/ML engineering, but the sources and curriculum are yours to define — any field works.

## Requirements

- A Claude plan with **Claude Code**, **scheduled cloud agents (routines)**, and **artifacts**.
- A GitHub account; the repo you create must be connected to Claude's GitHub app so routines can commit to it.

## Quickstart

1. Click **Use this template** → create your own repo (**private recommended** — it will accumulate your personal listening log).
2. Clone it, open a terminal in it, run `claude`.
3. Type `/setup`. Claude interviews you (schedule, language, listener profile, topic domain), personalizes the sources and curriculum, publishes your player, and creates the two routines.
4. Bookmark the player URL it prints. Your first episode arrives on the next daily run.

## How it works

- The **daily routine** reads `sources.md`, researches the last 24h, writes a spoken-prose digest into `digests/`, commits, and refreshes the player artifact.
- The **weekly routine** writes a deep-dive episode from the next unchecked item in `curriculum.md`.
- The **player artifact** does browser TTS with play/pause and listened/pending tracking in localStorage. It never writes anywhere (artifact pages can't make network calls) — its **sync** pill copies a `mark listened: ...` string you paste into any Claude chat.
- `log.md` is the durable listened/pending record; all state changes travel through git commits.
- Day-to-day management is conversational: "mark yesterday listened", "add source X", "promote that topic to my curriculum" — see `CLAUDE.md` for the chat ops any Claude session in this repo understands.

Architecture contract: `USECASES.md`. Operating manual for Claude sessions: `CLAUDE.md`.

## Layout

```
config.md        instance settings, written by /setup (absent until then)
sources.md       tiered source list (tier 1 = daily, tier 2 = weekly scan)
curriculum.md    learning syllabus; next unchecked box = next deep-dive
digests/         one markdown file per episode (+ optional .es.md rendition)
log.md           listened / pending record
routines/        the prompts the scheduled agents follow
player/          build.py + template → player.html (published as the artifact)
.claude/skills/  /setup (first run) and /update (pull template improvements)
```

## Language

English is always canonical. Optionally, episodes also get a Spanish rendition (spoken register, technical terms kept in English) and the player offers AUTO/EN/ES listening modes with position mapping between languages. Other secondary languages need small edits to `player/template.html` (voice mapping is EN/ES in this version).

## Updating your instance

Template improvements (player features, prompt fixes) flow one way, on your command: run `/update` in your repo and Claude fetches the template's latest files without touching your digests, log, or config.

## Make it yours

If this sounds like your kind of morning: hit **Use this template** to create your own repo, run `/setup` to get your first briefing scheduled, and if earbrief earns a spot on your phone's home screen, a ⭐ on this repo helps others find it.

## License

MIT
