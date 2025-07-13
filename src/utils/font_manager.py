#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体管理系统 - 现代化响应式设计版
Google Fontsを使用して多言語対応
"""

from pathlib import Path
from typing import Optional, Dict, List

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication


class ModernFontManager:
    """现代化字体管理器"""
    
    # 扩展的字体家族配置
    FONT_FAMILIES = {
        'primary': 'Inter',           # 主要字体（现代化无衬线）
        'japanese': 'Noto Sans JP',   # 日本语
        'chinese': 'Noto Sans SC',    # 简体中文
        'korean': 'Noto Sans KR',     # 韩语
        'monospace': 'JetBrains Mono', # 现代化等宽字体
        'display': 'Inter',           # 标题字体
        'fallback': [
            'Inter', 'Noto Sans', 'Roboto', 'Helvetica Neue', 
            'Arial', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'
        ]
    }
    
    # 响应式字体大小映射
    RESPONSIVE_SIZES = {
        'xs': 12,
        'sm': 14,
        'base': 16,
        'lg': 18,
        'xl': 20,
        '2xl': 24,
        '3xl': 32
    }
    
    def __init__(self):
        self.font_database = QFontDatabase()
        self.loaded_fonts = set()
        # 设置固定的中等字体大小
        self.default_font_size = 18  # 中等偏大的字体
        self.system_fonts = self._detect_system_fonts()
        
    def _detect_system_fonts(self) -> List[str]:
        """检测系统可用字体"""
        return self.font_database.families()
    
    def load_google_fonts(self):
        """加载Google Fonts和系统字体"""
        try:
            # 字体目录
            font_dir = Path(__file__).parent.parent.parent / "fonts"
            loaded_count = 0

            if font_dir.exists():
                # 加载本地字体文件
                font_extensions = ['*.ttf', '*.otf', '*.woff', '*.woff2']
                for ext in font_extensions:
                    for font_file in font_dir.glob(ext):
                        font_id = self.font_database.addApplicationFont(str(font_file))
                        if font_id != -1:
                            families = self.font_database.applicationFontFamilies(font_id)
                            self.loaded_fonts.update(families)
                            loaded_count += len(families)
                            print(f"✅ フォント読み込み成功: {families}")

            # システム利用可能フォントを検出
            available_families = self.system_fonts
            system_font_count = 0

            # 個別フォントをチェック（改良版）
            for family_name in self.FONT_FAMILIES.values():
                if isinstance(family_name, str):
                    if self._is_font_available_detailed(family_name, available_families):
                        self.loaded_fonts.add(family_name)
                        system_font_count += 1
                        print(f"✅ {family_name} - 利用可能")
                    else:
                        print(f"❌ {family_name} - 利用不可")

            # フォールバックフォントもチェック
            for fallback_font in self.FONT_FAMILIES['fallback']:
                if self._is_font_available_detailed(fallback_font, available_families):
                    self.loaded_fonts.add(fallback_font)
                    system_font_count += 1
                    print(f"✅ {fallback_font} - フォールバック利用可能")

            print(f"フォント読み込み完了: ローカル {loaded_count}個, システム {system_font_count}個")

            if not self.loaded_fonts:
                print("⚠️  推奨フォントが見つかりません。システムデフォルトフォントを使用します。")

        except Exception as e:
            print(f"フォント読み込みエラー: {e}")

    def _is_font_available_detailed(self, font_name: str, available_families: list) -> bool:
        """詳細なフォント可用性チェック"""
        # 直接マッチ
        if font_name in available_families:
            return True

        # 大文字小文字を無視してチェック
        font_lower = font_name.lower()
        for family in available_families:
            if family.lower() == font_lower:
                return True

        # 部分マッチ（主要な部分が含まれているか）
        font_keywords = font_name.lower().split()
        for family in available_families:
            family_lower = family.lower()
            if all(keyword in family_lower for keyword in font_keywords):
                return True

        # 特別なマッピング
        special_mappings = {
            'noto sans jp': ['noto sans cjk jp', 'source han sans', 'noto sans cjk'],
            'noto sans sc': ['noto sans cjk sc', 'source han sans', 'noto sans cjk'],
            'noto sans kr': ['noto sans cjk kr', 'source han sans', 'noto sans cjk'],
            'inter': ['inter ui', 'inter variable'],
            'segoe ui': ['segoe', 'segoe ui regular'],
            'system-ui': ['ubuntu', 'dejavu sans', 'liberation sans', 'arial', 'helvetica']
        }

        if font_lower in special_mappings:
            for mapping in special_mappings[font_lower]:
                for family in available_families:
                    if mapping in family.lower():
                        return True

        return False
    
    def get_best_font(self, language: str = 'auto', size: Optional[int] = None) -> QFont:
        """获取最适合的字体"""
        if size is None:
            size = self.default_font_size
            
        font_family = self._get_font_family_for_language(language)
        font = QFont(font_family, size)
        
        # 现代化字体设置
        font.setStyleHint(QFont.StyleHint.SansSerif)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        
        # 优化渲染
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        
        return font
    
    def get_monospace_font(self, size: Optional[int] = None) -> QFont:
        """获取现代化等宽字体"""
        if size is None:
            size = self.default_font_size
            
        # 现代化等宽字体优先级
        monospace_fonts = [
            'JetBrains Mono',
            'Fira Code',
            'Source Code Pro',
            'Cascadia Code',
            'Consolas',
            'Monaco',
            'Menlo',
            'DejaVu Sans Mono',
            'Liberation Mono',
            'Courier New',
            'monospace'
        ]
        
        for font_name in monospace_fonts:
            if self._is_font_available(font_name):
                font = QFont(font_name, size)
                font.setStyleHint(QFont.StyleHint.Monospace)
                font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
                font.setFixedPitch(True)
                return font
        
        # 回退
        font = QFont('monospace', size)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        return font
    
    def get_display_font(self, size: Optional[int] = None) -> QFont:
        """获取标题/显示字体"""
        if size is None:
            size = self.RESPONSIVE_SIZES['xl']
            
        font_family = self._get_font_family_for_language('display')
        font = QFont(font_family, size)
        font.setWeight(QFont.Weight.Bold)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        
        return font
    
    def _get_font_family_for_language(self, language: str) -> str:
        """根据语言获取字体家族"""
        language = language.lower()
        
        # 语言特定字体选择
        font_mapping = {
            'japanese': self.FONT_FAMILIES['japanese'],
            'jp': self.FONT_FAMILIES['japanese'],
            'chinese': self.FONT_FAMILIES['chinese'],
            'zh': self.FONT_FAMILIES['chinese'],
            'cn': self.FONT_FAMILIES['chinese'],
            'korean': self.FONT_FAMILIES['korean'],
            'kr': self.FONT_FAMILIES['korean'],
            'display': self.FONT_FAMILIES['display']
        }
        
        # 检查特定语言字体
        for key, font_family in font_mapping.items():
            if key in language:
                if self._is_font_available(font_family):
                    return font_family
        
        # 主要字体
        if self._is_font_available(self.FONT_FAMILIES['primary']):
            return self.FONT_FAMILIES['primary']
        
        # 回退字体
        for fallback_font in self.FONT_FAMILIES['fallback']:
            if self._is_font_available(fallback_font):
                return fallback_font
        
        return 'system'
    
    def _is_font_available(self, font_name: str) -> bool:
        """检查字体是否可用（改进版）"""
        if font_name in self.loaded_fonts:
            return True

        # 直接检查系统字体
        if font_name in self.system_fonts:
            return True

        # 检查字体的变体名称
        font_variants = self._get_font_variants(font_name)
        for variant in font_variants:
            if variant in self.system_fonts:
                return True

        # 使用Qt字体匹配来验证
        try:
            from PySide6.QtGui import QFont, QFontInfo
            test_font = QFont(font_name)
            font_info = QFontInfo(test_font)
            actual_family = font_info.family()

            # 如果实际字体家族与请求的相近，认为可用
            if self._fonts_similar(font_name.lower(), actual_family.lower()):
                return True

        except Exception:
            pass

        return False

    def _get_font_variants(self, font_name: str) -> list:
        """获取字体的可能变体名称"""
        variants = [font_name]

        # 常见的字体名称映射
        font_mappings = {
            'Noto Sans JP': ['Noto Sans CJK JP', 'NotoSansCJK-Regular', 'Noto Sans CJK', 'Source Han Sans'],
            'Noto Sans SC': ['Noto Sans CJK SC', 'NotoSansCJK-Regular', 'Noto Sans CJK', 'Source Han Sans'],
            'Noto Sans KR': ['Noto Sans CJK KR', 'NotoSansCJK-Regular', 'Noto Sans CJK', 'Source Han Sans'],
            'Inter': ['Inter UI', 'Inter Variable'],
            'Roboto': ['Roboto Regular'],
            'JetBrains Mono': ['JetBrainsMono-Regular', 'JetBrains Mono Regular'],
            'Segoe UI': ['Segoe UI Regular', 'Segoe'],
            'system-ui': ['Ubuntu', 'DejaVu Sans', 'Liberation Sans', 'Arial']
        }

        if font_name in font_mappings:
            variants.extend(font_mappings[font_name])

        return variants

    def _fonts_similar(self, font1: str, font2: str) -> bool:
        """检查两个字体名称是否相似"""
        # 移除常见的后缀和前缀
        clean1 = font1.replace(' regular', '').replace(' bold', '').replace('-regular', '').replace('-bold', '')
        clean2 = font2.replace(' regular', '').replace(' bold', '').replace('-regular', '').replace('-bold', '')

        # 检查是否包含主要部分
        return clean1 in clean2 or clean2 in clean1 or abs(len(clean1) - len(clean2)) <= 2
    
    def get_responsive_font_size(self, size_key: str) -> int:
        """获取响应式字体大小（固定大小，不再缩放）"""
        return self.RESPONSIVE_SIZES.get(size_key, self.default_font_size)
    
    def create_scaled_font(self, base_font: QFont, zoom_level: int = 100) -> QFont:
        """创建字体（保持兼容性，但不再缩放）"""
        # 返回固定大小的字体，不再进行缩放
        scaled_font = QFont(base_font)
        scaled_font.setPointSize(self.default_font_size)
        return scaled_font
    
    def create_weighted_font(self, base_font: QFont, weight: QFont.Weight) -> QFont:
        """创建不同字重的字体"""
        weighted_font = QFont(base_font)
        weighted_font.setWeight(weight)
        return weighted_font
    
    def apply_application_font(self, language: str = 'auto', zoom_level: int = 100):
        """アプリケーション全体にフォントを適用（固定サイズ）"""
        app = QApplication.instance()
        if not app:
            return

        font = self.get_best_font(language)
        font.setPointSize(self.default_font_size)

        app.setFont(font)
        print(f"フォント適用: {font.family()} {font.pointSize()}pt (固定サイズ)")

    def apply_unified_fonts_to_window(self, window, zoom_level: int = 100):
        """ウィンドウ全体に統一されたフォントを適用（固定サイズ）"""
        try:
            from PySide6.QtWidgets import QMainWindow

            if not isinstance(window, QMainWindow):
                return

            # アプリケーション全体の基本フォントを更新
            app = QApplication.instance()
            if app:
                app_font = self.get_best_font()
                app_font.setPointSize(self.default_font_size)
                app.setFont(app_font)

            # 基本フォント設定
            base_font = self.get_best_font()
            base_font.setPointSize(self.default_font_size)

            # ウィンドウ自体にフォントを設定
            window.setFont(base_font)

            # メニューバーフォント
            menubar = window.menuBar()
            if menubar:
                menu_font = self.get_best_font()
                menu_font.setPointSize(self.get_responsive_font_size('sm'))
                menubar.setFont(menu_font)

                # すべてのメニューとサブメニューに適用
                self._apply_font_to_menus(menubar, menu_font)

            # ステータスバーフォント
            statusbar = window.statusBar()
            if statusbar:
                status_font = self.get_best_font()
                status_font.setPointSize(self.get_responsive_font_size('xs'))
                statusbar.setFont(status_font)

            # 中央ウィジェットフォント
            central_widget = window.centralWidget()
            if central_widget:
                central_widget.setFont(base_font)
                self._apply_font_recursively(central_widget, 100)

        except Exception as e:
            print(f"統一フォント適用エラー: {e}")

    def _apply_font_to_menus(self, menubar, font):
        """メニューバーのすべてのメニューにフォントを適用"""
        for action in menubar.actions():
            if action.menu():
                menu = action.menu()
                menu.setFont(font)
                # サブメニューも処理
                for sub_action in menu.actions():
                    if sub_action.menu():
                        sub_action.menu().setFont(font)

    def _apply_font_recursively(self, widget, zoom_level: int = 100):
        """ウィジェットとその子要素に再帰的にフォントを適用（固定サイズ）"""
        try:
            from PySide6.QtWidgets import QTextEdit, QLabel, QPushButton, QComboBox, QLineEdit

            # ウィジェットタイプに応じて適切なフォントを設定
            if isinstance(widget, QTextEdit):
                # ログ用等幅フォント
                mono_font = self.get_monospace_font()
                mono_font.setPointSize(self.get_responsive_font_size('sm'))
                widget.setFont(mono_font)
            elif isinstance(widget, (QLabel, QPushButton, QComboBox, QLineEdit)):
                # 通常のUIフォント
                ui_font = self.get_best_font()
                ui_font.setPointSize(self.get_responsive_font_size('base'))
                widget.setFont(ui_font)

            # 子ウィジェットを処理
            for child in widget.children():
                if hasattr(child, 'setFont'):
                    self._apply_font_recursively(child, 100)

        except Exception as e:
            print(f"再帰的フォント適用エラー: {e}")
    
    def get_font_info(self) -> Dict:
        """获取字体信息"""
        return {
            'loaded_fonts': sorted(list(self.loaded_fonts)),
            'system_fonts': len(self.system_fonts),
            'default_size': self.default_font_size,
            'primary_font': self._get_font_family_for_language('auto'),
            'available_families': self.system_fonts[:20]  # 前20个
        }
    
    def get_font_hierarchy(self, zoom_level: int = 100) -> Dict[str, QFont]:
        """获取字体层级（固定大小）"""
        return {
            'display': self.get_display_font(self.get_responsive_font_size('2xl')),
            'title': self.get_best_font(size=self.get_responsive_font_size('xl')),
            'subtitle': self.get_best_font(size=self.get_responsive_font_size('lg')),
            'body': self.get_best_font(size=self.get_responsive_font_size('base')),
            'caption': self.get_best_font(size=self.get_responsive_font_size('sm')),
            'small': self.get_best_font(size=self.get_responsive_font_size('xs')),
            'monospace': self.get_monospace_font(self.get_responsive_font_size('base'))
        }


# 全局字体管理器实例
_font_manager = None


def get_font_manager() -> ModernFontManager:
    """获取全局字体管理器"""
    global _font_manager
    if _font_manager is None:
        _font_manager = ModernFontManager()
        _font_manager.load_google_fonts()
    return _font_manager


def setup_application_fonts(language: str = 'auto', zoom_level: int = 100):
    """设置应用程序字体（固定大小）"""
    font_manager = get_font_manager()
    font_manager.apply_application_font(language, 100)


def get_ui_font(language: str = 'auto', size: Optional[int] = None, zoom_level: int = 100) -> QFont:
    """获取UI字体（固定大小）"""
    font_manager = get_font_manager()
    if size:
        return font_manager.get_best_font(language, size)
    return font_manager.get_best_font(language)


def get_log_font(size: Optional[int] = None, zoom_level: int = 100) -> QFont:
    """获取日志字体（固定大小）"""
    font_manager = get_font_manager()
    if size:
        return font_manager.get_monospace_font(size)
    return font_manager.get_monospace_font()


# 向后兼容
FontManager = ModernFontManager
