"""Regenerate the generated parts of docs/reference/glossary.md and common-mistakes.md.

Reads tools/lessons.yml (reading order), then for every lesson file that exists:
  - glossary: bold terms defined in the "## Key terms" section
  - common mistakes: paragraphs starting with "Watch out:"

Only the text between <!-- generated:start --> and <!-- generated:end --> is replaced.
Run from anywhere:  .venv/Scripts/python tools/build_reference.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
REF = DOCS / "reference"
START, END = "<!-- generated:start -->", "<!-- generated:end -->"

SKIP_FIRST_WORDS = {"a", "an", "the", "your", "our", "each", "every", "one", "this", "that", "in", "on", "as"}
VERBS = r"(?:is|are|means|refers|stands|has|have|names|holds|writes|identifies|splits|describes|takes|gives|runs)"


def lessons():
    """Yield (folder_name, folder_title, chapter_title, lesson_title, relative_path)."""
    data = yaml.safe_load((ROOT / "tools" / "lessons.yml").read_text(encoding="utf-8"))
    for f in data["folders"]:
        name = f["folder"]
        if "lessons" in f:
            groups = [("", name, f["lessons"])]
        else:
            groups = [
                (c["title"], f"{name}/{ci:02d}-{c['slug']}", c["lessons"])
                for ci, c in enumerate(f["chapters"], 1)
            ]
        for ctitle, cfolder, entries in groups:
            for li, e in enumerate(entries, 1):
                yield name, f["title"], ctitle, e[1], f"{cfolder}/{li:02d}-{e[0]}.md"


def link(path: str) -> str:
    return os.path.relpath(DOCS / path, REF).replace("\\", "/")


def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    n = re.search(r"^## ", rest, re.M)
    return rest[: n.start()] if n else rest


def mask(text: str):
    """Hide code spans, links and math so sentence splitting does not break inside them."""
    saved: list[str] = []

    def keep(m):
        saved.append(m.group(0))
        return f"\x00{len(saved) - 1}\x00"

    text = re.sub(r"`[^`]*`|\$[^$]*\$|\[[^\]]*\]\([^)]*\)", keep, text)
    return text, saved


def unmask(text: str, saved: list[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: saved[int(m.group(1))], text)


def strip_citations(s: str) -> str:
    # "([RFC 791](url), [MDN](url))" and "([source](url))"
    s = re.sub(r"\s*\((?:\[[^\]]*\]\([^)]*\)[,;]?\s*)+\)", "", s)
    # trailing bare "[RFC 791](url)" is kept as plain text
    return re.sub(r"\s+([.,;])", r"\1", s).strip()


def split_sentences(par: str) -> list[str]:
    par, saved = mask(par)
    par = re.sub(r"\b(e\.g|i\.e|etc|vs)\.", lambda m: m.group(0).replace(".", "\x01"), par)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z*\x00])", par)
    return [unmask(p.replace("\x01", "."), saved) for p in parts]


SKIPPED: list[tuple[str, str]] = []


def clean_term(term: str, text: str) -> str:
    """Lower-case a sentence-initial capital when the lesson also uses the lower-case form."""
    if re.fullmatch(r"[A-Z][a-z]+(?:[ -][a-z]+)*", term) and re.search(
        r"(?<![\w*])" + re.escape(term[0].lower() + term[1:]) + r"(?!\w)", text
    ):
        return term[0].lower() + term[1:]
    return term


def extract_terms(text: str) -> list[tuple[str, str]]:
    body = section(text, "Key terms")
    out = []
    # drop tables, code fences, html tags
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    for par in re.split(r"\n\s*\n", body):
        par = par.strip()
        if not par or par.startswith(("|", "<", "-", "!", "#", "$$")):
            continue
        par = " ".join(par.split())
        for sent in split_sentences(par):
            for m in re.finditer(r"\*\*([^*]+)\*\*", sent):
                term = m.group(1).strip()
                before = re.sub(r"\*\*", "", sent[: m.start()]).split()
                after = sent[m.end():].lstrip()
                at_start = len(before) <= 1 and (not before or before[0].lower() in SKIP_FIRST_WORDS)
                if not (at_start or re.match(VERBS + r"\b", after)):
                    continue
                d = strip_citations(re.sub(r"\*\*", "", sent))
                if re.search(r"\b(those|others|the others?)\b|^(It|Its|They|Their|This|These)\b", d):
                    SKIPPED.append((term, d))  # sentence depends on context the glossary line lacks
                    continue
                if len(d) > 220 and "; " in d[60:]:
                    d = d[: d.index("; ", 60)] + "."
                term = clean_term(term, text)
                out.append((term, d))
    return out


def extract_mistakes(text: str) -> list[str]:
    out = []
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    for par in re.split(r"\n\s*\n", body):
        par = " ".join(par.split())
        if par.startswith("Watch out:"):
            item = strip_citations(par[len("Watch out:"):].strip())
            out.append(item[:1].upper() + item[1:] if item[:1].isalpha() else item)
    return out


def replace_generated(path: Path, generated: str) -> None:
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n\n{generated.strip()}\n\n{END}"
    if START in text and END in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def fix_links(text: str, rel: str) -> str:
    """Links inside a lesson are relative to the lesson; make them relative to docs/reference."""

    def repl(m):
        target = m.group(2)
        if re.match(r"[a-z]+:|#|/", target):
            return m.group(0)
        path, _, frag = target.partition("#")
        full = (DOCS / rel).parent / path
        new = os.path.relpath(full.resolve(), REF.resolve()).replace("\\", "/")
        return f"[{m.group(1)}]({new}{'#' + frag if frag else ''})"

    return re.sub(r"\[([^\]]*)\]\(([^)]*)\)", repl, text)


def main() -> None:
    terms: dict[str, list] = {}
    display: dict[str, str] = {}
    mistakes: dict[str, list] = {}
    folder_titles: dict[str, str] = {}
    n_mistakes = 0
    for folder, ftitle, ctitle, title, rel in lessons():
        p = DOCS / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for term, d in extract_terms(text):
            key = term.lower().strip("`")
            display.setdefault(key, term)
            entries = terms.setdefault(key, [])
            if all(e[2] != rel for e in entries):
                entries.append((fix_links(d, rel), title, rel))
        for m in extract_mistakes(text):
            folder_titles[folder] = ftitle
            mistakes.setdefault(folder, []).append((fix_links(m, rel), title, rel))
            n_mistakes += 1

    lines = []
    letters = sorted({(k[0].upper() if k[0].isalpha() else "#") for k in terms}, key=lambda c: (c == "#", c))
    for letter in letters:
        lines.append(f"## {letter}\n")
        keys = sorted(
            (k for k in terms if (k[0].upper() if k[0].isalpha() else "#") == letter),
            key=lambda k: k,
        )
        for k in keys:
            (d, title, rel), *others = terms[k]
            line = f"- **{display[k]}**: {d} ([{title}]({link(rel)}))"
            if others:
                line += " Also in: " + ", ".join(f"[{t}]({link(r)})" for _, t, r in others) + "."
            lines.append(line)
        lines.append("")
    replace_generated(REF / "glossary.md", "\n".join(lines))

    lines = []
    for folder, items in mistakes.items():
        lines.append(f"## {folder_titles[folder]}\n")
        for m, title, rel in items:
            lines.append(f"- {m} ([{title}]({link(rel)}))")
        lines.append("")
    replace_generated(REF / "common-mistakes.md", "\n".join(lines))

    print(f"skipped context-dependent sentences: {len(SKIPPED)}")
    print(f"glossary terms: {len(terms)}  (duplicates merged: {sum(len(v) - 1 for v in terms.values())})")
    print(f"common mistakes: {n_mistakes} in {len(mistakes)} folders")


if __name__ == "__main__":
    sys.exit(main())
