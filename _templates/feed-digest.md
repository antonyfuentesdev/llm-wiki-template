---
title: <platform> posts — <YYYY-MM-DD> <HHMM>
type: post
platform: <x | linkedin | bluesky | mastodon | other>
fetched: <YYYY-MM-DD>
acquired_by: user | agent-search | api
post_count: <n>
high_signal: <n>
---

<!-- Save as wiki/<partition>/raw/<YYYY-MM>/<YYYY-MM-DD>-<HHMM>-<platform>-posts.md. Shallow
     bookmarks add `source: bookmarks` to the frontmatter above. This file is append-only:
     written once, never reopened; a later batch the same day gets its own file with a
     different HHMM. Delete every HTML comment in this template before saving — raw files
     can't be fixed afterwards. -->

# <platform> posts — <YYYY-MM-DD> <HHMM>

## post-<id>

- author: @<handle>
- platform: <platform>
- posted: <YYYY-MM-DDTHH:MM:SSZ | unknown>
- url: <permalink, or empty>
- signal: high

<Verbatim post text. Thread continuations stay in this block, in order.>

## post-<id>

- author: @<handle>
- platform: <platform>
- posted: <YYYY-MM-DDTHH:MM:SSZ | unknown>
- url: <permalink, or empty>
- signal: low

<Verbatim post text.>

<!-- FORMAT RULES (delete before saving)

These are load-bearing. Retrieval relies on plain text search rather than a separate index,
so consistency here is the difference between findable and lost.

- Key names and order are fixed: author, platform, posted, url, signal — each on its own
  line, each prefixed "- ", always in that order. This is what makes
  grep -r "signal: high" wiki/*/raw/ and grep -r -A6 "author: @someone" wiki/*/raw/ work.
- The "## post-<id>" header is the citation anchor. Use the platform's own post ID so it's
  stable and de-duplicable. With no ID, use local-<YYYYMMDDHHMM>-<n> (batch timestamp,
  position in this digest). Cite as
  [thread](raw/2026-08/2026-08-06-1430-x-posts.md#post-1738291043) with the footnote key
  x-post-1738291043.
- Body text is verbatim. No summarizing, no cleanup, no truncation. Threads stay whole in
  one block; splitting a thread across anchors makes it uncitable as a single claim.
- signal records the verdict from signal.md, so triage stays inspectable. When extraction
  feels wrong, tune signal.md rather than arguing with single posts.

WORKED EXAMPLE (delete before saving)

## post-1738291043

- author: @jane_doe
- platform: x
- posted: 2026-08-06T09:12:00Z
- url: https://x.com/jane_doe/status/1738291043
- signal: high

Everyone benchmarks cache hit rate. Almost nobody benchmarks what happens during
invalidation storms, which is where every system I've debugged actually fell over.

2/ The failure isn't the cache — it's the thundering herd hitting the origin the
moment a hot key expires. Stampede protection is the feature, not the cache.

## post-local-202608061430-2

- author: @some_account
- platform: x
- posted: unknown
- url:
- signal: low

Hot take: most engineers overthink caching.

The first would update a caching topic page, cited to #post-1738291043. The second was
pasted without a link, so it gets a local label instead of an invented ID. It asserts
nothing checkable and goes nowhere, but it stays in the digest: storage is free and
deletion isn't. -->
