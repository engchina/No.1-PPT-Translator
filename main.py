#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT翻訳アプリケーション - 現代的デザインシステム
Material Design 3.0に基づく現代的なPowerPoint翻訳アプリケーション
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase

# 現代的UIシステムをインポート
from src.ui.modern_main_window import ModernMainWindow
from src.ui.modern_design_system import MaterialDesign3, modern_font_system


def setup_application():
    """アプリケーションの基本設定"""
    # 高DPI対応の設定（QApplication作成前に設定）
    # Qt 6.0以降では自動的に有効になるため、これらの設定は条件付きで適用
    try:
        from PySide6.QtCore import qVersion
        qt_version = qVersion()
        major_version = int(qt_version.split('.')[0])

        # Qt 5.x系でのみ高DPI設定を適用
        if major_version < 6:
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        # Qt 6.0以降では自動的に処理されるため設定不要

    except (AttributeError, ValueError):
        # 属性が存在しない場合やバージョン解析に失敗した場合は無視
        pass

    # QApplicationの初期化
    app = QApplication(sys.argv)

    # アプリケーション情報の設定
    app.setApplicationName("PPT Translator")
    app.setApplicationVersion(".0.0")
    app.setOrganizationName("Modern Design Lab")
    app.setApplicationDisplayName("PPT Translator")

    return app


def setup_modern_fonts():
    """現代的フォントシステムの設定"""
    try:
        # システムフォント情報を取得
        available_fonts = QFontDatabase.families()

        print("=== 現代的フォントシステム初期化 ===")
        print(f"システム利用可能フォント数: {len(available_fonts)}")

        # 推奨フォントの確認
        recommended_fonts = ['Noto Sans JP', 'Inter', 'Roboto', 'system-ui', 'Segoe UI']
        found_fonts = []

        for font in recommended_fonts:
            if font in available_fonts:
                found_fonts.append(font)
                print(f"✅ {font} - 利用可能")
            else:
                print(f"❌ {font} - 利用不可")

        if found_fonts:
            print(f"使用フォント: {found_fonts[0]}")
        else:
            print("デフォルトシステムフォントを使用")

        return True

    except Exception as e:
        print(f"フォント設定エラー: {e}")
        return False


def display_system_info():
    """システム情報を表示"""
    app = QApplication.instance()
    if app:
        screen = app.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            dpi = screen.logicalDotsPerInch()
            device_pixel_ratio = screen.devicePixelRatio()

            print("\n=== システム情報 ===")
            print(f"画面サイズ: {screen_size.width()}x{screen_size.height()}")
            print(f"DPI: {dpi}")
            print(f"デバイスピクセル比: {device_pixel_ratio}")

            # 高DPI表示の検出
            if dpi > 120:
                print(f"高DPI表示を検出: 固定フォントサイズで最適化済み")


def main():
    """アプリケーションのメインエントリーポイント"""
    print("🎨 PPT Translator v1.0.0")
    print("=" * 60)
    print("Material Design 3.0に基づく現代的なPowerPoint翻訳アプリケーション")
    print("=" * 60)

    try:
        # アプリケーションを設定
        app = setup_application()

        # フォントシステムを設定
        if not setup_modern_fonts():
            print("⚠️  フォント設定に問題がありますが、続行します...")

        # システム情報を表示
        display_system_info()

        # 現代的フォントシステムを初期化
        print("\n=== 現代的フォントシステム適用 ===")
        modern_font_system.apply_global_font()  # 固定フォントサイズ

        # Material Design 3.0 情報を表示
        print("\n=== Material Design 3.0 デザインシステム ===")
        print(f"カラーパレット: {len(MaterialDesign3.COLORS)} 色")
        print(f"タイポグラフィスケール: {len(MaterialDesign3.TYPOGRAPHY)} スタイル")
        print(f"エレベーションレベル: {len(MaterialDesign3.ELEVATION)} レベル")
        print(f"角丸半径: {len(MaterialDesign3.CORNER_RADIUS)} サイズ")
        print(f"スペーシング: {len(MaterialDesign3.SPACING)} サイズ")

        # メインウィンドウの作成
        print("\n=== メインウィンドウ作成 ===")
        main_window = ModernMainWindow()

        print("✅ 現代的UIシステムが正常に初期化されました")
        print("\n🚀 アプリケーションを起動中...")

        # ウィンドウを表示（アニメーション付きで表示される）
        # main_window.show() は ModernMainWindow の __init__ で自動的に呼ばれる

        # メインウィンドウの参照を保持（ガベージコレクション防止）
        app.main_window = main_window

        # アプリケーションを実行
        exit_code = app.exec()

        print(f"\n👋 アプリケーション終了 (コード: {exit_code})")
        return exit_code

    except ImportError as e:
        print(f"\n❌ モジュールインポートエラー: {e}")
        print("必要な依存関係がインストールされていない可能性があります。")
        return 1

    except Exception as e:
        print(f"\n❌ アプリケーション実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

        # エラーダイアログを表示（可能な場合）
        try:
            app = QApplication.instance()
            if app:
                QMessageBox.critical(
                    None,
                    "アプリケーションエラー",
                    f"アプリケーションの実行中にエラーが発生しました:\n\n{str(e)}\n\n"
                    "詳細はコンソールログを確認してください。"
                )
        except:
            pass

        return 1


if __name__ == "__main__":
    sys.exit(main())
