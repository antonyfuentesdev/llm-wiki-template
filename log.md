# Log

Append-only, newest at the bottom. Every entry starts with `## [YYYY-MM-DD] <op> | <scope> |
<detail>` so the file stays parseable:

```bash
grep "^## \[" log.md | tail -20        # the last 20 things that happened
grep "^## \[.*\] feed" log.md          # every feed batch
grep "^## \[.*\] restructure" log.md   # how the wiki's shape has changed
```

Operations are `init`, `ingest` (one entry per deep source), `feed` (one entry per batch,
never per post), `query`, `lint`, `restructure`, and `schema`. See [AGENTS.md](AGENTS.md) §9.

---

## [2026-10-29] init | repo | Scaffolded from the template — 3 partitions, templates, schema
