# 🎮 HSR Automation - 崩坏星穹铁道自动化助手

一个基于Python + Kivy + OpenCV的自动化工具，支持桌面和Android平台。

![版本](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.9--3.11-green)
![平台](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android-orange)

## ✨ 功能特性

### 🎯 核心功能

- ✅ **智能登录** - 三阶段持续检测，无时间限制
- ✅ **每日委托** - 自动完成委托任务（可选）
- ✅ **自动挑战** - 120开拓力副本自动挑战
- ✅ **智能战斗** - 自动启用倍速和自动战斗
- ✅ **循环刷本** - 自动"再来一次"直到完成
- ✅ **奖励领取** - 自动领取所有任务奖励
- ✅ **礼物检查** - 智能判断并领取礼物

### 🎨 界面特性

- 📱 现代化UI设计，浅色主题
- ✅ 一键启动/停止
- ⚙️ 可选功能开关（每日委托等）
- 📊 实时日志显示

## 🚀 快速开始

### 桌面版（Windows/Mac/Linux）

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 准备模板图像

将游戏中的按钮/界面截图放入 `templates/` 目录（已包含示例模板）。

#### 3. 运行程序

```bash
python main.py
```

#### 4. 使用流程

1. 打开崩坏星穹铁道游戏
2. 在程序中配置选项（勾选需要的功能）
3. 点击 **START** 开始自动化
4. 等待完成或点击 **STOP** 停止

---

### Android版

#### 📲 打包成APK

**Windows用户（推荐使用Docker）:**

```batch
# 双击运行
build_android_docker.bat
```

**Linux/macOS用户:**

```bash
chmod +x build_android.sh
./build_android.sh
```

详细步骤请查看：
- 📚 [详细构建指南](BUILD_ANDROID_GUIDE.md)
- 🚀 [快速开始](QUICK_START_ANDROID.md)
- 📱 [Android版说明](README_ANDROID.md)

#### ⚠️ Android版限制

当前版本主要为**桌面环境**设计，Android APK需要额外适配：

- ❌ 屏幕截图功能（需要MediaProjection API）
- ❌ 点击模拟功能（需要Accessibility Service）
- ❌ 运行时权限申请

**推荐方案**：使用桌面版或在Android模拟器中运行桌面版游戏。

---

## 📁 项目结构

```
D:\插件\
├── 📄 核心代码
│   ├── main.py                      # Kivy UI主程序
│   ├── automation_engine.py         # 自动化引擎核心
│   ├── image_processor.py          # 图像识别（OpenCV）
│   ├── game_controller.py          # 游戏控制（点击/滑动）
│   └── task_manager.py             # 任务管理器
│
├── 📦 Android打包
│   ├── buildozer.spec              # Buildozer配置
│   ├── requirements.txt            # Python依赖
│   ├── Dockerfile                  # Docker构建环境
│   ├── build_android.sh            # Linux/Mac构建脚本
│   └── build_android_docker.bat    # Windows构建脚本
│
├── 📚 文档
│   ├── README.md                   # 本文件
│   ├── BUILD_ANDROID_GUIDE.md      # Android详细指南
│   ├── README_ANDROID.md           # Android版说明
│   ├── QUICK_START_ANDROID.md      # 快速开始
│   └── 项目文件清单.md              # 文件清单
│
└── 🖼️ templates/                    # 图像模板目录（25个模板）
```

## 🎯 完整功能流程

```
登录游戏
    ↓
检测task按钮（登录成功）
    ↓
[可选] 每日委托流程
    ├── 点击task → 进入委托界面
    ├── 检查派遣状态
    ├── 领取奖励 / 再次派遣
    └── 关闭委托界面
    ↓
进入120开拓力副本
    ├── 搜索"120开拓力"
    ├── 点击前往
    ├── 进入副本
    ├── 调整队伍（点击加号5次）
    └── 点击挑战 → 开始挑战
    ↓
战斗控制
    ├── 智能倍速控制（检测并开启）
    └── 智能自动战斗（检测并开启）
    ↓
循环刷本
    ├── 检测"再来一次" → 点击
    ├── 等待10秒
    ├── 检测"退出关卡" → 点击
    └── 继续领取奖励
    ↓
领取奖励
    ├── 点击close
    ├── 点击task
    └── 持续点击所有"领取"按钮
    ↓
礼物检查
    ├── 比较400/500置信度
    ├── 如果500更高 → 点击gift（2次）
    └── 关闭礼物界面
    ↓
完成！
```

## 🛠️ 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Python** | 主要编程语言 | 3.9-3.11 |
| **Kivy** | 跨平台UI框架 | 2.3.0+ |
| **OpenCV** | 图像识别和处理 | 4.8.0+ |
| **NumPy** | 数值计算 | 1.24.0+ |
| **Pillow** | 图像处理 | 10.0.0+ |
| **PyAutoGUI** | 桌面自动化 | 0.9.54+ |
| **Buildozer** | Android打包工具 | 1.5.0+ |

## 📋 依赖安装

```bash
# 核心依赖
pip install kivy>=2.3.0
pip install numpy>=1.24.0
pip install pillow>=10.0.0
pip install opencv-python>=4.8.0
pip install pyyaml>=6.0.0

# 桌面环境额外依赖
pip install pyautogui>=0.9.54

# Android构建工具
pip install buildozer>=1.5.0
```

或直接安装全部依赖：

```bash
pip install -r requirements.txt
```

## ⚙️ 配置选项

### UI选项

- **Daily Commission** - 勾选以启用每日委托自动化

### 高级配置

可以在代码中调整：
- 图像匹配置信度阈值
- 各阶段等待时间
- 点击延迟时间
- 循环次数限制

## 🎨 模板图像说明

项目使用图像识别技术，需要准备以下模板图像（已包含示例）：

| 模板 | 说明 | 重要性 |
|------|------|--------|
| `login_button_first.png` | 首次登录按钮 | 🔴 必需 |
| `game_start_screen.png` | 游戏开始界面 | 🔴 必需 |
| `task.png` | 任务按钮 | 🔴 必需 |
| `weituo.png` | 委托界面 | 🟡 可选 |
| `120kaituoli.png` | 120开拓力标识 | 🔴 必需 |
| ... | 其他模板 | - |

**提示**: 可以根据实际游戏界面重新截图并替换模板。

## 🐛 故障排除

### 常见问题

**Q: 点击没有反应？**
- A: 确保游戏窗口在前台，检查日志中的点击坐标

**Q: 图像识别失败？**
- A: 检查模板图像是否清晰，尝试降低置信度阈值

**Q: Windows构建Android失败？**
- A: 使用Docker方案，或在WSL2/Linux环境构建

**Q: Android APK安装后无法使用？**
- A: 当前版本需要额外适配Android API，推荐使用桌面版

### 日志查看

程序运行时会输出详细日志：
- 🔍 检测状态
- ✅ 成功操作
- ❌ 错误信息
- ⏰ 等待状态

## 🔒 免责声明

- 本项目仅供**学习交流**使用
- 请勿用于**商业目的**
- 使用本工具可能违反游戏服务条款
- 使用风险自负，开发者不承担任何责任

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

- 项目主页：GitHub
- 问题反馈：Issues
- 开发团队：HSR Automation Team

## 🎉 致谢

感谢以下开源项目：
- [Kivy](https://kivy.org/) - 跨平台UI框架
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [Buildozer](https://github.com/kivy/buildozer) - Android打包工具

---

**版本**: 1.0  
**更新日期**: 2025-10-06  
**开发者**: HSR Automation Team

⭐ 如果这个项目对你有帮助，请给个Star！
