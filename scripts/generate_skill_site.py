#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MARK_SOURCE = ROOT / ".github" / "assets" / "consulting-workflows-mark.svg"

SITE_CSS = """
:root {
  --bg: #efe8db;
  --bg-deep: #17313a;
  --panel: rgba(251, 248, 241, 0.94);
  --panel-strong: #fffdf8;
  --ink: #142227;
  --muted: #4c5d63;
  --line: rgba(20, 34, 39, 0.12);
  --line-strong: rgba(20, 34, 39, 0.22);
  --accent: #b4532a;
  --accent-deep: #8c3718;
  --accent-soft: rgba(180, 83, 42, 0.14);
  --teal: #2d6f73;
  --teal-soft: rgba(45, 111, 115, 0.12);
  --shadow: 0 24px 60px rgba(18, 31, 37, 0.14);
  --shadow-tight: 0 16px 28px rgba(18, 31, 37, 0.08);
  --radius: 22px;
  --radius-sm: 14px;
  --max: 1220px;
  --mono: "IBM Plex Mono", "SFMono-Regular", ui-monospace, monospace;
  --sans: "IBM Plex Sans", "Aptos", sans-serif;
  --serif: "Newsreader", Georgia, serif;
}

* { box-sizing: border-box; }
html {
  scroll-behavior: smooth;
  background: var(--bg);
}
body {
  margin: 0;
  font-family: var(--sans);
  color: var(--ink);
  text-rendering: optimizeLegibility;
  background:
    radial-gradient(circle at top left, rgba(180, 83, 42, 0.16), transparent 26%),
    radial-gradient(circle at top right, rgba(45, 111, 115, 0.18), transparent 24%),
    linear-gradient(180deg, #f7f2e8 0%, var(--bg) 34%, #e5ddd0 100%);
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *,
  *::before,
  *::after {
    animation: none !important;
    transition: none !important;
  }
}
a {
  color: var(--accent-deep);
  text-decoration: none;
  transition: color 160ms ease, background-color 160ms ease, border-color 160ms ease, transform 160ms ease;
}
a:hover { color: var(--accent); }
a:focus-visible,
button:focus-visible,
[role="button"]:focus-visible {
  outline: 3px solid rgba(180, 83, 42, 0.34);
  outline-offset: 3px;
}
code, pre { font-family: var(--mono); }
code {
  background: rgba(20, 34, 39, 0.08);
  padding: 0.16rem 0.38rem;
  border-radius: 6px;
  font-size: 0.9em;
}
pre {
  background: #102127;
  color: #f4f0e8;
  padding: 1rem 1.1rem 1.05rem;
  overflow-x: auto;
  border-radius: 16px;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}
pre code { background: transparent; padding: 0; color: inherit; }
.shell::before {
  content: "$ ";
  color: #e6b78a;
}
.skip-link {
  position: absolute;
  left: 1rem;
  top: -3rem;
  z-index: 20;
  padding: 0.7rem 0.95rem;
  border-radius: 999px;
  background: var(--bg-deep);
  color: #f6efe3;
}
.skip-link:focus-visible { top: 1rem; }
.site-shell {
  width: min(calc(100% - 2rem), var(--max));
  margin: 0 auto;
}
.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  padding: 1rem 0 0;
}
.topbar-inner {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 0.8rem 1rem;
  background: rgba(247, 242, 232, 0.8);
  border: 1px solid rgba(20, 34, 39, 0.08);
  border-radius: 999px;
  backdrop-filter: blur(18px);
  box-shadow: var(--shadow-tight);
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  color: var(--ink);
  font-weight: 700;
  letter-spacing: 0.02em;
}
.brand img {
  width: 40px;
  height: 40px;
}
.nav {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.nav a {
  color: var(--muted);
  padding: 0.55rem 0.85rem;
  border-radius: 999px;
  touch-action: manipulation;
}
.nav a:hover {
  background: rgba(20, 34, 39, 0.06);
  text-decoration: none;
}
.hero {
  padding: 2.3rem 0 2rem;
}
.hero-card {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 86% 18%, rgba(230, 183, 138, 0.28), transparent 16%),
    radial-gradient(circle at 14% 0%, rgba(70, 131, 136, 0.24), transparent 18%),
    linear-gradient(140deg, rgba(251, 248, 241, 0.96), rgba(233, 243, 242, 0.92) 42%, rgba(251, 245, 236, 0.96));
  border: 1px solid rgba(20, 34, 39, 0.1);
  border-radius: 32px;
  padding: 2.1rem;
  box-shadow: var(--shadow);
}
.hero-card::after {
  content: "";
  position: absolute;
  inset: auto -8% -18% auto;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(20, 34, 39, 0.08), transparent 70%);
  pointer-events: none;
}
.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.72rem;
  color: var(--teal);
  font-weight: 700;
}
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(260px, 1fr);
  gap: 1.8rem;
}
.hero h1 {
  margin: 0.55rem 0 0.85rem;
  font-family: var(--serif);
  font-size: clamp(2.7rem, 5vw, 5.2rem);
  line-height: 0.92;
  letter-spacing: -0.05em;
  max-width: 12ch;
  text-wrap: balance;
}
.hero p {
  margin: 0;
  font-size: 1.08rem;
  color: var(--muted);
  max-width: 42rem;
  line-height: 1.6;
}
.hero-actions {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
  margin-top: 1.4rem;
}
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.88rem 1.08rem;
  border-radius: 999px;
  font-weight: 700;
  border: 1px solid transparent;
  touch-action: manipulation;
}
.button-primary {
  color: white;
  background: linear-gradient(135deg, var(--accent), var(--accent-deep));
  box-shadow: 0 12px 26px rgba(140, 55, 24, 0.2);
}
.button-secondary {
  color: var(--ink);
  background: rgba(255, 255, 255, 0.64);
  border-color: rgba(20, 34, 39, 0.1);
}
.button:hover {
  text-decoration: none;
  transform: translateY(-1px);
}
.hero-stats {
  display: grid;
  gap: 0.85rem;
}
.stat {
  background: rgba(20, 34, 39, 0.92);
  color: #f6efe3;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 1.05rem 1rem 0.98rem;
  box-shadow: var(--shadow-tight);
}
.stat-label {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(246, 239, 227, 0.64);
  margin-bottom: 0.32rem;
}
.stat-value {
  font-family: var(--serif);
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 0.95;
  text-wrap: balance;
}
.stat-copy {
  margin-top: 0.3rem;
  color: rgba(246, 239, 227, 0.82);
  font-size: 0.95rem;
  line-height: 1.5;
}
.section {
  padding: 1.35rem 0 2.3rem;
}
.section-head {
  margin-bottom: 1.1rem;
}
.section-head h2 {
  margin: 0;
  font-family: var(--serif);
  font-size: clamp(1.8rem, 2.6vw, 2.7rem);
  letter-spacing: -0.04em;
  text-wrap: balance;
}
.section-head p {
  margin: 0.5rem 0 0;
  color: var(--muted);
  max-width: 44rem;
  line-height: 1.6;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
  gap: 1.1rem;
}
.skill-card, .panel {
  background: var(--panel);
  border: 1px solid rgba(20, 34, 39, 0.1);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.skill-card {
  position: relative;
  overflow: hidden;
  padding: 1.2rem 1.2rem 1.08rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.skill-card::before {
  content: "";
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent), var(--teal));
}
.skill-card h3 {
  margin: 0;
  font-family: var(--serif);
  font-size: 1.38rem;
  line-height: 1.05;
  letter-spacing: -0.03em;
  text-wrap: balance;
}
.skill-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
}
.meta-row {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
}
.pill {
  display: inline-flex;
  align-items: center;
  padding: 0.34rem 0.58rem;
  border-radius: 999px;
  background: var(--teal-soft);
  color: var(--teal);
  font-size: 0.84rem;
  font-weight: 700;
}
.pill.alt {
  background: var(--accent-soft);
  color: var(--accent-deep);
}
.skill-card .cta {
  margin-top: auto;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-weight: 700;
}
.two-col {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
  gap: 1.1rem;
}
.panel {
  padding: 1.25rem;
}
.panel h3 {
  margin: 0 0 0.8rem;
  font-family: var(--serif);
  font-size: 1.28rem;
  line-height: 1.05;
}
.panel p:last-child {
  margin-bottom: 0;
}
.steps {
  margin: 0;
  padding-left: 1.2rem;
}
.steps li {
  margin: 0 0 0.5rem;
}
.footer {
  padding: 2rem 0 3rem;
  color: var(--muted);
  font-size: 0.95rem;
}
.footer a {
  color: inherit;
  font-weight: 700;
}
.page-grid {
  display: grid;
  grid-template-columns: minmax(0, 270px) minmax(0, 1fr);
  gap: 1.2rem;
  padding: 1rem 0 2.5rem;
}
.sidebar {
  position: sticky;
  top: 6.2rem;
  align-self: start;
}
.sidebar .panel {
  background: rgba(249, 244, 236, 0.86);
}
.sidebar h3 {
  margin-bottom: 0.7rem;
}
.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar li + li {
  margin-top: 0.34rem;
}
.sidebar a {
  color: var(--muted);
}
.content .panel + .panel {
  margin-top: 1rem;
}
.content h2,
.content h3 {
  letter-spacing: -0.03em;
  scroll-margin-top: 6.8rem;
}
.content h2 {
  margin-top: 0;
  font-family: var(--serif);
  font-size: clamp(1.7rem, 2.4vw, 2.35rem);
  text-wrap: balance;
}
.content ul,
.content ol {
  padding-left: 1.2rem;
}
.content li + li {
  margin-top: 0.32rem;
}
.content p,
.content li {
  color: var(--ink);
  line-height: 1.64;
}
.lead {
  font-size: 1.05rem;
  color: var(--muted);
  line-height: 1.65;
}
.file-list {
  columns: 2;
  column-gap: 1rem;
  padding-left: 1rem;
}
.file-list li {
  break-inside: avoid;
}
.callout {
  padding: 1rem 1rem 1.02rem;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(45, 111, 115, 0.12), rgba(180, 83, 42, 0.08));
  border: 1px solid rgba(20, 34, 39, 0.1);
}
.reference-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}
.reference-card {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.54), transparent 26%),
    linear-gradient(180deg, rgba(247, 242, 232, 0.95), rgba(236, 244, 243, 0.94));
  border: 1px solid rgba(20, 34, 39, 0.1);
  border-radius: 20px;
  padding: 1rem 1rem 0.95rem;
  box-shadow: var(--shadow-tight);
}
.reference-card h3 {
  margin: 0 0 0.45rem;
  font-family: var(--serif);
  font-size: 1.2rem;
  line-height: 1.03;
}
.reference-card p {
  margin: 0 0 0.7rem;
  color: var(--muted);
  line-height: 1.55;
}
.reference-card ul {
  margin: 0;
  padding-left: 1rem;
}
.reference-card li {
  color: var(--ink);
  font-size: 0.95rem;
}
.reference-card li + li {
  margin-top: 0.24rem;
}
.kicker-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.9rem;
}
.kicker {
  background: rgba(20, 34, 39, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 1rem 1rem 1.02rem;
  color: #f6efe3;
  box-shadow: var(--shadow-tight);
}
.kicker h3 {
  margin: 0 0 0.35rem;
  font-family: var(--serif);
  font-size: 1.18rem;
  line-height: 1.03;
}
.kicker p {
  margin: 0;
  color: rgba(246, 239, 227, 0.82);
  line-height: 1.55;
}
.hero-index .hero-card {
  min-height: 28rem;
}
.hero-index .hero-grid {
  align-items: end;
}
.hero-skill .hero-card {
  background:
    radial-gradient(circle at 92% 16%, rgba(230, 183, 138, 0.22), transparent 14%),
    linear-gradient(145deg, rgba(20, 34, 39, 0.96), rgba(31, 56, 62, 0.96));
  color: #f6efe3;
}
.hero-skill .hero-card .eyebrow,
.hero-skill .hero-card p,
.hero-skill .button-secondary {
  color: rgba(246, 239, 227, 0.82);
}
.hero-skill .button-secondary {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.14);
}
.hero-skill .button-secondary:hover {
  color: #ffffff;
}
main { display: block; }
@media (max-width: 920px) {
  .hero-grid,
  .two-col,
  .page-grid {
    grid-template-columns: 1fr;
  }
  .sidebar { position: static; }
  .file-list { columns: 1; }
  .topbar { position: static; }
  .hero h1 { max-width: none; }
}
@media (max-width: 640px) {
  .site-shell {
    width: min(calc(100% - 1rem), var(--max));
  }
  .topbar-inner,
  .hero-card,
  .panel,
  .skill-card,
  .kicker,
  .reference-card {
    padding-left: 0.95rem;
    padding-right: 0.95rem;
  }
  .hero-card { border-radius: 24px; }
}
"""


