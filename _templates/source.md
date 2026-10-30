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
     The file name is the raw file's slug with its date stripped. -->

# <Source title>

**Author:** <author> · **Published:** <date> · **Captured:** <date> ·
**Original:** <url> · **Raw:** [<slug>](../raw/<YYYY-MM>/<YYYY-MM-DD>-<slug>.md)

## Summary

<!-- Two or three paragraphs: what the source argues, what it's for, and what kind of source
     it is. Enough that reading this page substitutes for re-reading the original in most
     cases. -->

## Key takeaways

<!-- Claims worth remembering, each cited into the raw file with a heading anchor, and a short
     verbatim quote for numbers, definitions, and contestable claims (AGENTS.md §7). -->

- <Claim worth remembering.>[^<slug>]

## What this changed in the wiki

<!-- Pages created or updated because of this source. This is the audit trail: it answers
     "why does this page say that?" months later. -->

- [<Page name>](../<page>.md) — <what changed and why>.

## Contradictions and tensions

<!-- Where this source disagrees with something already in the wiki. Name both sides and cite
     both; don't resolve it silently. Keep _None._ when there are none. -->

_None._

## Leads not followed

<!-- Sources this one cites that look worth reading. Candidates only: nothing gets ingested
     without approval. Keep _None._ when there are none. -->

_None._

[^<slug>]: [<Source title>](../raw/<YYYY-MM>/<YYYY-MM-DD>-<slug>.md#<heading>) — "<short verbatim quote>"
