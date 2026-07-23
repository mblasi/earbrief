# earbrief — operating instructions for Claude

This repo is the state of a personal news/learning audio pipeline. No application code; **README.md** is the architecture, **USECASES.md** is the use-case/harness contract. Read both before changing anything.

**First run:** if `config.md` does not exist, this instance is not initialized — run the `setup` skill before anything else.

Instance values (player artifact URL, routine IDs, schedule, languages, listener profile) live in `config.md`. The instance is split into **fronts** — independent topic areas under `fronts/<id>/`, each with its own `front.md` (metadata), `sources.md`, optional `curriculum.md`, and `digests/`. `log.md` is global, one line per episode with a front column. Episode ids are front-qualified: `<front>/<digest-stem>`, e.g. `ai/2026-07-13-news`.

## Chat ops you will be asked to do (harness H4)

- "mark <episode> listened" → check the `- [ ]` line in `log.md`, commit, push, then rebuild and republish the player (procedure below) so the checked state shows on next reload.
- pasted `mark listened: <id>, <id>` (from the player's sync button) → ids look like `ai/2026-07-13-news` (front/digest-stem); check the matching `log.md` lines (match by date + front + type), commit, push, then rebuild and republish the player (procedure below). The player only shows the checked state after a rebuild+republish, so do one as part of this op.
- "rate <episode> N" or pasted `rate: <id>=<n>, <id>=<n>` (the player's sync string; may arrive after a `mark listened:` segment, separated by `;`) → n is 1–5; append ` — ★n` to the matching `log.md` line (match by date + front + type; replace any existing ★ suffix), commit, push, then rebuild and republish the player so devices see the rating as synced.
- "add/disable source X" → edit the relevant front's `fronts/<id>/sources.md` (prefix a line with `x` to disable; ask which front only if genuinely ambiguous), commit, push.
- "promote <topic>" → add unchecked item under Track E in the relevant front's `curriculum.md` (max 3 there), commit, push.
- "add front <name>" → create `fronts/<slug>/` with a `front.md` (follow the shape of an existing one; pick an unused hue, next `order`), a researched `sources.md` for that area, a `curriculum.md` only if the user wants deep-dives there, and `digests/.gitkeep`. Commit, push, rebuild and republish the player so the new front's tab appears.
- "disable/enable front <name>" → flip `enabled:` in its `front.md`, commit, push, rebuild and republish (disabled fronts drop out of the player and the routines; their files stay).
- "rebuild and republish the player" → see procedure below.
- "update from upstream" → run the `update` skill.

## Player rebuild procedure

1. `python3 player/build.py` — must print the per-front episode counts; heed paragraph-mismatch warnings.
2. If `player/template.html` was edited, syntax-check the embedded script before publishing (an unescaped quote once broke the whole player):
   `node -e "const h=require('fs').readFileSync('player/player.html','utf8');new Function(h.match(/<script>([\s\S]*)<\/script>/)[1].replace('const EPISODES','var EPISODES'));console.log('ok')"`
3. Republish with the Artifact tool: `file_path` player/player.html, `url` set to `player_artifact_url` from `config.md` (ALWAYS pass `url` — publishing without it mints a new address and breaks the phone bookmark), favicon 📻.

## Invariants

- English digest (`fronts/<front>/digests/<stem>.md`) is canonical; the secondary-language rendition (`<stem>.<lang>.md`, if configured) must keep the exact paragraph count/order and carry no `## Sources` section.
- Episode bodies are spoken prose for TTS: no lists, tables, code blocks, URLs, or math notation.
- Fronts are independent editorial universes: sources, curriculum, ratings, and editorial rules never leak across fronts. `log.md` and `config.md` are the only shared state.
- `log.md` line format: `- [ ] date — front — type — title` (+ optional ` — ★n`). Lines without a front column are pre-migration legacy and map to the implicit `main` front.
- All state changes go through git commits; the player page never writes anywhere.
- Cloud routines (IDs in config.md) regenerate content daily/weekly; don't duplicate their work by hand unless a run failed. One daily run covers all enabled fronts; the weekly deep-dive rotates round-robin across fronts with a curriculum.
- Template-owned vs instance-owned files are listed in the `update` skill; keep personal state out of template-owned files.
