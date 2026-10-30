# LLM wiki template

A starter repo for a personal knowledge base that an AI coding agent writes and maintains.
You collect sources and ask questions. The agent reads each source, files a full copy,
summarizes it, updates every related page, keeps the indexes current, and cites each claim
to the text it came from.

Open it in Cursor, Claude Code, Codex, or any agent that reads `AGENTS.md`, and hand it
something to read. No database, no server. It's a folder of markdown files in git.

## Where this comes from

The pattern is Andrej Karpathy's
[LLM wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). His idea:
instead of making an LLM search your documents at every question, have it build and maintain
a wiki from them, so the knowledge accumulates. The gist describes three layers (raw sources,
the wiki, a schema file) and three operations (ingest, query, lint), and leaves the details
to you and your agent.

This template is one worked-out set of those details, refined over two personal versions.
The rules the agent follows are in [AGENTS.md](AGENTS.md). [PLAN.md](PLAN.md) explains why
each rule exists.

## How it differs from RAG

Retrieval-augmented generation (RAG) tools search your files for relevant chunks when you
ask a question, then write an answer from them. Nothing carries over to the next question.

Here the work happens when a source comes in. The agent folds it into pages that already
exist: a topic page's thesis gets rewritten, a person's page gets a new fact, a
disagreement with an older source is recorded on both sides. By the time you ask, the
synthesis is written, and you can read the page yourself.

| | RAG | This wiki |
| --- | --- | --- |
| When synthesis happens | At every question | When a source is added |
| What accumulates | Nothing | Pages, links, flagged contradictions |
| How you check an answer | Trust the retrieved chunks | Follow the footnote to the captured text |
| Infrastructure | Embeddings, vector store | Markdown and git |

The cost is effort per source: one article can touch ten pages. That's the agent's time.

## Quickstart

1. **Make a private copy with clean history.** Your wiki will hold personal material, so
   keep it private and leave the template's commits behind. GitHub's **Use this template**
   button does both.

