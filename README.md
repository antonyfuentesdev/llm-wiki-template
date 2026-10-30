# LLM wiki template

A starter repo for a personal knowledge base that an AI coding agent writes and maintains.
You collect sources and ask questions. The agent reads each source, files a full copy,
summarizes it, updates every related page, keeps the indexes current, and cites everything
back to the exact text it came from.

Clone it, open it in Cursor, Claude Code, Codex, or any agent that reads `AGENTS.md`, and
hand it something to read. No setup, no database, no server. It's a folder of markdown files
in git.

## Where this comes from

The pattern is Andrej Karpathy's
[LLM wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). His idea:
instead of asking an LLM to search your documents every time you have a question, have it
build and maintain a wiki from them, so the knowledge accumulates. The gist describes three
layers (raw sources, the wiki, a schema file) and three operations (ingest, query, lint), and
leaves the details to you and your agent.

This template is one worked-out set of those details, refined over two personal versions.
The rules the agent follows are in [AGENTS.md](AGENTS.md). Why each rule exists is in
[PLAN.md](PLAN.md).

## How it differs from RAG

Most "chat with your documents" tools use retrieval-augmented generation (RAG): at question
time, the model searches your files for relevant chunks and writes an answer from them.
Nothing carries over to the next question. A question that needs five documents makes the
model find and piece together all five, every time.

Here the work happens when a source comes in. The agent reads it once and folds it into
pages that already exist: the topic page's thesis gets rewritten, a person's page gets a new
fact, a disagreement with an older source gets recorded on both sides. By the time you ask a
question, the synthesis is already written. You read one page instead of five documents, and
you can open the page yourself without asking anything.

| | RAG | This wiki |
| --- | --- | --- |
| When synthesis happens | At every question | When a source is added |
| What accumulates | Nothing | Pages, links, flagged contradictions |
| What you can browse | Your original files | A linked wiki plus your original files |
| How you check an answer | Trust the retrieved chunks | Follow the footnote to the captured text |
| Infrastructure | Embeddings, vector store | Markdown and git |

The tradeoff is effort per source: one article might touch ten pages. That's the agent's
time, not yours.

## Quickstart

1. **Start a private copy with clean history.** Your wiki will hold personal material, so
   make it private and don't carry over the template's commits (GitHub's **Use this
   template** button does this).

