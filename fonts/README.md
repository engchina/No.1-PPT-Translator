# PPT Translator フォントシステム

PPT Translatorは現代的なデザインシステムを採用しており、最適な表示のために推奨フォントの使用を強く推奨します。

## 🚀 クイックスタート

### 自動インストール（推奨）

```bash
# システムフォントインストールガイドを表示
python scripts/install_system_fonts.py

# または、フォントファイルを自動ダウンロード（要インターネット接続）
python scripts/download_fonts.py
```

### 手動インストール

以下の推奨フォントをシステムにインストールしてください。

## 📝 推奨フォント

### 1. Noto Sans (主要フォント) ⭐

- **用途**: 一般的なUI要素、多言語テキスト
- **対応言語**: ラテン文字、キリル文字、ギリシャ文字など
- **重要度**: 必須
- **ダウンロード**: https://fonts.google.com/noto/specimen/Noto+Sans

### 2. Noto Sans JP (日本語) ⭐

- **用途**: 日本語テキスト表示
- **対応言語**: 日本語（ひらがな、カタカナ、漢字）
- **重要度**: 必須（日本語使用時）
- **ダウンロード**: https://fonts.google.com/noto/specimen/Noto+Sans+JP

### 3. Noto Sans SC (中国語簡体字)

- **用途**: 中国語簡体字テキスト
- **対応言語**: 中国語簡体字
- **重要度**: 推奨（中国語使用時）
- **ダウンロード**: https://fonts.google.com/noto/specimen/Noto+Sans+SC

### 4. Inter (現代的UI)

- **用途**: モダンなUI要素
- **特徴**: 高い可読性、現代的デザイン
- **重要度**: 推奨
- **ダウンロード**: https://fonts.google.com/specimen/Inter

### 5. JetBrains Mono (等幅フォント)

- **用途**: ログ表示、コード表示
- **特徴**: プログラミング向け等幅フォント
- **重要度**: 推奨
- **ダウンロード**: https://fonts.google.com/specimen/JetBrains+Mono

## インストール方法

### 方法1: 手動ダウンロード
1. 上記のリンクから各フォントをダウンロード
2. TTFファイルをこの `fonts/` ディレクトリに配置
3. アプリケーションを再起動

### 方法2: システムフォントを使用
- システムにNoto Fontsがインストールされている場合、自動的に検出されます
- Windows: Microsoft Store から "Noto Sans" を検索してインストール
- macOS: Font Book でフォントをインストール
- Linux: パッケージマネージャーでnoto-fontsをインストール

## ファイル構成例

```
fonts/
├── README.md (このファイル)
├── NotoSans-Regular.ttf
├── NotoSans-Bold.ttf
├── NotoSansJP-Regular.ttf
├── NotoSansJP-Bold.ttf
├── NotoSansSC-Regular.ttf
├── NotoSansSC-Bold.ttf
├── NotoSansMono-Regular.ttf
└── NotoSansMono-Bold.ttf
```

## フォールバック

フォントが見つからない場合、以下の順序でフォールバックします：

1. **Noto Sans系フォント** (推奨)
2. **Arial** (Windows標準)
3. **Helvetica** (macOS標準)
4. **sans-serif** (システムデフォルト)

## 注意事項

- フォントファイルは著作権で保護されています
- Google Fontsは無料で使用できますが、ライセンスを確認してください
- 大きなフォントファイルはアプリケーションのサイズを増加させます
- 必要な言語のフォントのみをインストールすることを推奨します

## トラブルシューティング

### フォントが表示されない場合
1. フォントファイルが正しいディレクトリに配置されているか確認
2. ファイル名が正しいか確認（大文字小文字を含む）
3. アプリケーションを再起動
4. システムにフォントがインストールされているか確認

### 文字化けが発生する場合
1. 対象言語に対応したフォントがインストールされているか確認
2. フォントファイルが破損していないか確認
3. システムの言語設定を確認

## ライセンス

Google Noto Fontsは SIL Open Font License 1.1 の下で提供されています。
詳細: https://scripts.sil.org/OFL
