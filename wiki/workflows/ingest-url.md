---
type: workflow
partition: workflows
created: 2026-10-29
updated: 2026-10-29
sources: []
tags: [ingest, deep-source, fetch, pdf]
status: active
---

# Ingest a URL or file

Turn a web page, PDF, or local file into a captured deep source and cascade what it says into
the wiki.

## When to use this

The human hands over one or more URLs or file paths and asks to ingest, save, or file them.
Also when asked to "find and ingest" something: search first, then run this for each pick.

Not this: pasted text ([ingest-pasted-text](ingest-pasted-text.md)), a batch of social posts
(also that page), files waiting in `inbox/` ([ingest-inbox](ingest-inbox.md)), or bookmarks
pulled from an API ([the X example](../../examples/x-bookmark-ingest.md)).

## Success and failure

Success: one raw file per source holding the full text, one source page per source, every
touched page updated and cited, indexes and log current, a report and scoped lint delivered,
nothing committed.

Failure: a raw file that holds a paywall stub, a cookie banner, a summary instead of the
text, or a link with no body. Those must never reach `raw/`, because they can't be fixed
there afterwards.

## First move

Read [preferences.md](../../preferences.md), the [registry](../partitions.md), and the
indexes of the partitions the sources probably belong to. Then check for duplicates: search
`wiki/*/raw/` for each URL (or file name and title). A hit means this source is already
captured — ask whether it's a re-capture before doing anything else.

## Preconditions

- Raw path: `wiki/<partition>/raw/YYYY-MM/YYYY-MM-DD-slug.md`, dated today (AGENTS.md §5.1).
- Downloads and conversions happen in `tmp/`, never directly in `raw/`.

## Steps

1. **Fetch the original into `tmp/`.** Escalate only on failure: a plain HTTP fetch, then
   your agent's web-fetch tool, then a real browser if your harness has one. For a local
   file, read it in place. → verify: the body is the actual content — it reads as the
   article from start to end, and it's longer than the page's navigation and footer.
2. **Stop on a degraded fetch.** Paywall, login wall, consent page, empty body, or obviously
   truncated text: skip this source, and in the report ask the human to paste the text or
   provide the file. → verify: nothing for this source was written under `raw/`.
3. **Convert to markdown with a tool, not by retyping.** Use whatever deterministic
   converter the environment has (pandoc, trafilatura or readability, markitdown), writing
   into `tmp/`. With none, retyping is allowed, but check completeness section by section.
   Keep headings, lists, code, tables, and figure captions in their original order. Remove
   site navigation, ads, and related-article lists. Add no commentary. Read the text first,
   then view the images separately.
   For a PDF, keep the original binary next to the markdown with the same date-slug. For
   images that carry content, save them with the date-slug prefix and describe each where it
   appears, inside a `> [!capture-note] Agent description of <image-file>` block (AGENTS.md
   §5.1). → verify: headings and length match the original.
4. **Choose the partition** the source is most about, per the registry. → verify: the
   registry's not-here line for that partition doesn't exclude it.
5. **Write the raw file:** move the checked conversion from `tmp/` to the raw path and add
   acquisition frontmatter. `unknown` for anything you can't find; `acquired_by: user` when
   handed the URL, `agent-search` when you found it. → verify: the frontmatter keys match
   AGENTS.md §5.1 exactly.
6. **Write the source page** from `_templates/source.md` at `<partition>/sources/<slug>.md`,
   where the slug is the raw file's minus its date. Cite into the raw file with the key
   `[^<slug>]`, pointing at heading anchors and quoting the raw file for numbers and
   contestable claims (AGENTS.md §7). List cited-but-unfollowed references under "Leads not
   followed". → verify: no HTML comments or `<placeholders>` remain.
   **If preferences.md says ingest is interactive,** stop here: give the human the key
   takeaways and the pages you plan to touch, and wait for their steer.
7. **Cascade.** Update every entity, concept, and topic page the source substantively
   touches. Create a page from its template only per AGENTS.md §12 (see Page sprawl below).
   Rewrite topic theses rather than appending. Record contradictions on both sides
   (AGENTS.md §7). Link across partitions where the subject warrants it. → verify: every
   page touched is listed under the source page's "What this changed in the wiki", and each
   has the raw file in `sources:`.
8. **Update indexes and log.** Partition index entries, the root index summary if the
   partition's focus shifted, `updated:` dates, one `ingest` log entry per source.
   → verify: every new page is in its index and has an inbound link from a non-index page.
9. **Report, then run a scoped lint** ([lint-pass](lint-pass.md)). Include the review
   commands from AGENTS.md §10. → verify: the report lists anything skipped, and why.

## Failure modes

- **Filing the summary instead of the text.** Some fetch tools return a model-written
  summary of the page. Check the output against the original; if you can't get the full
  text, treat it as a degraded fetch.
- **Fixing a raw file after the fact.** If you notice a capture problem after writing the
  raw file, don't edit it. Capture a corrected file and mark the old one superseded on the
  source page (AGENTS.md §5.1).
- **A thin cascade.** Writing the source page and stopping. The source page is the receipt;
  the updates to topic and entity pages are the actual ingest.
- **Page sprawl.** Creating a page for every name in the source. Create an entity or concept
  page when a source discusses it substantively (a section or more, or it is central to the
  source), or when a second source mentions it. A passing mention goes into an existing
  page's text.
- **Following leads.** A source's references are leads, not tasks. Note them; ingest nothing
  the human didn't ask for (AGENTS.md §5.4).
