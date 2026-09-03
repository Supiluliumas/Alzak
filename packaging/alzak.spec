# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

root = Path(SPEC).resolve().parents[1]

a = Analysis(
    [str(root / "src" / "alzak" / "__main__.py")],
    pathex=[str(root / "src")],
    binaries=[],
    datas=[(str(root / "assets"), "assets"), (str(root / "levels"), "levels")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "_pytest", "PyInstaller"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Alzak",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

collection = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="Alzak",
)

if sys.platform == "darwin":
    app = BUNDLE(
        collection,
        name="Alzak.app",
        icon=None,
        bundle_identifier="cz.alzak.platformer.demo",
        info_plist={"NSHighResolutionCapable": True},
    )
