# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['D:\\Python\\App\\App_convert_py\\main.py'],
            pathex=[],
            binaries=[],
            datas=[('D:\\\\Python\\\\App\\\\App_convert_py\\\\compiler\\\\Keep', 'compiler'), ('D:\\\\Python\\\\App\\\\App_convert_py\\\\GUI\\\\ui', 'GUI\\\\ui'), ('D:\\\\Python\\\\App\\\\App_convert_py\\\\GUI\\\\images\\\\Logo', 'GUI\\\\Images\\\\Logo')],
            hiddenimports=[],
            hookspath=[],
            hooksconfig={},
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher,
            noarchive=False)

to_remove = ["_AES", "_ARC4", "_DES", "_DES3", "_SHA256", "_counter"]
for b in a.binaries:
    if any(f'{crypto}.cp37-win_amd64.pyd' in b[1] for crypto in to_remove):
        print(f"Removing {b[1]}")
        a.binaries.remove(b)

pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)

exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='Convert Python - v1.0',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None, uac_admin=False, icon='D:\\Python\\App\\App_convert_py\\GUI\\images\\Logo\\logoPython.ico')
