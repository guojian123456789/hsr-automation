# 🎮 HSR Automation - Android版本

崩坏星穹铁道自动化助手 - Android应用

## 📱 功能特性

- ✅ 自动登录游戏
- ✅ 自动执行每日委托
- ✅ 自动领取奖励
- ✅ 自动挑战副本（120开拓力）
- ✅ 智能倍速和自动战斗控制
- ✅ 礼物检查和领取
- ✅ 可选功能开关（每日委托等）

## 🔧 构建APK

### Windows用户（推荐使用Docker）

**前置要求：**
- 安装Docker Desktop：https://www.docker.com/products/docker-desktop
- 确保Docker Desktop正在运行

**构建步骤：**

1. **双击运行** `build_android_docker.bat`
   
   或者在命令行中执行：
   ```batch
   build_android_docker.bat debug
   ```

2. **等待构建完成**（首次构建约30-60分钟）

3. **找到APK文件**：`bin\hsrautomation-1.0-arm64-v8a-debug.apk`

**构建选项：**
```batch
build_android_docker.bat debug    # 构建调试版本（默认）
build_android_docker.bat release  # 构建发布版本
build_android_docker.bat clean    # 清理构建文件
```

### Linux/macOS用户

**前置要求：**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装buildozer
pip3 install buildozer cython==0.29.33
```

**构建步骤：**
```bash
# 赋予执行权限
chmod +x build_android.sh

# 构建
./build_android.sh debug
```

## 📲 安装到手机

### 方法1：使用ADB（推荐）

1. **启用USB调试**
   - 打开手机设置 → 关于手机
   - 连续点击"版本号"7次，启用开发者模式
   - 返回设置 → 系统 → 开发者选项
   - 启用"USB调试"

2. **连接手机到电脑**
   ```bash
   # 检查设备连接
   adb devices
   
   # 安装APK
   adb install bin\hsrautomation-1.0-arm64-v8a-debug.apk
   ```

### 方法2：直接传输

1. 将APK文件传输到手机（通过QQ、微信、USB等）
2. 在手机上找到APK文件
3. 点击安装（可能需要允许"未知来源"安装）

## ⚠️ 重要说明

### Android特殊权限

应用在Android上需要以下特殊权限：

1. **无障碍服务（Accessibility Service）**
   - 用途：模拟点击操作
   - 设置路径：设置 → 辅助功能 → 已安装的服务 → HSR Automation → 开启

2. **悬浮窗权限**
   - 用途：显示悬浮控制界面
   - 设置路径：设置 → 应用管理 → HSR Automation → 权限 → 悬浮窗 → 允许

3. **截屏权限**
   - 用途：截取游戏画面进行识别
   - 首次运行时会弹出授权请求

### 当前限制

**注意：** 当前版本主要为**桌面环境**设计，在Android上需要进一步适配：

- ❌ Android屏幕截图功能需要适配（使用MediaProjection API）
- ❌ Android点击模拟需要适配（使用Accessibility Service）
- ❌ 需要在运行时申请特殊权限

**建议：** 如需在Android上使用，需要额外开发Android特定的功能适配层。

## 🛠️ 项目结构

```
D:\插件\
├── main.py                      # 主程序入口（Kivy UI）
├── automation_engine.py         # 自动化引擎（核心逻辑）
├── image_processor.py          # 图像处理（OpenCV）
├── game_controller.py          # 游戏控制（点击、滑动）
├── task_manager.py             # 任务管理器
├── templates/                  # 图像模板目录
│   ├── login_button_first.png
│   ├── game_start_screen.png
│   ├── task.png
│   ├── weituo.png
│   ├── ... (更多模板)
│   └── gift.png
├── buildozer.spec              # Android打包配置
├── requirements.txt            # Python依赖
├── build_android.sh            # Linux/Mac构建脚本
├── build_android_docker.bat    # Windows Docker构建脚本
├── BUILD_ANDROID_GUIDE.md      # 详细构建指南
└── README_ANDROID.md           # 本文件
```

## 📋 依赖项

- **Python**: 3.9-3.11
- **Kivy**: 2.3.0+（跨平台UI框架）
- **OpenCV**: 4.8.0+（图像识别）
- **NumPy**: 1.24.0+（数值计算）
- **Pillow**: 10.0.0+（图像处理）
- **PyYAML**: 6.0.0+（配置管理）

## 🎯 使用流程

1. **启动应用**
2. **配置选项**（勾选需要执行的功能）
3. **启动游戏**（崩坏星穹铁道）
4. **点击"START"**开始自动化
5. **等待执行完成**或点击"STOP"停止

## 🔄 更新计划

- [ ] Android MediaProjection API集成（屏幕截图）
- [ ] Android Accessibility Service集成（点击模拟）
- [ ] 运行时权限申请
- [ ] 前台Service保持运行
- [ ] 通知栏状态显示
- [ ] 更多自定义选项

## 📄 许可证

本项目仅供学习交流使用，请勿用于商业目的。

## 🆘 问题反馈

如遇到问题，请查看：
1. `BUILD_ANDROID_GUIDE.md` - 详细构建指南
2. `.buildozer/android/platform/build-*/logs/` - 构建日志
3. Buildozer文档：https://buildozer.readthedocs.io/

## 💡 提示

- **首次构建时间长**：首次构建需要下载Android SDK/NDK（约1-2GB），请耐心等待
- **网络问题**：如果下载速度慢，可以配置国内镜像源
- **存储空间**：确保至少有5GB可用空间
- **构建失败**：查看错误日志，通常是依赖库编译问题

---

**开发者**: HSR Automation Team  
**版本**: 1.0  
**更新日期**: 2025-10-06




