from pathlib import Path


def test_spec_includes_runtime_data_and_excludes_development_tools() -> None:
    content = Path("packaging/alzak.spec").read_text(encoding="utf-8")
    assert 'root / "assets"' in content
    assert 'root / "levels"' in content
    assert '"pytest"' in content
    assert '"PyInstaller"' in content
    assert "console=False" in content
    assert 'sys.platform == "win32"' in content
    assert "a.binaries" in content
    assert "alzak_devtools" not in content


def test_ci_defines_all_three_artifacts() -> None:
    content = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    for name in ("alzak-windows-x64", "alzak-macos-arm64", "alzak-macos-x86_64"):
        assert f"name: {name}" in content
    assert "runs-on: macos-15" in content
    assert "runs-on: macos-15-intel" in content
