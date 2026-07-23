# Demo instance

Sample state for the public demo artifact linked from the main README: three
fronts, a handful of evergreen sample episodes (not real news), one rated
deep-dive. Nothing here flows into instances created from the template.

Rebuild and republish after a player change:

```
cp -r player demo/player            # build.py treats its parent's parent as root
python3 demo/player/build.py
```

then republish `demo/player/player.html` with the Artifact tool, passing the
demo URL below as `url` (never publish without it).

- demo_artifact_url: https://claude.ai/code/artifact/4c1db192-1d52-41a9-8cfb-6d31f9204e7d
