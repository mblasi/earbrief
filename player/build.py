#!/usr/bin/env python3
"""Compile digests/*.md into player/player.html. Stdlib only.

Canonical episodes are English (digests/<id>.md). An optional Spanish
companion (digests/<id>.es.md) carries a translated title/body; the player
exposes it as a listening-language choice.

Usage: python3 player/build.py   (from repo root or anywhere)
"""
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        return None
    meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    body, _, src_block = m.group(2).partition("\n## Sources")
    sources = []
    for line in src_block.strip().splitlines():
        u = re.search(r"https?://\S+", line)
        if not u:
            continue
        name = line[: u.start()].strip().strip("—-–: ").strip()
        sources.append({"name": name or u.group(0), "url": u.group(0).rstrip(").,")})
    return meta, body.strip(), sources


episodes = []
for f in sorted(root.glob("digests/*.md"), reverse=True):  # newest first
    if f.name.endswith(".es.md"):
        continue
    parsed = parse(f)
    if not parsed:
        print(f"skip {f.name}: no frontmatter")
        continue
    meta, body, sources = parsed
    ep = {
        "id": f.stem,
        "date": meta.get("date", ""),
        "type": meta.get("type", "news"),
        "title": meta.get("title", f.stem).strip().strip('"'),
        "words": int(meta.get("words", "0") or 0),
        "text": body,
        "sources": sources,
    }
    es = f.with_name(f.stem + ".es.md")
    if es.exists():
        parsed_es = parse(es)
        if parsed_es:
            meta_es, body_es, _ = parsed_es
            n_en = len([p for p in body.split("\n\n") if p.strip()])
            n_es = len([p for p in body_es.split("\n\n") if p.strip()])
            if n_en != n_es:
                print(f"warn {es.name}: paragraph count {n_es} != {n_en} (position mapping will clamp)")
            ep["title_es"] = meta_es.get("title", ep["title"]).strip().strip('"')
            ep["text_es"] = body_es
    episodes.append(ep)

def norm(t):
    return re.sub(r"\s+", " ", t).strip().strip('"').lower()


# listened state from log.md (source of truth) → baked into the player as seed
log_keys = set()
for line in (root / "log.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"-\s*\[x\]\s*(\S+)\s*—\s*(\w+)\s*—\s*(.+)$", line, re.I)
    if m:
        log_keys.add((m.group(1), m.group(2).lower(), norm(m.group(3))))
listened = [e["id"] for e in episodes if (e["date"], e["type"], norm(e["title"])) in log_keys]
matched = {(e["date"], e["type"], norm(e["title"])) for e in episodes}
for k in log_keys - matched:
    print(f"warn log.md: checked entry matches no episode: {' — '.join(k)}")

tpl = (root / "player" / "template.html").read_text(encoding="utf-8")
out = tpl
for marker, payload in (
    ("/*__EPISODES__*/[]", episodes),
    ("/*__LISTENED__*/[]", listened),
):
    if marker not in out:
        raise SystemExit(f"template.html: marker {marker} not found")
    out = out.replace(marker, json.dumps(payload, ensure_ascii=False))
(root / "player" / "player.html").write_text(out, encoding="utf-8")
n_es = sum(1 for e in episodes if "text_es" in e)
print(f"built player/player.html with {len(episodes)} episodes ({n_es} with Spanish, {len(listened)} listened per log.md)")
