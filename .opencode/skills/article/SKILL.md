---
name: article
description: Generate a podcast episode from a specific article URL, resuming and explaining its content. Run when you want to create ad-hoc audio content from an interesting article.
---

# earbrief /article

Generate a podcast episode that summarizes and explains a specific article. This is an on-demand operation for creating ad-hoc content from articles you find interesting and want to listen to.

## Usage

User provides an article URL and optionally:
- Which front to file it under (if ambiguous, ask)
- Custom title (otherwise derive from article)

## Pre-check

1. Verify the article URL is accessible via WebFetch
2. If config.md doesn't exist, tell the user to run `/setup` first
3. Ask which front to file the episode under if:
   - Multiple fronts are enabled AND
   - The article topic is genuinely ambiguous
   Otherwise pick the most relevant front based on the article's subject matter and each front's editorial identity in their `front.md`.

## Execution

1. **Fetch the article**: Use WebFetch to get the full article content from the provided URL.

2. **Get today's date**: Run `date +%F` (call it TODAY).

3. **Determine the front**: 
   - Read all enabled fronts' `front.md` files to understand their editorial identities
   - Pick the front whose editorial focus best matches the article's topic
   - If genuinely ambiguous, ask the user
   - Call the chosen front's id FRONT

4. **Generate episode ID**: Use format `TODAY-article-N` where N starts at 1 and increments if there are already article episodes for TODAY in that front.

5. **Read context**:
   - Read `config.md` for listener profile, secondary language, and word targets
   - Read `fronts/FRONT/front.md` for editorial identity and word count settings
   - Read `log.md` and check this front's rated episodes (` — ★n` suffixes) to understand the listener's interests in this front
   - Target 60-70% of the front's daily_words (this is shorter than a news digest since it's a single article)

6. **Write the English digest** at `fronts/FRONT/digests/<episode-id>.md`:
   - **Frontmatter**: 
     ```
     ---
     title: <catchy title, derived from article or user-provided>
     date: TODAY
     type: article
     words: <actual word count>
     ---
     ```
   - **Body** is SPOKEN PROSE for text-to-speech:
     - No bullet lists, tables, code blocks, URLs, markdown headers mid-episode
     - Spell out acronyms on first use; write numbers as you would say them
     - Structure:
       1. **Cold open** (1-2 sentences): Hook — what's interesting about this article?
       2. **Context** (1 paragraph): Who wrote it, where it appeared, why it matters now
       3. **Summary** (3-4 paragraphs): The article's main points, arguments, and evidence — not a play-by-play but the through-line
       4. **Analysis** (2-3 paragraphs): What this means, connections to broader themes, what the listener should take away
       5. **Close** (1 sentence): One sharp takeaway or question to chew on
     - Audience: the listener profile in config.md, through this front's editorial lens
   - **Sources section**: After the body, add:
     ```
     ## Sources
     <article title> — <article URL>
     ```

7. **Write secondary language rendition** (if configured):
   - If `config.md` sets a secondary language (not `none`), write `fronts/FRONT/digests/<episode-id>.<lang>.md`
   - Translate the body into that language (spoken register, neutral Latin American for Spanish)
   - Keep proper nouns and technical jargon in English where natural
   - **CRITICAL**: Exactly the same number of paragraphs in the same order as the English version
   - Frontmatter: translated title, same date/type, translated word count
   - **Do NOT** include a `## Sources` section in the rendition file

8. **Update log.md**: Add at the top of the episodes list (right below `<!-- newest first -->`):
   ```
   - [ ] TODAY — FRONT — article — <title>
   ```

9. **Rebuild the player**: Run `python3 player/build.py` — verify it reports the per-front episode counts correctly.

10. **Commit and push**:
    - Commit with message: `add article episode: <title>`
    - End commit message with: `Co-Authored-By: AI Agent <noreply@github.com>`
    - Push to default branch

## Post-execution

After successful completion:
1. Report the episode details (front, title, word count, episode ID)
2. Mention the original article URL
3. Remind the user that GitHub Pages deployment was triggered and they can reload the player page in a minute to listen

## Notes

- Article episodes use type `article` (not `news` or `deepdive`) to distinguish them in the log
- They count toward the front's pending queue (affects future digest length decisions in step 3 of routines/daily.md)
- Ratings work the same way: the listener can rate article episodes and those ratings influence future content
- Multiple article episodes can be generated per day (hence the `-N` suffix if needed)
