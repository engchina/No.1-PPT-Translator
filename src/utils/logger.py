#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ログシステム
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Signal


class LogLevel:
    """ログレベル定数"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class QtLogHandler(logging.Handler, QObject):
    """Qt用ログハンドラー"""
    
    log_message = Signal(str, int)  # メッセージ, レベル
    
    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)
    
    def emit(self, record):
        """ログレコードを処理"""
        try:
            msg = self.format(record)
            self.log_message.emit(msg, record.levelno)
        except Exception:
            self.handleError(record)


class AppLogger:
    """アプリケーションロガー"""
    
    def __init__(self, name: str = "PPTTranslator"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 重複ハンドラーを防ぐ
        if not self.logger.handlers:
            self._setup_handlers()
        
        self.qt_handler: Optional[QtLogHandler] = None
    
    def _setup_handlers(self):
        """ハンドラーの設定"""
        # ファイルハンドラー
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"ppt_translator_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def setup_qt_handler(self) -> QtLogHandler:
        """Qt用ハンドラーを設定"""
        if self.qt_handler is None:
            self.qt_handler = QtLogHandler()
            self.qt_handler.setLevel(logging.INFO)
            
            # シンプルなフォーマッター
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            self.qt_handler.setFormatter(formatter)
            
            self.logger.addHandler(self.qt_handler)
        
        return self.qt_handler
    
    def debug(self, message: str):
        """デバッグログ"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """情報ログ"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告ログ"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """エラーログ"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """重大エラーログ"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """例外ログ"""
        self.logger.exception(message)


class ProgressTracker:
    """進捗追跡クラス"""
    
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.step_descriptions = {}
    
    def set_step_description(self, step: int, description: str):
        """ステップの説明を設定"""
        self.step_descriptions[step] = description
    
    def next_step(self, description: Optional[str] = None) -> tuple[int, str]:
        """次のステップに進む"""
        self.current_step += 1
        
        if description:
            self.step_descriptions[self.current_step] = description
        
        step_desc = self.step_descriptions.get(self.current_step, f"ステップ {self.current_step}")
        progress_percent = int((self.current_step / self.total_steps) * 100)
        
        return progress_percent, step_desc
    
    def get_progress(self) -> tuple[int, str]:
        """現在の進捗を取得"""
        progress_percent = int((self.current_step / self.total_steps) * 100)
        step_desc = self.step_descriptions.get(self.current_step, f"ステップ {self.current_step}")
        return progress_percent, step_desc
    
    def reset(self):
        """進捗をリセット"""
        self.current_step = 0
        self.step_descriptions.clear()


# グローバルロガーインスタンス
app_logger = AppLogger()


def get_logger() -> AppLogger:
    """グローバルロガーを取得"""
    return app_logger
