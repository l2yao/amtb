# AGENTS.md — LLM Wiki Schema

This repository is configured as an **LLM-maintained wiki** following the Karpathy "LLM Wiki" pattern. This file is the schema: it tells the LLM how the wiki is structured, what conventions to follow, and what workflows to run. Read this file first at the start of every session before touching the wiki.

## Purpose

Build a persistent, interlinked, compounding knowledge base of Traditional Chinese Buddhist teachings (淨空老和尚 / Chin Kung, AMTB corpus). The wiki sits between the reader and the raw source corpus. The LLM writes and maintains the wiki; the human curates sources and asks questions.

## Repository layout

```
amtb/
  AGENTS.md           <- this file (schema)
  amtb/
    doc/              <- RAW SOURCES (immutable, never edited)
    wiki/             <- THE WIKI (LLM-owned markdown)
      SCHEMA.md       <- page templates & examples
      README.md       <- home/overview
      index.md        <- content catalog
      log.md          <- chronological activity log
      raw-manifest.md <- generated catalog of all raw series
      tools/
        gen_manifest.py
      認識佛教/ 三皈五戒/ ...   <- category folders
```

## The three layers

1. **Raw sources** — `amtb/doc/`. Curated, immutable, git-tracked. The LLM reads from here, **never writes**. One exception: `wiki/tools/gen_manifest.py` is a read-only generator that parses metadata and writes the manifest into the wiki (not into raw).
2. **The wiki** — `amtb/wiki/`. LLM-owned markdown. Create/update pages on ingest, query, and lint.
3. **The schema** — this file + `wiki/SCHEMA.md`. Co-evolve with the human.

## Raw source format

- 10 top-level categories (認識佛教, 三皈五戒, 入門經典, 淨土五經一論, 大乘經論, 其他經律論, 社會教育, 祖師大德, 講經培訓, 開示問答與活動).
- Each category → topic folders → **series folders** named by code (e.g. `17-001`) → numbered `.md` pages (`0001.md`, `0002.md`, ...).
- A series = one teaching title (possibly many sessions/集). There are **1,269 series folders, ~15,300 pages** (includes 6 `_EN` English variants).
- Every page's **first line** is metadata:
  `題目　　（共N集 | 第一集）　　日期　　地點　　檔名：CODE-PAGE`
  Example: `認識佛教　　（第一集）　　1991/12　　美國邁阿密　　檔名：17-001-0001`
- `.doc`/`.pdf`/`.docx` duplicates exist alongside `.md` — ignore them; read only `.md`.
- See `wiki/raw-manifest.md` for the full navigable catalog (regenerate with `python wiki/tools/gen_manifest.py` when needed).

## Wiki structure

One folder per category. Inside each category folder: a category page, topic pages, and source pages. Concept pages live in `wiki/概念/`.

```
wiki/
  認識佛教.md                 <- category page
  認識佛教/
    認識佛陀教育.md            <- topic page
    17-001.md                 <- source page (one per series)
  ...
  概念/
    三皈依.md
    五戒.md
    念佛.md
    ...
```

**Language**: all wiki page content is Traditional Chinese. Frontmatter tags/values may be Chinese or English. Never auto-translate sources; quote sparingly.

## Page types

### Category page (`認識佛教.md`)
- YAML frontmatter: `type: category`, `tags`, `updated`, `sources` (count).
- Lists the topic pages with one-line descriptions, plus a short synthesis of what the category covers.

### Topic page (`認識佛陀教育.md`)
- `type: topic`, `category`.
- One per sutra/subject within a category. Lists its series with links, notes thematic structure.

### Source page (`17-001.md`)
- `type: source`, `category`, `topic`, `code`, `title`, `date`, `place`, `pages`, `raw`.
- Sections: 概要 (summary), 重點 (key teachings), 相關概念 (wikilinks to concepts), 相關頁面 (links to related series/topics).
- One page per series; cite the raw path so the reader can drill in.

### Concept page (`概念/念佛.md`)
- `type: concept`.
- Cross-cutting Buddhist concepts that appear across many sources. Evolving entity page: definition, how different sources present it, key quotes with citation to series code, related concepts.
- Create a concept page when a term is central and recurs; do not create pages for one-off mentions.

### Answer pages (filed queries)
- `type: answer`. Created when a good Q&A result deserves persistence (comparisons, syntheses). Lives under `wiki/問答/`.

## Conventions

- **Naming**: files use the natural Chinese name for concepts/topics; source pages use the numeric code. No spaces in filenames; if needed use `_`.
- **Links**: Obsidian-style wikilinks `[[認識佛陀教育]]`, `[[概念/念佛]]`. For source pages, link the code text: `[[17-001]]`.
- **Frontmatter**: always YAML `---` block. Keys: `type`, `category`, `topic`, `code`, `title`, `date`, `place`, `pages`, `raw`, `tags`, `updated`. Use `date: YYYY-MM-DD` or `YYYY/M` as available.
- **Citations**: when a claim comes from a specific series, cite it as `〔17-001〕` or link `[[17-001]]`. When a concept page synthesizes multiple sources, list source codes.
- **Immutable raw**: never modify anything under `amtb/doc/`.

## Workflows

### Ingest (one series at a time, with human review)
1. Read `wiki/raw-manifest.md` and `wiki/index.md` to find the series and check what exists.
2. Read the source pages of the series (all `.md` in the folder; start with `0001.md`).
3. Write/update the **source page** in the wiki: 概要, 重點, metadata, raw path.
4. Update/create **concept pages** referenced by the teachings.
5. Update the **topic page** and **category page** if the series adds structure or emphasis.
6. Update **`index.md`** (add/refresh the entry).
7. Append an entry to **`log.md`**: `## [YYYY-MM-DD] ingest|CODE 標題` plus a short note.
8. Report to the human what was done; ask which series to ingest next.

### Query
1. Read `wiki/index.md` first to find relevant pages, then drill into them.
2. Synthesize an answer citing sources (`〔CODE〕`).
3. If the answer is durable (comparison, analysis, synthesis), file it as an answer page under `wiki/問答/` and update `index.md` + `log.md`.

### Lint (periodic health-check)
- Find contradictions between pages, stale claims superseded by newer sources, orphan pages (no inbound links), important concepts missing a page, and data gaps fillable by web search.
- Fix what is fixable in the wiki; report findings to the human; append a `lint` entry to `log.md`.

## index.md and log.md

- **index.md** — content catalog, organized by category. Every page gets a line: link + one-line summary (+ optional tags). Updated on every ingest/query-filing. The primary navigation tool.
- **log.md** — append-only timeline. Every entry starts with `## [YYYY-MM-DD] type|detail`. Types: `ingest`, `query`, `answer`, `lint`, `schema`. The log is parseable with `grep "^## \[" wiki/log.md`.

## Tools

- `python wiki/tools/gen_manifest.py` — regenerates `wiki/raw-manifest.md` from the raw corpus. Run when the corpus changes or at session start if unsure.

## Rules of thumb

- Prefer updating existing pages over creating new ones; keep the wiki small and linked.
- When in doubt about emphasis, ask the human.
- Never invent metadata; if the raw line is missing a field, leave it blank rather than guess.
- Keep every page focused; split long pages when they exceed roughly 150 lines.
