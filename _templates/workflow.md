---
type: workflow
partition: workflows
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources: []
tags: []
status: active
---

# <Workflow name>

One sentence: the outcome a later agent is trying to achieve.

## When to use this

Recognition: this situation vs not this. Specific enough that an agent can tell whether the
current task qualifies — vague triggers are why workflows go unused.

## Success and failure

How to know the run worked or failed. Name the evidence, not a frozen command.

## First move

Where to start: what to read, and what to check before touching anything.

## Preconditions

What must be true before starting. Exact only when it is a contract (anchors, append-only
paths, manifest keys, `tmp/`). Everything else is intent.

## Steps

Each step is intent, the tool for that step if it matters, and a check. Name what to achieve
and how to know it worked. Do not paste session-specific flags, file lists, or tool-call
sequences.

1. **<Intent>** → verify: <check>
2. **<Intent>** → verify: <check>
3. **<Intent>** → verify: <check>

## Failure modes

What goes wrong in practice, and the first correct recovery. When a run surprises you,
propose an edit to this page; it changes only with the human's approval and a `schema` log
entry (AGENTS.md §1).

## Notes

Anything learned from running this that doesn't fit above.
