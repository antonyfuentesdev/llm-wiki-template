# Preferences

Your standing instructions to the agent. It reads this file at the start of every session,
and it overrides the defaults in [AGENTS.md](AGENTS.md) where the two conflict.

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

Things that belong elsewhere: what counts as a high-signal post (AGENTS.md §6), and partition
scopes ([wiki/partitions.md](wiki/partitions.md)).

## Rules

_None yet._
