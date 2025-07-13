# PPT Translator Desktop

基于 PySide6 开发的 PowerPoint 翻译桌面应用程序，使用 AI 大语言模型进行智能翻译。

## 功能特点

- 🎯 **智能翻译**: 支持 OpenAI GPT 模型进行高质量翻译
- 🖥️ **桌面应用**: 基于 PySide6 的现代化桌面界面
- 📊 **进度显示**: 实时显示翻译进度和详细日志
- ⚙️ **配置管理**: 灵活的 API 配置和应用设置
- 🔍 **缩放支持**: 100%-250% UI 缩放，适配高分屏显示
- 🎨 **Google字体**: 使用Noto Sans系列字体，完美支持中日英多语言
- 📦 **独立打包**: 使用 PyInstaller 打包为独立可执行文件
- 🌐 **多语言支持**: 支持中文、日文、英文互译

## 支持的模型

- OpenAI GPT-4o (推荐)
- xai.grok-3 (通过 OCI Generative AI)

## 系统要求

- Windows 10/11, macOS 10.14+, 或 Linux
- Python 3.8+ (开发环境)
- 4GB+ RAM
- 网络连接 (用于 API 调用)

## 快速开始

### 方法一：使用预编译版本

1. 从 [Releases](../../releases) 下载最新版本
2. 解压到任意目录
3. 运行 `PPTTranslator.exe` (Windows) 或 `PPTTranslator` (Linux/macOS)
4. 在设置中配置 API 密钥

### 方法二：从源码运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/No.1-PPT-Translator.git
   cd No.1-PPT-Translator
   ```

2. **安装依赖**
   ```bash
   conda create -n no.1-ppt-translator python=3.11 -y
   conda activate no.1-ppt-translator
   pip install -r requirements.txt
   ```

3. **配置环境**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置 API 密钥
   ```

4. **运行应用**
   ```bash
   python main.py
   ```

## 配置说明

### API 配置

在 `.env` 文件中配置以下参数：

```env
# OpenAI API设定
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4o

# 应用设置
DEFAULT_TARGET_LANGUAGE=Japanese
OUTPUT_DIRECTORY=outputs
```

### 支持的配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 必填 |
| `OPENAI_BASE_URL` | API 基础 URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL_NAME` | 使用的模型名称 | `gpt-4o` |
| `DEFAULT_TARGET_LANGUAGE` | 默认目标语言 | `Japanese` |
| `OUTPUT_DIRECTORY` | 输出目录 | `outputs` |
| `UI_ZOOM_LEVEL` | UI 缩放级别 (100-250) | `100` |

## 使用方法

1. **启动应用**: 运行 `PPTTranslator.exe` 或 `python main.py`

2. **配置 API**:
   - 点击菜单 "ファイル" → "設定"
   - 输入 OpenAI API 密钥
   - 配置其他选项

3. **选择文件**: 点击 "ファイルを選択" 选择要翻译的 PPTX 文件

4. **设置翻译选项**:
   - 选择使用的模型
   - 选择目标语言

5. **开始翻译**: 点击 "翻訳開始" 按钮

6. **查看结果**: 翻译完成后，文件将保存到输出目录

### UI 缩放功能

应用支持 100% 到 250% 的 UI 缩放，特别适合高分屏用户：

**设置缩放级别:**
- 方法一：菜单 "表示" → "ズーム" → 选择缩放级别
- 方法二：菜单 "ファイル" → "設定" → "一般設定" → "UIズームレベル"

**支持的缩放级别:**
- 100% (默认)
- 110%, 120%, 130%, ..., 250% (10% 递增)

### 字体系统

应用使用 Google Noto Sans 字体系列，提供优秀的多语言支持：

**主要字体:**
- **Noto Sans**: 主要UI字体，支持拉丁文、西里尔文等
- **Noto Sans JP**: 日语专用字体（平假名、片假名、汉字）
- **Noto Sans SC**: 中文简体字专用字体
- **Noto Sans Mono**: 等宽字体，用于日志显示

**字体特性:**
- 默认字体大小：16pt
- 自动语言检测和字体选择
- 高质量抗锯齿渲染
- 完整的Unicode支持

## 构建说明

### 从源码构建

**Windows:**
```bash
# 运行构建脚本
build.bat
```

**Linux/macOS:**
```bash
# 给脚本执行权限
chmod +x build.sh
# 运行构建脚本
./build.sh
```

**手动构建:**
```bash
# 安装依赖
pip install -r requirements.txt

