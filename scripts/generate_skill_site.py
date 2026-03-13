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
  --bg: #f6f3eb;
  --panel: #fffdf8;
  --panel-2: #f0f6f6;
  --ink: #17222d;
  --muted: #52606d;
  --line: #d8ddd7;
  --accent: #1f6f8b;
  --accent-2: #2faea1;
  --accent-3: #f2b134;
  --shadow: 0 18px 48px rgba(23, 34, 45, 0.08);
  --radius: 20px;
  --radius-sm: 12px;
  --max: 1180px;
  --mono: "SFMono-Regular", ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, monospace;
  --sans: "Segoe UI", "Aptos", "Helvetica Neue", sans-serif;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--sans);
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(47, 174, 161, 0.14), transparent 30%),
    radial-gradient(circle at top right, rgba(242, 177, 52, 0.16), transparent 22%),
    linear-gradient(180deg, #fbfaf6 0%, var(--bg) 100%);
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code, pre { font-family: var(--mono); }
code {
  background: #eef4f5;
  padding: 0.12rem 0.36rem;
  border-radius: 6px;
  font-size: 0.92em;
}
pre {
  background: #13202b;
  color: #eef6f7;
  padding: 1rem 1.1rem;
  overflow-x: auto;
  border-radius: 14px;
}
pre code { background: transparent; padding: 0; color: inherit; }
.shell::before {
  content: "$ ";
  color: #9fd4d1;
}
.site-shell {
  width: min(calc(100% - 2rem), var(--max));
  margin: 0 auto;
}
.topbar {
  padding: 1rem 0 0;
}
.topbar-inner {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.8rem;
  color: var(--ink);
  font-weight: 700;
  letter-spacing: 0.01em;
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
  padding: 0.5rem 0.8rem;
  border-radius: 999px;
}
.nav a:hover {
  background: rgba(31, 111, 139, 0.08);
  text-decoration: none;
}
.hero {
  padding: 3rem 0 2rem;
}
.hero-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(240, 246, 246, 0.92));
  border: 1px solid rgba(216, 221, 215, 0.9);
  border-radius: 28px;
  padding: 2rem;
  box-shadow: var(--shadow);
}
.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.76rem;
  color: var(--accent);
  font-weight: 700;
}
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(260px, 1fr);
  gap: 1.5rem;
}
.hero h1 {
  margin: 0.45rem 0 0.8rem;
  font-size: clamp(2rem, 4vw, 3.6rem);
  line-height: 0.98;
  letter-spacing: -0.04em;
}
.hero p {
  margin: 0;
  font-size: 1.08rem;
  color: var(--muted);
  max-width: 56rem;
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
  padding: 0.82rem 1.05rem;
  border-radius: 999px;
  font-weight: 700;
  border: 1px solid transparent;
}
.button-primary {
  color: white;
  background: linear-gradient(135deg, var(--accent), #255d90);
}
.button-secondary {
  color: var(--ink);
  background: rgba(31, 111, 139, 0.08);
  border-color: rgba(31, 111, 139, 0.14);
}
.hero-stats {
  display: grid;
  gap: 0.85rem;
}
.stat {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(216, 221, 215, 0.85);
  border-radius: 18px;
  padding: 1rem 1rem 0.95rem;
}
.stat-label {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 0.32rem;
}
.stat-value {
  font-size: 1.7rem;
  font-weight: 800;
  letter-spacing: -0.04em;
}
.stat-copy {
  margin-top: 0.3rem;
  color: var(--muted);
  font-size: 0.95rem;
}
.section {
  padding: 1.2rem 0 2.2rem;
}
.section-head {
  margin-bottom: 1rem;
}
.section-head h2 {
  margin: 0;
  font-size: clamp(1.4rem, 2vw, 2rem);
  letter-spacing: -0.03em;
}
.section-head p {
  margin: 0.45rem 0 0;
  color: var(--muted);
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}
.skill-card, .panel {
  background: var(--panel);
  border: 1px solid rgba(216, 221, 215, 0.9);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}
.skill-card {
  padding: 1.15rem 1.15rem 1.05rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.skill-card h3 {
  margin: 0;
  font-size: 1.12rem;
}
.skill-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.48;
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
  background: rgba(47, 174, 161, 0.1);
  color: #165952;
  font-size: 0.84rem;
  font-weight: 700;
}
.pill.alt {
  background: rgba(242, 177, 52, 0.14);
  color: #8d5c00;
}
.skill-card .cta {
  margin-top: auto;
  font-weight: 700;
}
.two-col {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
  gap: 1rem;
}
.panel {
  padding: 1.2rem;
}
.panel h3 {
  margin: 0 0 0.8rem;
  font-size: 1.08rem;
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
  grid-template-columns: minmax(0, 240px) minmax(0, 1fr);
  gap: 1.2rem;
  padding: 1rem 0 2.5rem;
}
.sidebar {
  position: sticky;
  top: 1rem;
  align-self: start;
}
.sidebar .panel {
  background: rgba(255, 255, 255, 0.82);
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
.content h2, .content h3 {
  letter-spacing: -0.02em;
}
.content h2 {
  margin-top: 0;
}
.content ul, .content ol {
  padding-left: 1.2rem;
}
.content li + li {
  margin-top: 0.32rem;
}
.content p, .content li {
  color: var(--ink);
  line-height: 1.58;
}
.lead {
  font-size: 1.05rem;
  color: var(--muted);
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
  padding: 0.95rem 1rem;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(31, 111, 139, 0.08), rgba(47, 174, 161, 0.08));
  border: 1px solid rgba(31, 111, 139, 0.12);
}
@media (max-width: 920px) {
  .hero-grid, .two-col, .page-grid {
    grid-template-columns: 1fr;
  }
  .sidebar {
    position: static;
  }
  .file-list {
    columns: 1;
  }
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
    <title>{html.escape(page_title)}</title>
    <link rel="stylesheet" href="{html.escape(asset_prefix)}style.css">
  </head>
  <body>
    <div class="site-shell">
      <header class="topbar">
        <div class="topbar-inner">
          <a class="brand" href="{html.escape(home_href)}">
            <img src="{html.escape(asset_prefix)}consulting-workflows-mark.svg" alt="Consulting Workflows mark">
            <span>Consulting Workflows</span>
          </a>
          <nav class="nav">
            <a href="{html.escape(home_href)}">Home</a>
            <a href="{html.escape(release_url)}">Releases</a>
            <a href="{html.escape(repo_url)}">Repository</a>
          </nav>
        </div>
      </header>
      {body}
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
              </div>
              <h3>{html.escape(skill.title)}</h3>
              <p>{html.escape(summary)}</p>
              <a class="cta" href="skills/{quote(skill.slug)}/index.html">Open skill page</a>
            </article>
            """
        )
    body = f"""
    <section class="hero">
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
          <h3>Workflow shape</h3>
          <ol class="steps">
            <li>Catalog source inputs and record observations.</li>
            <li>Check consistency and unresolved evidence gaps.</li>
            <li>Build storyline and choose the right delivery form.</li>
            <li>Turn the structure into report, presentation, workshop, or final document outputs.</li>
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
    section_nav = "".join(
        f'<li><a href="#{slugify(heading)}">{html.escape(heading)}</a></li>'
        for heading, _ in skill.sections
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
    <section class="hero">
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
            {section_nav}
          </ul>
        </div>
      </aside>
      <main class="content">
        <section class="panel">
          <h2>Overview</h2>
          {skill.intro_html or f"<p>{html.escape(skill.description)}</p>"}
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
