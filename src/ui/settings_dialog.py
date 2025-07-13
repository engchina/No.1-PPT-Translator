#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ダイアログ - Material Design 3.0ベース
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QComboBox, QFileDialog, QMessageBox,
    QTabWidget, QWidget
)

from ..utils.config import ConfigManager
from .modern_design_system import MaterialDesign3, modern_font_system
from .modern_components import ModernCard, ModernButton, ModernLabel, ModernContainer


class ModernSettingsDialog(QDialog):
    """Material Design 3.0ベースの設定ダイアログ"""

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self._init_modern_ui()
        self._setup_modern_styling()
        self.load_settings()

    def _init_modern_ui(self):
        """現代的UIの初期化"""
        self.setWindowTitle("設定 - PPT Translator")
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
        """レスポンシブサイズ設定"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            # 画面サイズに基づくレスポンシブ設定
            if screen_size.width() >= 1920:
                self.resize(900, 700)
            elif screen_size.width() >= 1366:
                self.resize(800, 650)
            else:
                self.resize(700, 600)
        else:
            self.resize(700, 600)

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

        # タブウィジェットを作成
        tab_widget = self._create_modern_tabs()
        main_container.add_widget(tab_widget)

        # ボタンエリアを作成
        button_area = self._create_modern_buttons()
        main_container.add_widget(button_area)

        layout.addWidget(main_container)

    def _create_modern_tabs(self) -> QTabWidget:
        """現代的タブウィジェットを作成"""
        tab_widget = QTabWidget()

        # Material Design 3.0スタイルを適用
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {MaterialDesign3.COLORS['surface_container']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['medium']}px;
            }}
            QTabBar::tab {{
                background-color: {MaterialDesign3.COLORS['surface_variant']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                padding: {MaterialDesign3.SPACING['md']}px {MaterialDesign3.SPACING['lg']}px;
                margin-right: {MaterialDesign3.SPACING['xs']}px;
                border-top-left-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                border-top-right-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                color: {MaterialDesign3.COLORS['on_surface_variant']};
            }}
            QTabBar::tab:selected {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                border-bottom: 2px solid {MaterialDesign3.COLORS['primary']};
                color: {MaterialDesign3.COLORS['primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {MaterialDesign3.COLORS['surface_container_low']};
            }}
        """)

        # API設定タブ
        api_tab = self._create_api_tab()
        tab_widget.addTab(api_tab, "API設定")

        # 一般設定タブ
        general_tab = self._create_general_tab()
        tab_widget.addTab(general_tab, "一般設定")

        return tab_widget

    def _create_api_tab(self) -> QWidget:
        """API設定タブを作成"""
        container = ModernContainer("vertical", "lg")

        # OpenAI設定カード
        openai_card = self._create_openai_card()
        container.add_widget(openai_card)

        # OCI設定カード
        oci_card = self._create_oci_card()
        container.add_widget(oci_card)

        container.add_stretch()
        return container

    def _create_openai_card(self) -> ModernCard:
        """OpenAI設定カードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)
        layout.setSpacing(MaterialDesign3.SPACING['md'])

        # カードタイトル
        title_label = ModernLabel("OpenAI API設定", "headline_small")
        title_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface']};")
        layout.addWidget(title_label)

        # フォームレイアウト
        form_layout = QGridLayout()
        form_layout.setSpacing(MaterialDesign3.SPACING['md'])

        # API Key
        api_key_label = ModernLabel("API Key:", "body_medium")
        api_key_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("OpenAI APIキーを入力してください")
        self._style_input_field(self.api_key_edit)

        # Base URL
        base_url_label = ModernLabel("Base URL:", "body_medium")
        base_url_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        self.base_url_edit = QLineEdit()
        self.base_url_edit.setPlaceholderText("https://api.openai.com/v1")
        self._style_input_field(self.base_url_edit)

        # Model Name
        model_label = ModernLabel("モデル名:", "body_medium")
        model_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        self.model_name_edit = QLineEdit()
        self.model_name_edit.setPlaceholderText("gpt-4o")
        self._style_input_field(self.model_name_edit)

        form_layout.addWidget(api_key_label, 0, 0)
        form_layout.addWidget(self.api_key_edit, 0, 1)
        form_layout.addWidget(base_url_label, 1, 0)
        form_layout.addWidget(self.base_url_edit, 1, 1)
        form_layout.addWidget(model_label, 2, 0)
        form_layout.addWidget(self.model_name_edit, 2, 1)

        layout.addLayout(form_layout)
        return card

    def _create_oci_card(self) -> ModernCard:
        """OCI設定カードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)
        layout.setSpacing(MaterialDesign3.SPACING['md'])

        # カードタイトル
        title_label = ModernLabel("OCI GenAI設定（オプション）", "headline_small")
        title_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface']};")
        layout.addWidget(title_label)

        # フォームレイアウト
        form_layout = QGridLayout()
        form_layout.setSpacing(MaterialDesign3.SPACING['md'])

        # Compartment ID
        compartment_label = ModernLabel("Compartment ID:", "body_medium")
        compartment_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        self.compartment_id_edit = QLineEdit()
        self.compartment_id_edit.setPlaceholderText("OCI Compartment IDを入力してください")
        self._style_input_field(self.compartment_id_edit)

        # Config Profile
        profile_label = ModernLabel("設定プロファイル:", "body_medium")
        profile_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        self.config_profile_edit = QLineEdit()
        self.config_profile_edit.setPlaceholderText("DEFAULT")
        self._style_input_field(self.config_profile_edit)

        form_layout.addWidget(compartment_label, 0, 0)
        form_layout.addWidget(self.compartment_id_edit, 0, 1)
        form_layout.addWidget(profile_label, 1, 0)
        form_layout.addWidget(self.config_profile_edit, 1, 1)

        layout.addLayout(form_layout)
        return card

    def _create_general_tab(self) -> QWidget:
        """一般設定タブを作成"""
        container = ModernContainer("vertical", "lg")

        # 一般設定カード
        general_card = self._create_general_card()
        container.add_widget(general_card)

        container.add_stretch()
        return container

    def _create_general_card(self) -> ModernCard:
        """一般設定カードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)
        layout.setSpacing(MaterialDesign3.SPACING['md'])

        # カードタイトル
        title_label = ModernLabel("一般設定", "headline_small")
        title_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface']};")
        layout.addWidget(title_label)

        # フォームレイアウト
        form_layout = QGridLayout()
        form_layout.setSpacing(MaterialDesign3.SPACING['md'])

        # デフォルト言語
        lang_label = ModernLabel("デフォルト対象言語:", "body_medium")
        lang_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        self.default_language_combo = QComboBox()
        self.default_language_combo.addItems(["Japanese", "English", "Chinese"])
        self._style_combo_box(self.default_language_combo)

        # 出力ディレクトリ
        output_label = ModernLabel("出力ディレクトリ:", "body_medium")
        output_label.setStyleSheet(f"color: {MaterialDesign3.COLORS['on_surface_variant']};")
        output_layout = QHBoxLayout()
        output_layout.setSpacing(MaterialDesign3.SPACING['sm'])

        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("出力ディレクトリを選択")
        self._style_input_field(self.output_dir_edit)

        browse_btn = ModernButton("参照", "outlined", "medium")
        browse_btn.clicked.connect(self.browse_output_dir)

        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(browse_btn)

        form_layout.addWidget(lang_label, 0, 0)
        form_layout.addWidget(self.default_language_combo, 0, 1)
        form_layout.addWidget(output_label, 1, 0)
        form_layout.addLayout(output_layout, 1, 1)

        layout.addLayout(form_layout)
        return card

    def _style_input_field(self, field: QLineEdit):
        """入力フィールドにMaterial Design 3.0スタイルを適用"""
        field.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['extra_small']}px;
                padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
                background-color: {MaterialDesign3.COLORS['surface_container_highest']};
                color: {MaterialDesign3.COLORS['on_surface']};
                min-height: 24px;
            }}
            QLineEdit:focus {{
                border: 2px solid {MaterialDesign3.COLORS['primary']};
                background-color: {MaterialDesign3.COLORS['surface_container']};
            }}
        """)

    def _style_combo_box(self, combo: QComboBox):
        """コンボボックスにMaterial Design 3.0スタイルを適用"""
        combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['extra_small']}px;
                padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
                background-color: {MaterialDesign3.COLORS['surface_container_highest']};
                color: {MaterialDesign3.COLORS['on_surface']};
                min-height: 24px;
            }}
            QComboBox:focus {{
                border: 2px solid {MaterialDesign3.COLORS['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {MaterialDesign3.COLORS['on_surface_variant']};
            }}
        """)

    def _create_modern_buttons(self) -> QWidget:
        """現代的ボタンエリアを作成"""
        button_container = QWidget()
        button_container.setStyleSheet(f"""
            QWidget {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                border-top: 1px solid {MaterialDesign3.COLORS['outline_variant']};
            }}
        """)

        layout = QHBoxLayout(button_container)
        layout.setContentsMargins(
            MaterialDesign3.SPACING['lg'],
            MaterialDesign3.SPACING['md'],
            MaterialDesign3.SPACING['lg'],
            MaterialDesign3.SPACING['md']
        )
        layout.setSpacing(MaterialDesign3.SPACING['md'])

        # キャンセルボタン
        self.cancel_btn = ModernButton("キャンセル", "outlined", "medium")
        self.cancel_btn.clicked.connect(self.reject)

        # 保存ボタン
        self.ok_btn = ModernButton("設定を保存", "filled", "medium")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setDefault(True)

        layout.addStretch()
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.ok_btn)

        return button_container

    def browse_output_dir(self):
        """出力ディレクトリを参照"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "出力ディレクトリを選択",
            self.output_dir_edit.text()
        )
        
        if dir_path:
            self.output_dir_edit.setText(dir_path)



    def load_settings(self):
        """設定を読み込み"""
        # API設定
        self.api_key_edit.setText(self.config_manager.get_openai_api_key() or "")
        self.base_url_edit.setText(self.config_manager.get_openai_base_url() or "")
        self.model_name_edit.setText(self.config_manager.get_openai_model_name() or "")
        self.compartment_id_edit.setText(self.config_manager.get_compartment_id() or "")
        self.config_profile_edit.setText(self.config_manager.get_config_profile() or "")

        # 一般設定
        default_lang = self.config_manager.get_default_language()
        if default_lang:
            index = self.default_language_combo.findText(default_lang)
            if index >= 0:
                self.default_language_combo.setCurrentIndex(index)

        self.output_dir_edit.setText(self.config_manager.get_output_directory() or "")

    def accept(self):
        """設定を保存して閉じる"""
        try:
            # API設定を保存
            self.config_manager.set_openai_api_key(self.api_key_edit.text())
            self.config_manager.set_openai_base_url(self.base_url_edit.text())
            self.config_manager.set_openai_model_name(self.model_name_edit.text())
            self.config_manager.set_compartment_id(self.compartment_id_edit.text())
            self.config_manager.set_config_profile(self.config_profile_edit.text())

            # 一般設定を保存
            self.config_manager.set_default_language(self.default_language_combo.currentText())
            self.config_manager.set_output_directory(self.output_dir_edit.text())

            self.config_manager.save_config()
            super().accept()

        except Exception as e:
            from .modern_components import ModernMessageBox
            ModernMessageBox.show_error(self, "エラー", f"設定の保存に失敗しました:\n{e}")


# 後方互換性のため
SettingsDialog = ModernSettingsDialog
