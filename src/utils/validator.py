#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定検証ユーティリティ
"""

import os
import requests
from typing import Tuple, List

from .config import ConfigManager


class ConfigValidator:
    """設定検証クラス"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def validate_openai_connection(self) -> Tuple[bool, str]:
        """OpenAI接続を検証"""
        try:
            api_key = self.config_manager.get_openai_api_key()
            base_url = self.config_manager.get_openai_base_url()
            
            if not api_key:
                return False, "API Keyが設定されていません"
            
            if not base_url:
                return False, "Base URLが設定されていません"
            
            # 簡単な接続テスト
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # モデル一覧を取得してテスト
            response = requests.get(
                f"{base_url.rstrip('/')}/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "接続成功"
            else:
                return False, f"接続失敗: HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "接続タイムアウト"
        except requests.exceptions.ConnectionError:
            return False, "接続エラー"
        except Exception as e:
            return False, f"予期しないエラー: {str(e)}"
    
    def validate_output_directory(self) -> Tuple[bool, str]:
        """出力ディレクトリを検証"""
        try:
            output_dir = self.config_manager.get_output_directory()
            
            # ディレクトリの作成を試行
            os.makedirs(output_dir, exist_ok=True)
            
            # 書き込み権限をテスト
            test_file = os.path.join(output_dir, "test_write.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                return True, "出力ディレクトリは正常です"
            except Exception:
                return False, "出力ディレクトリに書き込み権限がありません"
                
        except Exception as e:
            return False, f"出力ディレクトリの検証に失敗: {str(e)}"
    
    def validate_all(self) -> Tuple[bool, List[str]]:
        """全ての設定を検証"""
        errors = []
        
        # 基本設定の検証
        is_valid, config_errors = self.config_manager.validate_config()
        if not is_valid:
            errors.extend(config_errors)
        
        # OpenAI接続の検証
        openai_valid, openai_msg = self.validate_openai_connection()
        if not openai_valid:
            errors.append(f"OpenAI接続: {openai_msg}")
        
        # 出力ディレクトリの検証
        output_valid, output_msg = self.validate_output_directory()
        if not output_valid:
            errors.append(f"出力ディレクトリ: {output_msg}")
        
        return len(errors) == 0, errors
