# Listening log

Durable record. The player page tracks state on-device (localStorage); this file is the source of truth across devices and for the workflows. Sync by telling your AI assistant "mark <episode> listened" or during the weekly reconciliation.

Format: `- [x] date — front — type — title` (checked = listened; front = the front id, e.g. `ai`). A rating, if given, is appended as ` — ★n` (n = 1–5); routines read it as an interest signal, scoped to the episode's front.

## Episodes

<!-- newest first -->
