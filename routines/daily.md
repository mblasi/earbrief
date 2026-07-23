You are harness H1 (daily news digest) of the earbrief pipeline. The repo is already cloned in your working directory; it is pure state, no application code. Read README.md and USECASES.md first for the system contract, then config.md for this instance's settings (listener profile, secondary language, word targets, player artifact URL).

Get today's date with `date +%F` (call it TODAY).

The instance has one or more FRONTS: directories under `fronts/`, each with a `front.md` (metadata), its own `sources.md`, and its own `digests/`. Process every front whose `front.md` has `enabled: true`, in `order`. Each front is an independent editorial universe — its own sources, its own digest, its own log line. Steps 1–7 below run PER FRONT; steps 8–10 run once at the end.

For each enabled front (call its id FRONT):

1. If fronts/FRONT/digests/TODAY-news.md already exists, skip this front — done already.
2. Read fronts/FRONT/sources.md. Using WebSearch and WebFetch, research the last 24 hours across every active tier-1 source (lines starting with `-`; skip lines starting with `x`). On Fridays, also scan tier 2. Follow the editorial rules at the bottom of that sources.md and the editorial identity in front.md.
3. Read log.md, considering only this front's lines (`date — FRONT — type — title`). If 5 or more of them are unchecked (pending), target roughly half this front's daily word count and open the episode by saying you kept it short because the queue is growing. Otherwise target the front's `daily_words` from front.md, falling back to config.md. Also collect this front's ratings (` — ★n` suffixes, 1–5): they are the listener's interest signal. Skim the titles (and, for the strongest signals, the digests) of rated episodes to infer WHICH topics earned the stars; when ranking stories in step 4 and flagging deep-dive candidates in step 6, weight topics similar to ★4–5 episodes up and topics similar to ★1–2 episodes down. Ratings tune emphasis — they never override the front's editorial rules, and unrated episodes contribute nothing. Ratings never cross fronts.
4. Write fronts/FRONT/digests/TODAY-news.md IN ENGLISH (English is always the canonical language). Format (see existing files in that digests/ as reference):
   - Frontmatter: title (catchy), date, type: news, words (actual count).
   - Body is SPOKEN PROSE for text-to-speech: no bullet lists, no tables, no code blocks, no URLs, no markdown headers mid-story (a plain line naming the story is fine). Spell out acronyms on first use; write numbers as you would say them.
   - 5-7 stories, ranked by the front's editorial rules. Each: what happened, why it matters, one sharp takeaway.
   - One-sentence cold open framing the day; close with a short 'what to watch' outro.
   - After the body: `## Sources` with one `name — URL` line per source consulted.
   - Audience: the listener profile in config.md, through this front's lens.
5. If config.md sets a secondary language (not `none`), write the rendition fronts/FRONT/digests/TODAY-news.<lang>.md: translate the body into that language, spoken register, keeping proper nouns and field jargon in English where that is how the listener says them (for Spanish: neutral Latin American). CRITICAL: exactly the SAME number of paragraphs in the same order as the English body — the player maps listening position between languages by paragraph index. Frontmatter: title (translated), date, type: news, words (translated word count). Do NOT include a `## Sources` section in the rendition file.
6. If this front has a fronts/FRONT/curriculum.md and a story is a strong deep-dive candidate by that front's standards (methodologically new, structurally important), flag it in the outro AND add it as an unchecked item under Track E in that curriculum.md (keep Track E at 3 items max; drop the stalest if full). Fronts without a curriculum.md skip this step.
7. Add `- [ ] TODAY — FRONT — news — <title>` at the top of the episodes list in log.md (right below the `<!-- newest first -->` comment).

Once every enabled front is done:

8. Run `python3 player/build.py` — it must report the per-front episode counts AND (if a secondary language is configured) that your new episodes carry it.
9. Commit everything with message `daily digest TODAY` ending with the line: Co-Authored-By: Claude <noreply@anthropic.com> — then push to the default branch.
10. Republish the player: call the Artifact tool with file_path player/player.html, `url` set to the player artifact URL recorded in config.md (this updates it in place — never publish without `url`), favicon 📻, description 'Audio player for the daily briefing'. If the Artifact tool is unavailable in this environment, skip this step — the push in step 9 is still required.
