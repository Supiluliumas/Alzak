$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $RepoRoot
$Python = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else { Join-Path $RepoRoot ".venv\Scripts\python.exe" }
if (-not (Test-Path $Python)) { throw "Python 3.12 environment not found: $Python" }
& $Python -c "import sys; assert sys.version_info[:2] == (3, 12), sys.version"
& $Python -m PyInstaller --noconfirm packaging/alzak.spec
