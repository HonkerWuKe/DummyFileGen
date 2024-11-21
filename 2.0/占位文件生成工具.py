import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import argparse

class PlaceholderFileGenerator:
    def __init__(self):
        # 首先创建主窗口
        self.window = tk.Tk()
        self.window.title("DummyFileGen")
        self.window.geometry("800x600")

        # 然后初始化变量
        self.current_language = tk.StringVar(value="中文")
        self.path_var = tk.StringVar()
        self.filename_var = tk.StringVar()
        self.size_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="MB")
        self.content_type = tk.StringVar(value="zeros")
        self.batch_mode = tk.BooleanVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
        self.custom_content = tk.StringVar()  # 自定义内容
        self.batch_count = tk.StringVar(value="10")  # 批量生成数量
        self.test_mode = tk.BooleanVar()  # 测试模式开关
        self.custom_test_size = tk.StringVar(value="1")  # 自定义测试大小
        self.custom_test_unit = tk.StringVar(value="GB")  # 自定义测试单位

        # 完善语言字典，确保所有文本都有对应翻译
        self.languages = {
            "中文": {
                "title": "占位文件生成工具",
                "save_location": "保存位置:",
                "filename": "文件名:",
                "file_size": "文件大小:",
                "generate": "生成文件",
                "ready": "就绪",
                "batch_mode": "批量生成",
                "content_type": "文件内容:",
                "browse": "浏览",
                "complete": "完成",
                "file_generated": "文件生成完成！",
                "error": "错误",
                "select_save_location": "请选择保存位置",
                "enter_filename": "请输入文件名",
                "enter_file_size": "请输入文件大小",
                "all_zeros": "全零",
                "random_data": "随机数据",
                "custom_data": "自定义",
                "language": "语言:",
                "basic_settings": "基本设置",
                "file_settings": "文件设置",
                "test_mode": "U盘测试模式",
                "test_mode_tip": "用于测试U盘真实容量",
                "test_pattern": "测试方案:",
                "pattern_full": "完整测试",
                "pattern_quick": "快速测试",
                "pattern_custom": "自定义测试",
                "custom_test_size": "自定义测试大小:",
                "test_file_types": "测试文件类型:",
                "documents": "文档",
                "images": "图片",
                "videos": "视频",
                "system": "系统文件",
                "test_status": "测试状态:",
                "testing": "测试中...",
                "test_complete": "测试完成",
                "verify_files": "验证文件",
                "batch_count": "生成数量:",
                "custom_content": "自定义内容:",
                "start_test": "开始测试",
                "stop_test": "停止测试"
            },
            "English": {
                "title": "DummyFileGen",
                "save_location": "Save Location:",
                "filename": "Filename:",
                "file_size": "File Size:",
                "generate": "Generate",
                "ready": "Ready",
                "batch_mode": "Batch Mode",
                "content_type": "Content Type:",
                "browse": "Browse",
                "complete": "Complete",
                "file_generated": "File generation completed!",
                "error": "Error",
                "select_save_location": "Please select save location",
                "enter_filename": "Please enter filename",
                "enter_file_size": "Please enter file size",
                "all_zeros": "All Zeros",
                "random_data": "Random Data",
                "custom_data": "Custom Data",
                "language": "Language:",
                "basic_settings": "Basic Settings",
                "file_settings": "File Settings",
                "test_mode": "USB Drive Test Mode",
                "test_mode_tip": "Test real capacity of USB drive",
                "test_pattern": "Test Pattern:",
                "pattern_full": "Full Test",
                "pattern_quick": "Quick Test",
                "pattern_custom": "Custom Test",
                "custom_test_size": "Custom Test Size:",
                "test_file_types": "Test File Types:",
                "documents": "Documents",
                "images": "Images",
                "videos": "Videos",
                "system": "System Files",
                "test_status": "Test Status:",
                "testing": "Testing...",
                "test_complete": "Test Complete",
                "verify_files": "Verify Files",
                "batch_count": "Count:",
                "custom_content": "Custom Content:",
                "start_test": "Start Test",
                "stop_test": "Stop Test"
            }
        }
        
        # 创建主框架和其他UI元素
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== 顶部区域 =====
        top_frame = ttk.LabelFrame(self.main_frame, text=self.languages[self.current_language.get()]["basic_settings"], padding="10")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 语言选择和生成按钮（放在同一行）
        lang_frame = ttk.Frame(top_frame)
        lang_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        # 左侧放语言选择
        lang_left = ttk.Frame(lang_frame)
        lang_left.pack(side=tk.LEFT)
        ttk.Label(lang_left, text=self.languages[self.current_language.get()]["language"]).pack(side=tk.LEFT)
        language_combo = ttk.Combobox(lang_left, textvariable=self.current_language, 
                                    values=list(self.languages.keys()), width=10)
        language_combo.pack(side=tk.LEFT, padx=5)
        language_combo.bind('<<ComboboxSelected>>', self.update_language)
        
        # 右侧放生成按钮和进度条
        btn_right = ttk.Frame(lang_frame)
        btn_right.pack(side=tk.RIGHT)
        self.progress = ttk.Progressbar(btn_right, length=200, mode='determinate', 
                                      variable=self.progress_var)
        self.progress.pack(side=tk.LEFT, padx=(0, 10))
        self.generate_btn = ttk.Button(btn_right, text=self.languages[self.current_language.get()]["generate"], 
                                     command=self.start_generation)
        self.generate_btn.pack(side=tk.LEFT)
        
        # 保存位置
        path_frame = ttk.Frame(top_frame)
        path_frame.pack(fill=tk.X, pady=5)
        ttk.Label(path_frame, text=self.languages[self.current_language.get()]["save_location"]).pack(side=tk.LEFT)
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(path_frame, text=self.languages[self.current_language.get()]["browse"], 
                  command=self.browse_path).pack(side=tk.LEFT)
        
        # 文件名
        name_frame = ttk.Frame(top_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text=self.languages[self.current_language.get()]["filename"]).pack(side=tk.LEFT)
        self.filename_entry = ttk.Entry(name_frame, textvariable=self.filename_var)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # ===== 中部区域 =====
        middle_frame = ttk.LabelFrame(self.main_frame, text=self.languages[self.current_language.get()]["file_settings"], padding="10")
        middle_frame.pack(fill=tk.X, pady=10)
        
        # 文件大小设置
        size_frame = ttk.Frame(middle_frame)
        size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(size_frame, text=self.languages[self.current_language.get()]["file_size"]).pack(side=tk.LEFT)
        self.size_entry = ttk.Entry(size_frame, textvariable=self.size_var, width=15)
        self.size_entry.pack(side=tk.LEFT, padx=5)
        
        # 单位选择
        unit_combo = ttk.Combobox(size_frame, textvariable=self.unit_var, 
                                 values=["KB", "MB", "GB"], width=5)
        unit_combo.pack(side=tk.LEFT)
        
        # 文件内容选择
        content_frame = ttk.Frame(middle_frame)
        content_frame.pack(fill=tk.X, pady=10)
        ttk.Label(content_frame, text=self.languages[self.current_language.get()]["content_type"]).pack(side=tk.LEFT)
        
        # 内容类型选择
        content_types_frame = ttk.Frame(content_frame)
        content_types_frame.pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(content_types_frame, text=self.languages[self.current_language.get()]["all_zeros"], 
                       value="zeros", variable=self.content_type, 
                       command=self.toggle_custom_content).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(content_types_frame, text=self.languages[self.current_language.get()]["random_data"], 
                       value="random", variable=self.content_type,
                       command=self.toggle_custom_content).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(content_types_frame, text=self.languages[self.current_language.get()]["custom_data"], 
                       value="custom", variable=self.content_type,
                       command=self.toggle_custom_content).pack(side=tk.LEFT, padx=5)
        
        # 自定义内容输入框
        self.custom_frame = ttk.Frame(middle_frame)
        self.custom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.custom_frame, text=self.languages[self.current_language.get()]["custom_content"]).pack(side=tk.LEFT)
        self.custom_entry = ttk.Entry(self.custom_frame, textvariable=self.custom_content)
        self.custom_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.custom_frame.pack_forget()  # 初始隐藏
        
        # 批量生成选项
        batch_frame = ttk.Frame(middle_frame)
        batch_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(batch_frame, text=self.languages[self.current_language.get()]["batch_mode"], 
                       variable=self.batch_mode, command=self.toggle_batch_count).pack(side=tk.LEFT)
        
        # 批量生成数量
        self.batch_count_frame = ttk.Frame(batch_frame)
        self.batch_count_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(self.batch_count_frame, text=self.languages[self.current_language.get()]["batch_count"]).pack(side=tk.LEFT)
        self.batch_count_entry = ttk.Entry(self.batch_count_frame, textvariable=self.batch_count, width=5)
        self.batch_count_entry.pack(side=tk.LEFT, padx=5)
        self.batch_count_frame.pack_forget()  # 初始隐藏
        
        # 添加测试模式选项
        test_frame = ttk.LabelFrame(self.main_frame, text=self.languages[self.current_language.get()]["test_mode"])
        test_frame.pack(fill=tk.X, pady=10)
        
        ttk.Checkbutton(test_frame, text=self.languages[self.current_language.get()]["test_mode_tip"],
                       variable=self.test_mode, command=self.toggle_test_mode).pack(side=tk.TOP, pady=5)
        
        # 测试模式的控件（初始隐藏）
        self.test_controls_frame = ttk.Frame(test_frame)
        self.test_controls_frame.pack(fill=tk.X, pady=5)
        
        # 测试方案选择
        pattern_frame = ttk.Frame(self.test_controls_frame)
        pattern_frame.pack(fill=tk.X, pady=5)
        ttk.Label(pattern_frame, text=self.languages[self.current_language.get()]["test_pattern"]).pack(side=tk.LEFT)
        self.test_pattern = tk.StringVar(value="quick")
        ttk.Radiobutton(pattern_frame, text=self.languages[self.current_language.get()]["pattern_quick"],
                       value="quick", variable=self.test_pattern,
                       command=self.toggle_custom_test).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(pattern_frame, text=self.languages[self.current_language.get()]["pattern_full"],
                       value="full", variable=self.test_pattern,
                       command=self.toggle_custom_test).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(pattern_frame, text=self.languages[self.current_language.get()]["pattern_custom"],
                       value="custom", variable=self.test_pattern,
                       command=self.toggle_custom_test).pack(side=tk.LEFT, padx=10)
        
        # 自定义测试设置框架
        self.custom_test_frame = ttk.Frame(self.test_controls_frame)
        self.custom_test_frame.pack(fill=tk.X, pady=5)
        
        # 自定义测试大小设置
        size_frame = ttk.Frame(self.custom_test_frame)
        size_frame.pack(fill=tk.X, pady=5)
        ttk.Label(size_frame, text=self.languages[self.current_language.get()]["custom_test_size"]).pack(side=tk.LEFT)
        ttk.Entry(size_frame, textvariable=self.custom_test_size, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Combobox(size_frame, textvariable=self.custom_test_unit,
                    values=["MB", "GB"], width=5).pack(side=tk.LEFT)
        
        # 文件类型选择
        types_frame = ttk.Frame(self.custom_test_frame)
        types_frame.pack(fill=tk.X, pady=5)
        ttk.Label(types_frame, text=self.languages[self.current_language.get()]["test_file_types"]).pack(side=tk.LEFT)
        
        # 创建文件类型选择框
        self.file_types = {
            "documents": tk.BooleanVar(value=True),
            "images": tk.BooleanVar(value=True),
            "videos": tk.BooleanVar(value=True),
            "system": tk.BooleanVar(value=True)
        }
        
        for file_type, var in self.file_types.items():
            ttk.Checkbutton(types_frame, text=file_type.title(),
                          variable=var).pack(side=tk.LEFT, padx=5)
        
        # 初始隐藏自定义测试设置
        self.custom_test_frame.pack_forget()
        
        self.test_controls_frame.pack_forget()  # 初始隐藏测试控件
    
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
    
    def calculate_size_bytes(self):
        try:
            size = float(self.size_var.get())
            unit = self.unit_var.get()
            multiplier = {
                "KB": 1024,
                "MB": 1024 * 1024,
                "GB": 1024 * 1024 * 1024
            }
            return int(size * multiplier[unit])
        except ValueError:
            raise ValueError("请输入有效的数字大小")
    
    def generate_file(self):
        try:
            base_filepath = os.path.join(self.path_var.get(), self.filename_var.get())
            size_bytes = self.calculate_size_bytes()
            
            # 处理批量生成
            file_count = 1
            if self.batch_mode.get():
                try:
                    file_count = int(self.batch_count.get())
                    if file_count < 1:
                        raise ValueError("生成数量必须大于0")
                except ValueError as e:
                    messagebox.showerror("错误", str(e))
                    return
            
            for i in range(file_count):
                if file_count > 1:
                    filepath = f"{base_filepath}_{i+1}"
                else:
                    filepath = base_filepath
                
                self.generate_single_file(filepath, size_bytes)
                
                # 更新进度
                progress = ((i + 1) / file_count) * 100
                self.progress_var.set(progress)
                self.window.update_idletasks()
            
            self.status_var.set("文件生成完成！")
            messagebox.showinfo("完成", "文件生成完成！")
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
        finally:
            self.generate_btn.state(['!disabled'])
            self.progress_var.set(0)
    
    def generate_single_file(self, filepath, size_bytes):
        with open(filepath, 'wb') as f:
            block_size = 1024 * 1024  # 1MB块
            written = 0
            while written < size_bytes:
                remaining = size_bytes - written
                to_write = min(block_size, remaining)
                
                # 根据选择的内容类型生成数据
                if self.content_type.get() == "zeros":
                    data = b'\0' * to_write
                elif self.content_type.get() == "random":
                    data = os.urandom(to_write)
                else:  # custom
                    custom_content = self.custom_content.get().encode('utf-8')
                    if not custom_content:
                        custom_content = b'1'  # 默认值
                    # 重复自定义内容以填充所需大小
                    data = (custom_content * (to_write // len(custom_content) + 1))[:to_write]
                
                f.write(data)
                written += to_write
    
    def start_generation(self):
        lang = self.current_language.get()
        translations = self.languages[lang]
        
        # 验证输入
        if not self.path_var.get():
            messagebox.showerror(translations["error"], translations["select_save_location"])
            return
        if not self.filename_var.get():
            messagebox.showerror(translations["error"], translations["enter_filename"])
            return
        if not self.size_var.get():
            messagebox.showerror(translations["error"], translations["enter_file_size"])
            return
            
        # 在新线程中生成文件
        thread = threading.Thread(target=self.generate_file)
        thread.start()
    
    def run(self):
        self.window.mainloop()
    
    def update_language(self, event=None):
        """更新界面语言"""
        lang = self.current_language.get()
        translations = self.languages[lang]
        
        # 更新窗口标题
        self.window.title(translations["title"])
        
        def update_widget_texts(widget):
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Checkbutton, ttk.Radiobutton)):
                try:
                    current_text = widget.cget("text")
                    # 查找当前文本对应的键
                    for key, value in self.languages["中文"].items():
                        if current_text == value:
                            widget.configure(text=translations[key])
                            break
                        # 检查英文文本
                        elif current_text == self.languages["English"].get(key, ""):
                            widget.configure(text=translations[key])
                            break
                except:
                    pass
            
            elif isinstance(widget, ttk.LabelFrame):
                try:
                    current_text = widget.cget("text")
                    for key, value in self.languages["中文"].items():
                        if current_text == value:
                            widget.configure(text=translations[key])
                            break
                        elif current_text == self.languages["English"].get(key, ""):
                            widget.configure(text=translations[key])
                            break
                except:
                    pass
            
            # 递归更新所有子控件
            for child in widget.winfo_children():
                update_widget_texts(child)
        
        # 从主框架开始更新所有控件
        update_widget_texts(self.main_frame)
        
        # 更新状态文本
        current_status = self.status_var.get()
        for key in ["ready", "testing", "test_complete", "file_generated"]:
            if current_status in [self.languages["中文"][key], self.languages["English"][key]]:
                self.status_var.set(translations[key])
                break
    
    def toggle_custom_content(self):
        """切换自定义内容输入框的显示状态"""
        if self.content_type.get() == "custom":
            self.custom_frame.pack(fill=tk.X, pady=5)
        else:
            self.custom_frame.pack_forget()
    
    def toggle_batch_count(self):
        """切换批量生成数量输入框的显示状态"""
        if self.batch_mode.get():
            self.batch_count_frame.pack(side=tk.LEFT, padx=10)
        else:
            self.batch_count_frame.pack_forget()
    
    def toggle_test_mode(self):
        """切换测试模式"""
        if self.test_mode.get():
            self.test_controls_frame.pack(fill=tk.X, pady=5)
            # 预设测试文件格式
            self.content_type.set("random")  # 使用随机数据
            self.test_files = [
                # 快速测试方案
                {"size": "100", "unit": "MB", "ext": ".bin", "count": 10},
                {"size": "500", "unit": "MB", "ext": ".dat", "count": 4},
                {"size": "1", "unit": "GB", "ext": ".img", "count": 2},
                
                # 完整测试方案（在quick基础上添加）
                {"size": "2", "unit": "GB", "ext": ".iso", "count": 2},
                {"size": "4", "unit": "GB", "ext": ".img", "count": 1},
                
                # 各种格式文件测试
                {"size": "100", "unit": "MB", "ext": ".mp4", "count": 5},
                {"size": "50", "unit": "MB", "ext": ".jpg", "count": 10},
                {"size": "200", "unit": "MB", "ext": ".zip", "count": 5},
            ]
        else:
            self.test_controls_frame.pack_forget()
    
    def toggle_custom_test(self):
        """切换自定义测试设置的显示状态"""
        if self.test_pattern.get() == "custom":
            self.custom_test_frame.pack(fill=tk.X, pady=5)
        else:
            self.custom_test_frame.pack_forget()
    
    def get_test_files(self):
        """根据测试���式获取要生成的文件列表"""
        pattern = self.test_pattern.get()
        
        if pattern == "custom":
            # 自定义测试模式
            test_files = []
            size = float(self.custom_test_size.get())
            unit = self.custom_test_unit.get()
            
            if self.file_types["documents"].get():
                test_files.extend([
                    {"size": "10", "unit": "MB", "ext": ".doc", "count": 5},
                    {"size": "20", "unit": "MB", "ext": ".pdf", "count": 5}
                ])
            
            if self.file_types["images"].get():
                test_files.extend([
                    {"size": "50", "unit": "MB", "ext": ".jpg", "count": 10},
                    {"size": "100", "unit": "MB", "ext": ".png", "count": 5}
                ])
            
            if self.file_types["videos"].get():
                test_files.extend([
                    {"size": str(size/2), "unit": unit, "ext": ".mp4", "count": 2},
                    {"size": str(size/4), "unit": unit, "ext": ".mkv", "count": 4}
                ])
            
            if self.file_types["system"].get():
                test_files.extend([
                    {"size": str(size), "unit": unit, "ext": ".iso", "count": 1},
                    {"size": str(size/2), "unit": unit, "ext": ".img", "count": 2}
                ])
            
            return test_files
        else:
            # 使用预定义的测试文件
            return self.test_files[:3] if pattern == "quick" else self.test_files[:5]
    
    def start_test(self):
        """开始U盘测试"""
        pattern = self.test_pattern.get()
        if pattern == "quick":
            test_files = self.test_files[:3]  # 只使用前3种文件
        elif pattern == "full":
            test_files = self.test_files[:5]  # 使用前5种文件
        else:  # custom
            test_files = self.test_files  # 使用所有测试文件
        
        total_files = sum(f["count"] for f in test_files)
        files_generated = 0
        
        try:
            for test_file in test_files:
                self.size_var.set(test_file["size"])
                self.unit_var.set(test_file["unit"])
                self.file_ext.set(test_file["ext"])
                self.batch_count.set(str(test_file["count"]))
                
                # 生成这组测试文件
                self.generate_file()
                
                files_generated += test_file["count"]
                progress = (files_generated / total_files) * 100
                self.progress_var.set(progress)
                self.window.update_idletasks()
            
            # 测试完成后验证文件
            self.verify_files()
            
        except Exception as e:
            messagebox.showerror(self.languages[self.current_language.get()]["error"], str(e))
    
    def verify_files(self):
        """验证生成的文件"""
        # 这里可以添加文件验证逻辑
        # 例如：检查文件大小、读取内容、验证完整性等
        pass

def cli_mode():
    parser = argparse.ArgumentParser(description='DummyFileGen - Generate placeholder files')
    parser.add_argument('-o', '--output', help='Output directory', required=True)
    parser.add_argument('-n', '--name', help='Filename', required=True)
    parser.add_argument('-s', '--size', help='File size (e.g. 10MB, 1GB)', required=True)
    parser.add_argument('-t', '--type', choices=['zeros', 'random', 'custom'], 
                        default='zeros', help='Content type')
    parser.add_argument('-b', '--batch', type=int, help='Number of files to generate')
    
    args = parser.parse_args()
    
    # 处理命令行模式的文件生成
    generator = PlaceholderFileGenerator()
    generator.generate_from_cli(args)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cli_mode()
    else:
        app = PlaceholderFileGenerator()
        app.run()
