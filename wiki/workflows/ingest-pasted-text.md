---
type: workflow
partition: workflows
created: 2026-10-29
updated: 2026-10-29
sources: []
tags: [ingest, deep-source, feed, transcript, notes]
status: active
---

# Ingest pasted text

Capture text the human pastes into the chat — notes, a meeting transcript, a chat export, an
article body, or a pile of social posts — through the right pipeline.

## When to use this

The human pastes text and asks to ingest, save, or file it. The first decision is which
tier it belongs to:

| What was pasted | Tier | Raw file |
| --- | --- | --- |
| One long-form piece: an article, your own notes, a meeting transcript, a chat export, a book chapter | Deep (AGENTS.md §5.1) | `YYYY-MM-DD-slug.md` |
| Several short posts from X, LinkedIn, or similar | Feed (AGENTS.md §5.2) | `YYYY-MM-DD-HHMM-<platform>-posts.md`, one per partition |
| A single short post | Feed | a digest with one post |

If the paste mixes both — a long article plus some posts about it — split it and run both
paths. When unsure whether something is long-form, ask.

## Success and failure

Success: the text lands verbatim in `raw/`, nothing is lost or reworded, and the wiki pages
it touches are updated with citations.

Failure: tidied, summarized, or translated text in `raw/`; a digest with one file per post;
a source page for a digest; invented post IDs or timestamps.

## First move

Read [preferences.md](../../preferences.md) and the [registry](../partitions.md). Ask for
anything you need and can't infer — usually the date of a meeting, or where the text came
from — before writing the raw file, because you can't add it later.

## Steps — deep paste

1. **Write the raw file verbatim.** Markdown structure is fine (headings for speakers or
   sections); changing the words is not. Frontmatter per AGENTS.md §5.1 with
   `acquired_by: user`, `url:` empty unless the human named an origin, and `type: note`,
   `transcript`, or `chat`. Transcripts add `media:` naming the recording, if known.
   → verify: a diff of the paste against the raw body differs only in formatting.
2. **Continue at step 6 of [ingest-url](ingest-url.md)** — source page, cascade, indexes,
   log, report, scoped lint.

Meeting transcripts usually file under `projects`. Update the project's topic page with the
decisions and open items, and the entity pages of the people involved. Cite each decision to
the transcript.

## Steps — feed batch

1. **Split the paste into posts.** Keep each thread whole in one block. Pull IDs from post
   URLs; with no URL, use `local-<YYYYMMDDHHMM>-<n>` (AGENTS.md §5.2). → verify: the post
   count matches what the human pasted.
2. **Score each post** against AGENTS.md §6 and record `signal: high` or `low`. When unsure,
   `low`. → verify: every post has a verdict.
3. **Group by subject, then write one digest per partition** (and per platform) from
   `_templates/feed-digest.md`, with `post_count` and `high_signal` filled in. Remove the
   template's guidance sections. → verify: posts are verbatim, and keys appear in the fixed
   order.
4. **Extract the high-signal posts.** No source page. Update the topic and entity pages each
   post is relevant to, citing the anchor with the key `<platform>-post-<id>`.
   → verify: each high-signal post is cited at least once, or the report says why not.
5. **Update the partition index's feed digest line for the month, the root index if page
   counts changed, and log one `feed` entry for the whole batch.**
6. **Report** posts captured, high vs low, pages updated. **Run a scoped lint.**

## Failure modes

- **Cleaning up the paste.** Fixing typos or transcript errors in `raw/` destroys evidence.
  Note errors on the source page instead ("the transcript renders the product name as …").
- **Speaker names.** Transcripts often mangle names. Don't create entity pages from a garbled
  name; ask the human who it was.
- **Over-extracting a feed.** If most of a batch scores high, the rubric is too loose. Say so
  in the report and suggest a change to AGENTS.md §6 rather than extracting everything.
