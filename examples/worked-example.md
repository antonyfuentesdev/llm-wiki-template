# Worked example: one ingest, file by file

**Fictional.** The article, its author, the site, and every number below are invented. This
walkthrough shows what a single deep-source ingest produces under [AGENTS.md](../AGENTS.md),
so you know what to expect, and what to copy, before your first real one.

The setup: the `general` partition already holds one source, *Cache Invalidation Notes*
(captured 2026-07-20), and a `caching` topic page built from it. The human then says:

```text
Ingest this: https://example.com/caching-patterns
```

## 1. The raw file

Converted into `tmp/`, checked against the original, then moved to
`wiki/general/raw/2026-08/2026-08-06-caching-patterns.md`. It is never edited again. The body
is the article's own text; the only agent-written part is the marked image description.

```markdown
---
title: Caching Patterns at Scale
url: https://example.com/caching-patterns
author: Jane Doe
published: 2026-07-14
fetched: 2026-08-06
type: article
acquired_by: user
---

# Caching Patterns at Scale

## Write-through

With write-through caching, the application writes to the cache and the database in the same
request. Every write pays for the read that follows: writes get slower, and reads never see
stale data.

## Write-behind

Write-behind acknowledges the write once the cache has it and flushes to the database later.
Writes are fast, but a cache node that dies before flushing loses data.

## Stampedes

When a hot key expires, hundreds of requests miss at the same moment and all of them go to
the database. Request coalescing, where one request refills the key while the others wait,
cut origin load during expiry by 80 percent in our fleet.

![p99 latency by strategy](2026-08-06-caching-patterns-fig1.png)

> [!capture-note] Agent description of 2026-08-06-caching-patterns-fig1.png
> Bar chart titled "p99 read latency". Three bars: no cache 210 ms, write-through 18 ms,
> write-behind 15 ms. No error bars.
```

The image sits beside it as `2026-08-06-caching-patterns-fig1.png`.

## 2. The source page

`wiki/general/sources/caching-patterns.md`. The slug is the raw file's, minus its date. It
cites both raw files, so `sources:` lists both.

```markdown
---
type: source
partition: general
created: 2026-08-06
updated: 2026-08-06
sources: [wiki/general/raw/2026-08/2026-08-06-caching-patterns.md, wiki/general/raw/2026-07/2026-07-20-cache-invalidation-notes.md]
tags: [caching, distributed-systems]
status: active
---

# Caching Patterns at Scale

**Author:** Jane Doe · **Published:** 2026-07-14 · **Captured:** 2026-08-06 ·
**Original:** https://example.com/caching-patterns · **Raw:** [caching-patterns](../raw/2026-08/2026-08-06-caching-patterns.md)

## Summary

A practitioner's article comparing write-through and write-behind caching, then arguing that
the real failure in production caches is the stampede when a hot key expires, not the hit
rate. It reports one fleet's numbers rather than a benchmark.

## Key takeaways

- Write-through makes writes slower in exchange for reads that are never stale.[^caching-patterns]
- Request coalescing cut origin load during hot-key expiry by 80 percent in the author's
  fleet.[^caching-patterns-stampedes]

## What this changed in the wiki

- [Caching](../caching.md) — thesis rewritten: TTL expiry needs stampede protection on hot
  keys; disagreement with Cache Invalidation Notes recorded.
- [Write-through caching](../write-through-caching.md) — created; the article gives it a
  full section.

## Contradictions and tensions

This article says expiring hot keys send a stampede to the database;[^caching-patterns-stampedes]
Cache Invalidation Notes says plain TTLs have caused no trouble.[^cache-invalidation-notes]
Recorded on [Caching](../caching.md#disagreements).

## Leads not followed

- A 2019 paper on lease-based invalidation, cited in the Stampedes section.

[^caching-patterns]: [Caching Patterns at Scale](../raw/2026-08/2026-08-06-caching-patterns.md#write-through) — "every write pays for the read that follows"
[^caching-patterns-stampedes]: [Caching Patterns at Scale](../raw/2026-08/2026-08-06-caching-patterns.md#stampedes) — "cut origin load during expiry by 80 percent"
[^cache-invalidation-notes]: [Cache Invalidation Notes](../raw/2026-07/2026-07-20-cache-invalidation-notes.md#ttls) — "plain TTLs have been fine for us"
```

## 3. The topic page, rewritten

`wiki/general/caching.md`. Before this ingest, its thesis was one sentence:

