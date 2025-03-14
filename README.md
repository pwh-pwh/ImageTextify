# ImageTextify

一个简洁优雅的图片文字识别工具，支持中英文识别，具有现代化的苹果风格界面设计。

[English](README_EN.md) | 中文文档

## 功能特点

- 🖼️ 支持拖放图片或选择图片文件
- 📝 支持中英文文字识别
- 🎨 现代化苹果风格界面
- 🌈 支持多种主题切换
- 📋 一键复制识别结果
- 💾 支持保存结果到文件
- 🔄 实时识别进度显示
- 💫 流畅的操作体验
- 🛠️ 内置 Tesseract 配置检查工具

## 界面预览

![界面预览](docs/preview.png)

## 安装要求

1. Python 3.6 或更高版本
2. Tesseract-OCR 引擎

### 依赖包安装

```bash
pip install -r requirements.txt
```

### Tesseract-OCR 安装

1. Windows:
   - 下载 [Tesseract-OCR 安装包](https://github.com/UB-Mannheim/tesseract/wiki)
   - 安装时记得选择"Additional language data"以支持中文识别
   - 设置环境变量或在代码中指定 Tesseract 路径

2. macOS:
   ```bash
   brew install tesseract
   brew install tesseract-lang
   ```

3. Linux:
   ```bash
   sudo apt-get install tesseract-ocr
   sudo apt-get install tesseract-ocr-chi-sim
   ```

## 配置说明

1. 打开 `image_text_gui.py`，找到以下代码行：
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

2. 将路径修改为您系统中 Tesseract 的实际安装路径：
   - Windows: 通常为 `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - macOS/Linux: 通常不需要设置，系统会自动查找

## 使用说明

1. 运行程序：
   ```bash
   python image_text_gui.py
   ```

2. 使用方式：
   - 直接将图片拖放到程序窗口
   - 点击"选择图片"按钮选择图片文件
   - 使用菜单"文件->选择图片"
   - 点击"提取文字"开始识别
   - 识别完成后可以点击"复制结果"或"保存结果"

3. 菜单功能：
   - 文件菜单：选择图片、保存结果、退出程序
   - 工具菜单：检查 Tesseract 配置、清空结果
   - 主题菜单：切换界面主题
   - 帮助菜单：使用说明、检查更新、关于信息

## 主题切换

程序支持多种主题风格，可以在"主题"菜单中选择：

### 亮色主题
- litera (默认，类似苹果风格)
- cosmo
- flatly
- journal
- lumen
- minty
- pulse
- sandstone
- united
- yeti

### 暗色主题
- darkly
- cyborg
- vapor
- solar

## 常见问题

1. **找不到 Tesseract-OCR**
   - 确保已正确安装 Tesseract-OCR
   - 检查代码中的 Tesseract 路径设置是否正确
   - 使用工具菜单中的"检查 Tesseract 配置"功能进行诊断

2. **中文识别效果不好**
   - 确保安装了中文语言包
   - 检查图片质量，建议使用清晰的图片
   - 避免使用带有复杂背景的图片

3. **拖放功能无效**
   - 确保已正确安装 tkinterdnd2 包
   - 检查系统是否支持拖放功能

4. **主题切换失败**
   - 确保已正确安装 ttkbootstrap 包
   - 尝试重启程序后再次切换主题

## 技术栈

- Python 3.x
- tkinter & ttkbootstrap (GUI)
- Tesseract-OCR (文字识别引擎)
- Pillow (图片处理)
- tkinterdnd2 (拖放支持)

## 开发计划

- [ ] 批量识别功能
- [ ] 识别区域选择
- [ ] 自定义主题保存
- [ ] 多语言支持
- [ ] 图片预处理功能
- [ ] OCR 引擎切换

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-01-20)
- 初始版本发布
- 支持图片拖放和文件选择
- 支持中英文识别
- 现代化界面设计
- 复制结果功能
- 进度显示

### v1.1.0 (2024-01-21)
- 新增菜单栏
- 添加主题切换功能
- 新增 Tesseract 配置检查
- 添加结果保存功能
- 优化用户界面
- 添加关于对话框
- 增加使用说明

## 贡献指南

1. Fork 本仓库
2. 创建新的分支 `git checkout -b feature/your-feature`
3. 提交更改 `git commit -am 'Add some feature'`
4. 推送到分支 `git push origin feature/your-feature`
5. 创建 Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: [提交问题](https://github.com/pwh-pwh/ImageTextify/issues)
- GitHub Discussions: [参与讨论](https://github.com/pwh-pwh/ImageTextify/discussions)

## 致谢

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pwh-pwh/ImageTextify&type=Date)](https://star-history.com/#pwh-pwh/ImageTextify&Date)