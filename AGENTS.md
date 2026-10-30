# AGENTS.md — how to maintain this wiki

A personal knowledge base. The human curates sources and asks questions. You read,
summarize, cross-reference, file, and keep the bookkeeping straight.

This file is the contract. It works with any coding agent that can read and write files;
use whatever fetch and search tools your harness provides. Step-by-step procedures live in
[wiki/workflows/](wiki/workflows/index.md). Rationale lives in [PLAN.md](PLAN.md). On any
conflict, this file wins, except that [preferences.md](preferences.md) overrides its
defaults.

---

## 0. Start of every session

- **Always** read [preferences.md](preferences.md).
- **Ingest:** also read [wiki/partitions.md](wiki/partitions.md) and the index of every
  partition you might file into.
- **Query:** read [index.md](index.md), then the relevant partition indexes (§8).
- **Lint or restructure:** read [lint.md](lint.md) and the registry.
- **Tiny tasks** (typo, a question about this file): preferences only.

Reuse what you've already read this session unless it may have changed.

## 1. The inviolable rule

> **Any directory named `raw/` is append-only. Add files. Never edit them. Never delete
> them.** Everything else under `wiki/` is derived and may be rewritten freely.

A citation means nothing if the cited file no longer says what it said when the claim was
made. A source that is wrong, truncated, or superseded is **not** overwritten: capture a new
dated file and mark the old one superseded on its source page (§5.1).

## 2. Layout

```
AGENTS.md  CLAUDE.md  PLAN.md   the spec, a pointer to it, design rationale
preferences.md                  the human's standing instructions to you
index.md                        root catalog: read first when answering a question
log.md                          append-only chronological record
lint.md                         health-check checklist
_templates/                     copy these rather than improvising structure
tmp/                            scratch space, git-ignored
wiki/
  partitions.md                 partition registry: read before filing anything
  <partition>/
    index.md                    partition catalog
    raw/YYYY-MM/                captured sources, APPEND-ONLY
    sources/                    one summary page per deep source
    *.md                        entity, concept, topic, question pages
```

The scaffold ships three partitions: `general`, `projects`, and `workflows` (procedures for
operating this wiki).

## 3. Partitions

The registry in [wiki/partitions.md](wiki/partitions.md) is the only copy of partition
scopes. Don't repeat them elsewhere.

**Partitions are subjects.** Format, platform, source, and recency are metadata. A name that
describes *how something arrived* rather than *what it is about* belongs in frontmatter:
social posts file under their subject with `platform: x`, not into a `social` partition.

**One home per source.** When a source spans partitions, the one it's *most* about owns the
raw file and source page. Other partitions link across to it.

### Creating, splitting, merging, renaming

Two gates, both required:

1. **Mechanical trigger.** A *misfit* is a page that links to few or no other pages in its
   own partition. Misfits that link to each other form a *cluster*. At **8 pages** a cluster
   becomes a candidate partition. Clusters are intra-partition, so one partition's link
   graph is enough to find them.
2. **Written topical case.** What it's about, why its host no longer fits, what would belong
   elsewhere. If you can't say that in a few sentences, drop the proposal: the cluster is an
   artifact of ingest order.

**Proposals surface only during lint, never mid-ingest. Never restructure without
approval.** A direct request from the human counts as approval, but you still write the case
for the registry entry. Once approved: register it in `partitions.md`, create
`wiki/<name>/` from `_templates/partition-index.md` plus `raw/` and `sources/` (each with a
`.gitkeep`), move the clustered pages and their raw files with `git mv`, fix every inbound
link, update the root index, and log a `restructure` entry. A `git mv` of raw files during
an approved restructure is the only permitted change to `raw/`; content must not change.

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

- `sources:` lists every raw file the page cites, repo-root-relative (not a markdown link);
  `[]` when none. `updated:` changes on every edit; `created:` never does.
- `status:` `stub` is a placeholder, `active` is growing, `stable` is settled.
- Tags are lowercase and hyphenated. Reuse existing ones.
- Optional: `aliases` (entity, concept), `entity_kind` (entity: `person | company | tool |
  product | place | other`), `asked` (question: date).