@dataclass
class SkillDoc:
    slug: str
    title: str
    name: str
    description: str
    short_description: str
    intro_html: str
    sections: list[tuple[str, str]]
    file_paths: list[str]
    reference_docs: list["ReferenceDoc"]


@dataclass
class ReferenceDoc:
    key: str
    nav_label: str
    title: str
    intro_html: str
    sections: list[tuple[str, str]]


REFERENCE_ORDER = (
    ("workflow.md", "Workflow"),
    ("quality-standard.md", "Quality Standard"),
    ("validation-checklist.md", "Validation Checklist"),
    ("term-sheet.md", "Term Sheet"),
    ("repo-map.md", "Repo Map"),
    ("tracking-readme.md", "Tracking Templates"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a static GitHub Pages site for the consulting skill pack."
    )
    parser.add_argument(
        "--output",
        default="site",
        help="Output directory for the generated site (default: site).",
    )
    return parser.parse_args()


def parse_kv_yaml(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    frontmatter = parse_kv_yaml(text[4:end])
    return frontmatter, text[end + 5 :]


def parse_openai_interface(skill_dir: Path) -> dict[str, str]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return {}
    in_interface = False
    data: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if not in_interface:
            if line.strip() == "interface:":
                in_interface = True
            continue
        if not raw_line.startswith("  "):
            break
        stripped = line.strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def parse_body(body: str) -> tuple[str, str, list[tuple[str, str]]]:
    lines = body.splitlines()
    title = ""
    intro_lines: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, current_lines))
            current_heading = line[3:].strip()
            current_lines = []
            continue
        if current_heading is None:
            intro_lines.append(line)
        else:
            current_lines.append(line)

    if current_heading is not None:
        sections.append((current_heading, current_lines))

    intro_text = "\n".join(intro_lines).strip()
    cooked_sections = [(heading, "\n".join(content).strip()) for heading, content in sections]
    return title, intro_text, cooked_sections


