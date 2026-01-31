#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
from pathlib import Path
from typing import Set

WHITELIST = {"Root.md", "Informatics.md", "Economics.md"}
TRASH_DIR_NAME = "_TRASH"

# Matches [[File]] or [[File|Alias]]
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def find_markdown_files(root: Path) -> Set[Path]:
    return {p for p in root.rglob("*.md") if p.is_file()}


def extract_wikilinks(text: str) -> Set[str]:
    return {m.group(1).strip() for m in WIKI_LINK_PATTERN.finditer(text)}


def normalize_link_target(link_text: str) -> str:
    # Obsidian link targets can include subpaths like "folder/note"
    # We only care about the file name component when comparing.
    link_path = Path(link_text)
    name = link_path.name
    if not name.lower().endswith(".md"):
        name += ".md"
    return name


def main() -> int:
    root = Path.cwd()
    md_files = find_markdown_files(root)

    link_targets: Set[str] = set()
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        for link in extract_wikilinks(content):
            link_targets.add(normalize_link_target(link))

    candidates = []
    for md_file in md_files:
        if md_file.name in WHITELIST:
            continue
        if md_file.name not in link_targets:
            candidates.append(md_file)

    if not candidates:
        print("孤立したノートは見つかりませんでした。")
        return 0

    print("以下のファイルが孤立しています:")
    for f in sorted(candidates):
        print(f"- {f}")

    confirm = input("実行しますか？ (y/n): ").strip().lower()
    if confirm != "y":
        print("中止しました。")
        return 0

    trash_dir = root / TRASH_DIR_NAME
    trash_dir.mkdir(exist_ok=True)

    for f in candidates:
        destination = trash_dir / f.name
        if destination.exists():
            base = destination.stem
            suffix = destination.suffix
            i = 1
            while True:
                alt = trash_dir / f"{base} ({i}){suffix}"
                if not alt.exists():
                    destination = alt
                    break
                i += 1
        shutil.move(str(f), str(destination))
        print(f"{f} を _TRASH に移動しました")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
