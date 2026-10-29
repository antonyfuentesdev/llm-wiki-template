---
type: workflow
partition: workflows
created: 2026-10-29
updated: 2026-10-29
sources: []
tags: [x, bookmarks, ingest, api, media, optional]
status: active
---

# Ingest X bookmarks (optional)

Pull saved X bookmarks into the wiki as complete units — post, thread, top replies, quoted
post, media, and external links — without re-fetching anything already captured.

**Optional.** Skip this page unless you have connected the X API. Nothing else in the wiki
depends on it.

## When to use this

The human asks to ingest X bookmarks, or to catch up on bookmarks saved since the last run.
Not for pasted posts: those go through [ingest-pasted-text](ingest-pasted-text.md).

## Success and failure

Success: one manifest entry per bookmark; deep bookmarks have a raw file and a source page;
shallow ones sit in per-partition digests; a repeat run on an unchanged library fetches the
list once and captures nothing.

Failure: posts silently truncated to 280 characters; a thread or linked article missing from
a capture whose substance lived there; duplicates in `raw/` because the manifest was skipped.

## Preconditions

- An X API integration that can act as the user (OAuth 2.0 user context). The bookmarks
  endpoint does not accept app-only tokens. Any client works: an MCP server, a CLI, or plain
  HTTP. Keep credentials outside the repo.
- `wiki/.bookmarks-manifest.json` exists. Create it as `{}` on the first run. Shape:
  `{"<post-id>": {"fetched": "YYYY-MM-DD", "partition": "<name>", "raw": "<repo-relative path>"}}`.
- Scratch downloads go to `tmp/`, never into `wiki/`.

## Rules for this workflow

- **Models understand; tools only move bytes.** A description, transcript, summary, or
  classification of media must come from a model that looked at it. Shell tools may fetch
  files or convert a format the agent can't open (for example, video to still frames). They
  never stand in for reading.
- **Check the manifest before every fetch.** The bookmarks endpoint has no `since_id` and
  never reveals when something was bookmarked, so the manifest is the only defense against
  duplicates.
- **Spend API calls sparingly.** Fetch the list in one paginated call, batch lookups by ID,
  and use CDN or web fetches for media and links.

## Steps

1. **Fetch the bookmark list**, paginating until no `next_token` remains. Request the long-form
   body (`note_tweet`), article fields, referenced posts, attachments with media, and author
   expansions. → verify: the count of returned posts matches `result_count` across pages.
2. **Diff against the manifest.** Anything present is done. → verify: on a repeat run, the
   work list is empty.
3. **Reconstruct each conversation.** If the bookmark is a reply, resolve its
   `conversation_id` to the root first. Pull the root author's posts in that conversation
   within a bounded window after the root (post IDs are time-ordered snowflakes, so a time
   window maps to an ID range). Split them into the linear self-reply thread and the author's
   answers to other people. → verify: the window wasn't saturated; if it returned a full
   page, paginate.
4. **Pull the replies the author answered**, batched by ID. Rank by like count and keep the
   top few per bookmark. → verify: returned plus errored equals requested.
5. **Resolve quoted posts and their media.** → verify: every quoted media key resolves.
6. **Media.** Download images at original size into `tmp/` and have a model describe each
   one, transcribing on-screen text verbatim (garbled text included, marked as garbled). For
   video, extract evenly spaced still frames from the smallest variant and have a model read
   them; frames can't carry speech, so record whether the frames captured the video fully,
   partly, or not at all. Delete the video files. → verify: no video files under `wiki/`.
7. **External links.** Collect URLs from both the short text and the long-form body. Fetch
   each with the escalation ladder in [ingest-url](ingest-url.md). → verify: each kept link
   has real body text; a near-empty fetch is reported and skipped.
8. **Route and classify.** Route by subject per the [registry](../partitions.md), never by
   platform. A bookmark is **deep** when what was actually captured has a substantial body:
   a long-form post, an attached article, a substantive linked page, or a demo fully captured
   in frames. Otherwise it's **shallow**. Prefer deep when another page already cites it.
9. **Write `raw/`, then the manifest.** Deep bookmarks get
   `YYYY-MM-DD-x-<handle>-<slug>.md`, dated by the post's creation date, with sections in
   this fixed order so anchors stay predictable: `Post`, `Thread`, `Quoted post`, `Article`,
   `Top replies`, `Media`, `Links`. Omit sections that are empty. Shallow bookmarks go into
   `YYYY-MM-DD-HHMM-x-posts.md` per partition with `source: bookmarks`. → verify: one new
   manifest entry per bookmark; the raw-integrity commands are empty.
10. **Integrate, index, log** as in [ingest-url](ingest-url.md) step 6 onward: one `ingest`
    entry per deep bookmark, one `feed` entry per digest batch. Then a scoped lint.

## Failure modes

- **Silent 280-character truncation.** The short `text` field is capped; long posts carry
  their real body in `note_tweet`. Always prefer it when present.
- **Links that only exist in the long-form body.** URL entities on the short text describe
  the truncated text only. Union both sets.
- **Recent search only covers about a week.** On an older conversation it returns a near-empty
  result that looks like "no replies". Use the author-timeline window from step 3 instead.
- **Relevancy sort is not engagement.** Rank replies by like count yourself.
- **Scene-change frame selection fails on screen recordings,** which have no cuts. Sample at
  even intervals.
- **Large images get downscaled when read,** losing small text. Crop the region and re-read
  it at native resolution rather than guessing.
- **A linked page reflects the fetch date, not the post date.** Star counts, versions, and
  prices may have changed since the post. Attribute fetched content to `fetched:`.