# 使用 PyInstaller 构建
python build_exe.py
```

构建完成后，可执行文件将位于 `dist/` 目录中。

## 项目结构

```
No.1-PPT-Translator/
├── main.py                 # 应用入口点
├── requirements.txt        # Python 依赖
├── .env.example           # 环境变量示例
├── build_exe.py           # PyInstaller 构建脚本
├── build.bat              # Windows 构建脚本
├── build.sh               # Linux/macOS 构建脚本
├── src/
│   ├── ui/                # 用户界面
│   │   ├── main_window.py # 主窗口
│   │   └── settings_dialog.py # 设置对话框
│   ├── core/              # 核心功能
│   │   └── translator.py  # 翻译引擎
│   └── utils/             # 工具模块
│       ├── config.py      # 配置管理
│       ├── logger.py      # 日志系统
│       └── validator.py   # 配置验证
└── outputs/               # 输出目录
```

## 技术特性

### 核心技术栈

- **UI 框架**: PySide6 (Qt for Python)
- **翻译引擎**: OpenAI GPT API
- **文档处理**: python-pptx
- **打包工具**: PyInstaller
- **配置管理**: python-dotenv

### 翻译特性

- **智能占位符保护**: 自动识别并保护 `[PLACEHOLDER_X]` 格式的占位符
- **多线程处理**: 使用 QThread 进行后台翻译，不阻塞 UI
- **进度追踪**: 实时显示翻译进度和当前处理的幻灯片
- **错误恢复**: 自动重试机制，提高翻译成功率
- **格式保持**: 保持原始 PPT 的格式、样式和布局

### 支持的内容类型

- ✅ 文本框内容
- ✅ 表格单元格
- ✅ 备注页内容
- ✅ 多段落文本
- ❌ SmartArt 图形 (暂不支持)
- ❌ 图片中的文字 (暂不支持)

## 故障排除

### 常见问题

**Q: 应用启动失败**
A: 检查是否安装了所有依赖，运行 `pip install -r requirements.txt`

**Q: API 调用失败**
A:
- 检查 API 密钥是否正确
- 确认网络连接正常
- 验证 API 配额是否充足

**Q: 翻译结果不理想**
A:
- 尝试使用不同的模型 (如 gpt-4o)
- 检查源文本是否包含特殊字符
- 确认目标语言设置正确

**Q: 打包后的程序无法运行**
A:
- 确保目标系统满足最低要求
- 检查是否缺少系统依赖
- 查看错误日志文件

### 日志文件

应用会在以下位置生成日志文件：
- **开发模式**: `logs/ppt_translator_YYYYMMDD.log`
- **打包版本**: 程序目录下的 `logs/` 文件夹

## 开发指南

### 开发环境设置

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/No.1-PPT-Translator.git
   cd No.1-PPT-Translator
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装开发依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python main.py
   ```

### 代码结构说明

- `src/ui/`: 用户界面相关代码
- `src/core/`: 核心业务逻辑
- `src/utils/`: 工具和辅助功能

### 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

- 感谢 [engchina/llm-ppt-translator](https://github.com/engchina/llm-ppt-translator) 项目提供的灵感
- 感谢 OpenAI 提供强大的 GPT 模型
- 感谢 Qt 团队提供优秀的 PySide6 框架

## 更新日志

### v1.0.3 (2025-01-13)
- 🔧 修复窗口标题字体缩放问题，确保所有页面标题正确联动
- 🎨 改进对话框和菜单的字体缩放一致性
- ⚡ 优化样式表应用，提升字体渲染效果

### v1.0.2 (2025-01-13)
- 🎨 更新默认字体大小为16pt，提升可读性
- 🌐 集成Google Noto字体系列，完美支持中日英多语言
- 🔧 调整UI缩放范围为100%-250%，移除过大的缩放级别
- ⚡ 优化字体管理系统，提升渲染质量

### v1.0.1 (2025-01-13)
- 🔧 修复 UI 缩放功能，确保所有界面元素正确缩放
- 🔧 改进日志区域和文件选择标签的字体缩放
- 🔧 优化缩放应用逻辑，避免重复缩放问题

### v1.0.0 (2025-01-13)
- 🎉 初始版本发布
- ✨ 支持 PPT 文件翻译
- ✨ 现代化桌面界面
- ✨ 多模型支持
- ✨ 配置管理系统
- ✨ 进度显示和日志记录
- 🔍 UI 缩放功能 (100%-300%)
- 📦 PyInstaller 打包支持

---

如有问题或建议，请提交 [Issue](../../issues) 或联系开发团队。