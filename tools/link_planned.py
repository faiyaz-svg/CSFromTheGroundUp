"""Turn planned-lesson comments into real links once the lesson exists.

Lessons mention a lesson that hasn't been written yet like this:

    see long division<!-- link: ../01-elementary/07-long-division.md -->

When the target file exists, this script rewrites it as

    see [long division](../01-elementary/07-long-division.md)

The link text is the text just before the comment that matches the target's
title (its H1, or its title in tools/lessons.yml), ignoring case. Comments it
can't match are listed so they can be fixed by hand.

Run from the repo root:  .venv/Scripts/python tools/link_planned.py [--dry-run] [--tracked]
With --tracked, only files committed to git are edited or linked to, so
drafts on disk are left alone.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
COMMENT = re.compile(r"<!-- link: ([^ ]+?) -->")


def lesson_titles() -> dict[Path, str]:
    """Map each planned lesson path to its title from lessons.yml."""
    data = yaml.safe_load((ROOT / "tools" / "lessons.yml").read_text(encoding="utf-8"))
    titles = {}
    for f in data["folders"]:
        if "lessons" in f:
            for i, entry in enumerate(f["lessons"], 1):
                titles[(DOCS / f["folder"] / f"{i:02d}-{entry[0]}.md").resolve()] = entry[1]
        else:
            for ci, c in enumerate(f["chapters"], 1):
                for li, entry in enumerate(c["lessons"], 1):
                    path = DOCS / f["folder"] / f"{ci:02d}-{c['slug']}" / f"{li:02d}-{entry[0]}.md"
                    titles[path.resolve()] = entry[1]
    return titles


def tracked_files() -> set[Path]:
    out = subprocess.run(
        ["git", "ls-files", "docs"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return {(ROOT / line).resolve() for line in out.splitlines()}


def h1_title(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def candidates(target: Path, titles: dict[Path, str]) -> list[str]:
    names = []
    for title in (h1_title(target), titles.get(target.resolve())):
        if title:
            names.append(title)
            # "The Pythagorean theorem" is often written "the Pythagorean theorem"
            if title.lower().startswith("the "):
                names.append(title[4:])
    return sorted(set(names), key=len, reverse=True)


def process(
    md: Path, titles: dict[Path, str], dry_run: bool, tracked: set[Path] | None
) -> tuple[int, list[str]]:
    text = md.read_text(encoding="utf-8")
    out, pos, linked, problems = [], 0, 0, []
    for m in COMMENT.finditer(text):
        rel = m.group(1)
        target = (md.parent / rel).resolve()
        before = text[pos : m.start()]
        if not target.is_file() or (tracked is not None and target not in tracked):
            out.append(text[pos : m.end()])
            pos = m.end()
            continue
        for name in candidates(target, titles):
            if before.lower().endswith(name.lower()):
                start = len(before) - len(name)
                out.append(before[:start] + f"[{before[start:]}]({rel})")
                linked += 1
                break
        else:
            line_no = text.count("\n", 0, m.start()) + 1
            context = before[-50:].replace("\n", " ")
            problems.append(f"{md.relative_to(ROOT)}:{line_no}: no title match before '{rel}' (...{context})")
            out.append(before + m.group(0))
        pos = m.end()
    out.append(text[pos:])
    if linked and not dry_run:
        md.write_text("".join(out), encoding="utf-8", newline="\n")
    return linked, problems


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    tracked = tracked_files() if "--tracked" in sys.argv else None
    titles = lesson_titles()
    total, problems = 0, []
    for md in sorted(DOCS.rglob("*.md")):
        if tracked is not None and md.resolve() not in tracked:
            continue
        linked, found = process(md, titles, dry_run, tracked)
        if linked:
            print(f"{md.relative_to(ROOT)}: {linked} link(s) {'would be ' if dry_run else ''}added")
        total += linked
        problems += found
    print(f"{total} planned link(s) {'would be ' if dry_run else ''}turned into real links")
    if problems:
        print("\nNeeds a hand edit (target exists, but the text before the comment isn't its title):")
        print("\n".join(problems))


if __name__ == "__main__":
    main()
