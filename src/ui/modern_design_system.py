#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
現代的デザインシステム - Material Design 3.0に基づく
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient, QPainter, QPen, QBrush
from typing import Dict, Optional, Union
import math


class MaterialDesign3:
    """Material Design 3.0 デザインシステム"""
    
    # Material Design 3.0 カラーパレット
    COLORS = {
        # Primary Colors
        'primary': '#6750A4',
        'on_primary': '#FFFFFF',
        'primary_container': '#EADDFF',
        'on_primary_container': '#21005D',
        
        # Secondary Colors
        'secondary': '#625B71',
        'on_secondary': '#FFFFFF',
        'secondary_container': '#E8DEF8',
        'on_secondary_container': '#1D192B',
        
        # Tertiary Colors
        'tertiary': '#7D5260',
        'on_tertiary': '#FFFFFF',
        'tertiary_container': '#FFD8E4',
        'on_tertiary_container': '#31111D',
        
        # Error Colors
        'error': '#BA1A1A',
        'on_error': '#FFFFFF',
        'error_container': '#FFDAD6',
        'on_error_container': '#410002',
        
        # Surface Colors
        'surface': '#FEF7FF',
        'on_surface': '#1C1B1F',
        'surface_variant': '#E7E0EC',
        'on_surface_variant': '#49454F',
        'surface_container_lowest': '#FFFFFF',
        'surface_container_low': '#F7F2FA',
        'surface_container': '#F3EDF7',
        'surface_container_high': '#ECE6F0',
        'surface_container_highest': '#E6E0E9',
        
        # Outline Colors
        'outline': '#79747E',
        'outline_variant': '#CAC4D0',
        
        # Background
        'background': '#FEF7FF',
        'on_background': '#1C1B1F',
        
        # Inverse Colors
        'inverse_surface': '#313033',
        'inverse_on_surface': '#F4EFF4',
        'inverse_primary': '#D0BCFF',
        
        # Shadow
        'shadow': '#000000',
        'scrim': '#000000',
    }
    
    # タイポグラフィスケール
    TYPOGRAPHY = {
        'display_large': {'size': 57, 'weight': 400, 'line_height': 64},
        'display_medium': {'size': 45, 'weight': 400, 'line_height': 52},
        'display_small': {'size': 36, 'weight': 400, 'line_height': 44},
        'headline_large': {'size': 32, 'weight': 400, 'line_height': 40},
        'headline_medium': {'size': 28, 'weight': 400, 'line_height': 36},
        'headline_small': {'size': 24, 'weight': 400, 'line_height': 32},
        'title_large': {'size': 22, 'weight': 400, 'line_height': 28},
        'title_medium': {'size': 16, 'weight': 500, 'line_height': 24},
        'title_small': {'size': 14, 'weight': 500, 'line_height': 20},
        'label_large': {'size': 14, 'weight': 500, 'line_height': 20},
        'label_medium': {'size': 12, 'weight': 500, 'line_height': 16},
        'label_small': {'size': 11, 'weight': 500, 'line_height': 16},
        'body_large': {'size': 16, 'weight': 400, 'line_height': 24},
        'body_medium': {'size': 14, 'weight': 400, 'line_height': 20},
        'body_small': {'size': 12, 'weight': 400, 'line_height': 16},
    }
    
    # エレベーション（影）レベル
    ELEVATION = {
        'level_0': {'blur': 0, 'offset': 0, 'opacity': 0},
        'level_1': {'blur': 3, 'offset': 1, 'opacity': 0.15},
        'level_2': {'blur': 6, 'offset': 2, 'opacity': 0.15},
        'level_3': {'blur': 12, 'offset': 4, 'opacity': 0.15},
        'level_4': {'blur': 16, 'offset': 6, 'opacity': 0.15},
        'level_5': {'blur': 20, 'offset': 8, 'opacity': 0.15},
    }
    
    # 角丸半径
    CORNER_RADIUS = {
        'none': 0,
        'extra_small': 4,
        'small': 8,
        'medium': 12,
        'large': 16,
        'extra_large': 28,
        'full': 9999,
    }
    
    # スペーシング
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
        'xxxl': 64,
    }