def render_markdown(text: str) -> str:
    cleaned = text.strip("\n")
    if not cleaned:
        return ""
    lines = cleaned.splitlines()
    blocks, _ = render_blocks(lines, 0, 0)
    return "".join(blocks)


LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


def render_blocks(lines: list[str], start: int, base_indent: int) -> tuple[list[str], int]:
    blocks: list[str] = []
    i = start
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        list_match = LIST_RE.match(raw)
        if list_match and len(list_match.group(1)) < base_indent:
            break

        if raw.lstrip().startswith("```"):
            block, i = render_code_block(lines, i)
            blocks.append(block)
            continue

        if raw.startswith("### "):
            blocks.append(f"<h3>{render_inline(raw[4:].strip())}</h3>")
            i += 1
            continue

        if raw.startswith("#### "):
            blocks.append(f"<h4>{render_inline(raw[5:].strip())}</h4>")
            i += 1
            continue

        if list_match and len(list_match.group(1)) >= base_indent:
            block, i = render_list(lines, i, len(list_match.group(1)))
            blocks.append(block)
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            next_raw = lines[i]
            next_stripped = next_raw.strip()
            if not next_stripped:
                i += 1
                break
            if next_raw.lstrip().startswith("```") or next_raw.startswith("### ") or next_raw.startswith("#### "):
                break
            next_list_match = LIST_RE.match(next_raw)
            if next_list_match and len(next_list_match.group(1)) >= base_indent:
                break
            if next_list_match and len(next_list_match.group(1)) < base_indent:
                break
            paragraph_lines.append(next_stripped)
            i += 1
        blocks.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")
    return blocks, i


