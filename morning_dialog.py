#!/usr/bin/env python3
"""
交互对话框 - 用于选择心情和城市

每天定时弹出，让用户选择心情和城市
5分钟无响应则使用默认值

支持三种模式：
1. GUI 模式：弹出 tkinter 对话框
2. 命令行模式：在终端显示选项
3. 自动模式：无交互时自动使用默认值
"""

from typing import Optional, Tuple
import threading
import time
import sys

# 尝试导入 tkinter
try:
    import tkinter as tk
    from tkinter import ttk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


class MorningDialogConfig:
    """配置常量"""
    
    # 可选心情
    MOODS = ["开心", "平静", "兴奋", "忧郁", "思考"]
    
    # 可选城市
    CITIES = [
        "常州", "北京", "上海", "广州", "深圳",
        "杭州", "成都", "西安", "南京", "苏州",
        "重庆", "武汉", "长沙", "天津", "青岛",
        "厦门", "大连", "哈尔滨", "昆明", "三亚",
        "拉萨", "桂林", "丽江", "香港", "澳门", "台北"
    ]
    
    # 默认值
    DEFAULT_MOOD = "开心"
    DEFAULT_CITY = "常州"
    
    # 超时时间（秒）
    TIMEOUT = 300  # 5分钟


class MorningDialogGUI:
    """GUI 对话框（需要 tkinter）"""
    
    def __init__(self):
        self.result: Optional[Tuple[str, str]] = None
        self.window = None
        self.countdown = MorningDialogConfig.TIMEOUT
        self.countdown_label = None
        self.closed = False
        
    def show(self) -> Tuple[str, str]:
        """显示 GUI 对话框"""
        try:
            self.window = tk.Tk()
            self.window.title("🌤️ 早安问候")
            self.window.geometry("400x350")
            self.window.resizable(False, False)
            
            self._center_window()
            self.window.attributes('-topmost', True)
            self._create_widgets()
            
            timer_thread = threading.Thread(target=self._countdown_timer, daemon=True)
            timer_thread.start()
            
            self.window.protocol("WM_DELETE_WINDOW", self._on_close)
            self.window.mainloop()
            
        except Exception as e:
            print(f"⚠️ GUI 对话框显示失败: {e}")
            self.result = (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)
        
        if self.result is None:
            self.result = (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)
        
        return self.result
    
    def _center_window(self):
        self.window.update_idletasks()
        width = 400
        height = 350
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        # 标题
        title_frame = tk.Frame(self.window, bg="#4A90D9", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="☀️ 早安！请选择您今天的心情",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#4A90D9",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # 主内容区
        content_frame = tk.Frame(self.window, padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 心情选择
        mood_label = tk.Label(content_frame, text="😊 今天的心情：", font=("Microsoft YaHei", 12))
        mood_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.mood_var = tk.StringVar(value=MorningDialogConfig.DEFAULT_MOOD)
        
        mood_frame = tk.Frame(content_frame)
        mood_frame.pack(fill=tk.X, pady=(0, 15))
        
        for mood in MorningDialogConfig.MOODS:
            rb = tk.Radiobutton(
                mood_frame,
                text=mood,
                variable=self.mood_var,
                value=mood,
                font=("Microsoft YaHei", 11)
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # 城市选择
        city_label = tk.Label(content_frame, text="📍 所在城市：", font=("Microsoft YaHei", 12))
        city_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.city_var = tk.StringVar(value=MorningDialogConfig.DEFAULT_CITY)
        
        city_combo = ttk.Combobox(
            content_frame,
            textvariable=self.city_var,
            values=MorningDialogConfig.CITIES,
            font=("Microsoft YaHei", 11),
            state="readonly",
            width=30
        )
        city_combo.pack(fill=tk.X, pady=(0, 15))
        
        # 自定义城市
        custom_label = tk.Label(
            content_frame,
            text="或输入其他城市：",
            font=("Microsoft YaHei", 10),
            fg="gray"
        )
        custom_label.pack(anchor=tk.W)
        
        self.custom_city_var = tk.StringVar()
        custom_entry = tk.Entry(
            content_frame,
            textvariable=self.custom_city_var,
            font=("Microsoft YaHei", 11),
            width=30
        )
        custom_entry.pack(fill=tk.X, pady=(5, 15))
        
        # 倒计时
        self.countdown_label = tk.Label(
            content_frame,
            text=f"⏰ {self.countdown // 60}分{self.countdown % 60}秒后自动执行默认设置",
            font=("Microsoft YaHei", 10),
            fg="#FF6B6B"
        )
        self.countdown_label.pack(anchor=tk.W, pady=(5, 10))
        
        # 按钮
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        confirm_btn = tk.Button(
            button_frame,
            text="✅ 确认",
            font=("Microsoft YaHei", 12),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self._on_confirm
        )
        confirm_btn.pack(side=tk.RIGHT, padx=5)
        
        default_btn = tk.Button(
            button_frame,
            text="⚙️ 使用默认",
            font=("Microsoft YaHei", 12),
            bg="#9E9E9E",
            fg="white",
            width=12,
            command=self._on_default
        )
        default_btn.pack(side=tk.RIGHT, padx=5)
    
    def _countdown_timer(self):
        while self.countdown > 0 and not self.closed:
            time.sleep(1)
            self.countdown -= 1
            
            if not self.closed and self.countdown_label:
                try:
                    mins = self.countdown // 60
                    secs = self.countdown % 60
                    self.window.after(0, self._update_countdown, mins, secs)
                except:
                    pass
            
            if self.countdown <= 0 and not self.closed:
                self.window.after(0, self._on_timeout)
                break
    
    def _update_countdown(self, mins: int, secs: int):
        if self.countdown_label and not self.closed:
            self.countdown_label.config(text=f"⏰ {mins}分{secs}秒后自动执行默认设置")
    
    def _on_confirm(self):
        mood = self.mood_var.get()
        custom_city = self.custom_city_var.get().strip()
        city = custom_city if custom_city else self.city_var.get()
        self.result = (mood, city)
        self._close_window()
    
    def _on_default(self):
        self.result = (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)
        self._close_window()
    
    def _on_timeout(self):
        print("⏰ 5分钟无响应，使用默认设置")
        self.result = (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)
        self._close_window()
    
    def _on_close(self):
        if self.result is None:
            self.result = (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)
        self._close_window()
    
    def _close_window(self):
        self.closed = True
        if self.window:
            try:
                self.window.destroy()
            except:
                pass


class MorningDialogCLI:
    """命令行对话框"""
    
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self.result: Optional[Tuple[str, str]] = None
        
    def show(self) -> Tuple[str, str]:
        """显示命令行对话框"""
        print("\n" + "=" * 60)
        print("☀️ 早安！请选择您今天的心情")
        print("=" * 60)
        
        # 显示心情选项
        print("\n😊 今天的心情：")
        for i, mood in enumerate(MorningDialogConfig.MOODS, 1):
            print(f"  {i}. {mood}")
        
        # 心情选择
        print(f"\n⏰ {self.timeout}秒后自动使用默认设置")
        
        try:
            mood_input = input(f"心情 [默认: 1-{MorningDialogConfig.DEFAULT_MOOD}]: ").strip()
        except EOFError:
            print("\n⚠️ 无法读取输入，使用默认设置")
            return (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)
        
        if mood_input == "":
            mood = MorningDialogConfig.DEFAULT_MOOD
        else:
            try:
                idx = int(mood_input) - 1
                mood = MorningDialogConfig.MOODS[idx] if 0 <= idx < len(MorningDialogConfig.MOODS) else MorningDialogConfig.DEFAULT_MOOD
            except:
                mood = MorningDialogConfig.DEFAULT_MOOD
        
        # 显示城市选项
        print(f"\n📍 所在城市：")
        for i, city in enumerate(MorningDialogConfig.CITIES[:10], 1):
            print(f"  {i}. {city}")
        print(f"  ... 或直接输入城市名")
        
        try:
            city_input = input(f"城市 [默认: {MorningDialogConfig.DEFAULT_CITY}]: ").strip()
        except EOFError:
            print("\n⚠️ 无法读取输入，使用默认设置")
            return (mood, MorningDialogConfig.DEFAULT_CITY)
        
        if city_input == "":
            city = MorningDialogConfig.DEFAULT_CITY
        else:
            try:
                idx = int(city_input) - 1
                city = MorningDialogConfig.CITIES[idx] if 0 <= idx < len(MorningDialogConfig.CITIES) else city_input
            except:
                city = city_input
        
        print(f"\n✅ 您的选择:")
        print(f"   心情: {mood}")
        print(f"   城市: {city}")
        
        return (mood, city)


def is_interactive_terminal() -> bool:
    """检测是否在交互式终端中运行"""
    # 检查 stdin 是否是 TTY
    if sys.stdin.isatty():
        return True
    
    # 检查是否有终端
    try:
        import os
        if os.isatty(0):
            return True
    except:
        pass
    
    return False


def show_morning_dialog(force_interactive: bool = False) -> Tuple[str, str]:
    """
    显示早晨问候对话框
    
    自动检测环境：
    - 有 GUI 环境时显示 tkinter 对话框
    - 无 GUI 但有交互终端时使用命令行交互
    - 无交互环境时自动使用默认值
    
    Args:
        force_interactive: 强制使用交互模式（即使无终端）
    
    Returns:
        Tuple[str, str]: (心情, 城市)
    """
    # 1. 首先检测是否有 GUI 显示环境
    display_available = False
    
    if HAS_TKINTER:
        try:
            test_root = tk.Tk()
            test_root.withdraw()
            test_root.update()
            test_root.destroy()
            display_available = True
        except:
            display_available = False
    
    if display_available and HAS_TKINTER:
        # 有 GUI 环境
        print("🖥️ 检测到 GUI 环境，弹出对话框...")
        dialog = MorningDialogGUI()
        return dialog.show()
    
    # 2. 检测是否有交互终端
    if is_interactive_terminal() or force_interactive:
        # 有交互终端
        print("💻 使用命令行交互...")
        dialog = MorningDialogCLI(timeout=MorningDialogConfig.TIMEOUT)
        return dialog.show()
    
    # 3. 无交互环境，自动使用默认值
    print("🤖 无交互环境，自动使用默认设置...")
    print(f"   心情: {MorningDialogConfig.DEFAULT_MOOD}")
    print(f"   城市: {MorningDialogConfig.DEFAULT_CITY}")
    return (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)


def show_morning_dialog_auto() -> Tuple[str, str]:
    """自动模式：直接返回默认值"""
    print("🤖 自动模式: 使用默认设置")
    print(f"   心情: {MorningDialogConfig.DEFAULT_MOOD}")
    print(f"   城市: {MorningDialogConfig.DEFAULT_CITY}")
    return (MorningDialogConfig.DEFAULT_MOOD, MorningDialogConfig.DEFAULT_CITY)


# 测试
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true", help="自动模式")
    args = parser.parse_args()
    
    if args.auto:
        mood, city = show_morning_dialog_auto()
    else:
        mood, city = show_morning_dialog()
    
    print(f"\n最终结果: 心情={mood}, 城市={city}")
