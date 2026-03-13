#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import json
import importlib.util
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


def test_document_writer_mermaid_tooling_contract() -> None:
    package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    dev_dependencies = package_json.get("devDependencies", {})
    assert_true(
        "@mermaid-js/mermaid-cli" in dev_dependencies,
        "document-writer: missing @mermaid-js/mermaid-cli dev dependency",
    )

    render_script = SKILLS_DIR / "document-writer" / "scripts" / "render_mermaid.py"
    assert_true(render_script.exists(), "document-writer: missing scripts/render_mermaid.py")

    mermaid_config = SKILLS_DIR / "document-writer" / "assets" / "mermaid" / "mermaid-config.json"
    assert_true(mermaid_config.exists(), "document-writer: missing assets/mermaid/mermaid-config.json")
    config = json.loads(mermaid_config.read_text(encoding="utf-8"))
    assert_true(
        config.get("flowchart", {}).get("defaultRenderer") == "elk",
        "document-writer: Mermaid config must default to ELK renderer",
    )

    result = run([sys.executable, str(render_script), "--help"], cwd=ROOT)
    assert_true(result.returncode == 0, f"render_mermaid --help failed:\n{result.stderr}{result.stdout}")
    script_text = render_script.read_text(encoding="utf-8")
    assert_true("DEFAULT_WIDTH = 3200" in script_text, "document-writer: Mermaid width default regressed")
    assert_true("DEFAULT_SCALE = 5" in script_text, "document-writer: Mermaid scale default regressed")


def test_document_writer_mermaid_preprocessing_contract() -> None:
    export_script = SKILLS_DIR / "document-writer" / "scripts" / "export_docx.py"
    spec = importlib.util.spec_from_file_location("document_writer_export_docx", export_script)
    assert_true(spec is not None and spec.loader is not None, "document-writer: could not load export_docx module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    calls: list[tuple[str, str]] = []

    def fake_render(renderer_script, mermaid_source, output_dir, basename, env=None):
        calls.append((mermaid_source, basename))
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{basename}.png"
        output_file.write_bytes(b"png")
        return output_file

    module.render_mermaid_block = fake_render
    sample = """Intro text.\n\n<!-- FigureCaption: Figure 1: Example diagram -->\n:::mermaid\nflowchart LR\n  A-->B\n:::\n"""
    with tempfile.TemporaryDirectory() as tmp:
        transformed, count = module.preprocess_mermaid_blocks(
            markdown_text=sample,
            renderer_script=export_script.parent / "render_mermaid.py",
            working_dir=Path(tmp),
            env=None,
        )
    assert_true(count == 1, "document-writer: Mermaid preprocessing did not count diagrams correctly")
    assert_true(len(calls) == 1, "document-writer: Mermaid preprocessing did not render the diagram")
    assert_true("flowchart LR" in calls[0][0], "document-writer: Mermaid source was not passed through")
    assert_true(
        "![Figure 1: Example diagram](media/mermaid-figure-01.png)" in transformed,
        "document-writer: Mermaid block was not replaced with a captioned image",
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
        for reference_name in (
            "workflow.md",
            "quality-standard.md",
            "validation-checklist.md",
            "term-sheet.md",
            "repo-map.md",
            "tracking-readme.md",
        ):
            assert_true(
                (references_dir / reference_name).exists(),
                f"{skill_dir.name}: missing references/{reference_name}",
            )
        if skill_dir.name == "document-writer":
            continue
        templates = skill_dir / "assets" / "templates"
        assert_true(templates.exists(), f"{skill_dir.name}: missing assets/templates/")
        template_files = list(templates.glob("*.md"))
        assert_true(template_files, f"{skill_dir.name}: no template files under assets/templates/")


def test_reference_docs_are_discoverable_from_skill_contract() -> None:
    for path in find_skill_files():
        text = path.read_text(encoding="utf-8")
        for reference_name in (
            "references/workflow.md",
            "references/quality-standard.md",
            "references/validation-checklist.md",
            "references/term-sheet.md",
            "references/repo-map.md",
            "references/tracking-readme.md",
        ):
            assert_true(
                reference_name in text,
                f"{path.parent.name}: missing `{reference_name}` in SKILL.md",
            )


def test_reference_doc_heading_contract() -> None:
    expected_headings = {
        "workflow.md": (
            "## Purpose",
            "## Working files",
            "## Back-iteration loop",
            "## Handoff and closure",
        ),
        "quality-standard.md": (
            "## Purpose",
            "## Core standard",
            "## Authoring standard",
            "## Tracking standard",
            "## Handoff standard",
        ),
        "validation-checklist.md": (
            "## Purpose",
            "## How to use this checklist",
        ),
        "term-sheet.md": (
            "## Purpose",
            "## Core terms",
            "## Usage rules",
            "## Drift-control rules",
        ),
        "repo-map.md": (
            "## Purpose",
            "## Main files",
            "## Typical flow",
            "## Handoff note",
        ),
        "tracking-readme.md": (
            "## Purpose",
            "## Template roles",
            "## Working rule",
        ),
    }
    for path in find_skill_files():
        references_dir = path.parent / "references"
        for ref_name, headings in expected_headings.items():
            ref_path = references_dir / ref_name
            text = ref_path.read_text(encoding="utf-8")
            for heading in headings:
                assert_true(
                    heading in text,
                    f"{path.parent.name}: {ref_name} missing heading `{heading}`",
                )


def test_packaging_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp) / "package-out"
        output_base = output_dir / "skill-pack"
        version = "9.9.9"
        result = run(
            [
                sys.executable,
                str(ROOT / "scripts" / "package_skill_pack.py"),
                "--output",
                str(output_base),
                "--version",
                version,
            ],
            cwd=ROOT,
        )
        assert_true(result.returncode == 0, f"package_skill_pack failed:\n{result.stderr}{result.stdout}")
        collection_archive = output_dir / f"skill-pack-v{version}.zip"
        assert_true(collection_archive.exists(), "package_skill_pack did not create collection zip archive")
        with zipfile.ZipFile(collection_archive) as zf:
            names = set(zf.namelist())
        for skill_name in EXPECTED_SKILLS:
            prefix = f"skill-pack/{skill_name}/"
            assert_true(any(name.startswith(prefix) for name in names), f"archive missing {skill_name}/")
            skill_archive = output_dir / f"{skill_name}-v{version}.zip"
            assert_true(skill_archive.exists(), f"missing skill archive: {skill_archive.name}")
            with zipfile.ZipFile(skill_archive) as zf:
                skill_names = set(zf.namelist())
            assert_true(
                f"{skill_name}/SKILL.md" in skill_names,
                f"skill archive missing {skill_name}/SKILL.md",
            )


def test_site_generation_smoke() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output_dir = Path(tmp) / "site-out"
        result = run(
            [
                sys.executable,
                str(ROOT / "scripts" / "generate_skill_site.py"),
                "--output",
                str(output_dir),
            ],
            cwd=ROOT,
        )
        assert_true(result.returncode == 0, f"generate_skill_site failed:\n{result.stderr}{result.stdout}")
        assert_true((output_dir / "index.html").exists(), "site generator did not create index.html")
        assert_true((output_dir / "assets" / "style.css").exists(), "site generator did not create style.css")
        for skill_name in EXPECTED_SKILLS:
            page = output_dir / "skills" / skill_name / "index.html"
            assert_true(page.exists(), f"missing generated skill page: {page}")
            html_text = page.read_text(encoding="utf-8")
            assert_true(skill_name in html_text, f"generated skill page missing skill name: {skill_name}")


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
        ("site generation smoke", test_site_generation_smoke),
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
