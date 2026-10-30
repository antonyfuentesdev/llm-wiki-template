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

What can be a partition, and how one is created, split, merged, or renamed:
[AGENTS.md](../AGENTS.md) §3. New entries use this shape:

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
