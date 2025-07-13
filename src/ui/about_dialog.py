#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アプリについてダイアログ - Material Design 3.0ベース
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon

from .modern_design_system import MaterialDesign3, modern_font_system
from .modern_components import ModernCard, ModernButton, ModernLabel, ModernContainer


class ModernAboutDialog(QDialog):
    """Material Design 3.0ベースのアプリについてダイアログ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_modern_ui()
        self._setup_modern_styling()

    def _init_modern_ui(self):
        """現代的UIの初期化"""
        self.setWindowTitle("PPT Translator について")
        self.setModal(True)
        
        # レスポンシブサイズ設定
        self._setup_responsive_size()
        
        # メインレイアウト
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 現代的コンテンツを作成
        self._create_modern_content(layout)

    def _setup_responsive_size(self):
        """レスポンシブサイズ設定 - 統一版"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            # 画面サイズに基づくレスポンシブ設定（他のダイアログと統一）
            if screen_size.width() >= 1920:
                self.resize(800, 500)  # 4K/高解像度用
            elif screen_size.width() >= 1366:
                self.resize(700, 450)  # フルHD用
            else:
                self.resize(600, 400)  # 小画面用
        else:
            self.resize(600, 400)  # デフォルト

    def _setup_modern_styling(self):
        """現代的スタイリングを設定"""
        # Material Design 3.0フォントシステムを適用
        modern_font_system.apply_global_font(100)
        
        # ダイアログ全体のスタイル
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {MaterialDesign3.COLORS['background']};
            }}
        """)

    def _create_modern_content(self, layout):
        """現代的コンテンツを作成"""
        # メインコンテナ
        main_container = ModernContainer("vertical", "lg")
        main_container.setStyleSheet(f"""
            QWidget {{
                background-color: {MaterialDesign3.COLORS['background']};
            }}
        """)
        
        # アプリ情報カードを作成
        app_info_card = self._create_app_info_card()
        main_container.add_widget(app_info_card)
        
        # ボタンエリアを作成
        button_area = self._create_modern_buttons()
        main_container.add_widget(button_area)
        
        layout.addWidget(main_container)

    def _create_app_info_card(self) -> ModernCard:
        """アプリ情報カードを作成 - 拡大版対応"""
        card = ModernCard("level_2", "large")
        layout = QVBoxLayout(card)
        layout.setSpacing(MaterialDesign3.SPACING['xl'])  # より大きなスペーシング
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アプリアイコン（拡大版）
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setFixedSize(120, 120)  # より大きなアイコン
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {MaterialDesign3.COLORS['primary']};
                border-radius: 60px;
                color: {MaterialDesign3.COLORS['on_primary']};
                font-size: 48px;  /* より大きなフォント */
                font-weight: bold;
            }}
        """)
        icon_label.setText("PPT")
        layout.addWidget(icon_label)
        
        # アプリ名
        app_name_label = ModernLabel("PPT Translator", "display_small")
        app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name_label.setStyleSheet(f"""
            color: {MaterialDesign3.COLORS['on_surface']};
            font-weight: bold;
        """)
        layout.addWidget(app_name_label)
        
        # バージョン
        version_label = ModernLabel("v1.0.0", "title_large")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"""
            color: {MaterialDesign3.COLORS['primary']};
            font-weight: 500;
        """)
        layout.addWidget(version_label)
        
        # 説明（拡大版対応）
        description_label = ModernLabel(
            "Material Design 3.0に基づく現代的な\nPowerPoint翻訳アプリケーション。\n\n"
            "AI技術を使用してPowerPointファイルを高品質\nに翻訳します。",
            "body_large"
        )
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet(f"""
            color: {MaterialDesign3.COLORS['on_surface_variant']};
            line-height: 1.6;
            padding: {MaterialDesign3.SPACING['md']}px;
        """)
        layout.addWidget(description_label)

        # スペーサーを追加
        layout.addSpacing(MaterialDesign3.SPACING['lg'])

        # 技術情報（拡大版対応）
        tech_info_label = ModernLabel(
            "🎨 Material Design 3.0\n\n"
            "🤖 AI翻訳技術\n\n"
            "📱 レスポンシブデザイン\n\n"
            "🌐 多言語対応",
            "body_large"  # より大きなフォント
        )
        tech_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tech_info_label.setStyleSheet(f"""
            color: {MaterialDesign3.COLORS['on_surface_variant']};
            background-color: {MaterialDesign3.COLORS['surface_container_low']};
            border-radius: {MaterialDesign3.CORNER_RADIUS['medium']}px;
            padding: {MaterialDesign3.SPACING['lg']}px;
            line-height: 1.8;
            min-height: 120px;
        """)
        layout.addWidget(tech_info_label)
        
        return card

    def _create_modern_buttons(self) -> QWidget:
        """現代的ボタンエリアを作成 - 拡大版対応"""
        button_container = QWidget()
        button_container.setStyleSheet(f"""
            QWidget {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                border-top: 1px solid {MaterialDesign3.COLORS['outline_variant']};
            }}
        """)

        layout = QHBoxLayout(button_container)
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],  # より大きなマージン
            MaterialDesign3.SPACING['lg'],  # より大きなマージン
            MaterialDesign3.SPACING['xl'],  # より大きなマージン
            MaterialDesign3.SPACING['lg']   # より大きなマージン
        )
        layout.setSpacing(MaterialDesign3.SPACING['lg'])

        # OKボタン（拡大版）
        self.ok_btn = ModernButton("OK", "filled", "large")  # より大きなボタン
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)
        self.ok_btn.setMinimumWidth(120)  # 最小幅を設定

        layout.addStretch()
        layout.addWidget(self.ok_btn)

        return button_container


# 後方互換性のため
AboutDialog = ModernAboutDialog
