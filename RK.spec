# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect additional files (app_data.db, ui/, logic/, constants.py)
datas = [
    ('ui/*', 'ui'),
    ('ui/utils/*', 'ui/utils'),
    ('logic/*', 'logic'),
    ('icon/*', 'icon'),
] + collect_data_files('ttkbootstrap')  # If using ttkbootstrap

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=['peewee', 'pyzk'],  # Add external packages here
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'ruff', 'app_data.db'],  # Exclude unused heavy packages
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RK_ZKTeco',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable
    console=False,  # Hide console for GUI app
    icon='icon/app.ico',  # Windows icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RK_ZKTeco',
)

# macOS app bundle (add for macOS builds)
app = BUNDLE(
    coll,
    name='rk_zkteco.app',
    icon='icon/app.icns',  # macOS icon
    bundle_identifier='com.riajulkashem.RK_ZKTeco',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleName': 'RK_ZKTeco',
        'CFBundleDisplayName': 'RK FingerPrint Connector',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
)