def render_code_block(lines: list[str], start: int) -> tuple[str, int]:
    fence = lines[start].lstrip()
    language = fence[3:].strip()
    code_lines: list[str] = []
    i = start + 1
    while i < len(lines):
        if lines[i].lstrip().startswith("```"):
            i += 1
            break
        code_lines.append(lines[i])
        i += 1
    code = "\n".join(code_lines)
    css_class = f' class="language-{html.escape(language, quote=True)}"' if language else ""
    if language in {"bash", "shell", "sh"}:
        css_class = ' class="shell"'
    return f"<pre><code{css_class}>{html.escape(code)}</code></pre>", i


def render_list(lines: list[str], start: int, indent: int) -> tuple[str, int]:
    first_match = LIST_RE.match(lines[start])
    assert first_match is not None
    ordered = first_match.group(2).endswith(".")
    tag = "ol" if ordered else "ul"
    items: list[str] = []
    i = start

    while i < len(lines):
        raw = lines[i]
        match = LIST_RE.match(raw)
        if not match:
            break
        current_indent = len(match.group(1))
        current_ordered = match.group(2).endswith(".")
        if current_indent < indent or current_ordered != ordered:
            break
        if current_indent > indent:
            nested_html, i = render_list(lines, i, current_indent)
            if items:
                items[-1] = items[-1][:-5] + nested_html + "</li>"
            continue

        item_parts = [render_inline(match.group(3).strip())]
        i += 1
        while i < len(lines):
            next_raw = lines[i]
            next_match = LIST_RE.match(next_raw)
            next_stripped = next_raw.strip()
            if not next_stripped:
                i += 1
                continue
            if next_raw.lstrip().startswith("```"):
                code_html, i = render_code_block(lines, i)
                item_parts.append(code_html)
                continue
            if next_match:
                next_indent = len(next_match.group(1))
                next_ordered = next_match.group(2).endswith(".")
                if next_indent < indent:
                    break
                if next_indent == indent and next_ordered == ordered:
                    break
                if next_indent > indent:
                    nested_html, i = render_list(lines, i, next_indent)
                    item_parts.append(nested_html)
                    continue
            if len(next_raw) - len(next_raw.lstrip()) > indent:
                item_parts.append(f"<p>{render_inline(next_stripped)}</p>")
                i += 1
                continue
            break

        items.append(f"<li>{''.join(item_parts)}</li>")

    return f"<{tag}>{''.join(items)}</{tag}>", i


