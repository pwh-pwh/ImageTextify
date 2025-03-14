# 图片文字提取器

一个简洁优雅的图片文字识别工具，支持中英文识别，具有现代化的苹果风格界面设计。

## 功能特点

- 🖼️ 支持拖放图片或选择图片文件
- 📝 支持中英文文字识别
- 🎨 现代化苹果风格界面
- 📋 一键复制识别结果
- 🔄 实时识别进度显示
- 💫 流畅的操作体验

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
   - 或点击"选择图片"按钮选择图片文件
   - 点击"提取文字"开始识别
   - 识别完成后可以点击"复制结果"复制文字

## 自定义主题

程序默认使用类似苹果风格的 litera 主题，如果想要更换主题，可以修改以下代码行：

```python
self.style = ttk.Style(theme="litera")
```

可选主题包括：
- 亮色主题：litera, cosmo, flatly, journal, lumen, minty, pulse, sandstone, united, yeti
- 暗色主题：darkly, cyborg, vapor, solar

## 常见问题

1. **找不到 Tesseract-OCR**
   - 确保已正确安装 Tesseract-OCR
   - 检查代码中的 Tesseract 路径设置是否正确

2. **中文识别效果不好**
   - 确保安装了中文语言包
   - 检查图片质量，建议使用清晰的图片

3. **拖放功能无效**
   - 确保已正确安装 tkinterdnd2 包
   - 检查系统是否支持拖放功能

## 技术栈

- Python 3.x
- tkinter & ttkbootstrap (GUI)
- Tesseract-OCR (文字识别引擎)
- Pillow (图片处理)
- tkinterdnd2 (拖放支持)

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 支持图片拖放和文件选择
- 支持中英文识别
- 现代化界面设计
- 复制结果功能
- 进度显示

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！

## 联系方式

如有问题或建议，请通过 Issue 与我们联系。