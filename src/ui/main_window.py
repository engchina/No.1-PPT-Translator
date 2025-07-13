#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPT翻訳アプリケーションのメインウィンドウ - 现代化UI/UX优化版
"""
import os
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, QProgressBar,
    QTextEdit, QGroupBox, QMessageBox, QStatusBar, QMenuBar,
    QMenu, QSplitter, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, QSettings, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QAction, QFont, QIcon, QPalette, QColor, QLinearGradient, QPainter, QPen

from ..core.translator import PPTTranslator
from ..utils.config import ConfigManager
from ..utils.logger import get_logger, LogLevel
from ..utils.ui_helper import UIHelper
from ..utils.font_manager import get_font_manager, get_log_font


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
    """现代化メインウィンドウクラス"""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.translation_worker: Optional[TranslationWorker] = None
        self.logger = get_logger()
        
        # 现代化UI设置
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()
        self.setup_logging()
        self.load_settings()
        self.setup_modern_style()

        # UIが完全に初期化された後に統一フォントを適用
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self.apply_unified_fonts)
    
    def init_ui(self):
        """現代的UIの初期化"""
        self.setWindowTitle("PPT Translator")

        # レスポンシブウィンドウサイズ - 画面解像度に基づく
        self.setup_responsive_window()

        # 現代的メニューバーを作成
        self.create_modern_menu_bar()

        # 現代的ステータスバーを作成
        self.create_modern_status_bar()

        # 中央ウィジェットを作成
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # 現代的メインレイアウト
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 現代的カード式レイアウト
        self.create_modern_cards(main_layout)
        
    def setup_responsive_window(self):
        """レスポンシブウィンドウサイズ設定"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            # 画面サイズに基づくレスポンシブデザイン
            if screen_size.width() >= 1920 and screen_size.height() >= 1080:
                # 大画面 - 1440x900
                self.setMinimumSize(1000, 700)
                self.resize(1440, 900)
            elif screen_size.width() >= 1366 and screen_size.height() >= 768:
                # 中画面 - 1200x800
                self.setMinimumSize(900, 650)
                self.resize(1200, 800)
            else:
                # 小画面 - 1000x700
                self.setMinimumSize(800, 600)
                self.resize(1000, 700)
        else:
            # デフォルトサイズ
            self.setMinimumSize(800, 600)
            self.resize(1200, 800)
    
    def create_modern_menu_bar(self):
        """创建现代化菜单栏"""
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 使用自定义菜单栏
        
        # 現代的スタイル（フォントサイズを削除し、統一管理に委ねる）
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                padding: 8px 20px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 16px;
                margin: 0px 2px;
                border-radius: 6px;
                color: #495057;
            }
            QMenuBar::item:selected {
                background-color: #e9ecef;
                color: #212529;
            }
            QMenuBar::item:pressed {
                background-color: #dee2e6;
            }
        """)
        
        # ファイルメニュー
        file_menu = menubar.addMenu("ファイル")

        settings_action = QAction("設定", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        exit_action = QAction("終了", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)



        # ヘルプメニュー
        help_menu = menubar.addMenu("ヘルプ")

        about_action = QAction("このアプリについて", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_modern_status_bar(self):
        """创建现代化状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 現代的スタイル（フォントサイズを削除し、統一管理に委ねる）
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
                padding: 8px 20px;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        self.status_bar.showMessage("准备就绪")
    
    def create_modern_cards(self, main_layout):
        """创建现代化卡片式布局"""
        # 文件选择卡片
        file_card = self.create_file_selection_card()
        main_layout.addWidget(file_card)
        
        # 翻译设置卡片
        settings_card = self.create_translation_settings_card()
        main_layout.addWidget(settings_card)
        
        # 操作卡片
        action_card = self.create_action_card()
        main_layout.addWidget(action_card)
        
        # 日志卡片
        log_card = self.create_log_card()
        main_layout.addWidget(log_card)
    
    def create_file_selection_card(self) -> QFrame:
        """创建现代化文件选择卡片"""
        card = QFrame()
        card.setObjectName("fileCard")
        card.setStyleSheet("""
            #fileCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # タイトル
        title = QLabel("ファイル選択")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #212529;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        # ファイルパス表示
        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)

        self.file_path_label = QLabel("PPTXファイルを選択してください")
        self.file_path_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                padding: 12px;
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        self.file_path_label.setMinimumHeight(45)

        self.select_file_btn = QPushButton("ファイル選択")
        self.select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.select_file_btn.clicked.connect(self.select_file)
        
        file_layout.addWidget(self.file_path_label, 1)
        file_layout.addWidget(self.select_file_btn)
        
        layout.addLayout(file_layout)
        
        return card
    
    def create_translation_settings_card(self) -> QFrame:
        """创建现代化翻译设置卡片"""
        card = QFrame()
        card.setObjectName("settingsCard")
        card.setStyleSheet("""
            #settingsCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # タイトル
        title = QLabel("翻訳設定")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #212529;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        # 設定グリッド
        settings_grid = QGridLayout()
        settings_grid.setSpacing(15)

        # モデル選択
        model_label = QLabel("AIモデル:")
        model_label.setStyleSheet("font-size: 14px; color: #495057;")
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "gpt-4o",
            "cohere.command-r-08-2024",
            "cohere.command-r-plus-08-2024"
        ])
        self.model_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                min-height: 40px;
            }
            QComboBox:hover {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        # 選択後にフォーカスを失う機能を追加
        UIHelper.setup_combo_auto_blur(self.model_combo)

        # 対象言語
        lang_label = QLabel("対象言語:")
        lang_label.setStyleSheet("font-size: 14px; color: #495057;")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Japanese", "English", "Chinese"])
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                min-height: 40px;
            }
            QComboBox:hover {
                border-color: #007bff;
            }
        """)
        # 選択後にフォーカスを失う機能を追加
        UIHelper.setup_combo_auto_blur(self.language_combo)
        
        settings_grid.addWidget(model_label, 0, 0)
        settings_grid.addWidget(self.model_combo, 0, 1)
        settings_grid.addWidget(lang_label, 1, 0)
        settings_grid.addWidget(self.language_combo, 1, 1)
        
        layout.addLayout(settings_grid)
        
        return card
    
    def create_action_card(self) -> QFrame:
        """创建现代化操作卡片"""
        card = QFrame()
        card.setObjectName("actionCard")
        card.setStyleSheet("""
            #actionCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # 翻訳ボタン
        self.translate_btn = QPushButton("翻訳開始")
        self.translate_btn.setEnabled(False)
        self.translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
                min-height: 50px;
            }
            QPushButton:hover:!pressed:!disabled {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
        """)
        self.translate_btn.clicked.connect(self.start_translation)

        # 停止ボタン（初期状態では非表示）
        self.stop_btn = QPushButton("翻訳停止")
        self.stop_btn.setVisible(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 600;
                min-height: 50px;
            }
            QPushButton:hover:!pressed {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_translation)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 10px;
                text-align: center;
                height: 40px;
                font-size: 15px;
                font-weight: 600;
                color: white;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 10px;
            }
        """)
        # 设置进度条高度
        self.progress_bar.setMinimumHeight(40)
        self.progress_bar.setMaximumHeight(40)

        layout.addWidget(self.translate_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.progress_bar)
        
        return card
    
    def create_log_card(self) -> QFrame:
        """创建现代化日志卡片"""
        card = QFrame()
        card.setObjectName("logCard")
        card.setStyleSheet("""
            #logCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e9ecef;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(15)
        
        # タイトルとクリアボタン
        header_layout = QHBoxLayout()

        title = QLabel("翻訳ログ")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #212529;
            }
        """)

        clear_btn = QPushButton("ログクリア")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6c757d;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                color: #495057;
            }
        """)
        clear_btn.clicked.connect(self.clear_log)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # 日志文本区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_font = get_log_font()
        self.log_text.setFont(log_font)
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: #f8f9fa;
                padding: 10px;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        
        layout.addWidget(self.log_text)
        
        return card
    
    def setup_modern_style(self):
        """设置现代化全局样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            QScrollBar:vertical {
                border: none;
                background: #f1f3f4;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #c1c8cd;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a8b3bd;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
    
    def setup_logging(self):
        """日志系统设置"""
        qt_handler = self.logger.setup_qt_handler()
        qt_handler.log_message.connect(self.on_log_message)
    
    def on_log_message(self, message: str, level: int):
        """日志消息接收"""
        # 日志级别对应颜色
        colors = {
            LogLevel.ERROR: "#dc3545",
            LogLevel.WARNING: "#fd7e14",
            LogLevel.INFO: "#007bff",
            LogLevel.DEBUG: "#6c757d"
        }
        
        color = colors.get(level, "#6c757d")
        timestamp = self.get_current_time()
        
        # 现代化日志格式
        formatted_message = f'<span style="color: {color}; font-weight: 500;">[{timestamp}]</span> <span style="color: #495057;">{message}</span>'
        self.log_text.append(formatted_message)
    
    def select_file(self):
        """现代化文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择PPTX文件",
            "",
            "PowerPoint Files (*.pptx);;All Files (*)"
        )
        
        if file_path:
            self.file_path_label.setText(file_path)
            self.file_path_label.setStyleSheet("""
                QLabel {
                    color: #212529;
                    font-size: 14px;
                    padding: 12px;
                    background-color: #e7f3ff;
                    border: 1px solid #b3d9ff;
                    border-radius: 8px;
                }
            """)
            self.translate_btn.setEnabled(True)
            self.add_log(f"ファイルが選択されました: {file_path}")

    def start_translation(self):
        """翻訳開始"""
        if not self.file_path_label.text() or self.file_path_label.text() == "PPTXファイルを選択してください":
            from .modern_components import ModernMessageBox
            ModernMessageBox.show_warning(self, "警告", "まずPPTXファイルを選択してください。")
            return
    
        # UI状态更新
        self.translate_btn.setVisible(False)  # 翻訳ボタンを非表示
        self.stop_btn.setVisible(True)        # 停止ボタンを表示
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 创建并启动工作线程
        self.translation_worker = TranslationWorker(
            model_name=self.model_combo.currentText(),
            input_file=self.file_path_label.text(),
            target_lang=self.language_combo.currentText()
        )

        # 信号连接
        self.translation_worker.progress_updated.connect(self.update_progress)
        self.translation_worker.status_updated.connect(self.update_status)
        self.translation_worker.log_updated.connect(self.add_log)
        self.translation_worker.translation_finished.connect(self.on_translation_finished)
        self.translation_worker.translation_error.connect(self.on_translation_error)
        self.translation_worker.translation_stopped.connect(self.on_translation_stopped)
    
        # 开始翻译
        self.translation_worker.start()
    
    def update_progress(self, value: int):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def update_status(self, message: str):
        """更新状态栏"""
        self.status_bar.showMessage(message)
    
    def add_log(self, message: str):
        """添加日志"""
        self.logger.info(message)
    
    def get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def clear_log(self):
        """清除日志"""
        self.log_text.clear()
    
    def on_translation_finished(self, output_file: str):
        """翻訳完了処理"""
        self.progress_bar.setValue(100)
        self.status_bar.showMessage("翻訳完了")
        self.add_log(f"翻訳完了: {output_file}")

        # UI状態リセット
        self.reset_ui_state()

        # 現代的な完了ダイアログを表示
        from .modern_components import ModernMessageBox, ModernFileHelper

        if ModernMessageBox.show_translation_complete(self, output_file):
            # ダウンロードが選択された場合
            ModernFileHelper.download_file(self, output_file)

    def on_translation_error(self, error_message: str):
        """翻訳エラー処理"""
        self.status_bar.showMessage("翻訳エラー")
        self.add_log(f"エラー: {error_message}")

        # UI状態リセット
        self.reset_ui_state()

        # 現代的なエラーダイアログを表示
        from .modern_components import ModernMessageBox
        ModernMessageBox.show_error(self, "翻訳エラー", f"翻訳中にエラーが発生しました:\n\n{error_message}")

    def stop_translation(self):
        """翻訳を停止"""
        if self.translation_worker and self.translation_worker.isRunning():
            # 停止確認ダイアログを表示
            from .modern_components import ModernMessageBox
            if ModernMessageBox.show_question(self, "翻訳停止", "翻訳を停止しますか？\n\n進行中の作業は失われます。"):
                self.translation_worker.stop_translation()
                self.add_log("翻訳の停止が要求されました")

    def on_translation_stopped(self):
        """翻訳停止処理"""
        self.status_bar.showMessage("翻訳停止")

        # UI状態リセット
        self.reset_ui_state()

        self.add_log("翻訳が停止されました")

    def reset_ui_state(self):
        """UI状態をリセット"""
        self.translate_btn.setVisible(True)   # 翻訳ボタンを表示
        self.stop_btn.setVisible(False)       # 停止ボタンを非表示
        self.progress_bar.setVisible(False)

    def open_output_file(self, file_path: str):
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
            self.add_log(f"ファイルを開けません: {e}")

    def show_settings(self):
        """設定ダイアログを表示"""
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_settings()
            # 重新应用统一字体
            self.apply_unified_fonts()
    
    def show_about(self):
        """このアプリについて情報を表示"""
        from .about_dialog import ModernAboutDialog
        dialog = ModernAboutDialog(self)
        dialog.exec()
    
    def load_settings(self):
        """加载设置"""
        # 默认语言设置
        default_lang = self.config_manager.get_default_language()
        if default_lang:
            index = self.language_combo.findText(default_lang)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)
    
        # 窗口位置和大小恢复
        settings = QSettings()
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            UIHelper.center_window(self)
    
    def save_settings(self):
        """保存设置"""
        settings = QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 翻訳中の確認
        if self.translation_worker and self.translation_worker.isRunning():
            from .modern_components import ModernMessageBox
            if not ModernMessageBox.show_question(
                self,
                "確認",
                "翻訳が進行中です。終了してもよろしいですか？"
            ):
                event.ignore()
                return

            # 终止工作线程
            self.translation_worker.terminate()
            self.translation_worker.wait()

        # 保存设置
        self.save_settings()
        event.accept()
    



    def apply_unified_fonts(self):
        """統一フォントシステムを適用"""
        try:
            font_manager = get_font_manager()
            # 固定的中等字体大小，不再使用zoom
            font_manager.apply_unified_fonts_to_window(self, 100)
        except Exception as e:
            print(f"統一フォント適用エラー: {e}")




# 为了向后兼容，保留原来的类名
class MainWindow(ModernMainWindow):
    """向后兼容的MainWindow类"""
    pass