def render_inline(text: str) -> str:
    rendered = html.escape(text, quote=False)
    rendered = re.sub(
        r"`([^`]+)`",
        lambda m: f"<code>{html.escape(m.group(1), quote=False)}</code>",
        rendered,
    )
    rendered = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: (
            f'<a href="{html.escape(m.group(2), quote=True)}">'
            f"{m.group(1)}</a>"
        ),
        rendered,
    )
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    return rendered


def file_inventory(skill_dir: Path) -> list[str]:
    files: list[str] = []
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(ROOT)
        if "__pycache__" in rel.parts:
            continue
        if any(part.startswith(".") for part in rel.parts):
            continue
        files.append(rel.as_posix())
    return files


def parse_reference_doc(reference_path: Path, nav_label: str) -> ReferenceDoc:
    text = reference_path.read_text(encoding="utf-8")
    title, intro_text, sections = parse_body(text)
    rendered_sections = [(heading, render_markdown(content)) for heading, content in sections if content]
    intro_html = render_markdown(intro_text)
    if not intro_html:
        for heading, content in rendered_sections:
            if heading.lower() == "purpose":
                intro_html = content
                break
    return ReferenceDoc(
        key=reference_path.name,
        nav_label=nav_label,
        title=title or reference_path.stem,
        intro_html=intro_html,
        sections=rendered_sections,
    )


