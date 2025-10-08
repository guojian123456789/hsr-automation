# 🚀 快速开始 - 打包Android APK

## Windows用户（最简单的方法）

### 1️⃣ 安装Docker Desktop

下载并安装：https://www.docker.com/products/docker-desktop

### 2️⃣ 构建APK

双击运行：**`build_android_docker.bat`**

或在PowerShell中执行：
```powershell
.\build_android_docker.bat
```

### 3️⃣ 等待完成

⏰ 首次构建约需要 **30-60分钟**（会下载Android SDK/NDK）

✅ 完成后APK文件位于：`bin\hsrautomation-1.0-arm64-v8a-debug.apk`

### 4️⃣ 安装到手机

**方法A - 使用ADB：**
```bash
adb install bin\hsrautomation-1.0-arm64-v8a-debug.apk
```

**方法B - 直接传输：**
- 将APK传到手机，点击安装

---

## Linux/macOS用户

### 1️⃣ 安装依赖

```bash
# Ubuntu/Debian
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装buildozer
pip3 install buildozer cython==0.29.33
```

### 2️⃣ 构建APK

```bash
chmod +x build_android.sh
./build_android.sh
```

### 3️⃣ 安装

```bash
adb install bin/hsrautomation-1.0-arm64-v8a-debug.apk
```

---

## ⚠️ 重要提示

### 当前版本限制

本项目**主要为桌面环境设计**，打包成Android APK后：

✅ **UI界面可以正常显示**  
❌ **核心功能需要适配**（截图和点击需要Android特定API）

### 需要的适配工作

如需在Android上实际使用，需要：

1. **屏幕截图** - 集成MediaProjection API
2. **模拟点击** - 集成Accessibility Service  
3. **权限申请** - 运行时请求特殊权限

### 推荐方案

- **方案1（推荐）**：继续在**桌面版**（Windows/Mac）上使用
- **方案2**：在Android模拟器中运行桌面版游戏
- **方案3**：进行完整的Android适配开发

---

## 📚 详细文档

- **完整构建指南**：`BUILD_ANDROID_GUIDE.md`
- **Android版说明**：`README_ANDROID.md`
- **项目总览**：`README.md`

---

## 🎯 快速对比

| 环境 | 构建难度 | 功能完整度 | 推荐度 |
|------|---------|-----------|--------|
| **Windows桌面** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Android APK** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Android模拟器+桌面版** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**建议**：如果主要需求是自动化游戏，推荐使用**桌面版**或**模拟器+桌面版**方案。

---

💡 **有问题？** 查看 `BUILD_ANDROID_GUIDE.md` 获取详细帮助！




