#!/bin/bash

echo "PPT Translator ビルドスクリプト"
echo "================================"

# 仮想環境をアクティベート（存在する場合）
if [ -f "venv/bin/activate" ]; then
    echo "仮想環境をアクティベート中..."
    source venv/bin/activate
fi

# 依存関係をインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt

# PyInstallerでビルド
echo "PyInstallerでビルド中..."
python build_exe.py

echo ""
echo "ビルド完了!"
echo "実行ファイル: dist/PPTTranslator"
