# CS From the Ground Up

A self-study CS and software development textbook for one reader: a 4th-year CS student (economics minor, Ontario) preparing for the workforce. The thesis: with AI coding tools you need a solid general understanding (concepts, vocabulary, mental models, what to check) more than every detail. Lessons are short (a 10 minute read, about 600 to 1000 words of prose, cap 1200) with a quiz and a small lab. Python first, then JavaScript and TypeScript. The Markdown in `docs/` is published to https://faiyaz-svg.github.io/CSFromTheGroundUp/ and also read directly in VS Code. The sibling math book is https://faiyaz-svg.github.io/MathFromTheGroundUp/.

## Rules to follow

- Writing: `STYLE.md`. Every page must follow it, including the list of AI-writing patterns to avoid. Em dashes are the most common slip.
- Lesson structure: `LESSON_TEMPLATE.md`.
- Site look: `DESIGN.md`.
- Don't make decisions the reader hasn't agreed to. Ask first when a change goes beyond what was requested.

## Layout

- `docs/00-start-here` to `docs/16-the-workplace`: the book, in reading order. `docs/reference`: glossary, command cheat sheets, ports and status codes, common mistakes.
- Each folder has `index.md` (overview). Each chapter subfolder has an `index.md` cheat sheet. There are no diagnostics and no Anki decks.
- Lesson files are numbered: `docs/10-databases-sql-and-postgres/02-querying/04-joins.md`.
- `mkdocs.yml` holds the site config and the `nav`. A new page must be added to `nav` and to `docs/progress.md`.
- `tools/lessons.yml` lists the planned lessons. `tools/figures/` holds the scripts that draw SVG figures into `docs/assets/figures/`.
- `tools/make_sample_dbs.py` writes the seed data to `docs/assets/sql/` (`shop`, `events`, `warehouse`). `docs/javascripts/sqlrunner.js` runs SQL blocks in the browser with PGlite.

## Commands (Windows, Git Bash)

```bash
npm install                                  # PGlite, for check_sql.mjs (dev only)
py -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
.venv/Scripts/zensical serve                 # preview at http://127.0.0.1:8000/CSFromTheGroundUp/
.venv/Scripts/zensical build --clean
.venv/Scripts/python tools/make_sample_dbs.py   # regenerate the sample databases
node tools/check_sql.mjs                     # run every SQL block and SQL solution
.venv/Scripts/python tools/build_nav.py      # after adding lessons: nav, progress page, folder lesson lists
.venv/Scripts/python tools/link_planned.py   # turn <!-- link: ... --> comments into links once targets exist
```

Labs run on WSL2 Ubuntu with Docker Desktop. Check Linux and Docker commands with `wsl -e bash -lc "..."`.

## Before committing a page

1. Run the self-check in `STYLE.md` (search for em dashes, curly quotes, banned words and patterns).
2. Run every code snippet (Python, JavaScript, TypeScript, bash in WSL). Never invent a flag or API.
3. Run `node tools/check_sql.mjs` for every SQL block and SQL solution.
4. Check that every changing fact (version, price, free-tier limit) has an official link and "as of 2026".
5. `zensical build --clean` must report no issues.

## Git

- Work on `main`. About one commit per chapter (about 100 for the whole project), plus a few for setup and fixes. Short, plain messages ("add memory hierarchy chapter").
- No Co-Authored-By or any other attribution lines in commits or pull requests, even if a tool suggests one.