2. **Add the wiki to the workspace you already work in.** This is the best way to use it.
   Editors like Cursor let one workspace hold several folders. Add the wiki next to your
   code repos, and every new chat in that workspace loads the wiki's `AGENTS.md` along with your
   first message. The agent already knows what the wiki is and how to file into it, so you
   never explain it. See [Use it from your everyday workspace](#use-it-from-your-everyday-workspace).

   Or open the wiki folder on its own. Cursor and Codex read `AGENTS.md` automatically.
   Claude Code reads `CLAUDE.md`, which loads `AGENTS.md`. For any other agent, start the
   session with "Read AGENTS.md and follow it."

3. **Mark the start.** In the first session, ask the agent to append a fresh `init` entry
   to [log.md](log.md), dated today. The entry that ships is the template's.

4. **Give it a first source.**

   ```text
   Ingest this article: https://example.com/some-article-you-liked
   ```

   The agent captures the full text, writes a summary page, creates or updates the pages for
   the ideas and people in it, updates the indexes, logs what it did, and runs a quick health
   check. Then it hands you the commands to review its changes. To see what one ingest
   produces, file by file, read the [worked example](examples/worked-example.md).

5. **Review, then commit.** The agent leaves its changes uncommitted so you can read the
   diff first (see [How it stays trustworthy](#how-it-stays-trustworthy)).

Optional but useful: tell it how you like things done, and it will remember.

```text
From now on, write all summaries in Spanish, and skip entity pages for people mentioned only once.
```

That lands in [preferences.md](preferences.md), which the agent reads every session.

### Use it from your everyday workspace

The wiki works best as one folder in a multi-folder workspace, next to the projects you
are building. Each folder keeps its own repo and its own `AGENTS.md`. When you send the first
message of a chat, the agent receives the `AGENTS.md` of every folder in the workspace, so it
holds the wiki's rules from its first reply.

How that plays out:

1. You're building something with the agent, in a code repo.
2. You work out a deployment recipe, a debugging approach, or a decision worth keeping.
3. You say so, in the same chat. No setup, no pasted instructions.

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
histories stay separate. If the wiki isn't in your workspace, the same prompts work once you
open it, with one extra line to point the agent at `AGENTS.md`.

Setup: in Cursor, use **File → Add Folder to Workspace** and save the workspace file. Other
tools have an equivalent, such as extra directories in Claude Code. How each tool loads a
second folder's instructions differs and changes between versions, so test yours: start a
new chat and ask "What does the wiki's AGENTS.md say about `raw/`?" If the agent answers
without reading a file, it's loaded.

## What's in the box

```
AGENTS.md            the rules the agent follows (the "schema" in Karpathy's terms)
CLAUDE.md            points Claude Code at AGENTS.md
preferences.md       your standing instructions to the agent
signal.md            what makes a social post worth extracting; yours to edit
index.md             catalog of the whole wiki; the agent reads it first
log.md               append-only timeline of everything the agent did
lint.md              the health-check checklist
scripts/             check-wiki.py, the mechanical half of the health check
PLAN.md              why the rules are what they are
_templates/          one template per page type, plus the social-post digest
examples/            a worked example and optional procedures; outside the wiki
inbox/               drop files here for the agent to ingest
tmp/                 scratch space for downloads; contents are git-ignored
wiki/
  partitions.md      the list of partitions and what belongs in each
  general/           knowledge about the world (the default home)
  projects/          your own projects, decisions, meetings, collaborators
  workflows/         step-by-step procedures for the agent
    index.md         each partition has a catalog,
    raw/             captured sources (append-only),
    sources/         one summary page per source,
    *.md             and its entity, concept, topic, and question pages
```

A **partition** is a top-level subject folder. You start with three and the agent proposes
new ones when the evidence supports it.

Inside a partition, pages come in a few types:

| Type | What it is | Example |
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
- **The agent keeps the full text, not a link.** Links rot. A claim has to stay checkable
  against the words it came from, years later.
- **Every non-obvious claim has a footnote** pointing at the passage in the captured source:
  a heading anchor, plus a short verbatim quote for numbers, definitions, and contestable
  claims. Footnotes are named after the source (`[^caching-patterns]`), not numbered, so
  rewrites can't silently point them at the wrong file.
- **The agent's own knowledge is labeled.** It can add what it knows or infers, inside a
  callout marked "Agent-inferred, not from a source".
- **Pages are earned.** The agent creates a page for a person, tool, or idea when a source
  discusses it substantively (a section or more, or it is central to the source), or when a
  second source mentions it. A passing mention goes into an existing page's text.
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
| Bookmarks (optional) | Saved X bookmarks via the X API, using [an example procedure](examples/x-bookmark-ingest.md) | Each saved post is captured with its thread, replies, media, and links; substantial ones are treated as deep sources, the rest go into a digest |

The split exists because volume and value don't match. Twenty posts a day would bury the wiki
in summary pages if each got one. What counts as high signal is written in
[signal.md](signal.md), and it's yours to edit.

## Use cases

Anything where you collect information over weeks or months and want it organized rather
than scattered. Some that fit well:

**Research on a subject.** Reading papers and articles on one question over a few months. Each
source updates a topic page whose thesis changes as evidence accumulates, with a section for
where sources disagree and a list of open questions. At the end you have a literature review
that wrote itself as you read.

**Reading articles and papers.** Hand over links as you find them. Each gets a summary page,
and the ideas in it land on concept pages shared with everything else you've read, so the
fourth article on a technique adds to one page instead of creating a fourth island.

**Learning a subject.** Course notes, textbook chapters, tutorials, and your own questions.
Ask "explain X using only what I've read so far" and the answer shows its sources. File good
answers as question pages to build a study guide.

**Books.** File chapters or your notes as you read. The agent builds pages for characters,
arguments, and recurring themes, and links them across chapters.

**Meeting notes.** Paste a transcript after each meeting. Decisions and open items go onto the
project's page, cited to the exact lines of the transcript; the people involved get notes
about what they're working on.

**A project journal.** Paste end-of-day notes. The project's topic page keeps a current
status, the decisions made and why, and what's blocked, all traceable to the day it was
written.

**A decision log.** Record decisions with their context and the options you rejected. Months
later, "why did we pick this?" has a cited answer, and a new source that undercuts the
reasoning gets flagged against it.

**People notes.** A light personal CRM: who someone is, what they work on, what you talked
about, what you promised. Each fact links back to the meeting or message it came from. Keep
the repo private.

**Social feed and bookmark triage.** Paste the posts you'd otherwise lose in your timeline.
The agent scores them against your criteria, keeps all of them, and pulls only the useful
ones into your pages.

**Competitive analysis, due diligence, trip planning, hobby deep dives.** Gather sources on
companies, products, places, or gear; ask for comparisons; let the agent track where sources
contradict each other.

**Your own ideas.** Brain dumps and half-formed thoughts, captured as notes. The agent links
them to what you've read that supports or contradicts them.

## Prompt examples

Copy, paste, and edit. You don't need special phrasing; these show what's possible.

### Ingesting

```text
Ingest this: https://example.com/article-on-sleep-and-memory
```

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
Here are my notes from chapter 3 of the book I'm reading. Ingest them and link the
characters and themes to the pages from earlier chapters.

<paste notes>
```

```text
Feed batch from X — triage these and extract only what's high signal:

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
Where do my sources contradict each other on intermittent fasting?
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
This source was truncated when you captured it. Here's the full text — re-capture it and
mark the old one superseded.
```

```text
Raise the bar for high-signal posts: a post must include a number or a concrete example.
Update the signal criteria.
```

```text
Give me the commands to review what you changed.
```

### Filing answers back

```text
That answer is worth keeping. File it as a question page.
```

```text
Answer this and file it as a question page in projects: what are the open risks on the
website redesign?
```

```text
Update the question page on caching strategies with what the new article says.
```

## How it stays trustworthy

**Sources can't drift.** `raw/` folders are append-only. A summary can be rewritten a hundred
times; the text it cites stays exactly as captured.

**Every claim is traceable.** Footnotes point at the passage in the captured file, not at a
summary of it, and quote it where the claim is a number or contestable. Anything the agent
added from its own knowledge is labeled as such.

**A script checks the mechanics.** `python3 scripts/check-wiki.py` (standard-library Python,
no install) reports broken links and anchors, quotes missing from their source, orphan pages,
pages missing from their index, missing frontmatter, leftover template text, numbered
footnotes, and modified raw files. The agent runs it during every health check.

**You review every change in git.** The agent leaves its work uncommitted and hands you
review commands that split what changed in your pages from what came in as new source
material. For example:

```bash
git add -N .                                   # include new files in the diff
git diff -- 'wiki/' ':(exclude)wiki/*/raw/*'   # how the synthesis changed
```

The full set, including the append-only integrity checks and the details that fail silently
if changed, is in [AGENTS.md](AGENTS.md) §10.

**There's a paper trail.** [log.md](log.md) records every ingest, feed batch, filed answer,
health check, rule change, and structural change, one parseable line each:

```bash
grep "^## \[" log.md | tail -20
```

## Customizing

**Add a partition.** Ask the agent ("Add a partition called `cooking` for recipes and food
science"), or let it propose one during a lint when a group of related pages outgrows its
folder. Partition scopes are in [wiki/partitions.md](wiki/partitions.md); the rules are in
[AGENTS.md](AGENTS.md) §3. Good candidates name
a subject: `health`, `finance`, `machine-learning`, `parenting`. Bad candidates name a format
or source: `articles`, `twitter`, `2026`.

**Change what counts as high signal.** Edit [signal.md](signal.md), or ask the agent to.

**Tell the agent how you work.** State a rule once ("always…", "never…") and it lands in
[preferences.md](preferences.md). Edit that file by hand any time.

**Change page structure.** Edit the files in [_templates/](_templates/). Keep the frontmatter
field names in step with [AGENTS.md](AGENTS.md) §4.

## Using Obsidian

Optional, but a good viewer: open the repo root as a vault. A few settings keep your own edits
in line with the rules.

- **Files and links:** set *New link format* to *Relative path to file* and turn *Use
  [[Wikilinks]]* off, so your edits write plain markdown links like the agent's. Add
  `_templates/` and `examples/` to *Excluded files* to keep placeholders out of search and
  the graph.
- **Attachments:** images belong beside the raw file that uses them, never in a shared
  folder. Set *Default location for new attachments* to *Same folder as current file*; the
  agent moves them into place on ingest.
- **Web Clipper:** point the browser extension at `inbox/`, then tell the agent "ingest the
  inbox".
- **Dataview** can query the page frontmatter (`type`, `partition`, `tags`, `status`,
  `updated`) for live tables.
- **Graph view** shows the hubs and the orphans.

GitHub doesn't render the `[!inference]` and `[!capture-note]` callouts; they show as plain
quotes, which is fine. `.obsidian/` is git-ignored; remove that line from `.gitignore` if you
want to commit your vault settings.

## Optional integrations

The wiki works with nothing but an agent that can read, write, and fetch web pages. Anything
else is optional:

- **X bookmarks.** Connect the X API with user-level OAuth through whatever client your agent
  supports (an MCP server, a CLI, or HTTP), then follow the example procedure in
  [examples/x-bookmark-ingest.md](examples/x-bookmark-ingest.md). Keep
  credentials in your agent's secret store or environment, never in this repo.
- **Any other source with an API** (a read-later app, a notes app, a meeting recorder) can get
  its own workflow page in `wiki/workflows/`, built from
  [_templates/workflow.md](_templates/workflow.md).

## FAQ

**Which agent should I use?** Any coding agent that can edit files in a folder and fetch web
pages. The rules don't depend on a particular one.

**Do I need Obsidian?** No. It's a nice viewer, not a requirement
([setup notes](#using-obsidian)).

**Should the repo be public?** Your wiki, no. It will contain what you read, your notes, and
possibly notes about people. Keep it private. This template is public; your copy shouldn't be.

**Can I add files myself instead of asking the agent?** Yes. Drop them into `inbox/` (a
clipped article, a PDF, notes, a transcript) and say "ingest the inbox". The agent files
each one into the right `raw/` folder with its frontmatter and empties the inbox. Don't
write into `raw/` yourself.

**What happens when a source is wrong?** The agent captures a corrected copy as a new file and
marks the old one superseded. Nothing is overwritten.

**How big can it get?** The agent reads indexes first and opens only the pages it needs, so
size matters less than structure. When queries keep falling back to full-text search, or an
index passes about 150 lines, add a search tool before splitting partitions:
[qmd](https://github.com/tobi/qmd) is a local search engine for markdown, or the agent can
write a small grep script. Lint proposes this when it sees the signs.

**What about PDFs and images in git?** They're committed like any other file. If your repo
grows large from binaries, consider Git LFS for `*.pdf` and image files.

**Can several people share one wiki?** The template is built for one person, but nothing
stops a team. Review changes through pull requests instead of local diffs.

**How do I update to a newer version of this template?** The template owns `AGENTS.md`,
`lint.md`, `_templates/`, `wiki/workflows/`, `examples/`, and `scripts/`: compare those with the new
version and merge what you want. You own `preferences.md`, `signal.md`, `index.md`,
`log.md`, and everything else under `wiki/`; a template update never needs to touch them.

## Contributing

Issues and pull requests are welcome, especially ones that come from using it: a rule that
confused your agent, a step that produced bad pages, a use case the docs don't cover. Keep
changes generic. This repo is a starting point, so personal content, specific tools, and
specific services belong in your own copy.

## License

[MIT](LICENSE).
