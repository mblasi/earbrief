# Use cases & harnesses

Each use case names the harness that serves it. A harness is whichever Claude-native mechanism does the work: a scheduled routine, the player artifact, a chat command, or a repo file. Nothing here is custom infrastructure.

## Harness catalog

| Harness | What it is | State it touches |
|---|---|---|
| H1 daily-digest routine | Scheduled cloud agent, daily (`routines/daily.md`) | reads `sources.md`, writes `digests/`, refreshes player |
| H2 deep-dive routine | Scheduled cloud agent, weekly (`routines/weekly.md`) | reads `curriculum.md`, writes `digests/`, checks item off, refreshes player |
| H3 player artifact | One web page on the phone: TTS playback, progress, listened state (localStorage seeded from `log.md` at build; sync button emits a paste-string) | on-device only |
| H4 chat ops | Ad-hoc Claude Code session: "mark X listened", pasted `mark listened: <ids>` sync strings, "add source Y", "promote Z to curriculum" | `log.md`, `sources.md`, `curriculum.md` |
| H5 spark hook | Button in the player that opens a **new, external Claude session** prefilled with the episode context | none — fire and forget |

## Use cases

### UC1 — Stay current (daily)
Open the player, hit play on today's episode. **Harness:** H1 produces it, H3 plays it.

### UC2 — Close the knowledge gap (weekly)
The weekly deep-dive follows `curriculum.md` order. **Harness:** H2, H3.

### UC3 — Track listened vs pending
Player marks episodes automatically on-device (H3); `log.md` is the durable cross-device record. Sync is two-way but always passes through the repo:
- **Repo → devices:** `build.py` bakes the checked ids from `log.md` into the player; each device applies them as listened on load (once per id, so a local un-check for replay sticks). Reaches devices on the next rebuild/republish — the daily routine's, or ask for one.
- **Devices → repo:** episodes finished locally but unchecked in `log.md` surface a **sync N to log ⇪** pill in the player header; tapping copies `mark listened: <ids>` to the clipboard — paste it into any Claude chat and H4 updates `log.md`.
The player still never writes anywhere (artifact CSP blocks all outbound requests — that's why the paste hop exists). Weekly routine flags a growing pending pile and shortens episodes if needed.

### UC4 — Manage sources
Edit `sources.md` directly, or ask Claude (H4). Takes effect next routine run. Disable without deleting by prefixing a line with `x`.

### UC5 — Spark: an episode wakes up an idea
While listening, tap **Spark** on the episode. It opens a new Claude session (app or web) prefilled with the episode title, its key context, and your cue to deep-dive. That session is launched and managed **outside this solution** — the only responsibility here is firing it. Nothing is written to the repo; if the external session produces something worth keeping, bring it back via H4 (e.g. "promote this to curriculum Track E").

### UC6 — Choose the listening language
Sources and canonical episodes are always English; if `config.md` sets a secondary language, routines emit a pre-translated rendition (`.<lang>.md`, technical terms kept in English) at build time — the player cannot translate live (artifact CSP blocks external calls). Language resolution, highest precedence first: (1) per-episode pin — tap the language chip on a card to switch that episode to the other language, tap again to unpin (pinned = accent color + ✱); (2) the global AUTO/EN/ES toggle in the transport bar; (3) AUTO default = news in the secondary language, deep-dives in English. Episodes without a rendition always play in English. Position, voices, and duration adjust per language; listening position survives a language switch (paragraph mapping). **Harness:** H1/H2 translate, H3 plays.

### UC7 — Promote news to curriculum
Digest flags deep-dive candidates; say "promote <topic>" (H4) and it lands in `curriculum.md` Track E, picked up by the next H2 run.

## Adding a use case

1. Add a `### UCn — <name>` section here: the trigger, the harness (existing or new), and what state it reads/writes.
2. If it needs a new harness, prefer, in order: a repo file convention (free), a player feature (H3, still no backend), a chat op (H4), a new routine (H1/H2 pattern — costs a schedule).
3. Constraint that keeps this maintainable: harnesses may **only** communicate through repo files and the player page. No side channels, no services.
