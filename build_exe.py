#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller用ビルドスクリプト
"""

import os
import sys
import shutil
from pathlib import Path

import PyInstaller.__main__


def clean_build_dirs():
    """ビルドディレクトリをクリーンアップ"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"クリーンアップ中: {dir_name}")
            shutil.rmtree(dir_name)


def create_spec_file():
    """PyInstaller specファイルを作成"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'openai',
        'python_pptx',
        'dotenv',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PPTTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowsでコンソールウィンドウを非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # アイコンファイルがある場合はここに指定
)
'''
    
    with open('PPTTranslator.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("specファイルを作成しました: PPTTranslator.spec")


def build_executable():
    """実行ファイルをビルド"""
    print("PyInstallerでビルド中...")
    
    # PyInstallerを実行
    PyInstaller.__main__.run([
        'PPTTranslator.spec',
        '--clean',
        '--noconfirm'
    ])
    
    print("ビルド完了!")


def copy_additional_files():
    """追加ファイルをコピー"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("distディレクトリが見つかりません")
        return
    
    # README.mdをコピー
    if Path('README.md').exists():
        shutil.copy2('README.md', dist_dir / 'README.md')
        print("README.mdをコピーしました")
    
    # .env.exampleをコピー
    if Path('.env.example').exists():
        shutil.copy2('.env.example', dist_dir / '.env.example')
        print(".env.exampleをコピーしました")
    
    # outputsディレクトリを作成
    outputs_dir = dist_dir / 'outputs'
    outputs_dir.mkdir(exist_ok=True)
    print("outputsディレクトリを作成しました")


def main():
    """メイン処理"""
    print("PPT Translator ビルドスクリプト")
    print("=" * 40)
    
    # 現在のディレクトリを確認
    current_dir = Path.cwd()
    print(f"現在のディレクトリ: {current_dir}")
    
    # main.pyの存在確認
    if not Path('main.py').exists():
        print("エラー: main.pyが見つかりません")
        sys.exit(1)
    
    try:
        # ビルドディレクトリをクリーンアップ
        clean_build_dirs()
        
        # specファイルを作成
        create_spec_file()
        
        # 実行ファイルをビルド
        build_executable()
        
        # 追加ファイルをコピー
        copy_additional_files()
        
        print("\n" + "=" * 40)
        print("ビルドが正常に完了しました!")
        print(f"実行ファイル: {Path('dist') / 'PPTTranslator.exe'}")
        print("=" * 40)
        
    except Exception as e:
        print(f"ビルド中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
