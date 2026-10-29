---
type: index
scope: registry
created: 2026-10-29
updated: 2026-10-29
---

# Partition registry

The agent reads this before filing anything. Each entry has a scope and — more importantly —
a **not here** line. The negative boundary is what stops partitions from drifting into each
other.

## The rule for what can be a partition

**Partitions are subjects.** Format, platform, source, and recency are metadata, not folders.
If a proposed partition's name describes *how something arrived* rather than *what it is
about*, it belongs in frontmatter instead.

This is why there is no `social`, `articles`, or `2026` partition. A thread about caching is
knowledge about caching; it files alongside the paper and the conference talk on the same
subject, with `platform: x` recorded on the post. Splitting by delivery mechanism would
scatter one subject across several folders and quietly destroy the cross-linking that makes
this wiki worth more than its sources.

## Why the scaffold starts small

A new wiki doesn't know its own shape yet. Partitions drawn up front are guesses, and early
guesses act as gravity wells: once a folder exists, borderline material lands in it and every
later filing decision bends around it. So the scaffold starts with one broad partition for
knowledge (`general`), one for your own work (`projects`), and one for operating procedures
(`workflows`). Real subjects get carved out of `general` once there is evidence for them.

## Creating a new partition

Two gates, both required, and proposals surface **only during lint** — never mid-ingest.

1. **Mechanical trigger.** A page is a *misfit* when it links to few or no other pages in its
   own partition. A set of misfits that link to *each other* is a *cluster*. When a cluster
   reaches **8 pages**, the partition becomes a candidate.
2. **Written topical case.** What is the proposed partition about, why does its host no longer
   fit, and what would belong elsewhere? If that can't be articulated in a few sentences, the
   cluster is an artifact of ingest order and the proposal is dropped.

You can also just ask: "Add a partition called `cooking` for recipes and food science." The
request is the approval; the agent still writes the scope and not-here lines below.

On approval: register it here, create `wiki/<name>/{index.md,raw/,sources/}`, move the
clustered pages *and their raw files*, update every inbound link, add it to the root index,
and log a `restructure` entry. Splits, merges, and renames follow the same gates and the same
timing. See [AGENTS.md](../AGENTS.md) §3.

New entries use this shape:

```markdown
### <name>
- **Scope:** What it holds, in one or two lines.
- **Not here:** The nearest neighbors and where their material goes instead.
- **Created:** YYYY-MM-DD
- **Index:** [<name>/index.md](<name>/index.md)
```

---

## Registered partitions

### general
- **Scope:** Knowledge about the world: articles, papers, books, courses, talks, ideas you
  picked up, and the people, tools, and concepts in them. The default home for anything that
  isn't about your own work and has no more specific partition yet.
- **Not here:** Your own projects, decisions, and meetings (`projects`). Procedures for the
  agent to execute (`workflows`). A subject that has earned its own partition — check the
  entries below first.
- **Created:** 2026-10-29
- **Index:** [general/index.md](general/index.md)

### projects
- **Scope:** Things you are doing: projects, their decisions and status, meeting notes, and
  the people you work with on them. Each project usually gets a topic page that holds its
  current state.
- **Not here:** Knowledge that outlives the project, such as a technique you learned while
  doing it (`general`, linked from the project page). Reusable procedures (`workflows`).
- **Created:** 2026-10-29
- **Index:** [projects/index.md](projects/index.md)

### workflows
- **Scope:** Reusable procedures, prompts, and playbooks — steps that guide an agent through a
  task, including how to operate this wiki.
- **Not here:** Knowledge about how a tool works (`general`). One-off instructions with no
  reuse value. Standing behavior rules for the agent (`preferences.md` at the repo root).
- **Created:** 2026-10-29
- **Index:** [workflows/index.md](workflows/index.md)
