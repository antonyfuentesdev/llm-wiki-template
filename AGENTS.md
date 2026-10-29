# AGENTS.md — how to maintain this wiki

A personal knowledge base. The human curates sources and asks questions. You read,
summarize, cross-reference, file, and keep the bookkeeping straight.

This file is the operative spec. It works with any coding agent that can read and write
files (Cursor, Claude Code, Codex, and others). Where it says "your fetch tool" or "your
search tool", use whatever your harness provides. The reasoning behind these rules is in
[PLAN.md](PLAN.md); this file wins on any conflict.

---

## 0. Start of every session

Use the lightest preflight that still protects the work.

- **Always** read [preferences.md](preferences.md). It holds the human's standing
  instructions and overrides defaults in this file where they conflict.
- **Ingest:** also read [wiki/partitions.md](wiki/partitions.md) and the index of every
  partition you might file into.
- **Query:** read [index.md](index.md), then the relevant partition indexes (§8).
- **Lint or restructure:** read [lint.md](lint.md) and the registry.
- **Tiny tasks** (fix a typo, answer a question about this file): preferences only.

Reuse what you have already read in this session unless it may have changed.

## 1. The inviolable rule

> **Any directory named `raw/` is append-only. Add files. Never edit them. Never delete
> them.** Everything else under `wiki/` is derived and may be rewritten freely.

You write to both layers, so this is yours to enforce: a citation means nothing if the cited
file no longer says what it said when the claim was made.

A source that is wrong, truncated, or superseded is **not** overwritten. Capture a new dated
file and mark the old one superseded on its source page (§5.1).

## 2. Layout

```
AGENTS.md            this file — the spec
CLAUDE.md            pointer to this file for agents that read CLAUDE.md
preferences.md       the human's standing instructions to you
index.md             root catalog — read first when answering a question
log.md               append-only chronological record
lint.md              health-check checklist
PLAN.md              design decisions and their reasoning
_templates/          copy these rather than improvising structure
tmp/                 scratch space; contents are git-ignored
wiki/
  partitions.md      partition registry — read before filing anything
  <partition>/
    index.md         partition catalog
    raw/YYYY-MM/     captured sources, APPEND-ONLY
    sources/         one summary page per deep source
    *.md             entity, concept, topic, question, workflow pages
```

The scaffold ships three partitions: `general`, `projects`, and `workflows`. The last holds
the procedures for operating this wiki ([wiki/workflows/index.md](wiki/workflows/index.md)).

## 3. Partitions

Read [wiki/partitions.md](wiki/partitions.md) before filing. Each partition declares what it
holds and what belongs elsewhere. The registry is the only copy of partition scopes; don't
repeat them in other files.

**Partitions are subjects.** Format, platform, source, and recency are metadata, not folders.
If a partition name would describe *how something arrived* rather than *what it is about*,
it belongs in frontmatter. Social posts therefore file under their subject with
`platform: x` recorded, not into a `social` partition.

**One home per source.** When a source spans several partitions, the partition it is *most*
about owns the raw file and the source page. Pages in other partitions link across to it.

### Creating, splitting, merging, renaming

Two gates, both required:

1. **Mechanical trigger.** A page is a *misfit* when it links to few or no other pages in its
   own partition. A set of misfits that link to *each other* is a *cluster*. At **8 pages**, a
   cluster becomes a candidate partition. Clusters are always intra-partition, so detecting
   them needs only one partition's link graph.
2. **Written topical case.** What it's about, why its host no longer fits, what would belong
   elsewhere. If you can't state that in a few sentences, drop the proposal — the cluster is
   an artifact of ingest order.

**Proposals surface only during lint, never mid-ingest.**

**Never restructure without approval.** The human may also ask for a partition directly;
that request is the approval, but you still write the topical case for the registry entry.
Once approved: register it in `partitions.md`, create `wiki/<name>/` with `index.md` (from
`_templates/partition-index.md`) plus `raw/` and `sources/` (each with a `.gitkeep`), move
the clustered pages *and their raw files* with `git mv`, update every inbound link, add the
partition to the root index, append a `restructure` log entry.

Moving a raw file with `git mv` is the one permitted change to `raw/`, and only during an
approved restructure. Its content must not change.

## 4. Pages

### Frontmatter

Field names are exact.

