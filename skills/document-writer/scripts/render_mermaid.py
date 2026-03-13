#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_WIDTH = 2400
DEFAULT_SCALE = 4


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or f"command failed: {' '.join(cmd)}")


def render(input_file: Path, output_file: Path, config_file: Path, width: int, scale: int, background: str) -> None:
    cmd = [
        "npx",
        "mmdc",
        "--input",
        str(input_file),
        "--output",
        str(output_file),
        "--configFile",
        str(config_file),
        "--width",
        str(width),
        "--scale",
        str(scale),
        "--backgroundColor",
        background,
    ]
    run(cmd)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Mermaid diagrams to high-resolution PNG and SVG outputs."
    )
    parser.add_argument("input", type=Path, help="Path to the Mermaid source file (.mmd).")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory for generated assets. Defaults to the input file directory.",
    )
    parser.add_argument(
        "--basename",
        help="Base output filename without extension. Defaults to the input filename stem.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional Mermaid config file. Defaults to assets/mermaid/mermaid-config.json.",
    )
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Render width in pixels.")
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE, help="Render scale multiplier.")
    parser.add_argument(
        "--background",
        default="transparent",
        help="Background color passed to Mermaid CLI. Defaults to transparent.",
    )
    parser.add_argument(
        "--png-only",
        action="store_true",
        help="Generate only the PNG output.",
    )
    parser.add_argument(
        "--svg-only",
        action="store_true",
        help="Generate only the SVG output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.png_only and args.svg_only:
        raise SystemExit("Choose only one of --png-only or --svg-only.")

    if shutil.which("npx") is None:
        raise SystemExit("npx is required. Run `npm install` in the repo root first.")

    input_file = args.input.resolve()
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")

    script_dir = Path(__file__).resolve().parent
    default_config = script_dir.parent / "assets" / "mermaid" / "mermaid-config.json"
    config_file = (args.config or default_config).resolve()
    if not config_file.exists():
        raise SystemExit(f"Config file not found: {config_file}")

    output_dir = (args.output_dir or input_file.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.basename or input_file.stem

    outputs: list[Path] = []
    if not args.svg_only:
        outputs.append(output_dir / f"{basename}.png")
    if not args.png_only:
        outputs.append(output_dir / f"{basename}.svg")

    for output_file in outputs:
        render(input_file, output_file, config_file, args.width, args.scale, args.background)
        print(f"Rendered {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
