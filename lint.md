# Lint checklist

A health check over the wiki. Two modes, one checklist. The procedure for running a pass is
[wiki/workflows/lint-pass.md](wiki/workflows/lint-pass.md).

**Scoped** runs automatically at the end of every batch ingest. It covers the pages that batch
created or modified, plus every page linking to or from them, plus a cluster check across the
partitions the batch touched. Clusters are intra-partition by definition, so that check needs
only those partitions' link graphs — not the whole wiki.

**Full** runs on request and covers everything. It catches what scoped structurally cannot: a
claim in one partition contradicting one in another when neither was touched, an orphan
created months ago, drift between distant pages. Worth running every few weeks — the agent
should suggest one when it's been a while.

Output is a report plus proposed fixes. **Fixes apply only on approval.** Nothing in this file
authorizes the agent to change pages on its own.

---

## Content health

- [ ] **Contradictions.** Pages asserting incompatible things. Report both claims with their
      citations; don't silently pick a winner.
- [ ] **Stale claims.** Assertions a newer source supersedes. Note the superseding source.
- [ ] **Missing pages.** Concepts, entities, or people mentioned across several pages but
      lacking one of their own.
- [ ] **Missing cross-references.** Pages that clearly relate but don't link to each other.
      Cross-partition links deserve extra attention — the agent reads locally and under-links
      across boundaries by default.
- [ ] **Orphans.** Pages with no inbound links. Either something should link to them or they
      should be folded into a page that matters.

## Provenance health

- [ ] **Unsourced claims.** Non-obvious assertions with no citation and no inference callout.
      Every claim is either cited or visibly marked as the agent talking.
- [ ] **Broken links and citations.** Relative links, footnotes, or post anchors that point at
      files or headings that don't exist. Numbered footnotes (`[^1]`) are a violation too —
      keys only.
- [ ] **Frontmatter drift.** `sources:` lists every raw file the page cites and nothing else;
      field names match `AGENTS.md` §4.
- [ ] **Raw integrity.** No captured source has been modified, deleted, or renamed:

      git diff --name-only --diff-filter=MDR HEAD -- 'wiki/*/raw/*'
      git log --diff-filter=MDR -- 'wiki/*/raw/*'

      Both must come back empty, except renames recorded by an approved `restructure` log
      entry. `MDR` rather than `M` is deliberate — plain `M` misses deletions, which is the
      half of the append-only rule you cannot recover from. A non-empty result means every
      citation into the affected file is suspect.
- [ ] **Superseded sources.** Re-fetched or corrected sources whose old version isn't marked
      superseded on the corresponding source page.

## Structural health

- [ ] **Index drift.** Pages missing from their partition index, indexed pages that no longer
      exist, and page counts in the root index that no longer match reality.
- [ ] **Misfit clusters.** Groups of mutually-linked pages weakly connected to the rest of
      their partition. Report any cluster at or approaching 8 pages, each with the written
      topical case required to propose a new partition. This is the only place partition
      proposals are allowed to surface.
- [ ] **Registry accuracy.** Every partition in `wiki/partitions.md` exists on disk with
      `index.md`, `raw/`, and `sources/`; every partition on disk is registered.
- [ ] **Partition axis.** No partition has drifted into being defined by format, platform, or
      recency rather than subject. Those are metadata, not folders.

## Growth

- [ ] **Gaps.** Topics the wiki keeps gesturing at without covering. Propose candidate sources
      with one-line justifications — do not ingest them without approval.
- [ ] **Questions worth asking.** Connections or tensions across pages that would make good
      queries, and would become good pages once answered.
