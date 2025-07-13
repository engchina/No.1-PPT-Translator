@echo off
echo PPT Translator ビルドスクリプト
echo ================================

REM 仮想環境をアクティベート（存在する場合）
if exist "venv\Scripts\activate.bat" (
    echo 仮想環境をアクティベート中...
    call venv\Scripts\activate.bat
)

REM 依存関係をインストール
echo 依存関係をインストール中...
pip install -r requirements.txt

REM PyInstallerでビルド
echo PyInstallerでビルド中...
python build_exe.py

echo.
echo ビルド完了!
echo 実行ファイル: dist\PPTTranslator.exe
pause