2. **Add it to the workspace you already work in** (see
   [below](#use-it-from-your-everyday-workspace)), or open the wiki folder on its own.
   Cursor and Codex read `AGENTS.md` automatically. Claude Code reads `CLAUDE.md`, which
   loads `AGENTS.md`. For any other agent, start with "Read AGENTS.md and follow it."

3. **Mark the start.** Ask the agent to append a fresh `init` entry to [log.md](log.md),
   dated today. The entry that ships is the template's.

4. **Give it a first source.**

   ```text
   Ingest this article: https://example.com/some-article-you-liked
   ```

   The agent captures the text, writes a summary page, updates the related pages and
   indexes, logs what it did, runs a health check, and hands you the commands to review the
   changes. The [worked example](examples/worked-example.md) shows the result file by file.

5. **Review, then commit.** The agent leaves its changes uncommitted so you can read the diff
   first ([details](#how-it-stays-trustworthy)).

To set a standing rule, say it once: "From now on, write all summaries in Spanish." It lands
in [preferences.md](preferences.md), which the agent reads every session.

### Use it from your everyday workspace

The wiki works best as one folder in a multi-folder workspace, next to the projects you're
building. Each folder keeps its own repo and its own `AGENTS.md`. When you send the first
message of a chat, the agent receives the `AGENTS.md` of every folder in the workspace, so it
holds the wiki's rules from its first reply.

In practice:

1. You're building something with the agent, in a code repo.
2. You work out a deployment recipe, a debugging approach, or a decision worth keeping.
3. You say so in the same chat. No setup, no pasted instructions.

```text
That migration recipe took us three tries. File it as a workflow in the wiki.
```

```text
Add what we learned about rate-limit retries to the wiki, and cite the docs page we used.
```

```text
Before we start, check the wiki for anything we've already figured out about this.
```

The agent writes in the wiki folder while the code stays in the project repo, so the two
histories stay separate.

In Cursor, use **File → Add Folder to Workspace** and save the workspace file. Other tools
have an equivalent, such as extra directories in Claude Code. How each tool loads a second
folder's instructions varies by version, so test yours: in a new chat, ask "What does the
wiki's AGENTS.md say about `raw/`?" If the agent answers without reading a file, it's loaded.

## What's in the box

```
AGENTS.md          the rules the agent follows (the "schema" in Karpathy's terms)
CLAUDE.md          points Claude Code at AGENTS.md
preferences.md     your standing instructions to the agent
signal.md          what makes a social post worth extracting; yours to edit
index.md           catalog of the whole wiki; the agent reads it first
log.md             append-only timeline of everything the agent did
lint.md            the health-check checklist
scripts/           check-wiki.py, the mechanical half of the health check
PLAN.md            why the rules are what they are
_templates/        one template per page type, plus the social-post digest
examples/          a worked example and optional procedures; outside the wiki
inbox/             drop files here for the agent to ingest (never write into raw/ yourself)
tmp/               scratch space for downloads; git-ignored
wiki/
  partitions.md    the partitions and what belongs in each
  general/         knowledge about the world (the default home)
  projects/        your own projects, decisions, meetings, collaborators
  workflows/       step-by-step procedures for the agent
```

Each partition holds an `index.md` catalog, `raw/` (captured sources, append-only),
`sources/` (one summary page per source), and its entity, concept, topic, and question pages.
A **partition** is a top-level subject folder. You start with three, and the agent proposes
new ones when the evidence supports it.

| Page type | What it is | Example |
| --- | --- | --- |
| source | A summary of one captured source | `sources/caching-patterns.md` |
| entity | A person, company, tool, product, or place | `postgres.md` |
| concept | An idea, pattern, or technique | `write-through-caching.md` |
| topic | The running synthesis on a subject, with a thesis | `caching.md` |
| question | An answer you asked the agent to keep | `why-caches-stampede.md` |
| workflow | A reusable procedure | `workflows/ingest-url.md` |

## The rules, in plain language

- **Sources are never edited.** Anything in a `raw/` folder is added once and never changed or
  deleted. If a source was wrong, the agent captures a new copy and marks the old one
  superseded. This is what makes citations mean something.
- **The agent keeps the full text, not a link.** Links rot, and a claim has to stay checkable
  against its words years later.
- **Every non-obvious claim has a footnote** pointing at the passage in the captured source:
  a heading anchor, plus a short verbatim quote for numbers, definitions, and contestable
  claims. Footnotes are named after the source (`[^caching-patterns]`), not numbered, so a
  rewrite can't silently point one at the wrong file.
- **The agent's own knowledge is labeled.** What it adds from its own knowledge goes in a
  callout marked "Agent-inferred, not from a source".
- **Pages are earned.** A person, tool, or idea gets a page when a source discusses it
  substantively, or when a second source mentions it. A passing mention goes into an existing
  page's text.
- **Disagreements stay visible.** When two sources conflict, both claims stay on the page,
  each with its citation. The agent doesn't pick a winner.
- **Folders are subjects, not formats.** A thread about caching and a paper about caching go
  in the same partition. Where something came from is recorded in its metadata.
- **Structure changes need your approval.** The agent proposes new or merged partitions only
  during a health check, with evidence, and waits for a yes.
- **Health checks report; they don't fix.** The agent lists what's wrong and proposes fixes.
  You decide.

## Three kinds of sources

| Tier | Examples | What the agent does |
| --- | --- | --- |
| Deep | Articles, papers, PDFs, transcripts, book chapters, your notes, chat exports | Full text in `raw/`, a summary page, and updates to every related page |
| Feed | Batches of posts from X, LinkedIn, Bluesky, and similar | One digest file per batch; each post is scored high or low signal; only high-signal posts update pages |
| Bookmarks (optional) | Saved X bookmarks, via [an example procedure](examples/x-bookmark-ingest.md) | Each saved post is captured with its thread, replies, media, and links; substantial ones are treated as deep sources, the rest go into a digest |

Volume and value don't match: twenty posts a day would bury the wiki in summary pages if
each got one. What counts as high signal is in [signal.md](signal.md); edit it, or ask the
agent to.

## Use cases

Anything where you collect information over weeks or months and want it organized instead of
scattered.

- **Research on a subject.** Each paper or article updates a topic page whose thesis changes
  as evidence accumulates, with a section for where sources disagree and a list of open
  questions.
- **Reading and learning.** Hand over articles, course notes, book chapters, or your own
  questions. Ideas land on concept pages shared with everything else you've read, so the
  fourth article on a technique adds to one page instead of starting a fourth. Ask "explain X
  using only what I've read so far" and the answer shows its sources. File good answers as
  question pages to build a study guide.
- **Meetings and project journals.** Paste a transcript or end-of-day notes. Decisions and open
  items go onto the project's page, cited to the lines they came from.
- **A decision log.** Record decisions with their context and the options you rejected. Months
  later, "why did we pick this?" has a cited answer, and a new source that undercuts the
  reasoning gets flagged against it.
- **People notes.** A light personal CRM: who someone is, what they work on, what you
  promised. Each fact links to the meeting or message it came from. Keep the repo private.
- **Social feed and bookmark triage.** Paste the posts you'd otherwise lose in your timeline.
  The agent scores them against your criteria, keeps all of them, and pulls only the useful
  ones into your pages.
- **Comparisons and deep dives.** Companies, products, places, or gear. Ask for comparisons
  and let the agent track where sources contradict each other.
- **Your own ideas.** Capture brain dumps as notes. The agent links them to what you've read
  that supports or contradicts them.
- **Engineering recipes.** Procedures and lessons you work out while building, filed from the
  chat where you found them ([see above](#use-it-from-your-everyday-workspace)).

## Prompt examples

Copy, paste, and edit. You don't need special phrasing.

### Ingesting

```text
Ingest these three links. They're for my research on remote work and productivity.
https://example.com/a
https://example.com/b
https://example.com/c
```

```text
Ingest the PDF at ~/Downloads/paper.pdf. Keep the original file alongside the text.
```

```text
Ingest the inbox.
```

```text
Here's the transcript from today's planning meeting for the website redesign. Ingest it,
update the project page with decisions and open items, and tell me what's still unassigned.

<paste transcript>
```

```text
Feed batch from X: triage these and extract only what's high signal.

<paste posts, with their links if you have them>
```

```text
Find two or three well-regarded introductions to vector databases and ingest the best one.
Tell me what you passed over and why.
```

### Querying

```text
What do my sources say about spaced repetition? Cite them.
```

```text
Compare what the three papers I ingested on caching say about invalidation. Where do they
disagree?
```

```text
What changed in the wiki in the last two weeks?
```

```text
What did we decide about the database migration, and who decided it?
```

```text
What does the wiki not know yet about this topic? Suggest sources to fill the gaps, but
don't ingest anything.
```

### Maintenance

```text
Run a full lint.
```

```text
Add a partition called `health` for exercise, sleep, and nutrition. Move the pages that
belong there.
```

```text
The pages on "write-through caching" and "write-behind caching" overlap. Propose a merge.
```

```text
This source was truncated when you captured it. Here's the full text. Re-capture it and
mark the old one superseded.
```

### Filing answers back

```text
That answer is worth keeping. File it as a question page.
```

```text
Answer this and file it as a question page in projects: what are the open risks on the
website redesign?
```

## How it stays trustworthy

**A script checks the mechanics.** `python3 scripts/check-wiki.py` (standard-library Python,
no install) reports broken links and anchors, quotes missing from their source, orphan pages,
pages missing from their index, missing frontmatter, leftover template text, numbered
footnotes, and modified raw files. The agent runs it during every health check.

**You review every change in git.** The agent leaves its work uncommitted and hands you
commands that separate what changed in your pages from what came in as new source material:

```bash
git add -N .                                   # include new files in the diff
git diff -- 'wiki/' ':(exclude)wiki/*/raw/*'   # how the synthesis changed
```

The full set, including the append-only integrity checks, is in [AGENTS.md](AGENTS.md) §10.

**There's a paper trail.** [log.md](log.md) records every ingest, feed batch, filed answer,
health check, rule change, and structural change, one parseable line each:

```bash
grep "^## \[" log.md | tail -20
```

## Customizing

**Add a partition.** Ask the agent ("Add a partition called `cooking` for recipes and food
science"), or let it propose one during a lint when a group of related pages outgrows its
folder. Good partition names are subjects (`health`, `finance`, `machine-learning`). Bad ones
are formats or sources (`articles`, `twitter`, `2026`). The rules are in
[AGENTS.md](AGENTS.md) §3.

**Change page structure.** Edit the files in [_templates/](_templates/), and keep the
frontmatter field names in step with [AGENTS.md](AGENTS.md) §4.

## Using Obsidian

Optional. Open the repo root as a vault, then set these so your own edits follow the rules:

- **Links:** set *New link format* to *Relative path to file* and turn *Use [[Wikilinks]]*
  off. Add `_templates/` and `examples/` to *Excluded files* to keep placeholders out of
  search and the graph.
- **Attachments:** images belong beside the raw file that uses them. Set *Default location
  for new attachments* to *Same folder as current file*; the agent moves them into place on
  ingest.
- **Web Clipper:** point the extension at `inbox/`, then tell the agent "ingest the inbox".
- **Dataview** can query the page frontmatter (`type`, `partition`, `tags`, `status`,
  `updated`). **Graph view** shows hubs and orphans.

GitHub shows the `[!inference]` and `[!capture-note]` callouts as plain quotes, which is
fine. `.obsidian/` is git-ignored; remove that line from `.gitignore` to commit your vault
settings.

## Optional integrations

The wiki needs only an agent that can read, write, and fetch web pages.

- **X bookmarks.** Connect the X API with user-level OAuth through whatever client your agent
  supports (an MCP server, a CLI, or HTTP), then follow
  [examples/x-bookmark-ingest.md](examples/x-bookmark-ingest.md). Keep credentials in your
  agent's secret store or environment, never in this repo.
- **Any other source with an API** (a read-later app, a notes app, a meeting recorder) can get
  its own workflow page in `wiki/workflows/`, built from
  [_templates/workflow.md](_templates/workflow.md).

## FAQ

**Should the repo be public?** Your wiki, no. It will hold what you read, your notes, and
possibly notes about people. This template is public; your copy shouldn't be.

**What happens when a source is wrong?** The agent captures a corrected copy as a new file and
marks the old one superseded. Nothing is overwritten.

**How big can it get?** The agent reads indexes first and opens only the pages it needs, so
structure matters more than size. When queries keep falling back to full-text search, or an
index passes about 150 lines, add a search tool before splitting partitions:
[qmd](https://github.com/tobi/qmd) is a local search engine for markdown, or the agent can
write a small grep script. Lint proposes this when it sees the signs.

**What about PDFs and images in git?** They're committed like any other file. If binaries make
the repo large, consider Git LFS for `*.pdf` and image files.

**Can several people share one wiki?** The template is built for one person, but nothing
stops a team. Review changes through pull requests instead of local diffs.

**How do I update to a newer version of this template?** The template owns `AGENTS.md`,
`lint.md`, `_templates/`, `wiki/workflows/`, `examples/`, and `scripts/`. Compare those with
the new version and merge what you want. You own `preferences.md`, `signal.md`, `index.md`,
`log.md`, and everything else under `wiki/`; an update never needs to touch them.

## Contributing

Issues and pull requests are welcome, especially ones that come from using it: a rule that
confused your agent, a step that produced bad pages, a use case the docs don't cover. Keep
changes generic. This repo is a starting point, so personal content, specific tools, and
specific services belong in your own copy.

## License

[MIT](LICENSE).
