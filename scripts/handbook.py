#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


AUTO_TOPICS_START = "<!-- AUTO-GEN:TOPICS:START -->"
AUTO_TOPICS_END = "<!-- AUTO-GEN:TOPICS:END -->"
AUTO_PAGES_START = "<!-- AUTO-GEN:PAGES:START -->"
AUTO_PAGES_END = "<!-- AUTO-GEN:PAGES:END -->"


MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")
MD_HEADING_RE = re.compile(r"^\s*#\s+(.+?)\s*$")
FENCED_CODE_RE = re.compile(r"```[\s\S]*?```", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


@dataclass(frozen=True)
class LinkProblem:
    source: Path
    target_raw: str
    resolved: Optional[Path]
    reason: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def first_h1_title(md_path: Path) -> Optional[str]:
    try:
        for line in read_text(md_path).splitlines():
            m = MD_HEADING_RE.match(line)
            if m:
                return m.group(1).strip()
    except OSError:
        return None
    return None


def replace_block(text: str, start_marker: str, end_marker: str, new_block: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"missing markers: {start_marker} ... {end_marker}")
    before = text[: start + len(start_marker)]
    after = text[end:]
    return before + "\n" + new_block.rstrip() + "\n" + after


def iter_topics(handbook_dir: Path) -> list[Path]:
    topics: list[Path] = []
    for child in sorted(handbook_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name in {"docs", "plans", "assets"}:
            continue
        if (child / "README.md").exists():
            topics.append(child)
    return topics


def iter_topic_pages(topic_dir: Path) -> list[Path]:
    pages: list[Path] = []
    for p in sorted(topic_dir.glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        pages.append(p)
    return pages


def format_md_list(items: Iterable[tuple[str, str]]) -> str:
    lines = []
    for title, rel_link in items:
        lines.append(f"- [{title}]({rel_link})")
    return "\n".join(lines)


def gen_index(handbook_dir: Path) -> None:
    hb_readme = handbook_dir / "README.md"
    hb_text = read_text(hb_readme)

    topics = iter_topics(handbook_dir)
    topic_items: list[tuple[str, str]] = []
    for t in topics:
        title = first_h1_title(t / "README.md") or t.name
        topic_items.append((title, f"./{t.name}/"))

    hb_text = replace_block(hb_text, AUTO_TOPICS_START, AUTO_TOPICS_END, format_md_list(topic_items))
    write_text(hb_readme, hb_text)

    for t in topics:
        t_readme = t / "README.md"
        text = read_text(t_readme)
        pages = iter_topic_pages(t)
        page_items: list[tuple[str, str]] = []
        for p in pages:
            title = first_h1_title(p) or p.stem
            page_items.append((title, f"./{p.name}"))
        text = replace_block(text, AUTO_PAGES_START, AUTO_PAGES_END, format_md_list(page_items))
        write_text(t_readme, text)


def is_external_link(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def normalize_link_target(target: str) -> str:
    target = target.strip()
    if not target:
        return target
    # Drop title in markdown like (path "title") is not supported here; keep simple.
    return target


def resolve_relative_link(source_md: Path, target: str) -> Optional[Path]:
    target = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not target or target.startswith("#"):
        return None
    if is_external_link(target):
        return None
    if target.startswith("/"):
        # Repo-root relative
        return repo_root() / target.lstrip("/")
    return (source_md.parent / target).resolve()


def check_links(md_files: list[Path]) -> list[LinkProblem]:
    problems: list[LinkProblem] = []
    root = repo_root().resolve()

    for md in md_files:
        try:
            text = read_text(md)
        except OSError as e:
            problems.append(LinkProblem(md, "", None, f"read failed: {e}"))
            continue

        # Ignore links that appear in code (fenced or inline) to avoid false positives
        text = FENCED_CODE_RE.sub("", text)
        text = INLINE_CODE_RE.sub("", text)

        for raw in MD_LINK_RE.findall(text):
            target = normalize_link_target(raw)
            if is_external_link(target) or target.startswith("#") or not target.strip():
                continue

            resolved = resolve_relative_link(md, target)
            if resolved is None:
                continue

            # Must stay within repo (avoid following to outside)
            try:
                resolved.relative_to(root)
            except ValueError:
                problems.append(LinkProblem(md, target, resolved, "link resolves outside repo"))
                continue

            # Directory link with trailing slash is allowed if dir exists
            if target.endswith("/"):
                if not resolved.exists() or not resolved.is_dir():
                    problems.append(LinkProblem(md, target, resolved, "directory does not exist"))
                continue

            # File link
            if not resolved.exists():
                # Allow linking to a directory without trailing slash (common mistake, but exists)
                if resolved.with_suffix("").exists():
                    problems.append(LinkProblem(md, target, resolved, "missing file (did you mean a directory or add trailing / ?)"))
                else:
                    problems.append(LinkProblem(md, target, resolved, "target does not exist"))
                continue

    return problems


def list_md_files(base: Path) -> list[Path]:
    files: list[Path] = []
    for p in base.rglob("*.md"):
        # Skip git internals if any
        if ".git" in p.parts:
            continue
        files.append(p)
    return sorted(files)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="handbook.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("gen", help="Generate handbook indexes")
    p_gen.add_argument("--handbook-dir", default="handbook", help="handbook directory path")

    p_check = sub.add_parser("check", help="Check markdown links")
    p_check.add_argument("--path", default=".", help="directory to scan for .md files")

    args = parser.parse_args(argv)
    root = repo_root()

    if args.cmd == "gen":
        hb_dir = (root / args.handbook_dir).resolve()
        gen_index(hb_dir)
        return 0

    if args.cmd == "check":
        base = (root / args.path).resolve()
        md_files = list_md_files(base)
        problems = check_links(md_files)
        if problems:
            print("Markdown 链接校验失败：", file=sys.stderr)
            for pr in problems:
                resolved = str(pr.resolved) if pr.resolved else "-"
                print(f"- {pr.source.relative_to(root)} -> {pr.target_raw} ({pr.reason}) [{resolved}]", file=sys.stderr)
            return 2
        print(f"Markdown 链接校验通过：{len(md_files)} 个文件，0 个问题")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