- Index pages carry only `type: index`, `partition` (or `scope: root | registry` for
  [index.md](index.md) and [wiki/partitions.md](wiki/partitions.md)), `created`, `updated`.
  Raw files carry acquisition frontmatter instead (§5).

### Page types

| Type | Holds | Lives in |
| --- | --- | --- |
| `source` | One per deep source: summary, takeaways, what it changed | `<partition>/sources/` |
| `entity` | A person, company, tool, product, place | partition root |
| `concept` | An idea, pattern, theory, technique | partition root |
| `topic` | Evolving synthesis across sources; holds the thesis | partition root |
| `question` | A filed answer worth keeping | partition root |
| `workflow` | A reusable procedure | `wiki/workflows/` |
| `index` | A partition catalog | `<partition>/index.md` |

When a batch touches a topic page, rewrite its thesis rather than appending to it.

Copy the matching file from [_templates/](_templates/) and **delete its explanatory prose**;
it's guidance for you, not wiki content. Drop sections that would stay empty, except
`Sources` and the `_None._` markers on source pages.

### Names and links

- File names are lowercase, hyphenated, ASCII, short (`write-through-caching.md`). The slug
  is the name without `.md`. Name pages after the entity, idea, or core noun phrase. Search
  the partition first; if a page covers the subject under another name, update it and add an
  alias.
- Plain relative markdown links: `[Caching](../general/caching.md)`. Never `[[wikilinks]]`.
- Look for cross-partition links; reading the local partition first makes them the ones you
  miss.
- **Mind the depth.** Source pages sit one level down:

| From | To a raw file | To a sibling page |
| --- | --- | --- |
| `<partition>/<page>.md` | `raw/2026-08/file.md` | `other-page.md` |
| `<partition>/sources/<slug>.md` | `../raw/2026-08/file.md` | `../other-page.md` |

- **Every page needs an inbound link.** A partition index entry counts.

## 5. Sources — three tiers

Deep sources, feed posts, and bookmarks use different pipelines. **Never run a feed batch
through the deep pipeline**: at 10–30 posts a day it yields thousands of summary pages a
year for material that doesn't warrant them.

### 5.1 Deep sources

Articles, papers, PDFs, transcripts, book chapters, the human's own notes, chat exports.
Procedures: [ingest-url](wiki/workflows/ingest-url.md),
[ingest-pasted-text](wiki/workflows/ingest-pasted-text.md).

Store the **full converted text**, never just a link; a rotted URL takes every citation with
it. Keep the original's headings and order and add no commentary (that belongs on the source
page).

**Path:** `wiki/<partition>/raw/YYYY-MM/YYYY-MM-DD-slug.md`, dated by capture date in the
human's local time. Slug: three to six words from the title; append `-2` if taken. Before
fetching, search `wiki/*/raw/` for the URL or title; on a hit, ask whether it's a re-capture.

**Acquisition frontmatter**, written once, never touched again:

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

- Use `unknown` for an author or date you can't find; never guess. Leave `url:` empty for
  pasted text with no origin. Strip tracking and auth parameters from URLs.
- PDFs keep the original binary beside the extracted markdown, same date-slug. Transcripts
  may add `media:` naming the recording. Images share the raw file's date-slug prefix in the
  same month folder; there is no shared assets tree. Describe any image that carries content
  in the raw file at capture time, since it can't be edited later.
- **If a fetch fails or looks degraded** (paywall stub, empty body, consent page, mostly
  navigation), report it and skip. Ask the human to paste the text. Never file it.
- **Superseding.** One source page per source. On re-capture, the new raw file goes in
  today's month folder; the source page cites it, lists both raw files in `sources:`, and
  states which is superseded and why.

### 5.2 Feed sources

Short posts from X, LinkedIn, Bluesky, Mastodon, and similar. High volume, low average
signal. The human usually pastes them. Given a bare URL, try to fetch it; if that fails, ask
for the text. Never fabricate post content or IDs.

