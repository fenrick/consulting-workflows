#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[security-scan] missing required tool: $cmd" >&2
    exit 1
  fi
}

run_gitleaks() {
  echo "[security-scan] running gitleaks"
  if gitleaks dir "$ROOT_DIR" --redact --no-banner; then
    return 0
  fi
  echo "[security-scan] gitleaks failed" >&2
  return 1
}

run_pip_audit() {
  echo "[security-scan] running pip-audit"
  req_files=()
  while IFS= read -r file; do
    if [[ "$(basename "$file")" == "requirements-dev.txt" ]]; then
      continue
    fi
    req_files+=("$file")
  done < <(
    find "$ROOT_DIR" -type f \( -name "requirements*.txt" -o -name "constraints*.txt" \) \
      ! -path "*/.venv/*" ! -path "*/venv/*" ! -path "*/node_modules/*"
  )

  if [[ ${#req_files[@]} -eq 0 ]]; then
    echo "[security-scan] no requirements/constraints files found; skipping pip-audit"
    return 0
  fi

  for req in "${req_files[@]}"; do
    echo "[security-scan] pip-audit -r $req"
    pip-audit -r "$req" --progress-spinner off
  done
}

run_semgrep() {
  echo "[security-scan] running semgrep"
  semgrep scan --config auto --error "$ROOT_DIR"
}

main() {
  require_cmd gitleaks
  require_cmd pip-audit
  require_cmd semgrep

  run_gitleaks
  run_pip_audit
  run_semgrep
  echo "[security-scan] all checks passed"
}

main "$@"