```yaml
---
type: source | entity | concept | topic | question | workflow | index
partition: general
created: 2026-08-06
updated: 2026-08-06
sources: [wiki/general/raw/2026-08/2026-08-06-some-article.md]
tags: [caching, distributed-systems]
status: stub | active | stable
---
```

- `sources:` lists every raw file the page cites, repo-root-relative. Empty `[]` when none.
- `updated:` changes on every edit. `created:` never changes.
- `status:` — `stub` is a thin placeholder, `active` is still growing, `stable` is settled.
- Tags are lowercase and hyphenated. Reuse existing tags before inventing new ones.

Optional where relevant: `aliases` (entity, concept), `entity_kind` (entity: `person |
company | tool | product | place | other`), `asked` (question: the date asked).

Index pages carry only `type: index`, `partition` (or `scope: root | registry` for
[index.md](index.md) and [wiki/partitions.md](wiki/partitions.md)), `created`, and `updated`.
Raw files carry acquisition frontmatter instead (§5).

### Page types

| Type | Holds | Lives in |
| --- | --- | --- |
| `source` | One per deep source: summary, takeaways, what it changed | `<partition>/sources/` |
| `entity` | A person, company, tool, product, place | partition root |
| `concept` | An idea, pattern, theory, technique | partition root |
| `topic` | Evolving synthesis across many sources; holds the thesis | partition root |
| `question` | A filed answer worth keeping | partition root |
| `workflow` | A reusable procedure | `wiki/workflows/` |
| `index` | A partition catalog | `<partition>/index.md` |

Topic pages are where synthesis lives. When a batch touches one, rewrite its thesis rather
than appending to it.

Copy the matching file from [_templates/](_templates/). **Templates contain explanatory prose
describing what each section is for — delete it as you fill the page in.** It is guidance
for you, not content for the wiki. Drop sections that would stay empty, except `Sources` and
the `_None._` markers on source pages, which show the question was considered.

### Names

File names are lowercase, hyphenated, ASCII, and short: `write-through-caching.md`, not
`Write Through Caching (2026).md`. A slug is the file name without `.md`. Name entity pages
after the entity, concept pages after the idea, questions after their core noun phrase
(`why-caches-stampede.md`). Search the partition before creating a page; if a page already
covers the subject under another name, update it and add an alias.

### Links

Plain relative markdown: `[Caching](../general/caching.md)`. Never `[[wikilinks]]` — they
only render in Obsidian.

Look actively for cross-partition links. You read the local partition first, so those are
the connections you will systematically miss.

**Mind the depth.** Source pages sit one level below the partition root, so their paths
differ from every other page type:

| From | To a raw file | To a sibling page |
| --- | --- | --- |
| `<partition>/<page>.md` | `raw/2026-08/file.md` | `other-page.md` |
| `<partition>/sources/<slug>.md` | `../raw/2026-08/file.md` | `../other-page.md` |

The `sources:` frontmatter field is the exception: not a markdown link, always
repo-root-relative (`wiki/general/raw/2026-08/file.md`).

**Every page needs an inbound link.** A listing in its partition index counts.

## 5. Sources — three tiers

Deep sources, feed posts, and curated bookmarks go through different pipelines. **Never run a
feed batch through the deep pipeline** — at 10–30 posts a day that produces thousands of
summary pages a year for material that doesn't warrant them. Bookmarks sit between the two:
the human filtered them by saving them, so they earn per-item treatment when they carry the
body to justify it.

### 5.1 Deep sources

Articles, papers, PDFs, transcripts, book chapters, your own notes, chat exports.

Store the **full converted text**, never just a link — a URL that rots takes every citation
with it. Convert to markdown, keep the original's headings and order, and add no commentary
of your own. Commentary belongs on the source page.

**Path:** `wiki/<partition>/raw/YYYY-MM/YYYY-MM-DD-slug.md`, dated by the capture date in the
human's local time. The slug comes from the title, about three to six words. If the name is
taken, append `-2`.

**Before fetching,** check the source isn't already captured: search `wiki/*/raw/` for its
URL or title. If it is, ask whether this is a re-capture rather than filing a duplicate.

**Acquisition frontmatter**, written once and never touched again:

```yaml
---
title: Caching Patterns at Scale
url: https://example.com/caching-patterns
author: Jane Doe
published: 2026-07-14
fetched: 2026-08-06
type: article | pdf | transcript | note | chat | image
acquired_by: user | agent-search | agent-followed-link
partition: general
---
```

