from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


SECTION_PATTERN = re.compile(r"^\d{2} - .+\.md$")
PLACEHOLDER_LINES = {
    "Document Title",
    "Subtitle or working description",
}


def find_section_files(source_dir: Path) -> list[Path]:
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    section_files = sorted(
        path
        for path in source_dir.iterdir()
        if path.is_file() and SECTION_PATTERN.match(path.name)
    )
    if not section_files:
        raise FileNotFoundError(f"No section files found in: {source_dir}")
    return section_files


def is_placeholder_title_block(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return any(line in PLACEHOLDER_LINES for line in lines)


def parse_title_block(text: str) -> tuple[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError(
            "Title block must contain at least two non-empty lines: title and subtitle."
        )
    return lines[0], lines[1]


def load_title_block(title_file: Path | None, allow_placeholder: bool = False) -> str:
    if title_file is None or not title_file.exists():
        raise FileNotFoundError(
            "Title block file not found. Create report-body/title-block.md from assets/title-block-template.md."
        )

    text = title_file.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(
            "Title block is empty. Provide a real title and subtitle before assembly."
        )
    if not allow_placeholder and is_placeholder_title_block(text):
        raise ValueError(
            "Title block still contains placeholder title or subtitle text. Replace both lines before assembly."
        )
    return text + "\n\n"


def build_title_metadata(title_block: str) -> str:
    title, subtitle = parse_title_block(title_block)
    return "\n".join(
        [
            "---",
            f"title: {json.dumps(title)}",
            f"subtitle: {json.dumps(subtitle)}",
            "---",
        ]
    )


def build_report_text(section_files: list[Path], title_block: str) -> str:
    parts: list[str] = []
    parts.append(build_title_metadata(title_block.rstrip("\n")))
    for path in section_files:
        parts.append(path.read_text(encoding="utf-8").rstrip())
    return "\n\n".join(parts) + "\n"


def write_report(output_file: Path, report_text: str) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report_text, encoding="utf-8")


def sync_directory(source_dir: Path, output_dir: Path) -> None:
    if not source_dir.exists():
        return
    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(source_dir, output_dir)


def copy_file(source_file: Path, output_file: Path) -> None:
    if not source_file.exists():
        return
    output_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, output_file)


def assemble_report(
    source_dir: Path,
    output_file: Path,
    title_block: str | None = None,
    title_file: Path | None = None,
    allow_placeholder_title_block: bool = False,
    sync_media: bool = True,
    copy_bibliography: bool = True,
) -> None:
    section_files = find_section_files(source_dir)
    resolved_title_block = (
        title_block
        if title_block is not None
        else load_title_block(title_file, allow_placeholder=allow_placeholder_title_block)
    )
    report_text = build_report_text(section_files, title_block=resolved_title_block)
    write_report(output_file, report_text)

    if sync_media:
        sync_directory(source_dir / "media", output_file.parent / "media")
    if copy_bibliography:
        copy_file(source_dir / "references.bib", output_file.parent / "references.bib")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    project_root = Path.cwd()
    parser = argparse.ArgumentParser(
        description="Assemble the split report-body markdown files into a single combined report."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=project_root / "report-body",
        help="Directory containing the ordered report markdown files.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=project_root / "full" / "combined-report.md",
        help="Path to the combined output markdown file.",
    )
    parser.add_argument(
        "--title-file",
        type=Path,
        default=project_root / "report-body" / "title-block.md",
        help="Markdown file containing the title block for the combined output.",
    )
    parser.add_argument(
        "--allow-placeholder-title-block",
        action="store_true",
        help="Allow template placeholder title-block text. Use only for scaffolding, not for real output.",
    )
    parser.add_argument(
        "--skip-media",
        action="store_true",
        help="Do not sync the media directory beside the combined output.",
    )
    parser.add_argument(
        "--skip-bibliography",
        action="store_true",
        help="Do not copy references.bib beside the combined output.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    assemble_report(
        source_dir=args.source_dir,
        output_file=args.output_file,
        title_file=args.title_file,
        allow_placeholder_title_block=args.allow_placeholder_title_block,
        sync_media=not args.skip_media,
        copy_bibliography=not args.skip_bibliography,
    )
    print(f"Assembled {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
