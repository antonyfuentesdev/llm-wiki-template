---
type: workflow
partition: workflows
created: 2026-10-29
updated: 2026-10-29
sources: []
tags: [lint, maintenance, provenance]
status: active
---

# Run a lint pass

Check the wiki's health against [lint.md](../../lint.md), report what's wrong, and propose
fixes without applying them.

## When to use this

- **Scoped:** automatically at the end of every ingest or feed batch.
- **Full:** when the human asks ("run a full lint", "health check"), or suggest one when the
  last `lint | full` entry in `log.md` is a few weeks old.

## Success and failure

Success: a report grouped by the checklist's sections, each finding naming the page and the
evidence, each with a proposed fix; nothing changed on disk except the `log.md` entry.

Failure: silently fixing things; proposing a partition with no topical case; a report so
long the human can't act on it.

## First move

Decide the scope. Scoped: the pages this batch created or modified (from your own work, or
`git status` and `git diff --name-only`), plus pages linking to or from them, plus the
partitions they live in for the cluster check. Full: every page.

## Steps

1. **Run the mechanical checks.** Broken relative links and footnote targets, numbered
   footnotes, missing frontmatter fields, pages missing from their index, orphans, registry
   vs disk, and the two raw-integrity commands from lint.md. A short throwaway script in
   `tmp/` is fine for link checks on a large wiki. → verify: each check produced a count, even
   if zero.
2. **Run the judgment checks.** Contradictions, stale claims, unsourced claims, missing pages,
   missing cross-references, gaps. In a scoped pass, compare the touched pages against their
   neighbors; in a full pass, also compare topic pages across partitions.
3. **Check for clusters.** For each partition in scope, list the pages that link to few
   others in the partition, then group those that link to each other. Report any group at or
   near 8 pages with a written topical case (AGENTS.md §3). No case, no proposal.
4. **Write the report.** Most important first: integrity problems, then contradictions, then
   everything else. One line per finding plus its proposed fix.
5. **Log one `lint` entry** — `scoped` or `full`, the partitions covered, the finding count.
6. **Wait for approval.** Apply only the fixes the human approves. Restructures follow
   AGENTS.md §3.

## Failure modes

- **Treating a renamed raw file as corruption.** An approved restructure moves raw files with
  `git mv`, which shows as a rename in the history check. Match it to its `restructure` log
  entry before raising the alarm.
- **Cluster noise.** Pages from one big ingest batch link to each other because they arrived
  together, not because they form a subject. That's exactly what the topical case filters.
