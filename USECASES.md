# Use cases & harnesses

Each use case names the harness that serves it. A harness is whichever Claude-native mechanism does the work: a scheduled routine, the player artifact, a chat command, or a repo file. Nothing here is custom infrastructure.

## Harness catalog

| Harness | What it is | State it touches |
|---|---|---|
| H1 daily-digest routine | Scheduled cloud agent, daily (`routines/daily.md`); one pass per enabled front | reads each front's `sources.md`, writes its `digests/`, refreshes player |
| H2 deep-dive routine | Scheduled cloud agent, weekly (`routines/weekly.md`); one front per run, round-robin | reads that front's `curriculum.md`, writes its `digests/`, checks item off, refreshes player |
| H3 player artifact | One web page on the phone: front switcher, TTS playback, progress, listened state and star ratings (localStorage seeded from `log.md` at build; sync button emits a paste-string) | on-device only |
| H4 chat ops | Ad-hoc Claude Code session: "mark X listened", "rate X 4", pasted `mark listened: <ids>` / `rate: <id>=<n>` sync strings, "add source Y", "add front Z", "promote W to curriculum" | `log.md`, `fronts/` |
| H5 spark hook | Button in the player that opens a **new, external Claude session** prefilled with the episode context | none — fire and forget |

## Use cases

### UC1 — Stay current (daily)
Open the player, hit play on today's episodes — one per front. **Harness:** H1 produces them, H3 plays them.

### UC2 — Close the knowledge gap (weekly)
The weekly deep-dive follows the chosen front's `curriculum.md` order; fronts with a curriculum take turns (round-robin). News-only fronts (no curriculum.md) never get deep-dives. **Harness:** H2, H3.

### UC3 — Track listened vs pending
Player marks episodes automatically on-device (H3); `log.md` is the durable cross-device record. Sync is two-way but always passes through the repo:
- **Repo → devices:** `build.py` bakes the checked ids from `log.md` into the player; each device applies them as listened on load (once per id, so a local un-check for replay sticks). H4 rebuilds and republishes right after updating `log.md`, so the state reaches devices on the next player reload (the daily routine's rebuild also picks it up).
- **Devices → repo:** episodes finished locally but unchecked in `log.md` surface a **sync N to log ⇪** pill in the player header; tapping copies `mark listened: <ids>` to the clipboard — paste it into any Claude chat and H4 updates `log.md`.
The player still never writes anywhere (artifact CSP blocks all outbound requests — that's why the paste hop exists). Weekly routine flags a growing pending pile and shortens episodes if needed.

### UC4 — Manage sources
Edit a front's `sources.md` directly, or ask Claude (H4). Takes effect next routine run. Disable without deleting by prefixing a line with `x`.

### UC5 — Spark: an episode wakes up an idea
While listening, tap **Spark** on the episode. It opens a new Claude session (app or web) prefilled with the episode title, its key context, and your cue to deep-dive. That session is launched and managed **outside this solution** — the only responsibility here is firing it. Nothing is written to the repo; if the external session produces something worth keeping, bring it back via H4 (e.g. "promote this to curriculum Track E").

### UC6 — Choose the listening language
Sources and canonical episodes are always English; if `config.md` sets a secondary language, routines emit a pre-translated rendition (`.<lang>.md`, technical terms kept in English) at build time — the player cannot translate live (artifact CSP blocks external calls). Language resolution, highest precedence first: (1) per-episode pin — tap the language chip on a card to switch that episode to the other language, tap again to unpin (pinned = accent color + ✱); (2) the global AUTO/EN/ES toggle in the transport bar; (3) AUTO default = news in the secondary language, deep-dives in English. Episodes without a rendition always play in English. Position, voices, and duration adjust per language; listening position survives a language switch (paragraph mapping). **Harness:** H1/H2 translate, H3 plays.

### UC7 — Promote news to curriculum
Digest flags deep-dive candidates; say "promote <topic>" (H4) and it lands in that front's `curriculum.md` Track E, picked up when the front's H2 turn comes around.

### UC8 — Rate episodes to steer future content
After finishing an episode, its card shows a 1–5 star row (H3, on-device; tap the current rating again to clear). Ratings reach the repo the same way listened state does: the sync pill's paste-string gains a `rate: <id>=<n>` segment, or say "rate <episode> 4" directly (H4). Either way the rating lands as a ` — ★n` suffix on the episode's `log.md` line and is baked back into the player on the next rebuild. Routines read it as an interest signal: H1 weights story ranking and Track E deep-dive flagging toward topics of ★4–5 episodes and away from ★1–2; H2 lets ratings steer the angle and depth of the next lesson. Rating is optional — unrated episodes contribute no signal, and signals never cross fronts. **Harness:** H3 captures, H4 persists, H1/H2 consume.

### UC9 — Work N fronts
The listener follows several unrelated areas — say IT, politics, sport — each deserving its own sources, editorial rules, and (optionally) curriculum. A front is a directory `fronts/<id>/` with `front.md` (label, hue, order, enabled, word overrides), `sources.md`, optional `curriculum.md`, and `digests/`; that directory is the front's entire universe, and nothing (ratings, editorial rules, curricula) leaks between fronts. `log.md` stays global with a front column, and episode ids are front-qualified (`it/2026-07-22-news`), so listened/rating sync is one paste regardless of front count. In the player, tabs (tinted with each front's hue) switch the whole page — queue, stats, empty states, default play target — to the selected front; an All tab interleaves every front by date, labeling each card. Open a new front by saying "add front <name>" (H4 creates the directory, researches sources, rebuilds the player); mothball one with "disable front <name>" (`enabled: false` — files stay, routines and player skip it). H1 covers every enabled front per run; H2 rotates. Legacy single-topic instances migrate automatically on `/update`. **Harness:** repo file convention + H1/H2/H3/H4.

## Adding a use case

1. Add a `### UCn — <name>` section here: the trigger, the harness (existing or new), and what state it reads/writes.
2. If it needs a new harness, prefer, in order: a repo file convention (free), a player feature (H3, still no backend), a chat op (H4), a new routine (H1/H2 pattern — costs a schedule).
3. Constraint that keeps this maintainable: harnesses may **only** communicate through repo files and the player page. No side channels, no services.
