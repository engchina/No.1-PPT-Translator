#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現代的UIコンポーネント - Material Design 3.0ベース
"""

from PySide6.QtWidgets import (QWidget, QPushButton, QLabel, QFrame, QVBoxLayout,
                              QHBoxLayout, QTextEdit, QComboBox, QProgressBar,
                              QGraphicsDropShadowEffect, QSizePolicy, QDialog, QMessageBox,
                              QScrollArea)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal, QTimer
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPalette, QLinearGradient
from .modern_design_system import MaterialDesign3, ModernColorSystem, ModernAnimationSystem, modern_font_system
import math


class ModernCard(QFrame):
    """現代的カードコンポーネント"""
    
    def __init__(self, elevation: str = 'level_1', corner_radius: str = 'medium', parent=None):
        super().__init__(parent)
        self.elevation = elevation
        self.corner_radius = corner_radius
        self._setup_card()
    
    def _setup_card(self):
        """カードの基本設定"""
        # 背景色を設定
        self.setStyleSheet(f"""
            ModernCard {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS[self.corner_radius]}px;
            }}
        """)
        
        # 影効果を追加
        self._add_elevation()
        
        # レイアウトマージンを設定
        self.setContentsMargins(
            MaterialDesign3.SPACING['md'],
            MaterialDesign3.SPACING['md'],
            MaterialDesign3.SPACING['md'],
            MaterialDesign3.SPACING['md']
        )
    
    def _add_elevation(self):
        """エレベーション（影）効果を追加"""
        if self.elevation != 'level_0':
            shadow = QGraphicsDropShadowEffect()
            elevation_data = MaterialDesign3.ELEVATION[self.elevation]
            
            shadow.setBlurRadius(elevation_data['blur'])
            shadow.setOffset(0, elevation_data['offset'])
            shadow.setColor(QColor(0, 0, 0, int(255 * elevation_data['opacity'])))
            
            self.setGraphicsEffect(shadow)


class ModernButton(QPushButton):
    """現代的ボタンコンポーネント"""
    
    def __init__(self, text: str = "", button_type: str = "filled", 
                 size: str = "medium", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.size = size
        self._setup_button()
        self._setup_animations()
    
    def _setup_button(self):
        """ボタンの基本設定"""
        # フォントを設定
        font = modern_font_system.get_font('label_large')
        self.setFont(font)
        
        # サイズを設定
        if self.size == "small":
            self.setMinimumHeight(32)
            self.setMinimumWidth(64)
        elif self.size == "large":
            self.setMinimumHeight(56)
            self.setMinimumWidth(120)
        else:  # medium
            self.setMinimumHeight(40)
            self.setMinimumWidth(80)
        
        # スタイルを設定
        self._apply_button_style()
        
        # カーソルを設定
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _apply_button_style(self):
        """ボタンタイプに応じたスタイルを適用"""
        if self.button_type == "filled":
            self.setStyleSheet(f"""
                ModernButton {{
                    background-color: {MaterialDesign3.COLORS['primary']};
                    color: {MaterialDesign3.COLORS['on_primary']};
                    border: none;
                    border-radius: {MaterialDesign3.CORNER_RADIUS['large']}px;
                    padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['lg']}px;
                }}
                ModernButton:hover {{
                    background-color: {MaterialDesign3.COLORS['primary_container']};
                    color: {MaterialDesign3.COLORS['on_primary_container']};
                }}
                ModernButton:pressed {{
                    background-color: {MaterialDesign3.COLORS['primary']};
                }}
                ModernButton:disabled {{
                    background-color: {MaterialDesign3.COLORS['surface_variant']};
                    color: {MaterialDesign3.COLORS['on_surface_variant']};
                }}
            """)
        elif self.button_type == "outlined":
            self.setStyleSheet(f"""
                ModernButton {{
                    background-color: transparent;
                    color: {MaterialDesign3.COLORS['primary']};
                    border: 1px solid {MaterialDesign3.COLORS['outline']};
                    border-radius: {MaterialDesign3.CORNER_RADIUS['large']}px;
                    padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['lg']}px;
                }}
                ModernButton:hover {{
                    background-color: {MaterialDesign3.COLORS['primary_container']};
                    border-color: {MaterialDesign3.COLORS['primary']};
                }}
                ModernButton:pressed {{
                    background-color: {MaterialDesign3.COLORS['primary_container']};
                }}
            """)
        else:  # text
            self.setStyleSheet(f"""
                ModernButton {{
                    background-color: transparent;
                    color: {MaterialDesign3.COLORS['primary']};
                    border: none;
                    border-radius: {MaterialDesign3.CORNER_RADIUS['large']}px;
                    padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
                }}
                ModernButton:hover {{
                    background-color: {MaterialDesign3.COLORS['primary_container']};
                }}
                ModernButton:pressed {{
                    background-color: {MaterialDesign3.COLORS['primary_container']};
                }}
            """)
    
    def _setup_animations(self):
        """アニメーション設定"""
        self.press_animation = None
        self.release_animation = None
    
    def mousePressEvent(self, event):
        """マウスプレス時のアニメーション"""
        super().mousePressEvent(event)
        
        # スケールダウンアニメーション
        self.press_animation = ModernAnimationSystem.create_property_animation(
            self, b"geometry", "short2", "accelerate"
        )
        
        current_geometry = self.geometry()
        pressed_geometry = QRect(
            current_geometry.x() + 2,
            current_geometry.y() + 2,
            current_geometry.width() - 4,
            current_geometry.height() - 4
        )
        
        self.press_animation.setStartValue(current_geometry)
        self.press_animation.setEndValue(pressed_geometry)
        self.press_animation.start()
    
    def mouseReleaseEvent(self, event):
        """マウスリリース時のアニメーション"""
        super().mouseReleaseEvent(event)
        
        # スケールアップアニメーション
        self.release_animation = ModernAnimationSystem.create_property_animation(
            self, b"geometry", "short3", "decelerate"
        )
        
        current_geometry = self.geometry()
        normal_geometry = QRect(
            current_geometry.x() - 2,
            current_geometry.y() - 2,
            current_geometry.width() + 4,
            current_geometry.height() + 4
        )
        
        self.release_animation.setStartValue(current_geometry)
        self.release_animation.setEndValue(normal_geometry)
        self.release_animation.start()


class ModernLabel(QLabel):
    """現代的ラベルコンポーネント"""
    
    def __init__(self, text: str = "", typography_style: str = "body_medium", 
                 color: str = "on_surface", parent=None):
        super().__init__(text, parent)
        self.typography_style = typography_style
        self.color = color
        self._setup_label()
    
    def _setup_label(self):
        """ラベルの基本設定"""
        # フォントを設定
        font = modern_font_system.get_font(self.typography_style)
        self.setFont(font)
        
        # カラーを設定
        color = ModernColorSystem.get_color(self.color)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.setPalette(palette)
        
        # テキストの折り返しを有効化
        self.setWordWrap(True)


class ModernTextEdit(QTextEdit):
    """現代的テキストエディットコンポーネント"""
    
    def __init__(self, placeholder: str = "", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self._setup_text_edit()
    
    def _setup_text_edit(self):
        """テキストエディットの基本設定"""
        # フォントを設定
        font = modern_font_system.get_font('body_medium')
        self.setFont(font)
        
        # スタイルを設定
        self.setStyleSheet(f"""
            ModernTextEdit {{
                background-color: {MaterialDesign3.COLORS['surface_container_low']};
                color: {MaterialDesign3.COLORS['on_surface']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                padding: {MaterialDesign3.SPACING['sm']}px;
            }}
            ModernTextEdit:focus {{
                border: 2px solid {MaterialDesign3.COLORS['primary']};
            }}
        """)


class ModernComboBox(QComboBox):
    """現代的コンボボックスコンポーネント - HTML5準拠の優れたユーザー体験を提供"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_combo_box()
        self._connect_signals()
        self._setup_animations()

    def _setup_combo_box(self):
        """コンボボックスの基本設定"""
        # フォントを設定
        font = modern_font_system.get_font('body_medium')
        self.setFont(font)

        # スタイルを設定 - HTML5のselect要素に準拠
        self.setStyleSheet(f"""
            ModernComboBox {{
                background-color: {MaterialDesign3.COLORS['surface_container_low']};
                color: {MaterialDesign3.COLORS['on_surface']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                padding: {MaterialDesign3.SPACING['sm']}px {MaterialDesign3.SPACING['md']}px;
                min-height: 40px;
                font-size: 14px;
                font-weight: 400;
            }}
            ModernComboBox:hover {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
                border-color: {MaterialDesign3.COLORS['outline']};
            }}
            ModernComboBox:focus {{
                border: 2px solid {MaterialDesign3.COLORS['primary']};
                background-color: {MaterialDesign3.COLORS['surface_container_low']};
                outline: none;
            }}
            ModernComboBox:pressed {{
                background-color: {MaterialDesign3.COLORS['surface_container_high']};
            }}
            ModernComboBox::drop-down {{
                border: none;
                width: 32px;
                background-color: transparent;
            }}
            ModernComboBox::drop-down:hover {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
            }}
            ModernComboBox::down-arrow {{
                image: none;
                border: none;
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {MaterialDesign3.COLORS['on_surface_variant']};
                margin-right: 8px;
            }}
            ModernComboBox::down-arrow:disabled {{
                border-top-color: {MaterialDesign3.COLORS['on_surface_variant']};
                opacity: 0.38;
            }}
            ModernComboBox QAbstractItemView {{
                background-color: {MaterialDesign3.COLORS['surface_container_high']};
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                margin-top: 4px;
                selection-background-color: {MaterialDesign3.COLORS['primary_container']};
                selection-color: {MaterialDesign3.COLORS['on_primary_container']};
                padding: 4px;
            }}
            ModernComboBox QAbstractItemView::item {{
                padding: 8px 12px;
                min-height: 32px;
                border-radius: {MaterialDesign3.CORNER_RADIUS['extra_small']}px;
            }}
            ModernComboBox QAbstractItemView::item:selected {{
                background-color: {MaterialDesign3.COLORS['primary_container']};
                color: {MaterialDesign3.COLORS['on_primary_container']};
            }}
            ModernComboBox QAbstractItemView::item:hover {{
                background-color: {MaterialDesign3.COLORS['surface_container']};
            }}
        """)

    def _connect_signals(self):
        """シグナルを接続 - HTML5のselect要素の動作に準拠"""
        # ユーザーの選択時のみに反応（マウスクリック）
        self.activated.connect(self._on_item_activated)
        # キーボードでの選択にも対応
        self.currentIndexChanged.connect(self._on_selection_changed)
        # ポップアップが閉じられた時の処理
        self.view().pressed.connect(self._on_view_pressed)

    def _setup_animations(self):
        """アニメーション効果の設定"""
        self._hover_animation = None
        self._focus_animation = None

    def _on_item_activated(self, index):
        """アイテムがアクティブ化されたときの処理 - HTML5標準準拠"""
        if index >= 0:
            # ポップアップを即座に閉じる
            self.hidePopup()
            
            # 完全にフォーカスを失う
            self.clearFocus()
            
            # フォーカスを次のウィジェットに強制的に移動
            if self.window():
                self.window().setFocus()
                # 次のタブオーダーのウィジェットにフォーカスを移動
                self.window().focusNextChild()
            
            # 選択完了を通知
            self._emit_selection_complete()

    def _on_selection_changed(self, index):
        """選択が変更されたときの処理"""
        if index >= 0:
            # 即座にポップアップを閉じてフォーカスを外す
            self.hidePopup()
            self.clearFocus()
            if self.window():
                self.window().focusNextChild()

    def _on_view_pressed(self, index):
        """リストビューでアイテムがクリックされた時の処理"""
        # マウスクリックで選択された場合
        if index.isValid():
            self.setCurrentIndex(index.row())
            self.hidePopup()
            self.clearFocus()
            if self.window():
                self.window().focusNextChild()

    def _emit_selection_complete(self):
        """選択完了イベントを発行"""
        # 選択完了シグナルを発行
        self.setProperty("selectionComplete", True)

    def keyPressEvent(self, event):
        """キーボード操作 - HTML5 selectと同じ動作"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            # Enterキーで選択確定と同時に閉じる
            super().keyPressEvent(event)
            self.hidePopup()
            self.clearFocus()
            if self.window():
                self.window().focusNextChild()
        elif event.key() == Qt.Key.Key_Escape:
            # Escapeキーでキャンセルして閉じる
            self.hidePopup()
            self.clearFocus()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """マウスクリック処理の改善"""
        super().mousePressEvent(event)
        # マウスクリック後の処理はactivatedシグナルで処理される

    def showPopup(self):
        """ポップアップ表示"""
        super().showPopup()

    def hidePopup(self):
        """ポップアップ非表示 - 完全にフォーカスを失う"""
        super().hidePopup()
        # ポップアップが閉じられたら必ずフォーカスを外す
        self.clearFocus()
        
        # 親ウィジェットにフォーカスを戻す
        if self.parent():
            parent_widget = self.parent()
            while parent_widget and not parent_widget.isEnabled():
                parent_widget = parent_widget.parent()
            if parent_widget:
                parent_widget.setFocus()


class ModernProgressBar(QProgressBar):
    """現代的プログレスバーコンポーネント"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_progress_bar()
    
    def _setup_progress_bar(self):
        """プログレスバーの基本設定"""
        self.setStyleSheet(f"""
            ModernProgressBar {{
                background-color: {MaterialDesign3.COLORS['surface_variant']};
                border: none;
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                height: 24px;
                font-size: 14px;
                font-weight: 500;
                color: {MaterialDesign3.COLORS['on_primary']};
                text-align: center;
            }}
            ModernProgressBar::chunk {{
                background-color: {MaterialDesign3.COLORS['primary']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
            }}
        """)

        # 高さを設定 - より大きく、見やすく
        self.setMaximumHeight(24)
        self.setMinimumHeight(24)


class ModernContainer(QWidget):
    """現代的コンテナコンポーネント"""
    
    def __init__(self, layout_type: str = "vertical", spacing: str = "md", parent=None):
        super().__init__(parent)
        self.layout_type = layout_type
        self.spacing = spacing
        self._setup_container()
    
    def _setup_container(self):
        """コンテナの基本設定"""
        # レイアウトを設定
        if self.layout_type == "horizontal":
            layout = QHBoxLayout(self)
        else:
            layout = QVBoxLayout(self)
        
        # スペーシングを設定
        layout.setSpacing(MaterialDesign3.SPACING[self.spacing])
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(layout)
    
    def add_widget(self, widget: QWidget, stretch: int = 0):
        """ウィジェットを追加"""
        self.layout().addWidget(widget, stretch)
    
    def add_stretch(self, stretch: int = 1):
        """ストレッチを追加"""
        self.layout().addStretch(stretch)


class ModernMessageBox:
    """現代的メッセージボックス - Material Design 3.0ベース"""

    @staticmethod
    def show_translation_complete(parent, output_file: str) -> bool:
        """翻訳完了ダイアログを表示（ダウンロード機能付き）"""
        import os

        dialog = QDialog(parent)
        dialog.setWindowTitle("翻訳完了")
        dialog.setModal(True)

        # レスポンシブサイズ設定
        ModernMessageBox._setup_responsive_size(dialog)

        # 現代的スタイリング
        ModernMessageBox._setup_modern_styling(dialog)

        # レイアウト作成
        layout = QVBoxLayout(dialog)
        layout.setSpacing(MaterialDesign3.SPACING['lg'])
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アイコンとタイトル
        title_container = ModernContainer("horizontal", "md")

        # 成功アイコン（✓マーク）
        icon_label = ModernLabel("✓", "headline_medium", "primary")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['primary_container']};
                color: {MaterialDesign3.COLORS['on_primary_container']};
                border-radius: 24px;
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
            }}
        """)

        title_label = ModernLabel("翻訳が完了しました！", "headline_small", "on_surface")

        title_container.add_widget(icon_label)
        title_container.add_widget(title_label, 1)
        layout.addWidget(title_container)

        # メッセージ
        filename = os.path.basename(output_file)

        # ファイルの存在確認
        file_exists = os.path.exists(output_file)
        if file_exists:
            message_text = f"ファイルが正常に翻訳されました。\n\n出力ファイル: {filename}"
            download_btn_text = "ダウンロード"
        else:
            message_text = f"翻訳は完了しましたが、出力ファイルが見つかりません。\n\n予定されたファイル: {filename}\n\n出力フォルダを確認してください。"
            download_btn_text = "フォルダを開く"

        message_label = ModernLabel(
            message_text,
            "body_large",
            "on_surface_variant"
        )
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        message_label.setWordWrap(True)  # 自動換行を有効化
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # テキスト選択可能
        message_label.setMinimumHeight(80)  # 最小高さを設定
        message_label.setMaximumHeight(300)  # 最大高さを制限
        layout.addWidget(message_label)

        # ボタンエリア
        button_container = ModernContainer("horizontal", "md")
        button_container.add_stretch()

        # キャンセルボタン
        cancel_btn = ModernButton("閉じる", "outlined", "medium")
        cancel_btn.clicked.connect(dialog.reject)

        # ダウンロード/フォルダを開くボタン
        download_btn = ModernButton(download_btn_text, "filled", "medium")
        download_btn.setDefault(True)

        # ボタンの動作を設定
        if file_exists:
            # ファイルが存在する場合：ダウンロード機能
            download_btn.clicked.connect(dialog.accept)
        else:
            # ファイルが存在しない場合：フォルダを開く機能
            def open_output_folder():
                try:
                    output_dir = os.path.dirname(output_file)
                    if not output_dir or not os.path.exists(output_dir):
                        # デフォルトの出力ディレクトリを使用
                        output_dir = os.path.join(os.getcwd(), "output")
                        if not os.path.exists(output_dir):
                            output_dir = os.getcwd()

                    success = ModernFileHelper.open_folder(output_dir)
                    if success:
                        dialog.accept()
                    else:
                        # フォルダを開けない場合、パスを表示
                        ModernMessageBox.show_error(
                            dialog,
                            "フォルダを開けません",
                            f"出力フォルダを自動で開くことができませんでした。\n\n"
                            f"手動で以下のパスを確認してください:\n{output_dir}\n\n"
                            f"このパスをファイルマネージャーにコピーして開いてください。"
                        )
                except Exception as e:
                    ModernMessageBox.show_error(
                        dialog,
                        "フォルダを開けません",
                        f"出力フォルダを開くことができませんでした:\n\n{str(e)}\n\n"
                        f"手動でファイルを確認してください。"
                    )

            download_btn.clicked.connect(open_output_folder)

        button_container.add_widget(cancel_btn)
        button_container.add_widget(download_btn)
        layout.addWidget(button_container)

        # ダイアログを表示
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted and file_exists

    @staticmethod
    def show_error(parent, title: str, message: str):
        """エラーダイアログを表示"""
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setModal(True)

        # レスポンシブサイズ設定
        ModernMessageBox._setup_responsive_size(dialog)

        # 現代的スタイリング
        ModernMessageBox._setup_modern_styling(dialog)

        # レイアウト作成
        layout = QVBoxLayout(dialog)
        layout.setSpacing(MaterialDesign3.SPACING['lg'])
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アイコンとタイトル
        title_container = ModernContainer("horizontal", "md")

        # エラーアイコン（⚠マーク）
        icon_label = ModernLabel("⚠", "headline_medium", "error")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['error_container']};
                color: {MaterialDesign3.COLORS['on_error_container']};
                border-radius: 24px;
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
            }}
        """)

        title_label = ModernLabel(title, "headline_small", "on_surface")

        title_container.add_widget(icon_label)
        title_container.add_widget(title_label, 1)
        layout.addWidget(title_container)

        # メッセージ（改良版 - 自動換行とスクロール対応）
        message_label = ModernLabel(message, "body_large", "on_surface_variant")
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        message_label.setWordWrap(True)  # 自動換行を有効化
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # テキスト選択可能
        message_label.setMinimumHeight(60)  # 最小高さを設定
        message_label.setMaximumHeight(300)  # 最大高さを制限
        layout.addWidget(message_label)

        # ボタンエリア
        button_container = ModernContainer("horizontal", "md")
        button_container.add_stretch()

        # OKボタン
        ok_btn = ModernButton("OK", "filled", "medium")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(dialog.accept)

        button_container.add_widget(ok_btn)
        layout.addWidget(button_container)

        # ダイアログを表示
        dialog.exec()

    @staticmethod
    def show_warning(parent, title: str, message: str):
        """警告ダイアログを表示"""
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setModal(True)

        # レスポンシブサイズ設定
        ModernMessageBox._setup_responsive_size(dialog)

        # 現代的スタイリング
        ModernMessageBox._setup_modern_styling(dialog)

        # レイアウト作成
        layout = QVBoxLayout(dialog)
        layout.setSpacing(MaterialDesign3.SPACING['lg'])
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アイコンとタイトル
        title_container = ModernContainer("horizontal", "md")

        # 警告アイコン（⚠マーク）
        icon_label = ModernLabel("⚠", "headline_medium", "tertiary")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['tertiary_container']};
                color: {MaterialDesign3.COLORS['on_tertiary_container']};
                border-radius: 24px;
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
            }}
        """)

        title_label = ModernLabel(title, "headline_small", "on_surface")

        title_container.add_widget(icon_label)
        title_container.add_widget(title_label, 1)
        layout.addWidget(title_container)

        # メッセージ（改良版 - 自動換行とスクロール対応）
        message_label = ModernLabel(message, "body_large", "on_surface_variant")
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        message_label.setWordWrap(True)  # 自動換行を有効化
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # テキスト選択可能
        message_label.setMinimumHeight(60)  # 最小高さを設定
        message_label.setMaximumHeight(300)  # 最大高さを制限
        layout.addWidget(message_label)

        # ボタンエリア
        button_container = ModernContainer("horizontal", "md")
        button_container.add_stretch()

        # OKボタン
        ok_btn = ModernButton("OK", "filled", "medium")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(dialog.accept)

        button_container.add_widget(ok_btn)
        layout.addWidget(button_container)

        # ダイアログを表示
        dialog.exec()

    @staticmethod
    def show_question(parent, title: str, message: str) -> bool:
        """質問ダイアログを表示"""
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setModal(True)

        # レスポンシブサイズ設定
        ModernMessageBox._setup_responsive_size(dialog)

        # 現代的スタイリング
        ModernMessageBox._setup_modern_styling(dialog)

        # レイアウト作成
        layout = QVBoxLayout(dialog)
        layout.setSpacing(MaterialDesign3.SPACING['lg'])
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アイコンとタイトル
        title_container = ModernContainer("horizontal", "md")

        # 質問アイコン（?マーク）
        icon_label = ModernLabel("?", "headline_medium", "secondary")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['secondary_container']};
                color: {MaterialDesign3.COLORS['on_secondary_container']};
                border-radius: 24px;
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
            }}
        """)

        title_label = ModernLabel(title, "headline_small", "on_surface")

        title_container.add_widget(icon_label)
        title_container.add_widget(title_label, 1)
        layout.addWidget(title_container)

        # メッセージ（改良版 - 自動換行とスクロール対応）
        message_label = ModernLabel(message, "body_large", "on_surface_variant")
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        message_label.setWordWrap(True)  # 自動換行を有効化
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # テキスト選択可能
        message_label.setMinimumHeight(60)  # 最小高さを設定
        message_label.setMaximumHeight(300)  # 最大高さを制限
        layout.addWidget(message_label)

        # ボタンエリア
        button_container = ModernContainer("horizontal", "md")
        button_container.add_stretch()

        # いいえボタン
        no_btn = ModernButton("いいえ", "outlined", "medium")
        no_btn.clicked.connect(dialog.reject)

        # はいボタン
        yes_btn = ModernButton("はい", "filled", "medium")
        yes_btn.setDefault(True)
        yes_btn.clicked.connect(dialog.accept)

        button_container.add_widget(no_btn)
        button_container.add_widget(yes_btn)
        layout.addWidget(button_container)

        # ダイアログを表示
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted

    @staticmethod
    def _setup_responsive_size(dialog):
        """レスポンシブサイズ設定 - 拡大版"""
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            # 画面サイズに基づくレスポンシブ設定（大幅に拡大）
            if screen_size.width() >= 1920:
                dialog.resize(800, 500)  # 4K/高解像度用
            elif screen_size.width() >= 1366:
                dialog.resize(700, 450)  # フルHD用
            else:
                dialog.resize(600, 400)  # 小画面用
        else:
            dialog.resize(600, 400)  # デフォルト

    @staticmethod
    def _setup_modern_styling(dialog):
        """現代的スタイリング設定"""
        # Material Design 3.0フォントシステムを適用
        modern_font_system.apply_global_font(100)

        # ダイアログ全体のスタイル
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {MaterialDesign3.COLORS['background']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['large']}px;
            }}
        """)

    @staticmethod
    def _create_scrollable_message(message: str, max_height: int = 300) -> QScrollArea:
        """スクロール可能なメッセージエリアを作成"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setMaximumHeight(max_height)
        scroll_area.setMinimumHeight(80)

        # メッセージラベルを作成
        message_widget = QWidget()
        message_layout = QVBoxLayout(message_widget)
        message_layout.setContentsMargins(10, 10, 10, 10)

        message_label = ModernLabel(message, "body_large", "on_surface_variant")
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        message_layout.addWidget(message_label)
        message_layout.addStretch()

        scroll_area.setWidget(message_widget)

        # スクロールエリアのスタイル
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {MaterialDesign3.COLORS['outline_variant']};
                border-radius: {MaterialDesign3.CORNER_RADIUS['small']}px;
                background-color: {MaterialDesign3.COLORS['surface_container']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {MaterialDesign3.COLORS['surface_variant']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {MaterialDesign3.COLORS['outline']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {MaterialDesign3.COLORS['on_surface_variant']};
            }}
        """)

        return scroll_area

    @staticmethod
    def show_error_with_long_text(parent, title: str, message: str):
        """長いテキスト用のエラーダイアログを表示（スクロール対応）"""
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setModal(True)

        # 大きめのサイズ設定
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_size = screen.availableSize()
            # より大きなサイズを設定
            if screen_size.width() >= 1920:
                dialog.resize(900, 600)  # 4K/高解像度用
            elif screen_size.width() >= 1366:
                dialog.resize(800, 550)  # フルHD用
            else:
                dialog.resize(700, 500)  # 小画面用
        else:
            dialog.resize(700, 500)

        # 現代的スタイリング
        ModernMessageBox._setup_modern_styling(dialog)

        # レイアウト作成
        layout = QVBoxLayout(dialog)
        layout.setSpacing(MaterialDesign3.SPACING['lg'])
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アイコンとタイトル
        title_container = ModernContainer("horizontal", "md")

        # エラーアイコン（⚠マーク）
        icon_label = ModernLabel("⚠", "headline_medium", "error")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['error_container']};
                color: {MaterialDesign3.COLORS['on_error_container']};
                border-radius: 24px;
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
            }}
        """)

        title_label = ModernLabel(title, "headline_small", "on_surface")

        title_container.add_widget(icon_label)
        title_container.add_widget(title_label, 1)
        layout.addWidget(title_container)

        # スクロール可能なメッセージエリア
        scroll_area = ModernMessageBox._create_scrollable_message(message, 400)
        layout.addWidget(scroll_area)

        # ボタンエリア
        button_container = ModernContainer("horizontal", "md")
        button_container.add_stretch()

        # OKボタン
        ok_btn = ModernButton("OK", "filled", "medium")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(dialog.accept)

        button_container.add_widget(ok_btn)
        layout.addWidget(button_container)

        # ダイアログを表示
        dialog.exec()


