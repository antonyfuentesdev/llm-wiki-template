---
type: source
partition: <partition>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources: [wiki/<partition>/raw/<YYYY-MM>/<YYYY-MM-DD>-<slug>.md]
tags: []
status: active
---

<!-- This page lives in <partition>/sources/<slug>.md, one level below the partition root, so
     links out of it need ../ — ../raw/ for captured sources, ../<page>.md for sibling pages.
     Pages at the partition root use raw/ and <page>.md directly. The file name is the raw
     file's slug with its date stripped. Delete this comment. -->

# <Source title>

**Author:** <author> · **Published:** <date> · **Captured:** <date> ·
**Original:** <url> · **Raw:** [<slug>](../raw/<YYYY-MM>/<YYYY-MM-DD>-<slug>.md)

## Summary

Two or three paragraphs. What the source argues, what it's for, and what kind of source it is.
Enough that a future read of this page substitutes for re-reading the original in most cases.

## Key takeaways

- Claim worth remembering, with a citation into the raw file.[^<slug>]
- Another one.

## What this changed in the wiki

Pages created or updated because of this source. This is the audit trail — it answers "why
does this page say that?" months later.

- [Page name](../<page>.md) — what changed and why.

## Contradictions and tensions

Where this source disagrees with something already in the wiki. Name both sides and cite both;
don't resolve it silently.

_None._

## Leads not followed

Sources this one cites that look worth reading. Candidates only — nothing gets ingested
without approval.

_None._

[^<slug>]: [<Source title>](../raw/<YYYY-MM>/<YYYY-MM-DD>-<slug>.md)
