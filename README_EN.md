# ImageTextify

A sleek and elegant OCR (Optical Character Recognition) tool with a modern Apple-style interface, supporting both Chinese and English text recognition.

[English](README_EN.md) | [中文文档](README.md)

## Features

- 🖼️ Drag & drop or select image files
- 📝 Chinese and English text recognition
- 🎨 Modern Apple-style interface
- 🌈 Multiple theme options
- 📋 One-click text copy
- 💾 Save results to file
- 🔄 Real-time recognition progress
- 💫 Smooth user experience
- 🛠️ Built-in Tesseract configuration checker

## Interface Preview

![Interface Preview](docs/preview.png)

## Requirements

1. Python 3.6 or higher
2. Tesseract-OCR engine

### Package Installation

```bash
pip install -r requirements.txt
```

### Tesseract-OCR Installation

1. Windows:
   - Download [Tesseract-OCR installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Select "Additional language data" during installation for Chinese support
   - Set environment variables or specify Tesseract path in code

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

## Configuration

1. Open `image_text_gui.py`, locate the following line:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

2. Modify the path to match your Tesseract installation:
   - Windows: Usually `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - macOS/Linux: No configuration needed, system will find automatically

## Usage

1. Run the program:
   ```bash
   python image_text_gui.py
   ```

2. How to use:
   - Drag and drop images directly into the window
   - Click "Select Image" button to choose an image file
   - Use "File -> Select Image" from the menu
   - Click "Extract Text" to start recognition
   - After recognition, click "Copy Result" or "Save Result"

3. Menu Functions:
   - File Menu: Select Image, Save Result, Exit
   - Tools Menu: Check Tesseract Configuration, Clear Result
   - Theme Menu: Switch Interface Theme
   - Help Menu: User Guide, Check Updates, About

## Theme Options

The program supports various themes, available in the "Theme" menu:

### Light Themes
- litera (Default, Apple-style)
- cosmo
- flatly
- journal
- lumen
- minty
- pulse
- sandstone
- united
- yeti

### Dark Themes
- darkly
- cyborg
- vapor
- solar

## Troubleshooting

1. **Tesseract-OCR Not Found**
   - Ensure Tesseract-OCR is properly installed
   - Check if the Tesseract path in code is correct
   - Use "Check Tesseract Configuration" in Tools menu for diagnosis

2. **Poor Chinese Recognition**
   - Ensure Chinese language pack is installed
   - Check image quality, use clear images
   - Avoid images with complex backgrounds

3. **Drag & Drop Not Working**
   - Verify tkinterdnd2 package is installed correctly
   - Check if your system supports drag & drop

4. **Theme Switching Failed**
   - Ensure ttkbootstrap is installed correctly
   - Try restarting the program before switching themes

## Tech Stack

- Python 3.x
- tkinter & ttkbootstrap (GUI)
- Tesseract-OCR (OCR engine)
- Pillow (Image processing)
- tkinterdnd2 (Drag & drop support)

## Development Roadmap

- [ ] Batch recognition
- [ ] Recognition area selection
- [ ] Custom theme saving
- [ ] Multi-language support
- [ ] Image preprocessing
- [ ] OCR engine switching

## License

MIT License

## Changelog

### v1.1.0 (2024-01-21)
- Added menu bar
- Added theme switching
- Added Tesseract configuration checker
- Added result saving feature
- Improved user interface
- Added about dialog
- Added user guide

### v1.0.0 (2024-01-20)
- Initial release
- Image drag & drop and file selection
- Chinese and English recognition
- Modern interface design
- Copy result feature
- Progress display

## Contributing

1. Fork the repository
2. Create your feature branch `git checkout -b feature/your-feature`
3. Commit your changes `git commit -am 'Add some feature'`
4. Push to the branch `git push origin feature/your-feature`
5. Create a Pull Request

## Contact

For issues or suggestions, please contact through:

- GitHub Issues: [Submit Issue](https://github.com/pwh-pwh/ImageTextify/issues)
- GitHub Discussions: [Join Discussion](https://github.com/pwh-pwh/ImageTextify/discussions)

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=pwh-pwh/ImageTextify&type=Date)](https://star-history.com/#pwh-pwh/ImageTextify&Date)