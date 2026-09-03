#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON_BIN:-$repo_root/.venv/bin/python}"
if [[ ! -x "$python_bin" ]]; then
  echo "Python 3.12 environment not found: $python_bin" >&2
  exit 2
fi
"$python_bin" -c 'import sys; assert sys.version_info[:2] == (3, 12), sys.version'
"$python_bin" -m PyInstaller --noconfirm packaging/alzak.spec
