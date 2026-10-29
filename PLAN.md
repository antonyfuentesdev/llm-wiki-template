# Design notes

Why this template is shaped the way it is. [AGENTS.md](AGENTS.md) is the operative spec and
wins on any conflict; this file is background for when you want to change a rule and need to
know what it was protecting.

The pattern comes from Andrej Karpathy's
[LLM wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): three
layers (immutable raw sources, an LLM-maintained wiki, a schema file), three operations
(ingest, query, lint), and the claim that an LLM makes wiki maintenance cheap enough to keep
doing. The gist is deliberately abstract. Everything below is one concrete answer to the
questions it leaves open.

## Raw is append-only, not "never touched by the agent"

The gist says raw sources are immutable and the LLM never modifies them. Here the agent
fetches and files most sources itself, so it does write to `raw/`. The rule became
*append-only*: files are added, never edited or deleted.

That rule carries the whole provenance system. An agent that can edit its sources will
eventually "clean up" a source to agree with the summary it already wrote, and from then on a
citation proves nothing. Corrections add a new dated file and mark the old one superseded.

## Raw lives inside each partition

Each partition holds its own `raw/`, `sources/`, and synthesis pages, so one folder shows the
whole picture for a subject and can be moved as a unit. The cost is that a bare `git diff`
mixes long captured articles with the few lines that changed on a topic page. Git pathspecs
recover the split review (AGENTS.md §10). Three details there fail quietly if changed:
`git add -N .` (diff ignores new files otherwise), the trailing `/*` in pathspecs (a
directory-style pathspec matches nothing), and `MDR` (plain `M` misses deletions).

## Partitions are subjects, and the scaffold starts with few

A partition answers "what is this about", never "how did it arrive". A `social` partition
would put a thread about caching in a different folder from the caching paper, and since the
agent reads locally first, it would stop connecting them. Platform and format go in
frontmatter.

New partitions need two things: a cluster of 8 mutually-linked pages that don't fit their
host, and a written case for the subject. Links alone are too trusting, since pages from one
ingest batch link to each other because they arrived together. Judgment alone is too loose.
Eight is a starting value: raise it if lint keeps proposing partitions you reject, lower it if
you notice bad neighbors before lint does. Proposals come only during lint, so a batch ingest
never stops to ask structural questions.

The scaffold ships `general`, `projects`, and `workflows` rather than a guessed taxonomy.
Early partitions act as gravity wells: borderline material lands in whatever folder already
exists. Starting broad and carving subjects out on evidence avoids that.

## Three source tiers

Deep sources (articles, papers, transcripts, notes) each get a raw file and a source page.
Feed posts don't: at 10–30 a day they'd be most of the corpus by count and little of it by
value. They're captured in per-batch digests, triaged against a rubric the human owns
(AGENTS.md §6), and only high-signal posts update pages, cited by anchor. Saved bookmarks sit
between: someone already filtered them, so they get per-item treatment when they carry enough
body.

Digest structure is fixed because retrieval is plain text search. Fixed key names on their
own lines make `grep "signal: high"` work.

## Keyed footnotes, marked inference, surfaced contradictions

Pages are rewritten, not appended to. Numbered footnotes re-point silently when a rewrite
reorders sources; a key named after the raw file breaks loudly and tells the reader what backs
the claim. Citations go to raw files because source pages get rewritten too.

The agent may add its own knowledge, always inside an `[!inference]` callout, so you can tell
at a glance what is grounded. When sources disagree, both claims stay on the page with both
citations. A recorded disagreement is more useful than a manufactured consensus.

## Lint is scoped by default and never fixes on its own

A full pass after every daily batch would re-read hundreds of untouched pages. Scoped lint
checks what a batch touched plus its neighbors and the clusters in those partitions; a full
pass on request catches slow drift. Lint reports and proposes; the human approves.

## Preferences live outside AGENTS.md

AGENTS.md is the part of this repo you might want to update from the template later.
[preferences.md](preferences.md) is yours: tone, language, standing rules. Keeping them apart
means a template update doesn't overwrite your instructions, and the agent has a clear place
to record a rule you state once.

## Light preflight

The agent reads preferences every session and only the indexes a task needs. Reading the
whole wiki, or all of `log.md`, before every answer would cost more than most answers.

## Deliberately not built

- **A search index or vector store.** Indexes plus grep cover this. If retrieval starts
  missing things, fix structure first; tooling second.
- **Helper scripts.** The agent edits files directly. A script earns its place when the same
  mechanical job comes up often enough that shelling out is faster.
- **Obsidian config.** Links are plain relative markdown, so the wiki renders in any editor,
  on GitHub, and in Obsidian.
- **Tool-specific config.** The spec names no particular agent, model, or service, so it
  works across harnesses.