```markdown
## Current thesis

TTL-based expiry is enough for most read-heavy services.[^cache-invalidation-notes]
```

The new source qualifies that, so the thesis is rewritten rather than appended to, and the
older claim moves to `Disagreements` with its citation intact:

```markdown
---
type: topic
partition: general
created: 2026-07-20
updated: 2026-08-06
sources: [wiki/general/raw/2026-07/2026-07-20-cache-invalidation-notes.md, wiki/general/raw/2026-08/2026-08-06-caching-patterns.md]
tags: [caching, distributed-systems]
status: active
---

# Caching

## Current thesis

TTL expiry works until a key gets hot. When a hot key expires, the misses arrive together and
hit the database at once, so stampede protection matters more than hit rate.[^caching-patterns-stampedes]
The write strategy is a separate tradeoff: [write-through](write-through-caching.md) buys
fresh reads with slower writes.[^caching-patterns]

## What the sources say

One fleet reports that request coalescing cut origin load during expiry by 80
percent.[^caching-patterns-stampedes] No source yet measures stampedes directly.

## Disagreements

- **Are plain TTLs safe?** Cache Invalidation Notes: "plain TTLs have been fine for
  us."[^cache-invalidation-notes] Caching Patterns at Scale: hot-key expiry sends a stampede
  to the database.[^caching-patterns-stampedes]

> [!inference] Agent-inferred, not from a source
> The two may not conflict: the notes describe a low-traffic service, where few keys get hot
> enough to stampede.

## Open questions

- At what request rate does a key become hot enough to stampede?

## Related

- [Write-through caching](write-through-caching.md) — one of the write strategies compared.

## Sources

- [Cache Invalidation Notes](raw/2026-07/2026-07-20-cache-invalidation-notes.md) · [summary](sources/cache-invalidation-notes.md)
- [Caching Patterns at Scale](raw/2026-08/2026-08-06-caching-patterns.md) · [summary](sources/caching-patterns.md)

[^cache-invalidation-notes]: [Cache Invalidation Notes](raw/2026-07/2026-07-20-cache-invalidation-notes.md#ttls) — "plain TTLs have been fine for us"
[^caching-patterns]: [Caching Patterns at Scale](raw/2026-08/2026-08-06-caching-patterns.md#write-through) — "every write pays for the read that follows"
[^caching-patterns-stampedes]: [Caching Patterns at Scale](raw/2026-08/2026-08-06-caching-patterns.md#stampedes) — "cut origin load during expiry by 80 percent"
```

Two footnotes cite the same raw file at different headings, so the second key carries a
suffix. The new concept page, `write-through-caching.md`, is built from
`_templates/concept.md` the same way.

## 4. The index lines

In `wiki/general/index.md`, one line per page:

```markdown
## Topics and concepts

- [Caching](caching.md) — when TTL expiry is enough, and when hot keys need stampede protection.
- [Write-through caching](write-through-caching.md) — write to cache and store together; slower writes, fresh reads.

## Sources

- [Cache Invalidation Notes](sources/cache-invalidation-notes.md) — 2026-07-20 — notes from running TTL-only caching on a small service.
- [Caching Patterns at Scale](sources/caching-patterns.md) — 2026-08-06 — Jane Doe on write strategies and hot-key stampedes.
```

The partition's focus didn't shift, so its line in the root `index.md` stays as it was.

## 5. The log entries

Appended to the bottom of `log.md`, one for the ingest and one for the scoped lint that
followed it:

```markdown
## [2026-08-06] ingest | general | Caching Patterns at Scale
Created write-through-caching; rewrote the caching thesis; 1 contradiction recorded.

## [2026-08-06] lint | scoped | general — 0 findings
```

## 6. The report

What the agent tells the human at the end, followed by the review commands from AGENTS.md
§10. Nothing is committed.

```text
Ingested 1 source into general: Caching Patterns at Scale (Jane Doe, 2026-07-14).

Pages created: sources/caching-patterns, write-through-caching.
Pages updated: caching (thesis rewritten), general index.
Contradictions: 1. This article says hot-key expiry causes stampedes; Cache Invalidation
Notes says plain TTLs have been fine. Both are on caching.md under Disagreements, with my
guess at why they differ marked as inference.
Skipped: nothing. Lead not followed: a 2019 paper on lease-based invalidation.
Feed posts: none in this batch.
Scoped lint: check-wiki.py found nothing; no judgment findings.
```
