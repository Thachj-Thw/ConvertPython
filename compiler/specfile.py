import os


class SpecFile:
    ONE_DIR = """# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['%s'],
            pathex=%s,
            binaries=%s,
            datas=%s,
            hiddenimports=%s,
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
        [],
        exclude_binaries=True,
        name='%s',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=%s,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None , uac_admin=%s%s)
coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='%s')
"""
    ONE_FILE = """# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['%s'],
            pathex=%s,
            binaries=%s,
            datas=%s,
            hiddenimports=%s,
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
        name='%s',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=%s,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None, uac_admin=%s%s)
"""
    _path = os.path.join(os.path.dirname(__file__), "compile.spec")

    @staticmethod
    def one_file(
        input_file: str,
        pathex: list,
        binaries: list,
        data: list,
        hidden_imports: list,
        name: str,
        console: bool,
        uac_admin: bool,
        icon: str,
    ):
        data = SpecFile.ONE_FILE % (input_file, pathex, binaries, data, hidden_imports, name, console, uac_admin, f", icon='{icon}'" if icon else "")
        with open(SpecFile._path, "w", encoding="utf-8") as f:
            f.write(data)
        return SpecFile._path

    @staticmethod
    def one_dir(
        input_file: str,
        pathex: list,
        binaries: list,
        data: list,
        hidden_imports: list,
        name: str,
        console: bool,
        uac_admin: bool,
        icon: str
    ):
        data = SpecFile.ONE_DIR % (input_file, pathex, binaries, data, hidden_imports, name, console, uac_admin, f", icon='{icon}'" if icon else "", name)
        with open(SpecFile._path, "w", encoding="utf-8") as f:
            f.write(data)
        return SpecFile._path