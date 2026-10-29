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

Where to start. If the workflow depends on an external tool that hasn't been proven yet,
discovery belongs here once; after a successful run, move the chosen tools into Proven stack
and stop shopping.

## Proven stack

Required after a successful run that depended on external tools. Table of role → tool → why
it earned the slot (what was tried, what was rejected). Agents use this stack; they do not
re-select it. Omit this section when the workflow needs only the agent's built-in file,
search, and fetch tools, or while it has never been proven. Do not paste install flags,
versions, or last session's script — those come from live docs for the named tools.

| Role | Tool | Why it is here |
| --- | --- | --- |
| <role> | **<tool>** | <proven / rejected alternatives> |

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

What goes wrong in practice, and the first correct recovery. Add to this whenever a run
surprises you.

## Notes

Anything learned from running this that doesn't fit above.
