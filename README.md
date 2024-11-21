# 🚀 占位文件生成工具

![Octocat](https://github.com/fluidicon.png)

[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GUI](https://img.shields.io/badge/GUI-tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[简体中文](README.md) | [English](README_EN.md) | [繁體中文](README_TW.md) | [Français](README_FR.md) | [Русский](README_RU.md)

## 🌏 多语言支持 | Multilingual Support

### 🇨🇳 简体中文
这是一个使用Python开发的图形界面工具，用于快速生成指定大小的占位文件。该工具适用于测试存储空间、文件传输或需要特定大小文件的场景。

### 🇺🇸 English
This is a GUI tool developed in Python for quickly generating placeholder files of specified sizes. It is suitable for testing storage space, file transfers, or scenarios requiring files of specific sizes.

### 🇭🇰 繁體中文
這是一個使用Python開發的圖形界面工具，用於快速生成指定大小的占位檔案。該工具適用於測試存儲空間、檔案傳輸或需要特定大小檔案的場景。

## ✨ 核心特性

### 🛠️ 主要功能
- 可视化界面操作
- 支持自定义保存位置
- 自定义文件名称
- 灵活的文件大小设置
- 实时进度显示
- 异步生成机制

### 🎯 技术特点
- Tkinter GUI框架
- 多线程处理
- 分块写入算法
- 内存优化设计
- 异常处理机制
- 跨平台兼容

## 🎮 交互指南

### 1️⃣ 基础操作
1. 启动程序后，你会看到一个简洁的图形界面
2. 点击"浏览"按钮选择文件保存位置
3. 在文件名输入框中输入期望的文件名
4. 选择文件大小和单位（KB/MB/GB）
5. 点击"生成"按钮开始创建文件

### 2️⃣ 快捷键支持
- `Ctrl + B` - 打开文件浏览器
- `Ctrl + G` - 开始生成文件
- `Ctrl + Q` - 退出程序
- `Esc` - 取消当前操作

### 3️⃣ 进度提示
- 🔄 生成中：显示进度条和预计剩余时间
- ✅ 完成：弹出成功提示
- ❌ 错误：显示详细错误信息

### 4️⃣ 常见问题解答
1. **Q: 为什么生成大文件时界面会卡顿？**  
   A: 程序使用异步处理，界面可能短暂未响应，但不影响文件生成。

2. **Q: 如何取消正在进行的生成过程？**  
   A: 点击"取消"按钮或按 `Esc` 键。

3. **Q: 支持同时生成多个文件吗？**  
   A: 目前仅支持单文件生成，多文件支持正在开发中。

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/placeholder-file-generator.git

# 进入目录
cd placeholder-file-generator

# 运行程序
python main.py
```

## 📦 安装要求

- Python 3.x
- 无需额外依赖包

## 💡 使用场景

- 测试存储设备容量
- 模拟大文件传输
- 性能测试
- 文件系统测试

## 🔄 版本更新

### v1.0.0
- ✨ 基础文件生成功能
- 🎯 可视化操作界面
- 🛠️ 进度显示功能

### 开发计划
- [ ] 批量文件生成
- [ ] 自定义文件内容
- [ ] 多语言界面
- [ ] 命令行模式

## 🤝 参与贡献

1. 🍴 Fork 本项目
2. 🔧 创建特性分支
3. 📝 提交更改
4. 🔀 发起 Pull Request

---

如果觉得这个工具对你有帮助，请点个 ⭐️ 支持一下！