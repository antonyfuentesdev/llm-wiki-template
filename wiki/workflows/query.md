---
type: workflow
partition: workflows
created: 2026-10-29
updated: 2026-10-29
sources: []
tags: [query, retrieval, citations]
status: active
---

# Answer a question

Answer from what the wiki holds, cite the raw files behind each claim, and keep answers worth
keeping as question pages.

## When to use this

The human asks something the wiki might know: "what do my sources say about…", "compare…",
"where do they disagree…", "what changed lately…". Not this: questions about how the wiki
itself works — answer those from AGENTS.md.

## Success and failure

Success: every non-obvious claim in the answer is cited to a raw file, your own reasoning is
marked as inference, and gaps are stated plainly.

Failure: an answer built from general knowledge with wiki-flavored citations; citations to
source pages instead of raw files; a confident answer to a question the wiki doesn't cover.

## First move

Read [index.md](../../index.md), then the indexes of the partitions that look relevant. Pick
candidate pages from those before opening any page body.

## Steps

1. **Route.** From the indexes, choose a bounded set of pages — usually the topic pages first,
   since they hold the synthesis. → verify: you can say why each page is on the list.
2. **Read and verify.** Read the candidates. For each claim the answer will rest on, follow
   the footnote to its anchor in `raw/` and check that the passage says it; where the
   footnote carries a quote, find the quote there. → verify: no claim depends on a page
   whose footnote you didn't check, when the stakes are more than casual.
3. **Widen only if routing failed.** Search all of `wiki/`, including `raw/` and feed
   digests (`grep -r "signal: high" wiki/*/raw/` finds extracted posts). A hit in `raw/` with
   no wiki page pointing at it is also a lint finding — mention it.
4. **Answer.** Lead with the direct answer, then the support. Cite with links to raw files.
   Present disagreements with both sides cited. Mark anything from outside the wiki as
   inference. If the wiki doesn't cover the question, say that first. The answer can be
   prose, a table, a comparison, a slide outline, or a chart, whichever fits the question.
5. **Offer to file it.** If the answer would be useful again, offer to save it as a question
   page, embedding the table or outline, or linking a chart saved beside the page. On yes:
   copy `_templates/question.md` into the partition the question is about,
   use keyed footnotes into raw files, link it from at least one related page, add it to the
   partition index, and log a `query` entry.

## Question types

- **"What changed lately?"** Read the tail of `log.md` headers
  (`grep "^## \[" log.md | tail -30`), then the pages those entries name.
- **"Compare these sources."** Read their source pages, then their raw files for the points
  of difference. Organize by claim, not by source.
- **"Find contradictions."** Read the `Disagreements` sections of the relevant topic pages
  and the `Contradictions and tensions` sections of source pages. For a broad sweep, suggest
  a full lint instead.

## Failure modes

- **Reading everything.** Opening every page in a partition costs context and dilutes the
  answer. Route through the indexes; widen only when that fails.
- **Trusting a summary over its source.** Wiki pages are rewritten; raw files are not. When a
  page and its raw file disagree, the raw file is right, and the page needs a fix — report it.