Use `unknown` for an author or publish date you can't find; never guess. Leave `url:` empty
for pasted text with no origin. Strip tracking and auth parameters from captured URLs.

PDFs keep the original binary beside an extracted markdown file with the same date-slug
(`2026-08-06-slug.pdf` and `2026-08-06-slug.md`). Transcripts add an optional `media:` field
naming the recording they came from. Images sit in the same month folder as the raw file
referencing them, sharing its date-slug prefix (`2026-08-06-slug-fig1.png`). There is no
shared assets tree. If an image carries content (a chart, a screenshot of text), write a
description of it into the raw file at capture time, since the file can't be edited later.

**If a fetch fails or returns something suspect** — paywall stub, empty body, consent
interstitial, a page that is mostly navigation — report it and skip rather than filing a
degraded source. Ask the human to paste the text instead.

**Superseding.** Each source has one source page. When a source is re-captured, the new raw
file goes in today's month folder. The existing source page is updated to cite the new file,
lists both raw files in `sources:`, and states under its header which file is superseded and
why.

### 5.2 Feed sources

Short posts from X, LinkedIn, Bluesky, Mastodon, and similar. High volume, low average
signal.

**Acquisition:** the human usually supplies these as pasted text, since authenticated
timelines can't be fetched. Handed a bare post URL, try to fetch it; if that fails, ask for
the text rather than filing a stub. Never fabricate post content or IDs.

**One digest per batch per partition**, never one file per post:
`wiki/<partition>/raw/YYYY-MM/YYYY-MM-DD-HHMM-<platform>-posts.md`. A batch with posts from
several platforms writes one digest per platform per partition.

Group the batch by subject as you capture it, so posts land in the partition they're
*about*. Each batch writes a new file and never reopens an old one.

Digest frontmatter:

```yaml
---
title: x posts — 2026-08-06 1430
type: post
platform: x
partition: general
fetched: 2026-08-06
acquired_by: user
post_count: 24
high_signal: 3
---
```

**Digests never get source pages.** High-signal posts update the topic and entity pages
they're relevant to, cited by anchor. Low-signal posts stay in the digest, unextracted.

**Post format is fixed.** Key names, order, and the `## post-<id>` anchor are load-bearing —
retrieval uses plain text search, not a separate index. See
[_templates/feed-digest.md](_templates/feed-digest.md).

```markdown
## post-1738291043

- author: @jane_doe
- platform: x
- posted: 2026-08-06T09:12:00Z
- url: https://x.com/jane_doe/status/1738291043
- signal: high

Verbatim text, threads kept whole in one block.
```

`<id>` is the platform's own post ID, taken from the URL. When a pasted post has no URL or
ID, use `local-<YYYYMMDDHHMM>-<n>` (batch timestamp, position in the digest), leave `url:`
empty, and write `posted: unknown` if the time isn't known. That is a local label, never a
claimed platform ID.

Cite as `[thread](raw/2026-08/2026-08-06-1430-x-posts.md#post-1738291043)`.

### 5.3 Curated bookmarks (optional)

Only relevant if you connect a bookmarks source, such as the X API. The procedure is
[wiki/workflows/x-bookmark-ingest.md](wiki/workflows/x-bookmark-ingest.md).

A bookmark is a **deep bookmark** when it carries body worth citing on its own: a long-form
post, an attached article, a video with real content, or an external link that fetched
cleanly. It gets its own raw file and a source page, exactly like §5.1, at
`wiki/<partition>/raw/YYYY-MM/YYYY-MM-DD-<platform>-<handle>-<slug>.md`, with both the month
folder and the date taken from the post's creation date, not the fetch date. Everything else is a **shallow bookmark** and goes into a
per-partition digest under the §5.2 format, with `source: bookmarks` added to its
frontmatter.

A bookmark is never just the post that was saved. Capture the whole unit: the author's
self-reply thread, the top replies, the quoted post, attached media, and the text of
external links.

**Every capture is manifest-gated.** `wiki/.bookmarks-manifest.json` maps post ID to the raw
file it landed in. Never re-fetch a post already in the manifest; re-runs would otherwise
duplicate into append-only `raw/`.

### 5.4 Sourcing autonomy

