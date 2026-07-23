# Listening log

Durable record. The player artifact tracks state on-device (localStorage); this file is the source of truth across devices and for the routines. Sync by telling Claude "mark <episode> listened" or during the weekly reconciliation.

Format: `- [x] date — front — type — title` (checked = listened; front = the front id, e.g. `ai`). A rating, if given, is appended as ` — ★n` (n = 1–5); routines read it as an interest signal, scoped to the episode's front.

## Episodes

<!-- newest first -->
