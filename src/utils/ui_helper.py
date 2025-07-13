#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI相关的辅助功能 - 现代化响应式设计版
"""

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QTextEdit, QLabel, QPushButton, QComboBox, QLineEdit, QDialog
from PySide6.QtCore import QSettings, Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter
from .font_manager import get_font_manager


class ResponsiveUIHelper:
    """响应式UI辅助类"""
    
    @staticmethod
    def get_responsive_sizes(screen_size):
        """根据屏幕大小获取响应式尺寸"""
        width, height = screen_size.width(), screen_size.height()
        
        if width >= 1920 and height >= 1080:
            # 大屏幕 (1080p+)
            return {
                'window_width': 1440,
                'window_height': 900,
                'font_base_size': 16,
                'card_padding': 25,
                'button_padding': '16px 32px',
                'border_radius': 12
            }
        elif width >= 1366 and height >= 768:
            # 中等屏幕 (HD+)
            return {
                'window_width': 1200,
                'window_height': 800,
                'font_base_size': 15,
                'card_padding': 20,
                'button_padding': '14px 28px',
                'border_radius': 10
            }
        else:
            # 小屏幕
            return {
                'window_width': 1000,
                'window_height': 700,
                'font_base_size': 14,
                'card_padding': 15,
                'button_padding': '12px 24px',
                'border_radius': 8
            }
    
    @staticmethod

    

    
    @staticmethod
    def center_window_responsive(widget: QWidget):
        """响应式居中窗口"""
        app = QApplication.instance()
        if not app:
            return
            
        screen = app.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            widget_geometry = widget.frameGeometry()
            
            # 计算居中位置，考虑缩放
            center_point = screen_geometry.center()
            widget_geometry.moveCenter(center_point)
            
            # 确保窗口完全在屏幕内
            if widget_geometry.right() > screen_geometry.right():
                widget_geometry.moveRight(screen_geometry.right() - 20)
            if widget_geometry.bottom() > screen_geometry.bottom():
                widget_geometry.moveBottom(screen_geometry.bottom() - 20)
            if widget_geometry.left() < screen_geometry.left():
                widget_geometry.moveLeft(screen_geometry.left() + 20)
            if widget_geometry.top() < screen_geometry.top():
                widget_geometry.moveTop(screen_geometry.top() + 20)
                
            widget.move(widget_geometry.topLeft())
    
    @staticmethod
    def create_modern_stylesheet() -> str:
        """创建现代化样式表（固定样式）"""
        return f"""
            /* 现代化全局样式 */
            QWidget {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                font-size: 16px;
            }}

            /* 卡片样式 */
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e9ecef;
            }}

            /* 按钮样式 */
            QPushButton {{
                border-radius: 8px;
                font-weight: 500;
                outline: none;
            }}
            
            QPushButton:default {{
                background-color: #007bff;
                color: white;
                border: none;
            }}
            
            QPushButton:hover:!pressed:!disabled {{
                background-color: #0056b3;
            }}
            
            /* 输入框样式 */
            QLineEdit, QComboBox, QTextEdit {{
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 10px;
            }}

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
                border-color: #007bff;
                outline: none;
            }}

            /* 滚动条样式 */
            QScrollBar:vertical {{
                border: none;
                background: #f1f3f4;
                width: 8px;
                border-radius: 4px;
            }}

            QScrollBar::handle:vertical {{
                background: #c1c8cd;
                border-radius: 4px;
                min-height: 20px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: #a8b3bd;
            }}
        """


class UIHelper:
    """UI相关的辅助类 - 现代化版本"""
    

    

    

    
    @staticmethod
    def save_window_geometry(widget: QWidget, settings_key: str = "geometry"):
        """保存窗口位置和大小"""
        settings = QSettings()
        settings.setValue(settings_key, widget.saveGeometry())
    
    @staticmethod
    def restore_window_geometry(widget: QWidget, settings_key: str = "geometry") -> bool:
        """恢复窗口位置和大小"""
        settings = QSettings()
        geometry = settings.value(settings_key)
        if geometry:
            return widget.restoreGeometry(geometry)
        return False
    
    @staticmethod
    def center_window(widget: QWidget):
        """居中窗口"""
        ResponsiveUIHelper.center_window_responsive(widget)

    @staticmethod
    def setup_combo_auto_blur(combo_box: QComboBox):
        """コンボボックスに選択後自動フォーカス解除機能を追加"""
        from PySide6.QtCore import QTimer

        # シンプルなアプローチ：activated シグナルを使用
        def on_item_activated(index):
            # アイテムが選択されたときにフォーカスをクリア
            def clear_focus():
                combo_box.clearFocus()
                # 親ウィジェットにフォーカスを移す
                parent = combo_box.parent()
                if parent:
                    parent.setFocus()

            # 少し遅延してフォーカスをクリア（ドロップダウンが閉じるのを待つ）
            QTimer.singleShot(150, clear_focus)

        # シグナルを接続
        combo_box.activated.connect(on_item_activated)

        # 注意：currentIndexChanged は使用しない
        # プログラムによる変更でもフォーカスが失われるのを避けるため
    