The human directs most sourcing. Within that:

| Situation | You may |
| --- | --- |
| Handed a URL, file, or paste | Ingest directly |
| Asked to "find and ingest X" | Search, select, ingest — report what you chose *and what you passed over* |
| Lint identifies a gap | Propose candidates with one-line justifications; ingest only what's approved |
| A source you're reading cites something interesting | Note it under "Leads not followed" — **do not ingest it** |

Record `acquired_by` on every capture.

## 6. Signal criteria

**Owned by the human. Edit as your judgment sharpens.**

Applied to every feed post; the verdict goes in the `signal:` field so triage stays
auditable.

### High signal — extract into pages

- Makes a specific, checkable claim: a benchmark, a failure mode, a mechanism, a number.
- Reports firsthand experience with enough detail to be actionable.
- Contradicts or meaningfully qualifies something already in the wiki.
- Introduces a technique, tool, or concept the wiki doesn't cover.
- A thread that develops an argument, rather than a single assertion.

### Low signal — capture only

- Opinion with no supporting mechanism or evidence.
- Restates what the wiki already covers.
- Engagement bait, announcements, promotion, memes, hot takes.
- Depends on an image, video, or link that wasn't captured.
- Would produce a page that just paraphrases the post.

### When uncertain

Mark it `low` and move on. The digest keeps everything either way.

## 7. Provenance

**Every non-obvious claim is cited**, to the raw file rather than the source page — source
pages get rewritten, raw files don't.

**Footnote labels are keyed, never numbered.** The key is the cited raw file's slug with its
date stripped, which is also the source page's slug:

```markdown
Write-through caching trades write latency for read consistency.[^caching-patterns]

[^caching-patterns]: [Caching Patterns at Scale](raw/2026-08/2026-08-06-caching-patterns.md)
```

Numbering is positional, and pages here are *rewritten* rather than appended to (§4).
Reorder or drop one source during a rewrite and every later `[^2]` silently re-points to a
different raw file — the citation still renders, so nothing looks wrong. A key breaks loudly
instead, and it names its source at the point of use.

- Cite the same file twice on a page and reuse the key.
- Citing a section anchor inside a file, suffix the key with the anchor:
  `[^caching-patterns-thread]`.
- Feed posts use `<platform>-post-<id>`:
  `[^x-post-1738291043]: [thread](raw/2026-08/2026-08-06-1430-x-posts.md#post-1738291043)`.

**Your own knowledge is allowed, and always marked.** Training data, web search, and your
own inference are permitted, visually distinct from sourced claims:

```markdown
> [!inference] Agent-inferred, not from a source
> This likely generalizes to read-heavy workloads, though no source in the wiki
> addresses that case directly.
```

**Contradictions are surfaced, not resolved.** When a new source disagrees with an existing
page, record both claims with both citations — on the topic page's `Disagreements` section
and the new source page's `Contradictions and tensions`. Never silently overwrite the older
one, and never manufacture a consensus.

## 8. Operations

Step-by-step procedures, with checks and failure modes, live in
[wiki/workflows/](wiki/workflows/index.md). This section is the contract they implement.

### Ingest

1. **Acquire.** Fetch, convert, choose the partition, write to
   `wiki/<partition>/raw/YYYY-MM/` with acquisition frontmatter (§5.1). Feed batches instead
   group by subject into per-partition digests (§5.2), scoring each post against §6. Nothing
   under `raw/` is touched again after this step.
2. **Load state.** Read `wiki/partitions.md` and the indexes of every partition involved.
3. **Integrate.**
   - *Deep source:* write a source page at `<partition>/sources/<slug>.md`, then update every
     entity, concept, and topic page it touches, creating those that don't exist. One source
     commonly touches ten or more pages; that cascade is the work, not the source page.
     Record each touched page under the source page's "What this changed in the wiki".
   - *High-signal post:* no source page. Update the relevant topic and entity pages directly,
     cited to the post anchor.
   - *Low-signal post:* nothing.
4. **Flag contradictions** (§7).
5. **Update indexes** — every touched partition index (one line per page: link, then a
   one-line summary), the page counts in the root [index.md](index.md), and `updated:` on
   each.
6. **Log** one entry per deep source, one per feed *batch* (never per post).
7. **Report:** sources acquired, posts triaged high vs low, pages created, pages updated,
   contradictions found, acquisitions skipped and why.
