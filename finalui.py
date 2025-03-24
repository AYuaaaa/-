import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import pygame
import io
from know import extract_keywords
from search import search_poetry

class FlyingFlowersGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("飞花令游戏")
        self.geometry("1024x768")
        self.resizable(False, False)

        # 初始化背景音乐
        pygame.mixer.init()
        self.bg_music = None
        self.is_music_playing = False  # 添加音乐播放状态标志

        # 加载外部字体
        self.custom_font = tkfont.Font(family="custom_font", size=12)  # 字体名称和大小
        self.load_custom_font("宋体.ttf")  # 替换为你的字体文件路径

        # 创建界面容器
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 存储所有界面
        self.frames = {}
        for F in (MainMenu, GameInterface):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 显示主菜单界面
        self.show_frame("MainMenu")
        
    def load_custom_font(self, font_path):
        """加载外部字体文件"""
        try:
            # 使用 tkfont 加载字体
            self.custom_font = tkfont.Font(family=font_path, size=12)
        except Exception as e:
            print(f"加载字体失败：{e}")
            # 如果加载失败，使用默认字体
            self.custom_font = tkfont.Font(family="Arial", size=12)

    def show_frame(self, page_name):
        """显示指定的界面"""
        frame = self.frames[page_name]
        frame.tkraise()

    def toggle_music(self):
        """切换音乐播放状态"""
        if self.is_music_playing:
            self.stop_background_music()
        else:
            self.play_background_music("bgm.mp3")  # 替换为你的音乐文件路径
        self.is_music_playing = not self.is_music_playing

    def play_background_music(self, music_file):
        """播放背景音乐"""
        if self.bg_music:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # 循环播放

    def stop_background_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()

        # 创建音乐控制按钮
        image = Image.open("music_icon.png")  # 使用本地 PNG 图片
        tk_image = ImageTk.PhotoImage(image)
        music_button = tk.Button(
            self,
            image=tk_image,  # 使用图片
            command=self.toggle_music
        )
        music_button.image = tk_image  # 避免垃圾回收销毁图片
        music_button.place(relx=0.05, rely=0.05, anchor="nw")

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 加载背景图片
        self.bg_image = Image.open("五丸蛋糕.jpg")  # 替换为你的背景图片路径
        self.bg_image = self.bg_image.resize((1024, 768), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 添加开始游戏按钮
        button_font = tkfont.Font(size=14)
        start_button = tk.Button(
            self,
            text="开始游戏",
            font=button_font,
            command=lambda: controller.show_frame("GameInterface"),
        )
        start_button.place(relx=0.8, rely=0.3, anchor="center")




class GameInterface(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 创建一个文本框用于显示对话记录
        self.chat_history = tk.Text(self, width=80, height=20, font=controller.custom_font)
        self.chat_history.place(relx=0.1, rely=0.1, anchor="nw")
        self.chat_history.config(state=tk.DISABLED)  # 禁止用户直接编辑

        # 输入框和提交按钮
        self.input_entry = tk.Entry(self, width=60, font=controller.custom_font)
        self.input_entry.place(relx=0.1, rely=0.8, anchor="nw")

        submit_button = tk.Button(
            self,
            text="提交",
            font=("Arial", 12),
            command=self.submit_question,
        )
        submit_button.place(relx=0.8, rely=0.8, anchor="nw")

    def submit_question(self):
        """处理用户提交的问题"""
        user_input = self.input_entry.get()
        if user_input:
            # 显示用户输入
            self.chat_history.config(state=tk.NORMAL)  # 允许编辑
            self.chat_history.insert(tk.END, f"你：{user_input}\n")
            self.chat_history.config(state=tk.DISABLED)  # 禁止编辑
            self.input_entry.delete(0, tk.END)

            keywords = extract_keywords(user_input)
            results = search_poetry(keywords)
            
            self.chat_history.config(state=tk.NORMAL)
            if results:
                for title, author, content in results:
                    self.chat_history.insert(tk.END, f"{title} - {author}\n{content}\n\n")
            else:
                self.chat_history.insert(tk.END, "未找到相关诗句，请换个关键词试试！\n")
            self.chat_history.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = FlyingFlowersGame()
    app.mainloop()
