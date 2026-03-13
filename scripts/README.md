# Portfolio Test Commands

Install runtime dependency first:

```bash
python3 -m pip install -r requirements.txt
```

Run the quality/structure lint:

```bash
python3 scripts/validate_skill_portfolio.py
```

Run the full portfolio test suite:

```bash
python3 scripts/run_portfolio_tests.py
```

Run local security scans:

```bash
./scripts/run_security_scans.sh
```

Example local install (macOS):

```bash
brew install gitleaks semgrep pip-audit
```

The full suite includes:

- skill structure lint
- required output contract checks
- orchestrator pipeline consistency checks
- document-writer tracking artifact contract checks
- prohibited wording checks (to prevent runtime-skill fallback drift)
- end-to-end `document-writer` assembly and export checks (title/subtitle metadata, TOC depth, and document order)

Build a distributable archive:

```bash
python3 scripts/package_skill_pack.py
```

By default this creates:

- `dist/consulting-workflows.zip`
- `dist/<skill-name>.zip` for each skill under `skills/`

Add `--version X.Y.Z` to emit versioned filenames for the collection and per-skill archives.
Use `--include-repo-meta` only for internal sharing.

Generate the GitHub Pages skill site:

```bash
python3 scripts/generate_skill_site.py --output site
```