class ModernFontSystem:
    """現代的フォントシステム"""
    
    def __init__(self):
        self.font_families = {
            'primary': 'Inter',
            'japanese': 'Noto Sans JP',
            'chinese': 'Noto Sans SC',
            'monospace': 'JetBrains Mono',
        }
        self.base_zoom = 100
    
    def get_font(self, style: str, zoom_level: int = 100) -> QFont:
        """指定されたスタイルでフォントを取得（固定サイズ）"""
        if style not in MaterialDesign3.TYPOGRAPHY:
            style = 'body_medium'

        typography = MaterialDesign3.TYPOGRAPHY[style]
        # 固定サイズを使用、ズームは適用しない
        size = typography['size']
        weight = typography['weight']
        
        # フォントファミリーを決定
        font_family = self._get_best_font_family()
        
        font = QFont(font_family, size)
        
        # ウェイトを設定
        if weight >= 700:
            font.setWeight(QFont.Weight.Bold)
        elif weight >= 600:
            font.setWeight(QFont.Weight.DemiBold)
        elif weight >= 500:
            font.setWeight(QFont.Weight.Medium)
        else:
            font.setWeight(QFont.Weight.Normal)
        
        # アンチエイリアシングを有効化
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        
        return font
    
    def _get_best_font_family(self) -> str:
        """最適なフォントファミリーを取得"""
        try:
            # システムで利用可能なフォントを確認
            from PySide6.QtGui import QFontDatabase
            font_db = QFontDatabase()
            available_fonts = font_db.families()

            # 優先順位でフォントを選択
            for font_family in [self.font_families['japanese'],
                              self.font_families['primary'],
                              'system-ui', 'sans-serif']:
                if font_family in available_fonts:
                    return font_family
        except Exception as e:
            print(f"フォント検索エラー: {e}")

        # フォールバック
        return 'sans-serif'
    
    def apply_global_font(self, zoom_level: int = 100):
        """アプリケーション全体にフォントを適用（固定サイズ）"""
        app = QApplication.instance()
        if app:
            # 固定サイズのフォントを使用
            base_font = self.get_font('body_medium', 100)
            app.setFont(base_font)


class ModernColorSystem:
    """現代的カラーシステム"""
    
    @staticmethod
    def get_color(color_name: str, alpha: float = 1.0) -> QColor:
        """カラー名からQColorを取得"""
        if color_name not in MaterialDesign3.COLORS:
            color_name = 'on_surface'
        
        hex_color = MaterialDesign3.COLORS[color_name]
        color = QColor(hex_color)
        color.setAlphaF(alpha)
        return color
    
    @staticmethod
    def create_gradient(start_color: str, end_color: str, 
                       direction: str = 'vertical') -> QLinearGradient:
        """グラデーションを作成"""
        gradient = QLinearGradient()
        
        if direction == 'vertical':
            gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
            gradient.setStart(0, 0)
            gradient.setFinalStop(0, 1)
        elif direction == 'horizontal':
            gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
            gradient.setStart(0, 0)
            gradient.setFinalStop(1, 0)
        
        gradient.setColorAt(0, ModernColorSystem.get_color(start_color))
        gradient.setColorAt(1, ModernColorSystem.get_color(end_color))
        
        return gradient


class ModernAnimationSystem:
    """現代的アニメーションシステム"""
    
    EASING_CURVES = {
        'standard': QEasingCurve.Type.OutCubic,
        'decelerate': QEasingCurve.Type.OutQuart,
        'accelerate': QEasingCurve.Type.InQuart,
        'emphasized': QEasingCurve.Type.OutBack,
    }
    
    DURATIONS = {
        'short1': 50,
        'short2': 100,
        'short3': 150,
        'short4': 200,
        'medium1': 250,
        'medium2': 300,
        'medium3': 350,
        'medium4': 400,
        'long1': 450,
        'long2': 500,
        'long3': 550,
        'long4': 600,
    }
    
    @staticmethod
    def create_property_animation(target: QWidget, property_name: bytes,
                                duration: str = 'medium2',
                                easing: str = 'standard') -> QPropertyAnimation:
        """プロパティアニメーションを作成"""
        animation = QPropertyAnimation(target, property_name)
        animation.setDuration(ModernAnimationSystem.DURATIONS[duration])
        animation.setEasingCurve(ModernAnimationSystem.EASING_CURVES[easing])
        return animation
    
    @staticmethod
    def animate_fade_in(widget: QWidget, duration: str = 'medium2'):
        """フェードインアニメーション"""
        animation = ModernAnimationSystem.create_property_animation(
            widget, b"windowOpacity", duration, 'decelerate'
        )
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.start()
        return animation
    
    @staticmethod
    def animate_slide_in(widget: QWidget, direction: str = 'up', 
                        duration: str = 'medium3'):
        """スライドインアニメーション"""
        animation = ModernAnimationSystem.create_property_animation(
            widget, b"geometry", duration, 'emphasized'
        )
        
        current_geometry = widget.geometry()
        
        if direction == 'up':
            start_geometry = QRect(
                current_geometry.x(),
                current_geometry.y() + 50,
                current_geometry.width(),
                current_geometry.height()
            )
        elif direction == 'down':
            start_geometry = QRect(
                current_geometry.x(),
                current_geometry.y() - 50,
                current_geometry.width(),
                current_geometry.height()
            )
        elif direction == 'left':
            start_geometry = QRect(
                current_geometry.x() + 50,
                current_geometry.y(),
                current_geometry.width(),
                current_geometry.height()
            )
        else:  # right
            start_geometry = QRect(
                current_geometry.x() - 50,
                current_geometry.y(),
                current_geometry.width(),
                current_geometry.height()
            )
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(current_geometry)
        animation.start()
        return animation


# グローバルインスタンス
modern_font_system = ModernFontSystem()
