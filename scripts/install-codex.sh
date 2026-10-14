#!/usr/bin/env bash
# install-codex.sh — Install ix-recipes into ~/.codex/skills/
#
# Usage:
#   ./scripts/install-codex.sh               # install all skills
#   ./scripts/install-codex.sh critique      # install one skill
#   ./scripts/install-codex.sh --dry-run     # preview without writing

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CODEX_SKILLS_DIR="${HOME}/.codex/skills"
CODEX_DIST_DIR="${REPO_DIR}/codex-dist"

DRY_RUN=0
SKILL_ID=""

# --- Parse args ---
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --*)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
    *)
      SKILL_ID="$arg"
      ;;
  esac
done

# --- Header ---
echo "ix-recipes → Codex installer"
echo "Repo:   ${REPO_DIR}"
echo "Target: ${CODEX_SKILLS_DIR}"
[[ $DRY_RUN -eq 1 ]] && echo "Mode:   dry-run (no files written)"
echo "---"

# --- Build codex-dist ---
cd "$REPO_DIR"
if [[ -n "$SKILL_ID" ]]; then
  echo "Building: ${SKILL_ID}"
  python3 build.py "$SKILL_ID" --target codex
else
  echo "Building all skills..."
  python3 build.py --target codex
fi

# --- Install ---
if [[ $DRY_RUN -eq 0 ]]; then
  mkdir -p "$CODEX_SKILLS_DIR"
fi

count=0

if [[ -n "$SKILL_ID" ]]; then
  # Single skill
  src="${CODEX_DIST_DIR}/${SKILL_ID}/SKILL.md"
  dst_dir="${CODEX_SKILLS_DIR}/${SKILL_ID}"
  if [[ ! -f "$src" ]]; then
    echo "✗ Not found: ${src}" >&2
    exit 1
  fi
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "  [dry-run] would install: ${SKILL_ID} → ${dst_dir}/SKILL.md"
  else
    mkdir -p "$dst_dir"
    cp "$src" "${dst_dir}/SKILL.md"
    rm -rf "${dst_dir}/references"
    [[ -d "${CODEX_DIST_DIR}/${SKILL_ID}/references" ]] && cp -R "${CODEX_DIST_DIR}/${SKILL_ID}/references" "${dst_dir}/references"
    echo "  ✓ ${SKILL_ID} → ${dst_dir}/SKILL.md"
  fi
  count=1
else
  # All skills
  for skill_dir in "${CODEX_DIST_DIR}"/*/; do
    [[ -f "${skill_dir}/SKILL.md" ]] || continue
    skill_name="$(basename "$skill_dir")"
    dst_dir="${CODEX_SKILLS_DIR}/${skill_name}"
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "  [dry-run] would install: ${skill_name}"
    else
      mkdir -p "$dst_dir"
      cp "${skill_dir}/SKILL.md" "${dst_dir}/SKILL.md"
      rm -rf "${dst_dir}/references"
      [[ -d "${skill_dir}/references" ]] && cp -R "${skill_dir}/references" "${dst_dir}/references"
      echo "  ✓ ${skill_name}"
    fi
    count=$((count + 1))
  done
fi

# --- Summary ---
echo "---"
if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry-run complete. ${count} skill(s) would be installed."
else
  echo "Done. ${count} skill(s) installed → ${CODEX_SKILLS_DIR}"
  echo "Restart Codex to activate."
fi