class ModernFileHelper:
    """現代的ファイル操作ヘルパー"""

    @staticmethod
    def download_file(parent, source_file: str) -> bool:
        """ファイルダウンロード機能（名前を付けて保存）"""
        try:
            from PySide6.QtWidgets import QFileDialog
            import os
            import shutil

            # ソースファイルの存在確認
            if not os.path.exists(source_file):
                ModernMessageBox.show_error(
                    parent,
                    "ダウンロードエラー",
                    f"指定されたファイルが見つかりません:\n\n{source_file}\n\nファイルが移動または削除された可能性があります。"
                )
                return False

            # 元のファイル名を取得
            original_filename = os.path.basename(source_file)

            # 保存先を選択
            save_path, _ = QFileDialog.getSaveFileName(
                parent,
                "ファイルを保存",
                original_filename,
                "PowerPoint Files (*.pptx);;All Files (*)"
            )

            if save_path:
                # ファイルをコピー
                shutil.copy2(source_file, save_path)

                # 成功メッセージを表示
                ModernMessageBox.show_success(
                    parent,
                    "ダウンロード完了",
                    f"ファイルが正常に保存されました。\n\n保存先: {save_path}"
                )
                return True

            return False

        except FileNotFoundError:
            ModernMessageBox.show_error(
                parent,
                "ダウンロードエラー",
                f"ファイルが見つかりません:\n\n{source_file}"
            )
            return False

    @staticmethod
    def open_folder(folder_path: str) -> bool:
        """フォルダを開く（クロスプラットフォーム対応）"""
        try:
            import subprocess
            import platform
            import os
            import shutil

            if not os.path.exists(folder_path):
                return False

            system = platform.system()

            if system == "Windows":
                # Windows: explorer.exeを使用
                os.startfile(folder_path)
                return True

            elif system == "Darwin":  # macOS
                # macOS: openコマンドを使用
                subprocess.run(["open", folder_path], check=True)
                return True

            else:  # Linux/Unix
                # Linux: 複数の方法を試行

                # 1. xdg-openを試行（最も標準的）
                if shutil.which("xdg-open"):
                    try:
                        result = subprocess.run(
                            ["xdg-open", folder_path],
                            capture_output=True,
                            timeout=5,
                            check=False
                        )
                        if result.returncode == 0:
                            return True
                    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass

                # 2. nautilusを試行（GNOME）
                if shutil.which("nautilus"):
                    try:
                        subprocess.run(
                            ["nautilus", folder_path],
                            capture_output=True,
                            timeout=5,
                            check=True
                        )
                        return True
                    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass

                # 3. dolphinを試行（KDE）
                if shutil.which("dolphin"):
                    try:
                        subprocess.run(
                            ["dolphin", folder_path],
                            capture_output=True,
                            timeout=5,
                            check=True
                        )
                        return True
                    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass

                # 4. thunarを試行（XFCE）
                if shutil.which("thunar"):
                    try:
                        subprocess.run(
                            ["thunar", folder_path],
                            capture_output=True,
                            timeout=5,
                            check=True
                        )
                        return True
                    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass

                # 5. WSL環境の場合、Windows Explorerを試行
                if "microsoft" in platform.uname().release.lower() or "wsl" in platform.uname().release.lower():
                    try:
                        # WSLパスをWindowsパスに変換
                        windows_path = folder_path.replace("/mnt/", "").replace("/", "\\")
                        if windows_path.startswith("c\\"):
                            windows_path = "C:\\" + windows_path[2:]
                        elif windows_path.startswith("d\\"):
                            windows_path = "D:\\" + windows_path[2:]
                        elif windows_path.startswith("e\\"):
                            windows_path = "E:\\" + windows_path[2:]

                        subprocess.run(
                            ["explorer.exe", windows_path],
                            capture_output=True,
                            timeout=5,
                            check=True
                        )
                        return True
                    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass

                # すべて失敗した場合
                return False

        except Exception:
            return False

    @staticmethod
    def show_success(parent, title: str, message: str):
        """成功ダイアログを表示"""
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setModal(True)

        # レスポンシブサイズ設定
        ModernMessageBox._setup_responsive_size(dialog)

        # 現代的スタイリング
        ModernMessageBox._setup_modern_styling(dialog)

        # レイアウト作成
        layout = QVBoxLayout(dialog)
        layout.setSpacing(MaterialDesign3.SPACING['lg'])
        layout.setContentsMargins(
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl'],
            MaterialDesign3.SPACING['xl']
        )

        # アイコンとタイトル
        title_container = ModernContainer("horizontal", "md")

        # 成功アイコン（✓マーク）
        icon_label = ModernLabel("✓", "headline_medium", "primary")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"""
            ModernLabel {{
                background-color: {MaterialDesign3.COLORS['primary_container']};
                color: {MaterialDesign3.COLORS['on_primary_container']};
                border-radius: 24px;
                min-width: 48px;
                max-width: 48px;
                min-height: 48px;
                max-height: 48px;
            }}
        """)

        title_label = ModernLabel(title, "headline_small", "on_surface")

        title_container.add_widget(icon_label)
        title_container.add_widget(title_label, 1)
        layout.addWidget(title_container)

        # メッセージ（改良版 - 自動換行とスクロール対応）
        message_label = ModernLabel(message, "body_large", "on_surface_variant")
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        message_label.setWordWrap(True)  # 自動換行を有効化
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # テキスト選択可能
        message_label.setMinimumHeight(60)  # 最小高さを設定
        message_label.setMaximumHeight(300)  # 最大高さを制限
        layout.addWidget(message_label)

        # ボタンエリア
        button_container = ModernContainer("horizontal", "md")
        button_container.add_stretch()

        # OKボタン
        ok_btn = ModernButton("OK", "filled", "medium")
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(dialog.accept)

        button_container.add_widget(ok_btn)
        layout.addWidget(button_container)

        # ダイアログを表示
        dialog.exec()


# ModernMessageBoxにshow_successメソッドを追加
ModernMessageBox.show_success = ModernFileHelper.show_success
