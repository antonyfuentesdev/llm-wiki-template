---
type: workflow
partition: workflows
created: 2026-10-29
updated: 2026-10-29
sources: []
tags: [ingest, deep-source, inbox, web-clipper]
status: active
---

# Ingest the inbox

File everything the human dropped into `inbox/` as deep sources, then cascade each one into
the wiki, leaving the inbox empty except for files that couldn't be filed.

## When to use this

The human says "ingest the inbox", or asks to process files they saved there: Web Clipper
output, PDFs, notes, transcripts. Not this: a URL to fetch ([ingest-url](ingest-url.md)) or
text pasted into the chat ([ingest-pasted-text](ingest-pasted-text.md)).

## Success and failure

Success: each file sits in `wiki/<partition>/raw/YYYY-MM/` with acquisition frontmatter and
its original body unchanged, has a source page and a cascade, and is gone from `inbox/`.
Skipped files are still in `inbox/` and named in the report.

Failure: a reworded or "cleaned up" body in `raw/`; clipper frontmatter lost; a degraded clip
filed anyway; a duplicate of a source already captured.

## First move

Read [preferences.md](../../preferences.md) and the [registry](../partitions.md). List
`inbox/`, ignoring `.gitkeep`.

## Preconditions

- `inbox/` is not `raw/`. Moving and deleting files there is allowed; nothing in the wiki may
  link into it.
- Conversions happen in `tmp/`, as in [ingest-url](ingest-url.md).

## Steps

1. **Check for duplicates.** Search `wiki/*/raw/` for each file's URL (clippers record it in
   their frontmatter), title, and file name. On a hit, leave the file and ask whether it's a
   re-capture. → verify: every remaining file is new to the wiki.
2. **Check for degradation.** Paywall stub, consent page, empty or truncated body, mostly
   navigation: leave the file in `inbox/` and report it. → verify: only complete sources go on.
3. **Convert if needed.** Non-markdown files (PDF, HTML, docx) convert into `tmp/` as in
   ingest-url step 3; the original binary of a PDF goes beside the raw file. Markdown files
   need no conversion. → verify: headings and length match the original.
4. **Choose the partition and write the raw file** as in ingest-url steps 4–5, with
   `acquired_by: user` and `fetched:` set to today. Take `url`, `author`, and `published`
   from the clipper's frontmatter when present. Keep the body exactly as it was. If the file
   had its own frontmatter, move it whole into a fenced block at the top of the body:

   ````markdown
   ```yaml
   # original frontmatter
   title: Caching Patterns at Scale
   source: https://example.com/caching-patterns
   ```
   ````

   The only other body change allowed is pointing image links at images moved beside the
   raw file with its date-slug prefix (AGENTS.md §5.1). → verify: a diff of the original
   against the raw file shows only the new frontmatter, the fenced block, and image paths.
5. **Remove the file from `inbox/`.** → verify: `inbox/` holds only `.gitkeep` and the files
   you skipped.
6. **Continue at step 6 of ingest-url**: source page, cascade, indexes, log, report, scoped
   lint. One `ingest` log entry per file.

## Failure modes

- **Tidying the clip.** Clippers leave odd spacing, stray captions, and leftover buttons.
  Leave them; note real problems on the source page. If the clip is too broken to cite, it's
  degraded: skip it and ask for a better capture.
- **Deleting a skipped file.** A file you couldn't file stays in `inbox/` until the human
  decides what to do with it.
