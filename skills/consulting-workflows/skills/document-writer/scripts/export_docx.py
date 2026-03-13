#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the assembled markdown report to a packaged document using Pandoc."
    )
    parser.add_argument(
        "--input",
        default="full/combined-report.md",
        help="Markdown input file. Defaults to full/combined-report.md.",
    )
    parser.add_argument(
        "--output",
        default="full/combined-report",
        help="Document output path. If no suffix is provided, .docx is added automatically. Defaults to full/combined-report.",
    )
    parser.add_argument(
        "--reference-doc",
        default=None,
        help="Optional path to the reference document. Defaults to the target project's assets/reference.docx, then the bundled skill reference document.",
    )
    parser.add_argument(
        "--bibliography",
        default=None,
        help="Optional bibliography path. Defaults to full/references.bib, then report-body/references.bib if present.",
    )
    parser.add_argument(
        "--assemble",
        action="store_true",
        help="Run scripts/assemble_report.py before exporting.",
    )
    parser.add_argument(
        "--no-citeproc",
        action="store_true",
        help="Disable Pandoc citeproc.",
    )
    parser.set_defaults(toc=True)
    parser.add_argument(
        "--toc",
        dest="toc",
        action="store_true",
        help="Include a table of contents in the packaged document output.",
    )
    parser.add_argument(
        "--no-toc",
        dest="toc",
        action="store_false",
        help="Do not include a table of contents in the packaged document output.",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"[export_docx] {message}", file=sys.stderr)
    raise SystemExit(1)


def bundled_reference_doc() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "reference.docx"


def build_pandoc_env() -> dict[str, str]:
    env = os.environ.copy()

    if shutil.which("rsvg-convert", path=env.get("PATH")):
        return env

    candidates = [
        Path("/opt/homebrew/bin/rsvg-convert"),
        Path("/usr/local/bin/rsvg-convert"),
    ]
    candidates.extend(Path("/opt/homebrew/Cellar/librsvg").glob("*/bin/rsvg-convert"))

    for candidate in candidates:
        if candidate.exists():
            current = env.get("PATH", "")
            env["PATH"] = f"{candidate.parent}:{current}" if current else str(candidate.parent)
            return env

    return env


def run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    result = subprocess.run(cmd, check=False, env=env)
    if result.returncode != 0:
        fail(f"Command failed with exit code {result.returncode}: {' '.join(cmd)}")


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = {"w": W_NS}
W = f"{{{W_NS}}}"


def resolve_bibliography(explicit: str | None) -> Path | None:
    if explicit:
        path = Path(explicit)
        if not path.exists():
            fail(f"Bibliography not found: {path}")
        return path

    for candidate in (Path("full/references.bib"), Path("report-body/references.bib")):
        if candidate.exists():
            return candidate

    return None


def resolve_reference_doc(explicit: str | None) -> Path:
    candidates: list[Path] = []

    if explicit is not None:
        candidates.append(Path(explicit))
    else:
        candidates.append(Path("assets/reference.docx"))
        candidates.append(bundled_reference_doc())

    for candidate in candidates:
        if candidate.exists():
            return candidate

    fail(
        "Reference document not found. Provide --reference-doc or place assets/reference.docx in the target project."
    )
    raise AssertionError("unreachable")


def resolve_output_path(explicit: str) -> Path:
    path = Path(explicit)
    if path.suffix:
        return path
    return path.with_suffix(".docx")


def move_toc_after_executive_summary(docx_path: Path) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with zipfile.ZipFile(docx_path) as archive:
            archive.extractall(temp_path)

        document_xml = temp_path / "word" / "document.xml"
        tree = ET.parse(document_xml)
        root = tree.getroot()
        body = root.find("w:body", XML_NS)
        if body is None:
            return

        children = list(body)
        toc_index = next(
            (
                index
                for index, child in enumerate(children)
                if child.tag == f"{W}sdt"
                and child.find(".//w:docPartGallery[@w:val='Table of Contents']", XML_NS)
                is not None
            ),
            None,
        )
        if toc_index is None:
            return

        bookmark_id = None
        for child in children:
            if (
                child.tag == f"{W}bookmarkStart"
                and child.attrib.get(f"{W}name") == "executive-summary"
            ):
                bookmark_id = child.attrib.get(f"{W}id")
                break

        if bookmark_id is None:
            return

        toc_element = children[toc_index]
        body.remove(toc_element)
        children = list(body)

        insert_after = next(
            (
                index
                for index, child in enumerate(children)
                if child.tag == f"{W}bookmarkEnd"
                and child.attrib.get(f"{W}id") == bookmark_id
            ),
            None,
        )
        if insert_after is None:
            return

        body.insert(insert_after + 1, toc_element)
        tree.write(document_xml, encoding="UTF-8", xml_declaration=True)

        rebuilt = docx_path.with_suffix(".tmp.docx")
        with zipfile.ZipFile(rebuilt, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(temp_path.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(temp_path))
        rebuilt.replace(docx_path)


def main() -> None:
    args = parse_args()

    if shutil.which("pandoc") is None:
        fail("Pandoc is not installed or not on PATH.")

    pandoc_env = build_pandoc_env()

    if args.assemble:
        assemble_script = Path(__file__).resolve().parent / "assemble_report.py"
        run([sys.executable, str(assemble_script)], env=pandoc_env)

    input_path = Path(args.input)
    output_path = resolve_output_path(args.output)
    reference_doc = resolve_reference_doc(args.reference_doc)
    bibliography = resolve_bibliography(args.bibliography)

    if not input_path.exists():
        fail(f"Input markdown not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    resource_paths = []
    for candidate in (
        str(input_path.parent),
        ".",
        "full",
        "full/media",
        "report-body",
        "report-body/media",
    ):
        if candidate not in resource_paths:
            resource_paths.append(candidate)

    cmd = [
        "pandoc",
        str(input_path),
        "--from",
        "markdown",
        "--to",
        "docx",
        "--output",
        str(output_path),
        "--reference-doc",
        str(reference_doc),
        "--resource-path",
        ":".join(resource_paths),
    ]

    if bibliography is not None:
        cmd.extend(["--bibliography", str(bibliography)])
        if not args.no_citeproc:
            cmd.append("--citeproc")

    if args.toc:
        cmd.extend(["--toc", "--toc-depth", "1"])

    run(cmd, env=pandoc_env)
    if args.toc:
        move_toc_after_executive_summary(output_path)
    print(f"[export_docx] Wrote {output_path}")


if __name__ == "__main__":
    main()
