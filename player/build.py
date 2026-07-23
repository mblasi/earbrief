#!/usr/bin/env python3
"""Compile fronts/*/digests/*.md into player/player.html. Stdlib only.

A front is a directory under fronts/ with a front.md (metadata), its own
sources.md/curriculum.md, and a digests/ folder. Episode ids are
front-qualified: <front>/<digest-stem>, e.g. ai/2026-07-22-news.

Canonical episodes are English (digests/<id>.md). An optional Spanish
companion (digests/<id>.es.md) carries a translated title/body; the player
exposes it as a listening-language choice.

Legacy (pre-fronts) instances: a root-level digests/ folder is read as an
implicit front "main", its episode ids stay bare stems, and log.md lines
without a front column match it — nothing breaks before migration.

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


def front_meta(path):
    """Parse `- key: value` lines from a front.md."""
    meta = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^-\s*(\w+):\s*(.+?)\s*$", line)
        if m and not m.group(2).startswith("("):
            meta[m.group(1)] = m.group(2)
    return meta


# ---- discover fronts ----
fronts = []  # [{id, label, hue, order}] enabled only, display order
for fm in sorted(root.glob("fronts/*/front.md")):
    meta = front_meta(fm)
    fid = meta.get("id", fm.parent.name)
    if meta.get("enabled", "true").lower() == "false":
        continue
    fronts.append({
        "id": fid,
        "label": meta.get("label", fid),
        "hue": int(meta.get("hue", "28") or 28),
        "order": int(meta.get("order", "99") or 99),
        "dir": fm.parent,
    })
if (root / "digests").is_dir() and list((root / "digests").glob("*.md")):
    # legacy layout: treat root digests/ as an implicit front
    fronts.append({"id": "main", "label": "Briefing", "hue": 28, "order": 0,
                   "dir": root, "legacy": True})
fronts.sort(key=lambda f: (f["order"], f["id"]))


def episode_from(f, front):
    parsed = parse(f)
    if not parsed:
        print(f"skip {f.name}: no frontmatter")
        return None
    meta, body, sources = parsed
    ep = {
        "id": f.stem if front.get("legacy") else f"{front['id']}/{f.stem}",
        "front": front["id"],
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
    return ep


episodes = []
for front in fronts:
    for f in sorted(front["dir"].glob("digests/*.md"), reverse=True):  # newest first
        if f.name.endswith(".es.md"):
            continue
        ep = episode_from(f, front)
        if ep:
            episodes.append(ep)
episodes.sort(key=lambda e: e["date"], reverse=True)  # interleave fronts, newest first


def norm(t):
    return re.sub(r"\s+", " ", t).strip().strip('"').lower()


# listened state + ratings from log.md (source of truth) → baked into the player as seed
# line format: - [x] date — front — type — title — ★n   (front column absent on legacy lines)
front_ids = {f["id"] for f in fronts}
log_keys = set()
log_ratings = {}
for line in (root / "log.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"-\s*\[x\]\s*(.+)$", line, re.I)
    if not m:
        continue
    cols = [c.strip() for c in m.group(1).split("—")]
    stars = None
    sm = re.fullmatch(r"★([1-5])", cols[-1]) if len(cols) > 1 else None
    if sm:
        stars = int(sm.group(1))
        cols = cols[:-1]
    if len(cols) < 3:
        print(f"warn log.md: unparseable entry: {line.strip()}")
        continue
    date = cols[0]
    if cols[1] in front_ids:  # date — front — type — title[ — cont.]
        fid, typ, title = cols[1], cols[2], " — ".join(cols[3:])
    else:  # legacy: date — type — title[ — cont.]
        fid, typ, title = "main", cols[1], " — ".join(cols[2:])
    if not title:
        print(f"warn log.md: entry without title: {line.strip()}")
        continue
    key = (date, fid, typ.lower(), norm(title))
    log_keys.add(key)
    if stars:
        log_ratings[key] = stars


def key_of(e):
    return (e["date"], e["front"], e["type"], norm(e["title"]))


listened = [e["id"] for e in episodes if key_of(e) in log_keys]
ratings = {e["id"]: log_ratings[key_of(e)] for e in episodes if key_of(e) in log_ratings}
matched = {key_of(e) for e in episodes}
for k in log_keys - matched:
    print(f"warn log.md: checked entry matches no episode: {' — '.join(k)}")

fronts_payload = [{"id": f["id"], "label": f["label"], "hue": f["hue"]} for f in fronts]
tpl = (root / "player" / "template.html").read_text(encoding="utf-8")
out = tpl
for marker, payload in (
    ("/*__FRONTS__*/[]", fronts_payload),
    ("/*__EPISODES__*/[]", episodes),
    ("/*__LISTENED__*/[]", listened),
    ("/*__RATINGS__*/{}", ratings),
):
    if marker not in out:
        raise SystemExit(f"template.html: marker {marker} not found")
    out = out.replace(marker, json.dumps(payload, ensure_ascii=False))
(root / "player" / "player.html").write_text(out, encoding="utf-8")
n_es = sum(1 for e in episodes if "text_es" in e)
per_front = ", ".join(f"{f['id']}:{sum(1 for e in episodes if e['front'] == f['id'])}" for f in fronts) or "no fronts"
print(f"built player/player.html with {len(episodes)} episodes across {len(fronts)} fronts ({per_front}; {n_es} with Spanish, {len(listened)} listened, {len(ratings)} rated per log.md)")
