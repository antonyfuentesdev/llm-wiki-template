# Lint checklist

A health check over the wiki. Two modes, one checklist. The procedure for running a pass is
[wiki/workflows/lint-pass.md](wiki/workflows/lint-pass.md).

**Scoped** runs automatically after every ingest and every feed batch. It covers the pages
created or modified, plus every page linking to or from them, plus a cluster check across the
partitions touched. Clusters are intra-partition by definition, so that check needs only
those partitions' link graphs — not the whole wiki.

**Full** runs on request and covers everything. It catches what scoped structurally cannot: a
claim in one partition contradicting one in another when neither was touched, an orphan
created months ago, drift between distant pages. Worth running every few weeks — the agent
should suggest one when it's been a while.

The mechanical checks (marked *(script)*) run with `python3 scripts/check-wiki.py`; the rest
need judgment.

Output is a report plus proposed fixes. **Fixes apply only on approval.** Nothing in this file
authorizes the agent to change pages on its own.

Workflow pages (`type: workflow`) are procedures, not claims about the world. Checks marked
*(not workflows)* skip them.

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
- [ ] **Orphans** *(script)*. Pages with no inbound link from a non-index page. A partition
      index line is required but doesn't count. Either something should link to the page or it
      should be folded into a page that matters.

## Provenance health

- [ ] **Unsourced claims** *(not workflows)*. Non-obvious assertions with no citation and no
      inference callout. Every claim is either cited or visibly marked as the agent talking.
- [ ] **Broken links and citations** *(script)*. Relative links, footnotes, or post anchors
      that point at files or headings that don't exist. A footnote quote that doesn't appear
      in its raw file is a broken citation. Numbered footnotes (`[^1]`) are a violation too —
      keys only.
- [ ] **Frontmatter drift** *(script)*. Field names match `AGENTS.md` §4. *(Not workflows:)*
      `sources:` lists every raw file the page cites and nothing else.
- [ ] **Raw integrity** *(script, uncommitted only)*. Run the two append-only integrity
      commands in `AGENTS.md` §10. Both must come back empty, except renames recorded by an
      approved `restructure` log entry. A non-empty result means every citation into the
      affected file is suspect.
- [ ] **Superseded sources.** Re-fetched or corrected sources whose old version isn't marked
      superseded on the corresponding source page, and pages still citing a superseded raw file
      without its newer version (`check-wiki.py` reports these).

## Structural health

- [ ] **Index drift** *(script, partition indexes)*. Pages missing from their partition index,
      indexed pages that no longer exist, and root index summaries that no longer describe
      what a partition covers.
- [ ] **Template leftovers** *(script)*. HTML comments or `<placeholder>` text left in a page
      under `wiki/`. In a raw digest, report it but don't fix it: raw files stay as written.
- [ ] **Misfit clusters.** Misfits that link to each other (`AGENTS.md` §3: a misfit has at
      most one link to another page in its partition, not counting index pages or its own
      cluster). Report any cluster at or approaching 8 pages, each with the written topical
      case required to propose a new partition. This is the only place partition proposals are
      allowed to surface.
- [ ] **Registry accuracy.** Every partition in `wiki/partitions.md` exists on disk with
      `index.md`, `raw/`, and `sources/`; every partition on disk is registered.
- [ ] **Partition axis.** No partition has drifted into being defined by format, platform, or
      recency rather than subject. Those are metadata, not folders.

## Growth

- [ ] **Gaps.** Topics the wiki keeps gesturing at without covering. Propose candidate sources
      with one-line justifications — do not ingest them without approval.
- [ ] **Questions worth asking.** Connections or tensions across pages that would make good
      queries, and would become good pages once answered.
- [ ] **Search.** When queries keep falling back to full-text search, or an index passes about
      150 lines, propose a search tool (such as qmd, or a small grep script) *before*
      proposing a partition split.
- [ ] **Rule friction.** Rules in `AGENTS.md` that caused friction or rework since the last
      pass. Propose the edit; never apply it.