def load_reference_docs(skill_dir: Path) -> list[ReferenceDoc]:
    refs: list[ReferenceDoc] = []
    references_dir = skill_dir / "references"
    for filename, label in REFERENCE_ORDER:
        ref_path = references_dir / filename
        if ref_path.exists():
            refs.append(parse_reference_doc(ref_path, label))
    return refs


def repo_identity() -> tuple[str, str, str]:
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if repo:
        owner, name = repo.split("/", 1)
        return owner, name, f"https://github.com/{repo}"
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        remote = result.stdout.strip()
    except OSError:
        remote = ""
    if remote.endswith(".git"):
        remote = remote[:-4]
    if remote.startswith("git@github.com:"):
        repo = remote.split("git@github.com:", 1)[1]
        owner, name = repo.split("/", 1)
        return owner, name, f"https://github.com/{repo}"
    if remote.startswith("https://github.com/"):
        repo = remote.split("https://github.com/", 1)[1]
        owner, name = repo.split("/", 1)
        return owner, name, f"https://github.com/{repo}"
    return "fenrick", "consulting-workflows", "https://github.com/fenrick/consulting-workflows"


def build_skill_docs() -> list[SkillDoc]:
    docs: list[SkillDoc] = []
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(skill_text)
        ui = parse_openai_interface(skill_dir)
        title, intro_text, sections = parse_body(body)
        docs.append(
            SkillDoc(
                slug=skill_dir.name,
                title=ui.get("display_name") or title or skill_dir.name,
                name=frontmatter.get("name", skill_dir.name),
                description=frontmatter.get("description", ""),
                short_description=ui.get("short_description", ""),
                intro_html=render_markdown(intro_text),
                sections=[(heading, render_markdown(content)) for heading, content in sections if content],
                file_paths=file_inventory(skill_dir),
                reference_docs=load_reference_docs(skill_dir),
            )
        )
    return docs


