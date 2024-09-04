# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(2000)
print("Recursion limit:", sys.getrecursionlimit())

a = Analysis(
    ['Main.py'],
    pathex=['D:\\software\\Anaconda\\Anaconda3\\envs\\vtpShow\\Lib\\site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('D:\\software\\Anaconda\\Anaconda3\\envs\\vtpShow\\python.exe', None, 'OPTION')],
    name='ShowVtp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
