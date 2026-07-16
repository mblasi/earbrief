# earbrief — operating instructions for Claude

This repo is the state of a personal news/learning audio pipeline. No application code; **README.md** is the architecture, **USECASES.md** is the use-case/harness contract. Read both before changing anything.

**First run:** if `config.md` does not exist, this instance is not initialized — run the `setup` skill before anything else.

Instance values (player artifact URL, routine IDs, schedule, languages, listener profile) live in `config.md`.

## Chat ops you will be asked to do (harness H4)

- "mark <episode> listened" → check the `- [ ]` line in `log.md`, commit, push, then rebuild and republish the player (procedure below) so the checked state shows on next reload.
- pasted `mark listened: <id>, <id>` (from the player's sync button) → ids are digest stems like `2026-07-13-news`; check the matching `log.md` lines (match by date + type), commit, push, then rebuild and republish the player (procedure below). The player only shows the checked state after a rebuild+republish, so do one as part of this op.
- "add/disable source X" → edit `sources.md` (prefix a line with `x` to disable), commit, push.
- "promote <topic>" → add unchecked item under Track E in `curriculum.md` (max 3 there), commit, push.
- "rebuild and republish the player" → see procedure below.
- "update from upstream" → run the `update` skill.

## Player rebuild procedure

1. `python3 player/build.py` — must print the episode count; heed paragraph-mismatch warnings.
2. If `player/template.html` was edited, syntax-check the embedded script before publishing (an unescaped quote once broke the whole player):
   `node -e "const h=require('fs').readFileSync('player/player.html','utf8');new Function(h.match(/<script>([\s\S]*)<\/script>/)[1].replace('const EPISODES','var EPISODES'));console.log('ok')"`
3. Republish with the Artifact tool: `file_path` player/player.html, `url` set to `player_artifact_url` from `config.md` (ALWAYS pass `url` — publishing without it mints a new address and breaks the phone bookmark), favicon 📻.

## Invariants

- English digest (`digests/<id>.md`) is canonical; the secondary-language rendition (`<id>.<lang>.md`, if configured) must keep the exact paragraph count/order and carry no `## Sources` section.
- Episode bodies are spoken prose for TTS: no lists, tables, code blocks, URLs, or math notation.
- All state changes go through git commits; the player page never writes anywhere.
- Cloud routines (IDs in config.md) regenerate content daily/weekly; don't duplicate their work by hand unless a run failed.
- Template-owned vs instance-owned files are listed in the `update` skill; keep personal state out of template-owned files.