8. **Run a scoped lint** (below) and append its findings to the report.

**Don't commit.** Leave changes in the working tree so the human can review them with §10,
unless the human asks you to commit.

### Query

1. Read `index.md`, then the relevant partition indexes. Choose a bounded set of candidate
   pages from those before reading page bodies.
2. Read those pages and follow their footnotes into `raw/` for any claim the answer rests on.
3. Only if routing finds nothing, search the whole wiki (`wiki/`, including `raw/`).
4. Answer with citations to raw files. Mark your own reasoning as inference (§7). If the
   wiki doesn't cover the question, say so plainly before adding anything from outside it.
5. If the answer has lasting value, offer to file it as a `question` page. When filed, add it
   to the partition index and log a `query` entry.

### Lint

Checklist: [lint.md](lint.md). Two modes.

- **Scoped** — automatic after every batch. Pages this batch created or modified, plus pages
  linking to or from them, plus a cluster check across the partitions the batch touched.
- **Full** — on request. Everything. Catches what scoped cannot: contradictions between
  untouched pages in different partitions, months-old orphans, slow drift. Suggest one when
  the last full pass in `log.md` is a few weeks old.

**Report and propose. Never apply fixes without approval.** This is the only operation
permitted to propose restructuring. Log one `lint` entry per pass.

## 9. Logging

Append to the bottom of [log.md](log.md), always this header shape, with an optional body of
one to three lines:

```
## [YYYY-MM-DD] ingest | general | Caching Patterns at Scale
## [YYYY-MM-DD] feed | x | 24 posts → 3 high-signal, 6 pages updated
## [YYYY-MM-DD] query | general | How do the three papers disagree on scaling?
## [YYYY-MM-DD] lint | scoped | general, projects — 2 findings
## [YYYY-MM-DD] restructure | split general/ into general/ and ml/
## [YYYY-MM-DD] schema | Added a signal criterion for benchmark claims
```

Operations: `init`, `ingest`, `feed`, `query`, `lint`, `restructure`, `schema`. Use `schema`
for changes to this file, `preferences.md`, `lint.md`, or `_templates/`.

## 10. Review commands

Give the human these after an ingest. `git add -N .` is required first — without it
`git diff` ignores new files, which is most of what an ingest produces.

```bash
git add -N .

# How did the synthesis change? (excludes captured sources)
git diff -- 'wiki/' ':(exclude)wiki/*/raw/*'

# What source material came in?
git diff --stat -- 'wiki/*/raw/*'

# Append-only integrity, uncommitted — must be empty
git diff --name-only --diff-filter=MDR HEAD -- 'wiki/*/raw/*'

# Append-only integrity, history — must be empty
git log --diff-filter=MDR -- 'wiki/*/raw/*'
```

Two things fail silently if changed: the trailing `/*` (a directory-style pathspec like
`wiki/*/raw/` matches nothing and exits 0), and `MDR` (plain `M` misses deletions and
renames, which are the unrecoverable failures). An approved restructure that moved raw files
shows up as renames in the history check; confirm each one against its `restructure` log
entry.

## 11. Preferences

[preferences.md](preferences.md) holds the human's durable instructions: tone, language,
what to emphasize, what to skip. When the human states a rule meant to last ("always…",
"from now on…", "never…"), record it there in the same turn without being asked, and log a
`schema` entry. If you can't tell whether an instruction is durable, ask. When a new
preference contradicts an old one, replace the old one; the log keeps the history.

Changes to *this* file — partition rules, signal criteria, page conventions — are made only
when the human asks.

## 12. Standing habits

- Read the partition registry and relevant indexes before writing. Filing blind is how
  duplicate pages and orphans appear.
- Prefer updating an existing page to creating a neighbor for it.
- Read only what you need from large files. For `log.md`, take the tail of its headers
  (`grep "^## \[" log.md | tail -20`). For a long raw file, search for the passage rather than
  loading all of it.
- Use `tmp/` for scratch work — downloads, conversions, intermediate files. Nothing in it is
  committed, and nothing in the wiki may link into it.
- Never write credentials, tokens, or API keys into any file in this repo.
- When running parallel subagents, give each one the constraints it needs in its prompt
  rather than a reading list, and keep writes to indexes and `log.md` in the parent so they
  don't collide.
