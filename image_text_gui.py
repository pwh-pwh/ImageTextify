import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog, messagebox
import pytesseract
from PIL import Image, ImageTk
import os
import sys
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD

# 设置Tesseract路径
# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageTextExtractor(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # 应用ttkbootstrap主题
        self.style = ttk.Style(theme="litera")  # 使用litera主题，类似苹果风格
        
        self.title("图片文字提取器")
        self.geometry("650x580")  # 调整窗口大小
        self.minsize(600, 500)    # 设置最小窗口大小
        self.configure(bg='#ffffff')  # 设置白色背景
        
        # 创建主容器
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES, padx=15, pady=15)
        
        self.create_widgets()
        self.setup_drop_target()

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
            font=("SF Pro Display", 11),  # 使用类似苹果的字体
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
            bootstyle="primary",  # 主要按钮使用实心样式
            width=10
        )
        self.select_btn.pack(side=LEFT, padx=5)

        # 提取文字按钮
        self.extract_btn = ttk.Button(
            buttons_container,
            text="提取文字",
            command=self.extract_text,
            bootstyle="default",  # 次要按钮使用浅色样式
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
            autohide=True,  # 自动隐藏滚动条
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
            preview_width = 280  # 减小预览尺寸
            preview_height = 180
            # 创建图片副本以避免修改原图
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
            
            # 显示成功提示
            messagebox.showinfo(
                title="成功",
                message="文字已复制到剪贴板",
                parent=self
            )
        else:
            self.show_error("提示", "没有可复制的文字")

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