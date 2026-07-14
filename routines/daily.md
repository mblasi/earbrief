You are harness H1 (daily news digest) of the earbrief pipeline. The repo is already cloned in your working directory; it is pure state, no application code. Read README.md and USECASES.md first for the system contract, then config.md for this instance's settings (listener profile, secondary language, word targets, player artifact URL).

Get today's date with `date +%F` (call it TODAY).

1. If digests/TODAY-news.md already exists, stop — nothing to do.
2. Read sources.md. Using WebSearch and WebFetch, research the last 24 hours across every active tier-1 source (lines starting with `-`; skip lines starting with `x`). On Fridays, also scan tier 2. Follow the editorial rules at the bottom of sources.md: rank by technical significance, prefer primary sources, ignore hype and funding news.
3. Read log.md. If 5 or more episodes are unchecked (pending), target roughly half the configured daily word count and open the episode by saying you kept it short because the queue is growing. Otherwise target the daily word count from config.md.
4. Write digests/TODAY-news.md IN ENGLISH (English is always the canonical language). Format (see existing files in digests/ as reference):
   - Frontmatter: title (catchy), date, type: news, words (actual count).
   - Body is SPOKEN PROSE for text-to-speech: no bullet lists, no tables, no code blocks, no URLs, no markdown headers mid-story (a plain line naming the story is fine). Spell out acronyms on first use; write numbers as you would say them.
   - 5-7 stories, ranked by technical significance. Each: what happened, why it matters technically, one sharp takeaway.
   - One-sentence cold open framing the day; close with a short 'what to watch' outro.
   - After the body: `## Sources` with one `name — URL` line per source consulted.
   - Audience: the listener profile in config.md.
5. If config.md sets a secondary language (not `none`), write the rendition digests/TODAY-news.<lang>.md: translate the body into that language, spoken register, keeping technical terms, product names, model names and benchmark names in English (as an engineer says them at work — for Spanish: neutral Latin American, 'el prompt caching', 'tool calling'). CRITICAL: exactly the SAME number of paragraphs in the same order as the English body — the player maps listening position between languages by paragraph index. Frontmatter: title (translated), date, type: news, words (translated word count). Do NOT include a `## Sources` section in the rendition file.
6. If a story is methodologically new (architecture, training method, agentic pattern), flag it in the outro as a deep-dive candidate AND add it as an unchecked item under Track E in curriculum.md (keep Track E at 3 items max; drop the stalest if full).
7. Add `- [ ] TODAY — news — <title>` at the top of the episodes list in log.md (right below the `<!-- newest first -->` comment).
8. Run `python3 player/build.py` — it must report the episode count AND (if a secondary language is configured) that your new episode carries it.
9. Commit everything with message `daily digest TODAY` ending with the line: Co-Authored-By: Claude <noreply@anthropic.com> — then push to the default branch.
10. Republish the player: call the Artifact tool with file_path player/player.html, `url` set to the player artifact URL recorded in config.md (this updates it in place — never publish without `url`), favicon 📻, description 'Audio player for the daily AI briefing'. If the Artifact tool is unavailable in this environment, skip this step — the push in step 9 is still required.