def page_template(
    page_title: str,
    body: str,
    repo_url: str,
    release_url: str,
    asset_prefix: str,
    home_href: str,
) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#efe8db">
    <title>{html.escape(page_title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,500;6..72,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{html.escape(asset_prefix)}style.css">
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to Main Content</a>
    <div class="site-shell">
      <header class="topbar">
        <div class="topbar-inner">
          <a class="brand" href="{html.escape(home_href)}">
            <img src="{html.escape(asset_prefix)}consulting-workflows-mark.svg" alt="Consulting Workflows mark" width="40" height="40" fetchpriority="high">
            <span>Consulting Workflows</span>
          </a>
          <nav class="nav">
            <a href="{html.escape(home_href)}">Home</a>
            <a href="{html.escape(release_url)}">Releases</a>
            <a href="{html.escape(repo_url)}">Repository</a>
          </nav>
        </div>
      </header>
      <main id="main-content">
        {body}
      </main>
      <footer class="footer">
        Generated from the skill folders in <a href="{html.escape(repo_url)}">the repository</a>. If the site and source disagree, the source wins.
      </footer>
    </div>
  </body>
</html>
"""


def render_index(skills: list[SkillDoc], repo_url: str, release_url: str) -> str:
    cards = []
    for skill in skills:
        summary = skill.short_description or skill.description
        cards.append(
            f"""
            <article class="skill-card">
              <div class="meta-row">
                <span class="pill">{html.escape(skill.name)}</span>
                <span class="pill alt">{len(skill.file_paths)} files</span>
                <span class="pill alt">{len(skill.reference_docs)} reference docs</span>
              </div>
              <h3>{html.escape(skill.title)}</h3>
              <p>{html.escape(summary)}</p>
              <a class="cta" href="skills/{quote(skill.slug)}/index.html">Open skill page</a>
            </article>
            """
        )
    body = f"""
    <section class="hero hero-index">
      <div class="hero-card">
        <div class="hero-grid">
          <div>
            <div class="eyebrow">Agent skills distribution</div>
            <h1>Consulting-grade skills, packaged for runtimes that vary in how much structure they can tolerate.</h1>
            <p>
              This site is generated from the actual skill folders. It documents what each skill is for, what it ships with,
              and where it fits in the broader workflow.
            </p>
            <div class="hero-actions">
              <a class="button button-primary" href="{html.escape(release_url)}">Download latest release</a>
              <a class="button button-secondary" href="#skills">Browse skills</a>
            </div>
          </div>
          <div class="hero-stats">
            <div class="stat">
              <div class="stat-label">Skills</div>
              <div class="stat-value">{len(skills)}</div>
              <div class="stat-copy">Each packaged as its own ZIP and as part of the full collection.</div>
            </div>
            <div class="stat">
              <div class="stat-label">Primary use</div>
              <div class="stat-value">Structured delivery</div>
              <div class="stat-copy">Evidence intake, storyline design, drafting, workshops, and final document production.</div>
            </div>
            <div class="stat">
              <div class="stat-label">Trust model</div>
              <div class="stat-value">Source-driven</div>
              <div class="stat-copy">The site is generated from repo state, not hand-maintained marketing copy.</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="skills">
      <div class="section-head">
        <h2>Skills</h2>
        <p>Each page below reflects the shipped skill contract, bundled materials, and file inventory.</p>
      </div>
      <div class="card-grid">
        {''.join(cards)}
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <h2>What Changed In v1.4</h2>
        <p>The pack now exposes a real operating system for each skill, not just trigger text and task lists.</p>
      </div>
      <div class="kicker-list">
        <div class="kicker">
          <h3>Reference packs</h3>
          <p>Every skill now ships workflow, quality, validation, terminology, repo map, and tracking guidance.</p>
        </div>
        <div class="kicker">
          <h3>Enforced structure</h3>
          <p>The validator and test suite now fail if reference-doc structure drifts.</p>
        </div>
        <div class="kicker">
          <h3>Document export hardening</h3>
          <p><code>document-writer</code> now renders Mermaid figures into DOCX with caption styling and document-width control.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="two-col">
        <div class="panel">
          <h3>What gets published</h3>
          <div class="callout">
            Releases publish one collection archive and one archive per skill so stricter runtimes can install a single skill without manual extraction.
          </div>
          <ul>
            <li><code>consulting-workflows-vX.Y.Z.zip</code></li>
            <li><code>&lt;skill-name&gt;-vX.Y.Z.zip</code> for each skill</li>
          </ul>
        </div>
        <div class="panel">
          <h3>Reference system</h3>
          <ol class="steps">
            <li><strong>Workflow</strong>: operating sequence and back-iteration loop.</li>
            <li><strong>Quality standard</strong>: what good looks like before handoff.</li>
            <li><strong>Validation checklist</strong>: ordered release and handoff checks.</li>
            <li><strong>Term sheet / repo map / tracking</strong>: stable language, file responsibilities, and template discipline.</li>
          </ol>
        </div>
      </div>
    </section>
    """
    return page_template(
        "Consulting Workflows",
        body,
        repo_url,
        release_url,
        asset_prefix="assets/",
        home_href="index.html",
    )


def render_skill_page(skill: SkillDoc, repo_url: str, release_url: str) -> str:
    reference_nav = "".join(
        f'<li><a href="#ref-{slugify(ref.key)}">{html.escape(ref.nav_label)}</a></li>'
        for ref in skill.reference_docs
    )
    section_nav = "".join(
        f'<li><a href="#{slugify(heading)}">{html.escape(heading)}</a></li>'
        for heading, _ in skill.sections
    )
    reference_blocks = "".join(
        f"""
        <article class="reference-card" id="ref-{slugify(ref.key)}">
          <h3>{html.escape(ref.title)}</h3>
          {ref.intro_html}
          <ul>{"".join(f"<li>{html.escape(heading)}</li>" for heading, _ in ref.sections)}</ul>
        </article>
        """
        for ref in skill.reference_docs
    )
    section_blocks = "".join(
        f"""
        <section class="panel" id="{slugify(heading)}">
          <h2>{html.escape(heading)}</h2>
          {content}
        </section>
        """
        for heading, content in skill.sections
    )
    files_html = "".join(f"<li><code>{html.escape(path)}</code></li>" for path in skill.file_paths)
    summary = skill.short_description or skill.description
    body = f"""
    <section class="hero hero-skill">
      <div class="hero-card">
        <div class="eyebrow">Skill page</div>
        <h1>{html.escape(skill.title)}</h1>
        <p>{html.escape(summary)}</p>
        <div class="hero-actions">
          <a class="button button-primary" href="{html.escape(release_url)}">Get latest packaged release</a>
          <a class="button button-secondary" href="{html.escape(repo_url)}/tree/main/skills/{quote(skill.slug)}">Open source folder</a>
        </div>
      </div>
    </section>

    <div class="page-grid">
      <aside class="sidebar">
        <div class="panel">
          <h3>At a glance</h3>
          <div class="meta-row">
            <span class="pill">{html.escape(skill.name)}</span>
            <span class="pill alt">{len(skill.file_paths)} files</span>
          </div>
          <p class="lead">{html.escape(skill.description)}</p>
        </div>
        <div class="panel">
          <h3>Sections</h3>
          <ul>
            <li><a href="#reference-pack">Reference pack</a></li>
            {reference_nav}
            {section_nav}
            <li><a href="#file-inventory">File inventory</a></li>
          </ul>
        </div>
      </aside>
      <main class="content">
        <section class="panel">
          <h2>Overview</h2>
          {skill.intro_html or f"<p>{html.escape(skill.description)}</p>"}
        </section>
        <section class="panel" id="reference-pack">
          <h2>Reference Pack</h2>
          <p class="lead">These are the operating documents that define how the skill should be run, checked, and handed off.</p>
          <div class="reference-grid">
            {reference_blocks}
          </div>
        </section>
        {section_blocks}
        <section class="panel" id="file-inventory">
          <h2>File inventory</h2>
          <p class="lead">This is generated from the skill folder so the page stays tied to what actually ships.</p>
          <ul class="file-list">
            {files_html}
          </ul>
        </section>
      </main>
    </div>
    """
    return page_template(
        f"{skill.title} | Consulting Workflows",
        body,
        repo_url,
        release_url,
        asset_prefix="../../assets/",
        home_href="../../index.html",
    )


def slugify(text: str) -> str:
    out = []
    for char in text.lower():
        if char.isalnum():
            out.append(char)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-") or "section"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    output_dir = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output).resolve()

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "assets").mkdir(parents=True, exist_ok=True)

    owner, repo_name, repo_url = repo_identity()
    release_url = f"{repo_url}/releases/latest"

    skills = build_skill_docs()
    write_text(output_dir / "assets" / "style.css", SITE_CSS.strip() + "\n")
    shutil.copy2(MARK_SOURCE, output_dir / "assets" / "consulting-workflows-mark.svg")
    write_text(output_dir / ".nojekyll", "")
    write_text(output_dir / "index.html", render_index(skills, repo_url, release_url))

    for skill in skills:
        write_text(
            output_dir / "skills" / skill.slug / "index.html",
            render_skill_page(skill, repo_url, release_url),
        )

    print(f"[generate_skill_site] created: {output_dir}")
    print(f"[generate_skill_site] repo: {owner}/{repo_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
