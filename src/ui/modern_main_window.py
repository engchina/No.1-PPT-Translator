#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現代的メインウィンドウ - Material Design 3.0ベース
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QFileDialog, QMessageBox, QMenuBar, QStatusBar,
                              QApplication, QSplitter, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QThread, Signal
from PySide6.QtGui import QAction, QIcon, QFont

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.ui.modern_design_system import MaterialDesign3, ModernColorSystem, ModernAnimationSystem, modern_font_system
from src.ui.modern_components import (ModernCard, ModernButton, ModernLabel, 
                                     ModernTextEdit, ModernComboBox, ModernProgressBar, 
                                     ModernContainer)
from src.utils.config import ConfigManager
from src.core.translator import PPTTranslator


class TranslationWorker(QThread):
    """翻訳処理を行うワーカースレッド"""

    # シグナル定義
    progress_updated = Signal(int)  # 進捗更新
    status_updated = Signal(str)    # ステータス更新
    log_updated = Signal(str)       # ログ更新
    translation_finished = Signal(str)  # 翻訳完了（出力ファイルパス）
    translation_error = Signal(str)     # 翻訳エラー
    translation_stopped = Signal()      # 翻訳停止

    def __init__(self, model_name: str, input_file: str, target_lang: str):
        super().__init__()
        self.model_name = model_name
        self.input_file = input_file
        self.target_lang = target_lang
        self.translator = PPTTranslator()
        self._stop_requested = False  # 停止フラグ

    def run(self):
        """翻訳処理の実行"""
        try:
            if self._stop_requested:
                return

            self.status_updated.emit("翻訳を開始しています...")
            self.log_updated.emit(f"入力ファイル: {self.input_file}")
            self.log_updated.emit(f"対象言語: {self.target_lang}")
            self.log_updated.emit(f"使用モデル: {self.model_name}")

            # 翻訳実行
            output_file = self.translator.translate_ppt(
                model_name=self.model_name,
                input_ppt=self.input_file,
                target_lang=self.target_lang,
                progress_callback=self.progress_updated.emit,
                status_callback=self.status_updated.emit,
                log_callback=self.log_updated.emit,
                stop_callback=self._check_stop_requested  # 停止チェック用コールバック
            )

            if not self._stop_requested:
                self.translation_finished.emit(output_file)

        except Exception as e:
            if not self._stop_requested:
                self.translation_error.emit(str(e))

    def stop_translation(self):
        """翻訳を停止"""
        self._stop_requested = True
        self.log_updated.emit("翻訳の停止が要求されました...")
        self.translation_stopped.emit()

    def _check_stop_requested(self) -> bool:
        """停止が要求されているかチェック"""
        return self._stop_requested


