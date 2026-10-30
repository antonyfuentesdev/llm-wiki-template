# Preferences

Your standing instructions to the agent. It reads this file at the start of every session,
and it overrides the defaults in [AGENTS.md](AGENTS.md) where the two conflict. Two rules
can't be overridden: raw sources stay append-only (§1), and claims stay cited (§7).

You can edit this file by hand. The agent also adds to it when you state a rule meant to
last ("from now on, write summaries in Spanish"), and replaces an entry when a new rule
contradicts it. Each change gets a `schema` entry in [log.md](log.md).

Keep entries short. One rule per bullet, starting with **Always**, **Never**, or **Do**, and
ending with the date it was added or last changed:

```markdown
- **Always:** write page prose in British English. — added 2026-11-02
- **Never:** create entity pages for people mentioned only in passing. — added 2026-11-02
- **Do:** prefer academic papers over blog posts when asked to find sources. — added 2026-11-05
```

Things that belong elsewhere: what counts as a high-signal post ([signal.md](signal.md)), and
partition scopes ([wiki/partitions.md](wiki/partitions.md)).

## Rules

<!-- To review each source before the agent updates other pages, uncomment this line:
- **Do:** ingest interactively: pause after the source summary and ask what to emphasize. — added YYYY-MM-DD
-->

_None yet._
