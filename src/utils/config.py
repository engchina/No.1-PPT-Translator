#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定管理
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv, find_dotenv


class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self):
        # .envファイルを読み込み
        self._load_env_file()
        
        # デフォルト値
        self._defaults = {
            "OPENAI_BASE_URL": "https://api.openai.com/v1",
            "OPENAI_MODEL_NAME": "gpt-4o",
            "DEFAULT_TARGET_LANGUAGE": "Japanese",
            "OUTPUT_DIRECTORY": "outputs",
            "CONFIG_PROFILE": "DEFAULT"
        }
    
    def _load_env_file(self):
        """環境変数ファイルを読み込み"""
        # プロジェクトルートの.envファイルを探す
        project_root = Path(__file__).parent.parent.parent
        env_file = project_root / ".env"
        
        if env_file.exists():
            load_dotenv(env_file)
        else:
            # .envファイルが見つからない場合は自動検索
            load_dotenv(find_dotenv())
    
    def get_openai_api_key(self) -> Optional[str]:
        """OpenAI API Keyを取得"""
        return os.getenv("OPENAI_API_KEY")
    
    def set_openai_api_key(self, api_key: str):
        """OpenAI API Keyを設定"""
        os.environ["OPENAI_API_KEY"] = api_key
    
    def get_openai_base_url(self) -> str:
        """OpenAI Base URLを取得"""
        return os.getenv("OPENAI_BASE_URL", self._defaults["OPENAI_BASE_URL"])
    
    def set_openai_base_url(self, base_url: str):
        """OpenAI Base URLを設定"""
        os.environ["OPENAI_BASE_URL"] = base_url
    
    def get_openai_model_name(self) -> str:
        """OpenAI Model Nameを取得"""
        return os.getenv("OPENAI_MODEL_NAME", self._defaults["OPENAI_MODEL_NAME"])
    
    def set_openai_model_name(self, model_name: str):
        """OpenAI Model Nameを設定"""
        os.environ["OPENAI_MODEL_NAME"] = model_name
    
    def get_compartment_id(self) -> Optional[str]:
        """OCI Compartment IDを取得"""
        return os.getenv("COMPARTMENT_ID")
    
    def set_compartment_id(self, compartment_id: str):
        """OCI Compartment IDを設定"""
        os.environ["COMPARTMENT_ID"] = compartment_id
    
    def get_config_profile(self) -> str:
        """OCI Config Profileを取得"""
        return os.getenv("CONFIG_PROFILE", self._defaults["CONFIG_PROFILE"])
    
    def set_config_profile(self, config_profile: str):
        """OCI Config Profileを設定"""
        os.environ["CONFIG_PROFILE"] = config_profile
    
    def get_default_language(self) -> str:
        """デフォルト対象言語を取得"""
        return os.getenv("DEFAULT_TARGET_LANGUAGE", self._defaults["DEFAULT_TARGET_LANGUAGE"])
    
    def set_default_language(self, language: str):
        """デフォルト対象言語を設定"""
        os.environ["DEFAULT_TARGET_LANGUAGE"] = language
    
    def get_output_directory(self) -> str:
        """出力ディレクトリを取得"""
        output_dir = os.getenv("OUTPUT_DIRECTORY", self._defaults["OUTPUT_DIRECTORY"])
        
        # 相対パスの場合は絶対パスに変換
        if not os.path.isabs(output_dir):
            project_root = Path(__file__).parent.parent.parent
            output_dir = str(project_root / output_dir)
        
        return output_dir
    
    def set_output_directory(self, output_dir: str):
        """出力ディレクトリを設定"""
        os.environ["OUTPUT_DIRECTORY"] = output_dir


    
    def save_config(self):
        """設定を.envファイルに保存"""
        project_root = Path(__file__).parent.parent.parent
        env_file = project_root / ".env"
        
        # 現在の環境変数から設定を収集
        config_vars = [
            "OPENAI_API_KEY",
            "OPENAI_BASE_URL",
            "OPENAI_MODEL_NAME",
            "COMPARTMENT_ID",
            "CONFIG_PROFILE",
            "DEFAULT_TARGET_LANGUAGE",
            "OUTPUT_DIRECTORY",
            "UI_ZOOM_LEVEL"
        ]
        
        lines = []
        lines.append("# OpenAI API設定")
        
        for var in config_vars:
            value = os.getenv(var)
            if value:
                if var == "COMPARTMENT_ID":
                    lines.append("\n# OCI GenAI設定（オプション）")
                elif var == "DEFAULT_TARGET_LANGUAGE":
                    lines.append("\n# アプリケーション設定")
                
                lines.append(f"{var}={value}")
        
        # ファイルに書き込み
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        except Exception as e:
            raise Exception(f"設定ファイルの保存に失敗しました: {e}")
    
    def get_all_settings(self) -> dict:
        """すべての設定を辞書形式で取得"""
        return {
            'api_key': self.get_openai_api_key(),
            'base_url': self.get_openai_base_url(),
            'model_name': self.get_openai_model_name(),
            'compartment_id': self.get_compartment_id(),
            'config_profile': self.get_config_profile(),
            'default_language': self.get_default_language(),
            'output_directory': self.get_output_directory()
        }

    def set_setting(self, key: str, value):
        """設定値を設定（汎用メソッド）"""
        setting_map = {
            'api_key': self.set_openai_api_key,
            'base_url': self.set_openai_base_url,
            'model_name': self.set_openai_model_name,
            'compartment_id': self.set_compartment_id,
            'config_profile': self.set_config_profile,
            'default_language': self.set_default_language,
            'output_directory': self.set_output_directory
        }

        if key in setting_map:
            setting_map[key](value)
        else:
            # 直接環境変数に設定
            os.environ[key.upper()] = str(value)

    def validate_config(self) -> tuple[bool, list[str]]:
        """設定の妥当性を検証"""
        errors = []

        # 必須設定のチェック
        if not self.get_openai_api_key():
            errors.append("OpenAI API Keyが設定されていません")

        if not self.get_openai_base_url():
            errors.append("OpenAI Base URLが設定されていません")

        # 出力ディレクトリの存在確認
        output_dir = self.get_output_directory()
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            errors.append(f"出力ディレクトリの作成に失敗しました: {e}")

        return len(errors) == 0, errors