- **One digest per batch, per platform, per partition**, never one file per post:
  `wiki/<partition>/raw/YYYY-MM/YYYY-MM-DD-HHMM-<platform>-posts.md`. Group posts by subject
  as you capture. A digest is written once and never reopened.
- **Format is fixed** and load-bearing, since retrieval is plain text search: digest
  frontmatter, `## post-<id>` anchors, and the key order `author, platform, posted, url,
  signal`. Copy [_templates/feed-digest.md](_templates/feed-digest.md) exactly.
- `<id>` is the platform's post ID from the URL. With none, use
  `local-<YYYYMMDDHHMM>-<n>` (batch time, position), leave `url:` empty, and write
  `posted: unknown` if needed. It's a local label, never a claimed platform ID.
- Bodies are verbatim; threads stay whole in one block.
- **Digests never get source pages.** High-signal posts update topic and entity pages, cited
  by anchor. Low-signal posts stay in the digest, unextracted.

### 5.3 Curated bookmarks (optional)

Only if you connect a bookmarks source such as the X API. Procedure:
[x-bookmark-ingest](wiki/workflows/x-bookmark-ingest.md).

A **deep bookmark** carries body worth citing alone (long-form post, article, video with
content, external link that fetched cleanly). It gets its own raw file and source page like
§5.1, dated by the post's creation date. Everything else is **shallow**: a per-partition
digest under §5.2 with `source: bookmarks` added. Capture the whole unit, not just the saved
post. **Every capture is manifest-gated** by `wiki/.bookmarks-manifest.json`; never re-fetch
a post already in it.

### 5.4 Sourcing autonomy

| Situation | You may |
| --- | --- |
| Handed a URL, file, or paste | Ingest directly |
| Asked to "find and ingest X" | Search, select, ingest; report what you chose *and passed over* |
| Lint identifies a gap | Propose candidates with one-line justifications; ingest only what's approved |
| A source cites something interesting | Note it under "Leads not followed"; **do not ingest it** |

Record `acquired_by` on every capture.

## 6. Signal criteria

**Owned by the human. Edit as your judgment sharpens.** Applied to every feed post; the
verdict goes in `signal:` so triage stays auditable.

**High — extract into pages:**
- Makes a specific, checkable claim: a benchmark, a failure mode, a mechanism, a number.
- Reports firsthand experience with enough detail to act on.
- Contradicts or meaningfully qualifies something already in the wiki.
- Introduces a technique, tool, or concept the wiki doesn't cover.
- A thread that develops an argument rather than asserting once.

**Low — capture only:**
- Opinion with no mechanism or evidence.
- Restates what the wiki already covers.
- Engagement bait, announcements, promotion, memes, hot takes.
- Depends on an image, video, or link that wasn't captured.
- Would produce a page that just paraphrases the post.

**Uncertain:** mark it `low` and move on. The digest keeps everything either way.

## 7. Provenance

**Every non-obvious claim is cited to the raw file**, not the source page. Source pages get
rewritten; raw files don't.

