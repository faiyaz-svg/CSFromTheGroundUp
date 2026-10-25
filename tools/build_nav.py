"""Update the site navigation, the progress page and the folder lesson lists.

Reads tools/lessons.yml and writes:
  - the nav block in mkdocs.yml (between "# nav:start" and "# nav:end")
  - docs/progress.md (written lessons only, keeping any ticked boxes)
  - the lesson list in each docs/<folder>/index.md (between the
    "lessons:start" and "lessons:end" comments); a missing index.md is
    created as a short stub

Only pages that exist are linked or added to the nav, so the site never
has links to lessons that haven't been written.

Run from the repo root:  .venv/Scripts/python tools/build_nav.py
With --tracked, only pages committed to git count, so drafts on disk stay
out of the nav.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"
LESSONS = ROOT / "tools" / "lessons.yml"
PROGRESS = DOCS / "progress.md"

NAV_START = "# nav:start"
NAV_END = "# nav:end"
LIST_START = "<!-- lessons:start -->"
LIST_END = "<!-- lessons:end -->"

START_HERE = [
    ("How to use this book", "00-start-here/index.md"),
    ("Setting up your machine", "00-start-here/setting-up-your-machine.md"),
    ("Learning tech with AI", "00-start-here/learning-tech-with-ai.md"),
    ("Reading docs and error messages", "00-start-here/reading-docs-and-error-messages.md"),
    ("Progress", "progress.md"),
]

# Set by --tracked: the paths (relative to docs/) that git knows about.
TRACKED: set[str] | None = None

REFERENCE = [
    ("Reference", "reference/index.md"),
    ("Glossary", "reference/glossary.md"),
    ("Command cheat sheets", "reference/commands.md"),
    ("Ports, status codes and latency numbers", "reference/ports-status-codes-and-latency.md"),
    ("Common mistakes", "reference/common-mistakes.md"),
]


@dataclass
class Lesson:
    title: str
    path: str  # relative to docs/
    flags: list[str]

    @property
    def exists(self) -> bool:
        return exists(self.path)


@dataclass
class Chapter:
    title: str
    folder: str  # relative to docs/, e.g. "02-middle-school/02-ratios-rates-percents"
    lessons: list[Lesson] = field(default_factory=list)


@dataclass
class Folder:
    folder: str
    title: str
    tab: str
    summary: str
    before: str
    chapters: list[Chapter]  # a flat folder has one chapter with an empty title
    flat: bool

    def all_lessons(self) -> list[Lesson]:
        return [lesson for chapter in self.chapters for lesson in chapter.lessons]


def parse_lesson(entry: list, prefix: str, number: int) -> Lesson:
    # A title with an unquoted comma turns into extra list items, so check the shape.
    if not 2 <= len(entry) <= 3 or (len(entry) == 3 and not isinstance(entry[2], list)):
        raise SystemExit(f"bad lesson entry {entry!r}: quote titles that contain commas")
    slug, title = entry[0], entry[1]
    flags = list(entry[2]) if len(entry) > 2 else []
    if not set(flags) <= {"optional", "fast"}:
        raise SystemExit(f"bad flags in lesson entry {entry!r}")
    return Lesson(title=title, path=f"{prefix}/{number:02d}-{slug}.md", flags=flags)


def load_folders() -> list[Folder]:
    data = yaml.safe_load(LESSONS.read_text(encoding="utf-8"))
    folders = []
    for f in data["folders"]:
        name = f["folder"]
        if "lessons" in f:
            chapter = Chapter(title="", folder=name)
            chapter.lessons = [
                parse_lesson(entry, name, i) for i, entry in enumerate(f["lessons"], 1)
            ]
            chapters, flat = [chapter], True
        else:
            chapters, flat = [], False
            for ci, c in enumerate(f["chapters"], 1):
                cfolder = f"{name}/{ci:02d}-{c['slug']}"
                chapter = Chapter(title=c["title"], folder=cfolder)
                chapter.lessons = [
                    parse_lesson(entry, cfolder, li) for li, entry in enumerate(c["lessons"], 1)
                ]
                chapters.append(chapter)
        folders.append(
            Folder(
                folder=name,
                title=f["title"],
                tab=f.get("tab", f["title"]),
                summary=f.get("summary", ""),
                before=f.get("before", ""),
                chapters=chapters,
                flat=flat,
            )
        )
    return folders


def exists(path: str) -> bool:
    if TRACKED is not None:
        return path in TRACKED
    return (DOCS / path).is_file()


def tracked_paths() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "docs"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return {line.removeprefix("docs/") for line in out.splitlines()}


def q(text: str) -> str:
    """Quote a title for YAML (JSON strings are valid YAML)."""
    return json.dumps(text, ensure_ascii=False)


def build_nav(folders: list[Folder]) -> str:
    # The home page is the index of the "Start here" tab, so there is no
    # separate "Home" tab; the site title in the header also links home.
    lines = [NAV_START, "nav:", "  - Start here:", "      - index.md"]
    for title, path in START_HERE:
        if exists(path):
            lines.append(f"      - {q(title)}: {path}")

    for f in folders:
        index = f"{f.folder}/index.md"
        if not exists(index):
            continue
        lines.append(f"  - {q(f.tab)}:")
        lines.append(f"      - {index}")
        diagnostic = f"{f.folder}/diagnostic.md"
        if exists(diagnostic):
            lines.append(f"      - Diagnostic: {diagnostic}")
        for chapter in f.chapters:
            written = [lesson for lesson in chapter.lessons if lesson.exists]
            chapter_index = f"{chapter.folder}/index.md"
            if f.flat:
                for lesson in written:
                    lines.append(f"      - {q(lesson.title)}: {lesson.path}")
                continue
            if not written and not exists(chapter_index):
                continue
            lines.append(f"      - {q(chapter.title)}:")
            if exists(chapter_index):
                lines.append(f"          - {chapter_index}")
            for lesson in written:
                lines.append(f"          - {q(lesson.title)}: {lesson.path}")

    ref = [(t, p) for t, p in REFERENCE if exists(p)]
    if ref:
        lines.append("  - Reference:")
        for title, path in ref:
            if path == "reference/index.md":
                lines.append(f"      - {path}")
            else:
                lines.append(f"      - {q(title)}: {path}")

    lines.append(NAV_END)
    return "\n".join(lines)


def write_nav(folders: list[Folder]) -> None:
    text = MKDOCS.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(NAV_START) + r".*?" + re.escape(NAV_END), re.S)
    if not pattern.search(text):
        raise SystemExit(f"mkdocs.yml has no '{NAV_START}' ... '{NAV_END}' block")
    MKDOCS.write_text(pattern.sub(lambda _: build_nav(folders), text), encoding="utf-8", newline="\n")


def ticked_paths() -> set[str]:
    if not PROGRESS.is_file():
        return set()
    done = set()
    for line in PROGRESS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*- \[[xX]\] \[.*?\]\((.*?)\)", line)
        if m:
            done.add(m.group(1))
    return done


def write_progress(folders: list[Folder]) -> None:
    done = ticked_paths()
    total = sum(len(f.all_lessons()) for f in folders)
    written = sum(1 for f in folders for lesson in f.all_lessons() if lesson.exists)
    out = [
        "# Progress",
        "",
        "Tick each lesson when you finish it. On the website, ticks are saved in the "
        "browser you use, so each device keeps its own list. In VS Code, change "
        "`[ ]` to `[x]` in `docs/progress.md`.",
        "",
        f"Lessons written so far: {written} of {total}. New lessons appear here as they are added.",
        "",
    ]
    for f in folders:
        lessons = [lesson for lesson in f.all_lessons() if lesson.exists]
        if not lessons:
            continue
        out.append(f"## {f.title}")
        out.append("")
        for chapter in f.chapters:
            chapter_lessons = [lesson for lesson in chapter.lessons if lesson.exists]
            if not chapter_lessons:
                continue
            if chapter.title:
                out.append(f"### {chapter.title}")
                out.append("")
            for lesson in chapter_lessons:
                box = "x" if lesson.path in done else " "
                out.append(f"- [{box}] [{lesson.title}]({lesson.path})")
            out.append("")
    PROGRESS.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8", newline="\n")


def lesson_list(f: Folder) -> str:
    lines = [LIST_START, "## Lessons", ""]
    for ci, chapter in enumerate(f.chapters, 1):
        if not f.flat:
            chapter_index = f"{chapter.folder}/index.md"
            heading = f"{ci}. {chapter.title}"
            if exists(chapter_index):
                rel = chapter_index.removeprefix(f.folder + "/")
                heading = f"{ci}. [{chapter.title}]({rel})"
            lines += [f"### {heading}", ""]
        for li, lesson in enumerate(chapter.lessons, 1):
            notes = []
            if "optional" in lesson.flags:
                notes.append("optional")
            if "fast" in lesson.flags:
                notes.append("fast path")
            rel = lesson.path.removeprefix(f.folder + "/")
            text = f"[{lesson.title}]({rel})" if lesson.exists else f"{lesson.title} (not written yet)"
            if notes:
                text += f" ({', '.join(notes)})"
            lines.append(f"{li}. {text}")
        lines.append("")
    lines.append(LIST_END)
    return "\n".join(lines)


def write_folder_index(f: Folder) -> None:
    path = DOCS / f.folder / "index.md"
    block = lesson_list(f)
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        stub = [
            f"# {f.title}",
            "",
            f.summary,
            "",
            f"Before this folder: {f.before}",
            "",
            "The lessons and chapter cheat sheets for this folder are written in reading order.",
            "",
            block,
            "",
        ]
        path.write_text("\n".join(stub), encoding="utf-8", newline="\n")
        return
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(LIST_START) + r".*?" + re.escape(LIST_END), re.S)
    if pattern.search(text):
        text = pattern.sub(lambda _: block, text)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    global TRACKED
    if "--tracked" in sys.argv[1:]:
        TRACKED = tracked_paths()
    folders = load_folders()
    for f in folders:
        write_folder_index(f)
    write_progress(folders)
    write_nav(folders)
    total = sum(len(f.all_lessons()) for f in folders)
    written = sum(1 for f in folders for lesson in f.all_lessons() if lesson.exists)
    print(f"{len(folders)} folders, {written} of {total} lessons written; nav, progress and folder lists updated")


if __name__ == "__main__":
    main()
