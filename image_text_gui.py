import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog, messagebox, Menu
import pytesseract
from PIL import Image, ImageTk
import os
import sys
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
import webbrowser

# 设置Tesseract路径
# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageTextExtractor(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # 应用ttkbootstrap主题
        self.style = ttk.Style(theme="litera")  # 使用litera主题，类似苹果风格
        
        self.title("ImageTextify")
        self.geometry("650x580")
        self.minsize(600, 500)
        self.configure(bg='#ffffff')

        # 创建菜单栏
        self.create_menu()
        
        # 创建主容器
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES, padx=15, pady=15)
        
        self.create_widgets()
        self.setup_drop_target()

    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        # 文件菜单
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="选择图片", command=self.select_image)
        file_menu.add_command(label="保存结果", command=self.save_result)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit)

        # 工具菜单
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="检查Tesseract配置", command=self.check_tesseract)
        tools_menu.add_command(label="清空结果", command=self.clear_result)
        
        # 主题菜单
        theme_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="主题", menu=theme_menu)
        
        # 添加亮色主题
        light_theme_menu = Menu(theme_menu, tearoff=0)
        theme_menu.add_cascade(label="亮色主题", menu=light_theme_menu)
        light_themes = ['litera', 'cosmo', 'flatly', 'journal', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti']
        for theme in light_themes:
            light_theme_menu.add_command(label=theme, command=lambda t=theme: self.change_theme(t))
        
        # 添加暗色主题
        dark_theme_menu = Menu(theme_menu, tearoff=0)
        theme_menu.add_cascade(label="暗色主题", menu=dark_theme_menu)
        dark_themes = ['darkly', 'cyborg', 'vapor', 'solar']
        for theme in dark_themes:
            dark_theme_menu.add_command(label=theme, command=lambda t=theme: self.change_theme(t))

        # 帮助菜单
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="检查更新", command=self.check_update)
        help_menu.add_separator()
        help_menu.add_command(label="关于", command=self.show_about)

    def create_widgets(self):
        # 上传区域框架
        upload_frame = ttk.Frame(self.container)
        upload_frame.pack(fill=BOTH, expand=YES, pady=(0, 15))

        # 预览区域
        preview_frame = ttk.Labelframe(
            upload_frame,
            text="拖放图片到这里",
            padding=15,
            bootstyle="default"
        )
        preview_frame.pack(fill=BOTH, expand=YES)

        # 预览标签
        self.preview_label = ttk.Label(
            preview_frame,
            text="点击<选择图片>或直接拖放图片到此处",
            font=("SF Pro Display", 11),
            bootstyle="default",
            anchor=CENTER
        )
        self.preview_label.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        # 按钮区域
        button_frame = ttk.Frame(self.container)
        button_frame.pack(fill=X, pady=(0, 15))

        # 按钮容器（居中对齐）
        buttons_container = ttk.Frame(button_frame)
        buttons_container.pack(anchor=CENTER)

        # 选择图片按钮
        self.select_btn = ttk.Button(
            buttons_container,
            text="选择图片",
            command=self.select_image,
            bootstyle="primary",
            width=10
        )
        self.select_btn.pack(side=LEFT, padx=5)

        # 提取文字按钮
        self.extract_btn = ttk.Button(
            buttons_container,
            text="提取文字",
            command=self.extract_text,
            bootstyle="default",
            width=10
        )
        self.extract_btn.pack(side=LEFT, padx=5)

        # 复制结果按钮
        self.copy_btn = ttk.Button(
            buttons_container,
            text="复制结果",
            command=self.copy_result,
            bootstyle="default",
            width=10
        )
        self.copy_btn.pack(side=LEFT, padx=5)

        # 结果显示区域
        result_frame = ttk.Labelframe(
            self.container,
            text="识别结果",
            padding=15,
            bootstyle="default"
        )
        result_frame.pack(fill=BOTH, expand=YES)

        # 文本显示区域
        self.result_text = ScrolledText(
            result_frame,
            padding=10,
            height=8,
            font=("SF Pro Display", 10),
            autohide=True,
            bootstyle="default"
        )
        self.result_text.pack(fill=BOTH, expand=YES)

        # 状态栏
        self.status_frame = ttk.Frame(self.container)
        self.status_frame.pack(fill=X, pady=(15, 0))
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="就绪",
            font=("SF Pro Display", 9),
            bootstyle="default"
        )
        self.status_label.pack(side=LEFT)

        # 进度条
        self.progress = ttk.Progressbar(
            self.status_frame,
            bootstyle="primary-striped",
            mode="determinate",
            length=120
        )
        self.progress.pack(side=RIGHT)

        self.current_image = None

    def setup_drop_target(self):
        self.preview_label.drop_target_register(DND_FILES)
        self.preview_label.dnd_bind('<<Drop>>', self.handle_drop)

    def handle_drop(self, event):
        file_path = event.data
        file_path = file_path.strip('{}')
        self.load_image(file_path)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        try:
            image = Image.open(file_path)
            if image.mode not in ['RGB', 'L']:
                image = image.convert('RGB')
            self.current_image = image
            self.update_preview(image)
            self.status_label.configure(text=f"已加载: {os.path.basename(file_path)}")
            
            # 重置进度条
            self.progress.configure(value=0)
        except Exception as e:
            self.show_error("加载失败", str(e))

    def update_preview(self, image):
        try:
            # 调整图片大小以适应预览区域
            preview_width = 280
            preview_height = 180
            preview_image = image.copy()
            
            # 计算缩放比例
            ratio = min(preview_width/image.width, preview_height/image.height)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            
            preview_image = preview_image.resize(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(preview_image)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            self.show_error("预览失败", str(e))
            self.preview_label.configure(image="", text="预览失败")

    def extract_text(self):
        if not self.current_image:
            self.show_error("提示", "请先选择图片")
            return

        def extract():
            self.status_label.configure(text="正在识别...")
            self.extract_btn.configure(state='disabled')
            self.progress.configure(value=0)
            
            try:
                # 模拟进度
                self.progress.start(10)
                
                text = pytesseract.image_to_string(self.current_image, lang='chi_sim+eng')
                self.result_text.delete(1.0, END)
                self.result_text.insert(END, text)
                
                self.progress.stop()
                self.progress.configure(value=100)
                self.status_label.configure(text="识别完成")
                
                # 如果提取的文字为空，显示提示
                if not text.strip():
                    self.show_warning("提示", "未能识别到文字，请确保图片清晰且包含文字内容")
                
            except Exception as e:
                self.show_error("识别失败", str(e))
                self.status_label.configure(text="识别失败")
                self.progress.stop()
                self.progress.configure(value=0)
            finally:
                self.extract_btn.configure(state='normal')

        threading.Thread(target=extract, daemon=True).start()

    def copy_result(self):
        text = self.result_text.get(1.0, END).strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_label.configure(text="已复制到剪贴板")
            messagebox.showinfo("成功", "文字已复制到剪贴板", parent=self)
        else:
            self.show_error("提示", "没有可复制的文字")

    def save_result(self):
        text = self.result_text.get(1.0, END).strip()
        if not text:
            self.show_error("提示", "没有可保存的文字")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("成功", "文件保存成功", parent=self)
            except Exception as e:
                self.show_error("保存失败", str(e))

    def clear_result(self):
        self.result_text.delete(1.0, END)
        self.status_label.configure(text="已清空结果")

    def change_theme(self, theme_name):
        try:
            self.style.theme_use(theme_name)
            messagebox.showinfo("成功", f"主题已切换为: {theme_name}", parent=self)
        except Exception as e:
            self.show_error("主题切换失败", str(e))

    def check_tesseract(self):
        try:
            version = pytesseract.get_tesseract_version()
            languages = pytesseract.get_languages()
            info = f"Tesseract 版本: {version}\n"
            info += f"支持的语言: {', '.join(languages)}\n"
            info += f"Tesseract 路径: {pytesseract.pytesseract.tesseract_cmd}"
            messagebox.showinfo("Tesseract 配置信息", info, parent=self)
        except Exception as e:
            self.show_error("Tesseract 检查失败", 
                          f"错误信息: {str(e)}\n\n"
                          f"请检查：\n"
                          f"1. Tesseract 是否正确安装\n"
                          f"2. 环境变量是否正确设置\n"
                          f"3. 代码中的路径配置是否正确")

    def show_help(self):
        help_text = """使用说明：

1. 添加图片
   - 直接拖放图片到窗口
   - 或点击"选择图片"按钮
   - 或使用菜单"文件->选择图片"

2. 提取文字
   - 点击"提取文字"按钮开始识别
   - 等待识别完成

3. 处理结果
   - 点击"复制结果"复制到剪贴板
   - 使用菜单"文件->保存结果"保存到文件

4. 其他功能
   - 主题切换：在"主题"菜单中选择
   - Tesseract检查：在"工具"菜单中
   - 清空结果：在"工具"菜单中"""
        
        messagebox.showinfo("使用说明", help_text, parent=self)

    def check_update(self):
        webbrowser.open("https://github.com/pwh-pwh/ImageTextify/releases")

    def show_about(self):
        about_text = """ImageTextify v1.0.0

一个简洁优雅的图片文字识别工具，支持中英文识别，
具有现代化的苹果风格界面设计。

项目地址：https://github.com/pwh-pwh/ImageTextify

特点：
• 支持拖放图片
• 中英文识别
• 现代化界面
• 多种主题
• 实时进度显示

作者：pwh-pwh
许可证：MIT License"""
        
        about_dialog = ttk.Toplevel(self)
        about_dialog.title("关于 ImageTextify")
        about_dialog.geometry("400x450")
        about_dialog.resizable(False, False)
        
        # 创建内容框架
        content_frame = ttk.Frame(about_dialog, padding=20)
        content_frame.pack(fill=BOTH, expand=YES)
        
        # 显示图标（如果存在）
        if os.path.exists("icon.png"):
            try:
                icon = Image.open("icon.png")
                icon = icon.resize((64, 64), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon)
                icon_label = ttk.Label(content_frame, image=icon_photo)
                icon_label.image = icon_photo
                icon_label.pack(pady=(0, 10))
            except Exception:
                pass
        
        # 添加文本内容
        text_widget = ScrolledText(
            content_frame,
            wrap=WORD,
            height=15,
            font=("SF Pro Display", 10),
            padding=10
        )
        text_widget.pack(fill=BOTH, expand=YES)
        text_widget.insert(END, about_text)
        text_widget.configure(state=DISABLED)
        
        # 添加GitHub链接按钮
        def open_github():
            webbrowser.open("https://github.com/pwh-pwh/ImageTextify")
        
        github_btn = ttk.Button(
            content_frame,
            text="访问 GitHub",
            command=open_github,
            style="primary.TButton",
            width=20
        )
        github_btn.pack(pady=(10, 0))

    def show_error(self, title, message):
        messagebox.showerror(title=title, message=message, parent=self)
        
    def show_warning(self, title, message):
        messagebox.showwarning(title=title, message=message, parent=self)

if __name__ == "__main__":
    app = ImageTextExtractor()
    # 设置窗口图标
    if os.path.exists("icon.png"):
        app.iconphoto(True, ImageTk.PhotoImage(file="icon.png"))
    app.mainloop()