class ModernMainWindow(QMainWindow):
    """現代的メインウィンドウ"""
    
    def __init__(self):
        super().__init__()
        
        # 設定とマネージャーを初期化
        self.config_manager = ConfigManager()
        
        # 翻訳関連の状態
        self.selected_file_path = None
        self.translation_worker = None
        
        # UIを初期化
        self._init_modern_ui()
        self._setup_modern_styling()
        self._connect_signals()
        
        # 初期設定を読み込み
        self._load_initial_settings()
        
        # アニメーション付きで表示
        QTimer.singleShot(100, self._animate_window_entrance)
    
    def _init_modern_ui(self):
        """現代的UIの初期化"""
        self.setWindowTitle("PPT Translator")
        
        # ウィンドウサイズを設定（レスポンシブ）
        self._setup_responsive_window()
        
        # メニューバーを作成
        self._create_modern_menu_bar()
        
        # ステータスバーを作成
        self._create_modern_status_bar()
        
        # メインコンテンツエリアを作成
        self._create_main_content()
    
    def _setup_responsive_window(self):
        """レスポンシブウィンドウサイズ設定"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            # 画面サイズの80%を使用
            width = int(screen_size.width() * 0.8)
            height = int(screen_size.height() * 0.8)
            
            # 最小サイズを設定
            self.setMinimumSize(1000, 700)
            self.resize(width, height)
            
            # 画面中央に配置
            self.move(
                (screen_size.width() - width) // 2,
                (screen_size.height() - height) // 2
            )
    
    def _create_modern_menu_bar(self):
        """現代的メニューバーを作成"""
        menubar = self.menuBar()
        
        # メニューバーのスタイルを設定
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                color: {MaterialDesign3.COLORS['on_surface']};
                border-bottom: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
            }}
            QMenuBar::item {{
                background: transparent;
                padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
                margin: 0px {MaterialDesign3.SPACING['xs']}px;
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
            }}
            QMenuBar::item:selected {{
                background-color: {MaterialDesign3.COLORS['primary_container']};
                color: {MaterialDesign3.COLORS['on_primary_container']};
            }}
            QMenu {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                color: {MaterialDesign3.COLORS['on_surface']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                padding: {MaterialDesign3.SPACING['xs']}px;
            }}
            QMenu::item {{
                padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
                border-radius: {MaterialDesign3.CORNER_RADIUS['extra_small']}px;
            }}
            QMenu::item:selected {{
                background-color: {MaterialDesign3.COLORS['primary_container']};
                color: {MaterialDesign3.COLORS['on_primary_container']};
            }}
        """)
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル")
        
        settings_action = QAction("設定", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._show_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("終了", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        

        # ヘルプメニュー
        help_menu = menubar.addMenu("ヘルプ")
        
        about_action = QAction("このアプリについて", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _create_modern_status_bar(self):
        """現代的ステータスバーを作成"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("準備完了")
        
        # ステータスバーのスタイルを設定
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                color: {MaterialDesign3.COLORS['on_surface_variant']};
                border-top: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                padding: {MaterialDesign3.SPACING['xs']}px {MaterialDesign3.SPACING['md']}px;
            }}
        """)
    
    def _create_main_content(self):
        """メインコンテンツエリアを作成"""
        # 中央ウィジェット
        central_widget = QWidget()
        central_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {MaterialDesign3.COLORS['background']};
            }}
        """)
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(
            MaterialDesign3.SPACING['lg'],
            MaterialDesign3.SPACING['lg'],
            MaterialDesign3.SPACING['lg'],
            MaterialDesign3.SPACING['lg']
        )
        main_layout.setSpacing(MaterialDesign3.SPACING['lg'])
        
        # スプリッターでレイアウトを分割
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左側パネル（ファイル選択と設定）
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右側パネル（ログとプログレス）
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # スプリッターの比率を設定
        splitter.setSizes([400, 600])
    
    def _create_left_panel(self):
        """左側パネルを作成"""
        container = ModernContainer("vertical", "lg")
        
        # ファイル選択カード
        file_card = self._create_file_selection_card()
        container.add_widget(file_card)
        
        # 翻訳設定カード
        settings_card = self._create_translation_settings_card()
        container.add_widget(settings_card)
        
        # 翻訳ボタン
        self.translate_button = ModernButton("翻訳を開始", "filled", "large")
        self.translate_button.clicked.connect(self._start_translation)
        container.add_widget(self.translate_button)

        # 停止ボタン（初期状態では非表示）
        self.stop_button = ModernButton("翻訳を停止", "outlined", "large")
        self.stop_button.clicked.connect(self._stop_translation)
        self.stop_button.setVisible(False)
        container.add_widget(self.stop_button)

        container.add_stretch()
        
        return container
    
    def _create_right_panel(self):
        """右側パネルを作成"""
        container = ModernContainer("vertical", "lg")
        
        # プログレスカード
        progress_card = self._create_progress_card()
        container.add_widget(progress_card)
        
        # ログカード
        log_card = self._create_log_card()
        container.add_widget(log_card, 1)  # ストレッチ
        
        return container
    
    def _create_file_selection_card(self):
        """ファイル選択カードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)
        
        # タイトル
        title = ModernLabel("ファイル選択", "headline_small", "on_surface")
        layout.addWidget(title)
        
        # ファイルパス表示
        self.file_path_label = ModernLabel("PPTXファイルを選択してください", "body_medium", "on_surface_variant")
        self.file_path_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['surface_container_low']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                padding: {MaterialDesign3.SPACING['md']}px;
                min-height: 40px;
            }}
        """)
        layout.addWidget(self.file_path_label)
        
        # ファイル選択ボタン
        self.select_file_button = ModernButton("ファイルを選択", "outlined", "medium")
        self.select_file_button.clicked.connect(self._select_file)
        layout.addWidget(self.select_file_button)
        
        return card

    def _create_translation_settings_card(self):
        """翻訳設定カードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)

        # タイトル
        title = ModernLabel("翻訳設定", "headline_small", "on_surface")
        layout.addWidget(title)

        # AIモデル選択
        model_label = ModernLabel("AIモデル:", "label_large", "on_surface")
        layout.addWidget(model_label)

        self.model_combo = ModernComboBox()
        self.model_combo.setObjectName("model_combo")
        self.model_combo.addItems([
            "gpt-4o",
            "xai.grok-3"
        ])
        layout.addWidget(self.model_combo)

        # 対象言語選択
        lang_label = ModernLabel("対象言語:", "label_large", "on_surface")
        layout.addWidget(lang_label)

        self.language_combo = ModernComboBox()
        self.language_combo.setObjectName("language_combo")
        self.language_combo.addItems(["Japanese", "English", "Chinese"])
        layout.addWidget(self.language_combo)

        return card

    def _create_progress_card(self):
        """プログレスカードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)

        # タイトル
        title = ModernLabel("翻訳進行状況", "headline_small", "on_surface")
        layout.addWidget(title)

        # プログレスバー
        self.progress_bar = ModernProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 進捗詳細情報のコンテナ
        progress_details_layout = QHBoxLayout()

        # ステータステキスト
        self.progress_status = ModernLabel("待機中...", "body_medium", "on_surface_variant")
        progress_details_layout.addWidget(self.progress_status)

        # パーセンテージ表示
        self.progress_percentage = ModernLabel("0%", "body_medium", "primary")
        self.progress_percentage.setVisible(False)
        progress_details_layout.addWidget(self.progress_percentage)

        layout.addLayout(progress_details_layout)

        return card

    def _create_log_card(self):
        """ログカードを作成"""
        card = ModernCard("level_1", "medium")
        layout = QVBoxLayout(card)

        # ヘッダー
        header_layout = QHBoxLayout()

        title = ModernLabel("翻訳ログ", "headline_small", "on_surface")
        header_layout.addWidget(title)

        header_layout.addStretch()

        clear_button = ModernButton("クリア", "text", "small")
        clear_button.clicked.connect(self._clear_log)
        header_layout.addWidget(clear_button)

        layout.addLayout(header_layout)

        # ログテキストエリア
        self.log_text = ModernTextEdit("ログがここに表示されます...")
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        return card

    def _setup_modern_styling(self):
        """現代的スタイリングを設定"""
        # アプリケーション全体のフォントを設定（固定サイズ）
        modern_font_system.apply_global_font(100)

        # ウィンドウの背景色を設定
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {MaterialDesign3.COLORS['background']};
            }}
        """)

    def _connect_signals(self):
        """シグナルを接続"""
        pass

    def _load_initial_settings(self):
        """初期設定を読み込み"""
        try:
            # 設定ファイルから値を読み込み
            settings = self.config_manager.get_all_settings()

            # モデル設定
            if 'model_name' in settings:
                model_name = settings['model_name']
                index = self.model_combo.findText(model_name)
                if index >= 0:
                    self.model_combo.setCurrentIndex(index)

            # 言語設定
            if 'default_language' in settings:
                language = settings['default_language']
                index = self.language_combo.findText(language)
                if index >= 0:
                    self.language_combo.setCurrentIndex(index)

            # 固定フォントサイズを適用
            modern_font_system.apply_global_font(100)

        except Exception as e:
            self._add_log(f"設定読み込みエラー: {e}")

    def _animate_window_entrance(self):
        """ウィンドウ入場アニメーション"""
        # フェードインアニメーション
        self.setWindowOpacity(0.0)
        self.show()

        fade_animation = ModernAnimationSystem.create_property_animation(
            self, b"windowOpacity", "medium4", "decelerate"
        )
        fade_animation.setStartValue(0.0)
        fade_animation.setEndValue(1.0)
        fade_animation.start()

        # スライドインアニメーション
        current_geometry = self.geometry()
        start_geometry = QRect(
            current_geometry.x(),
            current_geometry.y() + 50,
            current_geometry.width(),
            current_geometry.height()
        )

        self.setGeometry(start_geometry)

        slide_animation = ModernAnimationSystem.create_property_animation(
            self, b"geometry", "medium4", "emphasized"
        )
        slide_animation.setStartValue(start_geometry)
        slide_animation.setEndValue(current_geometry)
        slide_animation.start()

    def _select_file(self):
        """ファイル選択ダイアログを表示"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "PPTXファイルを選択",
            "",
            "PowerPoint Files (*.pptx);;All Files (*)"
        )

        if file_path:
            self.selected_file_path = file_path
            self.file_path_label.setText(f"選択済み: {os.path.basename(file_path)}")
            self._add_log(f"ファイルが選択されました: {file_path}")

    def _start_translation(self):
        """翻訳を開始"""
        if not self.selected_file_path:
            from .modern_components import ModernMessageBox
            ModernMessageBox.show_warning(self, "警告", "まずPPTXファイルを選択してください。")
            return

        # UI状態を更新
        self.translate_button.setVisible(False)  # 翻訳ボタンを非表示
        self.stop_button.setVisible(True)        # 停止ボタンを表示
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_percentage.setVisible(True)  # パーセンテージ表示を表示
        self.progress_percentage.setText("0%")
        self.progress_status.setText("翻訳を開始しています...")
        self.status_bar.showMessage("翻訳中...")

        self._add_log("翻訳処理を開始しました")

        # 実際の翻訳処理を実装
        self._start_real_translation()

    def _start_real_translation(self):
        """実際の翻訳処理を開始"""
        # 翻訳ワーカーを作成
        self.translation_worker = TranslationWorker(
            model_name=self.model_combo.currentText(),
            input_file=self.selected_file_path,
            target_lang=self.language_combo.currentText()
        )

        # シグナル接続
        self.translation_worker.progress_updated.connect(self._update_progress)
        self.translation_worker.status_updated.connect(self._update_status)
        self.translation_worker.log_updated.connect(self._add_log)
        self.translation_worker.translation_finished.connect(self._on_translation_finished)
        self.translation_worker.translation_error.connect(self._on_translation_error)
        self.translation_worker.translation_stopped.connect(self._on_translation_stopped)

        # 翻訳開始
        self.translation_worker.start()

    def _update_progress(self, value: int):
        """進捗更新"""
        self.progress_bar.setValue(value)
        self.progress_percentage.setText(f"{value}%")
        if value > 0:
            self.progress_percentage.setVisible(True)

    def _update_status(self, message: str):
        """ステータス更新"""
        self.progress_status.setText(message)
        self.status_bar.showMessage(message)

    def _on_translation_error(self, error_message: str):
        """翻訳エラー処理"""
        self.progress_status.setText("翻訳エラー")
        self.status_bar.showMessage("翻訳エラー")
        self._add_log(f"エラー: {error_message}")

        # UI状態リセット
        self._reset_ui_state()

        # エラーダイアログを表示
        from .modern_components import ModernMessageBox
        ModernMessageBox.show_error(self, "翻訳エラー", f"翻訳中にエラーが発生しました:\n\n{error_message}")

    def _simulate_translation_progress(self):
        """翻訳進行状況をシミュレート（デモ用）"""
        self.progress_timer = QTimer()
        self.progress_value = 0

        def update_progress():
            self.progress_value += 5
            self.progress_bar.setValue(self.progress_value)

            if self.progress_value >= 100:
                self.progress_timer.stop()
                self._on_translation_finished("output_demo.pptx")
            else:
                self.progress_status.setText(f"翻訳中... {self.progress_value}%")

        self.progress_timer.timeout.connect(update_progress)
        self.progress_timer.start(200)  # 200ms間隔

    def _on_translation_finished(self, output_file: str):
        """翻訳完了処理"""
        self.progress_bar.setValue(100)
        self.progress_percentage.setText("100%")
        self.progress_status.setText("翻訳完了！")
        self.status_bar.showMessage("翻訳完了")

        self._add_log(f"翻訳が完了しました: {output_file}")

        # 少し待ってからUI状態リセット（ユーザーが完了状態を確認できるように）
        QTimer.singleShot(2000, self._reset_ui_state)

        # 現代的な完了ダイアログを表示
        from .modern_components import ModernMessageBox, ModernFileHelper

        if ModernMessageBox.show_translation_complete(self, output_file):
            # ダウンロードが選択された場合
            ModernFileHelper.download_file(self, output_file)

    def _open_output_file(self, file_path: str):
        """出力ファイルを開く"""
        try:
            import subprocess
            import platform

            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            self._add_log(f"ファイルを開けません: {e}")

    def _add_log(self, message: str):
        """ログメッセージを追加"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        self.log_text.append(log_entry)

        # 自動スクロール
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)

    def _clear_log(self):
        """ログをクリア"""
        self.log_text.clear()
        self._add_log("ログがクリアされました")

    def _stop_translation(self):
        """翻訳を停止"""
        if self.translation_worker and self.translation_worker.isRunning():
            # 停止確認ダイアログを表示
            from .modern_components import ModernMessageBox
            if ModernMessageBox.show_question(self, "翻訳停止", "翻訳を停止しますか？\n\n進行中の作業は失われます。"):
                self.translation_worker.stop_translation()
                self._add_log("翻訳の停止が要求されました")

    def _on_translation_stopped(self):
        """翻訳停止処理"""
        self.progress_status.setText("翻訳が停止されました")
        self.status_bar.showMessage("翻訳停止")

        # UI状態リセット
        self._reset_ui_state()

        self._add_log("翻訳が停止されました")

    def _reset_ui_state(self):
        """UI状態をリセット"""
        self.translate_button.setVisible(True)   # 翻訳ボタンを表示
        self.stop_button.setVisible(False)       # 停止ボタンを非表示
        self.progress_bar.setVisible(False)
        self.progress_percentage.setVisible(False)  # パーセンテージ表示を非表示
        self.progress_bar.setValue(0)
        self.progress_percentage.setText("0%")
        self.progress_status.setText("待機中...")



    def _show_settings(self):
        """設定ダイアログを表示"""
        from .settings_dialog import ModernSettingsDialog
        dialog = ModernSettingsDialog(self.config_manager, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            # 設定が変更された場合の処理
            self._load_initial_settings()
            self._add_log("設定が更新されました")

    def _show_about(self):
        """このアプリについてダイアログを表示"""
        from .about_dialog import ModernAboutDialog
        dialog = ModernAboutDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        """ウィンドウクローズ時の処理"""
        if self.translation_worker and self.translation_worker.isRunning():
            from .modern_components import ModernMessageBox
            if not ModernMessageBox.show_question(
                self,
                "確認",
                "翻訳が進行中です。終了してもよろしいですか？"
            ):
                event.ignore()
                return

        # 設定を保存
        try:
            self.config_manager.set_setting('model_name', self.model_combo.currentText())
            self.config_manager.set_setting('default_language', self.language_combo.currentText())
        except Exception as e:
            print(f"設定保存エラー: {e}")

        event.accept()
