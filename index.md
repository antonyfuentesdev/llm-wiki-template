---
type: index
scope: root
created: 2026-10-29
updated: 2026-10-29
---

# Index

The catalog of the whole wiki. The agent reads this first when answering a question, then
drills into the partitions and pages that look relevant. It is updated on every ingest.

For the chronological view of what happened when, see [log.md](log.md). For the rules the
agent follows, see [AGENTS.md](AGENTS.md).

## Partitions

Scope definitions live in [wiki/partitions.md](wiki/partitions.md) and are deliberately not
repeated here — one authoritative copy, no drift.

**Pages** counts the partition root: entity, concept, topic, question, and workflow pages,
excluding `index.md`. **Sources** counts the summary pages under `sources/`, one per deep
source. Feed digests are counted in neither — they live in `raw/` and are listed on each
partition index.

| Partition | Pages | Sources |
| --- | --- | --- |
| [general](wiki/general/index.md) | 0 | 0 |
| [projects](wiki/projects/index.md) | 0 | 0 |
| [workflows](wiki/workflows/index.md) | 5 | 0 |

## Open threads

Questions the wiki has raised but not answered, and gaps worth filling with a new source.
Lint proposes additions here; they land once the human approves them.

_None yet._
