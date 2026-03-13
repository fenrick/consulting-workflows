#!/usr/bin/env python3
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package this skill folder into a portable zip archive."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Zip output path. Defaults to ./dist/<skill-name>.zip.",
    )
    return parser.parse_args()


def iter_files(skill_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(skill_root.rglob("*")):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        if path.suffix in {".pyc", ".pyo", ".zip"}:
            continue
        if any(part.startswith(".") for part in path.relative_to(skill_root).parts):
            continue
        files.append(path)
    return files


def main() -> None:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    output = (
        Path(args.output).resolve()
        if args.output
        else (Path.cwd() / "dist" / f"{skill_root.name}.zip").resolve()
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in iter_files(skill_root):
            archive.write(path, path.relative_to(skill_root.parent))

    print(output)


if __name__ == "__main__":
    main()
