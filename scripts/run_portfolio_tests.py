#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

ALLOWED_OUTPUT_PREFIXES = (
    "tracking/",
    "inputs/",
    "report-body/",
    "full/",
)

EXPECTED_SKILLS = {
    "consulting-workflow-orchestrator",
    "input-evidence-cataloger",
    "evidence-consistency-auditor",
    "brief-storyline-architect",
    "report-storyboard-builder",
    "presentation-storyboard-builder",
    "workshop-writeup-composer",
    "document-writer",
}

REQUIRED_TRACKING_FILES = {
    "document-brief.md",
    "source-register.md",
    "review-notebook.md",
    "findings-workbook.md",
    "open-questions.md",
}

PROHIBITED_SKILL_PATTERNS = (
    r"\bdocx skill\b",
    r"\bnode\b.*\b(docx|document)\b",
)


class TestFailure(RuntimeError):
    pass


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


def assert_true(condition: bool, msg: str) -> None:
    if not condition:
        raise TestFailure(msg)


def find_skill_files() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def parse_skill_name(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("name: "):
            return line.split("name: ", 1)[1].strip()
    raise TestFailure("Missing `name:` in SKILL.md frontmatter")


def parse_output_paths_in_section(text: str, section_heading: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == section_heading:
            start = idx + 1
            break
    if start is None:
        return []
    end = len(lines)
    for idx in range(start, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    section_text = "\n".join(lines[start:end])
    pattern = re.compile(r"^\d+\.\s+`([^`]+)`", re.MULTILINE)
    return pattern.findall(section_text)


def test_structure_lint() -> None:
    result = run([sys.executable, str(ROOT / "scripts" / "validate_skill_portfolio.py")])
    assert_true(result.returncode == 0, f"Structure lint failed:\n{result.stderr}{result.stdout}")


def test_skill_set_complete() -> None:
    found = set()
    for path in find_skill_files():
        found.add(parse_skill_name(path.read_text(encoding="utf-8")))
    missing = EXPECTED_SKILLS - found
    assert_true(not missing, f"Missing expected skills: {sorted(missing)}")


def test_output_contracts() -> None:
    for path in find_skill_files():
        text = path.read_text(encoding="utf-8")
        name = parse_skill_name(text)
        if name == "document-writer":
            # document-writer has a broader workflow contract and doesn't use Required outputs.
            continue
        if name == "consulting-workflow-orchestrator":
            assert_true(
                "## Orchestration outputs" in text,
                f"{name}: missing `## Orchestration outputs` section",
            )
            outputs = parse_output_paths_in_section(text, "## Orchestration outputs")
        else:
            assert_true(
                "## Required outputs" in text,
                f"{name}: missing `## Required outputs` section",
            )
            outputs = parse_output_paths_in_section(text, "## Required outputs")
        assert_true(outputs, f"{name}: no required output paths detected")
        for out in outputs:
            assert_true(
                out.startswith(ALLOWED_OUTPUT_PREFIXES),
                f"{name}: invalid output path `{out}` (must live under tracking/inputs/report-body/full)",
            )


def test_orchestrator_pipeline_consistency() -> None:
    orchestrator = SKILLS_DIR / "consulting-workflow-orchestrator" / "SKILL.md"
    text = orchestrator.read_text(encoding="utf-8")
    for skill_name in EXPECTED_SKILLS - {"document-writer"}:
        assert_true(skill_name in text, f"orchestrator: missing `{skill_name}` in pipeline")
    assert_true("document-writer" in text, "orchestrator: missing `document-writer` in pipeline")


def test_document_writer_e2e() -> None:
    fixture = ROOT / "tests" / "fixtures" / "document-writer"
    dw_dir = SKILLS_DIR / "document-writer" / "scripts"

    fixture_report_body = fixture / "report-body"
    assert_true(
        fixture_report_body.exists(),
        f"missing fixture directory: {fixture_report_body}",
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        shutil.copytree(fixture_report_body, tmpdir / "report-body")
        (tmpdir / "full").mkdir(parents=True, exist_ok=True)
        (tmpdir / "tracking").mkdir(parents=True, exist_ok=True)

        assemble = run([sys.executable, str(dw_dir / "assemble_report.py")], cwd=tmpdir)
        assert_true(assemble.returncode == 0, f"assemble_report failed:\n{assemble.stderr}{assemble.stdout}")

        combined = (tmpdir / "full" / "combined-report.md").read_text(encoding="utf-8")
        assert_true('title: "Test Title"' in combined, "combined markdown missing title metadata")
        assert_true('subtitle: "Test Subtitle"' in combined, "combined markdown missing subtitle metadata")

        export = run(
            [sys.executable, str(dw_dir / "export_docx.py"), "--output", str(tmpdir / "full" / "report")],
            cwd=tmpdir,
        )
        assert_true(export.returncode == 0, f"export_docx failed:\n{export.stderr}{export.stdout}")

        docx_path = tmpdir / "full" / "report.docx"
        assert_true(docx_path.exists(), "export_docx did not create report.docx")

        with zipfile.ZipFile(docx_path) as archive:
            xml = archive.read("word/document.xml").decode("utf-8")

        assert_true('TOC \\o "1-1"' in xml or "TOC \\o &quot;1-1&quot;" in xml, "TOC is not level-1 only")

        title_idx = xml.find('pStyle ns0:val="Title"')
        if title_idx < 0:
            title_idx = xml.find('w:pStyle w:val="Title"')
        exec_idx = xml.find('name="executive-summary"')
        toc_idx = xml.find("docPartGallery")
        intro_idx = xml.find('name="introduction"')
        assert_true(title_idx >= 0 and exec_idx >= 0 and toc_idx >= 0 and intro_idx >= 0, "Could not locate title/executive-summary/TOC/introduction in document XML")
        assert_true(title_idx < exec_idx < toc_idx < intro_idx, "Document order is not title -> executive summary -> TOC -> introduction")


def test_document_writer_output_contract() -> None:
    text = (SKILLS_DIR / "document-writer" / "SKILL.md").read_text(encoding="utf-8")
    for filename in REQUIRED_TRACKING_FILES:
        assert_true(
            filename in text,
            f"document-writer: missing required tracking artifact `{filename}` in SKILL contract",
        )


def test_prohibited_wording() -> None:
    for path in find_skill_files():
        text = path.read_text(encoding="utf-8")
        for pattern in PROHIBITED_SKILL_PATTERNS:
            assert_true(
                re.search(pattern, text, flags=re.IGNORECASE) is None,
                f"{path}: prohibited phrasing matched `{pattern}`",
            )


def test_skill_self_containment() -> None:
    for path in find_skill_files():
        skill_dir = path.parent
        references_dir = skill_dir / "references"
        assert_true(references_dir.exists(), f"{skill_dir.name}: missing references/")
        assert_true(
            (references_dir / "quality-standard.md").exists(),
            f"{skill_dir.name}: missing references/quality-standard.md",
        )
        assert_true(
            (references_dir / "workflow.md").exists(),
            f"{skill_dir.name}: missing references/workflow.md",
        )
        if skill_dir.name == "document-writer":
            continue
        templates = skill_dir / "assets" / "templates"
        assert_true(templates.exists(), f"{skill_dir.name}: missing assets/templates/")
        template_files = list(templates.glob("*.md"))
        assert_true(template_files, f"{skill_dir.name}: no template files under assets/templates/")


def test_packaging_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output_base = Path(tmp) / "package-out" / "skill-pack"
        result = run(
            [
                sys.executable,
                str(ROOT / "scripts" / "package_skill_pack.py"),
                "--output",
                str(output_base),
            ],
            cwd=ROOT,
        )
        assert_true(result.returncode == 0, f"package_skill_pack failed:\n{result.stderr}{result.stdout}")
        archive = Path(f"{output_base}.zip")
        assert_true(archive.exists(), "package_skill_pack did not create zip archive")
        with zipfile.ZipFile(archive) as zf:
            names = set(zf.namelist())
        for skill_name in EXPECTED_SKILLS:
            prefix = f"consulting-workflows/{skill_name}/"
            assert_true(any(name.startswith(prefix) for name in names), f"archive missing {skill_name}/")


def main() -> int:
    tests = [
        ("structure lint", test_structure_lint),
        ("skill set complete", test_skill_set_complete),
        ("output contracts", test_output_contracts),
        ("orchestrator pipeline consistency", test_orchestrator_pipeline_consistency),
        ("document-writer output contract", test_document_writer_output_contract),
        ("prohibited wording", test_prohibited_wording),
        ("skill self-containment", test_skill_self_containment),
        ("packaging smoke", test_packaging_smoke),
        ("document-writer e2e", test_document_writer_e2e),
    ]
    failures: list[str] = []
    for name, fn in tests:
        try:
            fn()
            print(f"[run_portfolio_tests] PASS: {name}")
        except TestFailure as exc:
            failures.append(f"{name}: {exc}")
            print(f"[run_portfolio_tests] FAIL: {name}: {exc}", file=sys.stderr)
        except Exception as exc:  # defensive catch to avoid silent crashes in CI/local runs
            failures.append(f"{name}: unexpected error: {exc}")
            print(f"[run_portfolio_tests] FAIL: {name}: unexpected error: {exc}", file=sys.stderr)
    if failures:
        print("\n[run_portfolio_tests] SUMMARY: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("\n[run_portfolio_tests] SUMMARY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