**Footnote keys, never numbers.** The key is the raw file's slug with its date stripped
(also the source page's slug). Numbers are positional, and pages are rewritten, so
reordering silently re-points `[^2]` at a different file; a key fails loudly.

```markdown
Write-through caching trades write latency for read consistency.[^caching-patterns]

[^caching-patterns]: [Caching Patterns at Scale](raw/2026-08/2026-08-06-caching-patterns.md)
```

- Reuse the key when citing the same file twice. For a section anchor, suffix it
  (`[^caching-patterns-thread]`).
- Feed posts use `<platform>-post-<id>`:
  `[^x-post-1738291043]: [thread](raw/2026-08/2026-08-06-1430-x-posts.md#post-1738291043)`.

**Your own knowledge is allowed, and always marked:**

```markdown
> [!inference] Agent-inferred, not from a source
> This likely generalizes to read-heavy workloads, though no source in the wiki
> addresses that case directly.
```

**Contradictions are surfaced, not resolved.** Record both claims with both citations, on
the topic page's `Disagreements` section and the new source page's `Contradictions and
tensions`. Never silently overwrite the older claim or manufacture a consensus.

## 8. Operations

### Ingest

Follow the matching workflow. The outcome is the same for all of them:

1. Raw file(s) written per §5, before anything else. Nothing under `raw/` is touched again.
2. For a deep source: a source page, then **every** entity, concept, and topic page it
   touches updated or created. One source commonly touches ten or more pages; the cascade is
   the work, not the source page. List them under the source page's "What this changed in
   the wiki".
3. For a feed batch: high-signal posts update pages directly, cited by anchor; low-signal
   posts change nothing.
4. Contradictions flagged (§7).
5. Each touched partition index has one line per page (link, then a one-line summary); root
   [index.md](index.md) counts and `updated:` dates are current.
6. One log entry per deep source or feed batch (never per post).
7. Report: sources acquired, posts triaged high vs low, pages created and updated,
   contradictions, acquisitions skipped and why, plus the §10 review commands.
8. Scoped lint, with findings appended to the report.

**Don't commit** unless the human asks; they review with §10.

### Query

Procedure: [query](wiki/workflows/query.md). Route through the root index and partition
indexes to a bounded set of pages; follow footnotes into `raw/` for any claim the answer
rests on; search all of `wiki/` only if routing finds nothing. Cite raw files, mark your own
reasoning as inference (§7), and say plainly when the wiki doesn't cover the question. Offer
to file lasting answers as `question` pages (then index them and log a `query` entry).

### Lint

Checklist: [lint.md](lint.md). Procedure: [lint-pass](wiki/workflows/lint-pass.md).

- **Scoped**: automatic after every batch. Pages the batch created or modified, pages
  linking to or from them, and a cluster check on the partitions touched.
- **Full**: on request, everything. Suggest one when the last full pass in `log.md` is a few
  weeks old.

**Report and propose. Never apply fixes without approval.** Lint is the only operation that
may propose restructuring. Log one `lint` entry per pass.

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

Give the human these after an ingest. `git add -N .` comes first; without it `git diff`
ignores new files, which is most of what an ingest produces.

```bash
git add -N .

# How did the synthesis change? (excludes captured sources)
git diff -- 'wiki/' ':(exclude)wiki/*/raw/*'

# What source material came in?
git diff --stat -- 'wiki/*/raw/*'

# Append-only integrity, uncommitted: must be empty
git diff --name-only --diff-filter=MDR HEAD -- 'wiki/*/raw/*'

# Append-only integrity, history: must be empty
git log --diff-filter=MDR -- 'wiki/*/raw/*'
```

Two things fail silently if changed: the trailing `/*` (a directory-style pathspec matches
nothing and exits 0) and `MDR` (plain `M` misses deletions and renames, the unrecoverable
failures). Renames from an approved restructure are expected; confirm each against its
`restructure` log entry.

## 11. Preferences

[preferences.md](preferences.md) holds the human's durable instructions. When they state a
rule meant to last ("always…", "from now on…", "never…"), record it there in the same turn
and log a `schema` entry. If unsure whether it's durable, ask. A new preference that
contradicts an old one replaces it; the log keeps history.

Change this file (partition rules, signal criteria, page conventions) only when the human
asks.

## 12. Standing habits

- Prefer updating a page to creating a neighbor for it. A passing mention goes in an
  existing page's text; it earns a page when several sources discuss it.
- Read only what you need. For `log.md`, take the tail of its headers
  (`grep "^## \[" log.md | tail -20`); for a long raw file, search for the passage.
- Use `tmp/` for downloads and conversions. Nothing in it is committed, and nothing in the
  wiki may link into it.
- Never write credentials, tokens, or API keys into any file in this repo.
- With parallel subagents, put the constraints each needs in its prompt rather than a
  reading list, and keep index and `log.md` writes in the parent so they don't collide.
