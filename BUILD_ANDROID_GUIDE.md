# HSR Automation - Android打包指南

## 📱 将项目打包成Android APK

### 🛠️ 准备工作

#### 方法一：使用Linux/macOS（推荐）

Buildozer只能在Linux或macOS上运行。如果你使用Windows，请使用WSL2或虚拟机。

**1. 安装系统依赖（Ubuntu/Debian）**

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

**2. 安装Python依赖**

```bash
pip3 install --upgrade pip
pip3 install buildozer cython==0.29.33
```

**3. 配置环境**

```bash
# 设置Java环境变量
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# 验证Java版本
java -version
```

#### 方法二：使用Docker（最简单）

**创建Dockerfile：**

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && \
    pip3 install buildozer cython==0.29.33

WORKDIR /app

CMD ["/bin/bash"]
```

**使用Docker构建：**

```bash
# 构建Docker镜像
docker build -t hsr-builder .

# 运行容器并挂载项目目录
docker run -it -v "D:\插件:/app" hsr-builder

# 在容器内执行构建
cd /app
buildozer android debug
```

### 📦 开始打包

**1. 清理旧的构建文件（如果有）**

```bash
buildozer android clean
```

**2. 初始化并构建APK**

```bash
# 第一次构建（会下载Android SDK/NDK，需要较长时间）
buildozer android debug

# 如果构建成功，APK文件会在：
# ./bin/hsrautomation-1.0-arm64-v8a-debug.apk
```

**3. 构建release版本（可选）**

```bash
# 生成release版APK（需要签名）
buildozer android release

# 签名APK（需要先创建密钥）
# 创建密钥
keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias

# 签名APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.jks bin/hsrautomation-1.0-arm64-v8a-release-unsigned.apk my-key-alias

# 对齐APK
zipalign -v 4 bin/hsrautomation-1.0-arm64-v8a-release-unsigned.apk bin/hsrautomation-1.0-release.apk
```

### 🔧 常见问题解决

#### 问题1：下载速度慢

```bash
# 设置国内镜像源
export GRADLE_OPTS="-Dorg.gradle.daemon=true -Dorg.gradle.jvmargs='-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8'"
```

#### 问题2：内存不足

```bash
# 在buildozer.spec中添加
[app]
android.gradle_dependencies = 

[buildozer]
# 增加Java堆内存
android.gradle_jvmargs = -Xms512m -Xmx2048m
```

#### 问题3：OpenCV编译失败

如果OpenCV编译失败，可以尝试使用opencv-python-headless：

修改`buildozer.spec`：
```ini
requirements = python3,kivy,numpy,pillow,opencv-python-headless,pyyaml
```

### 📲 安装APK到手机

**方法1：通过ADB**

```bash
# 确保手机开启USB调试
adb devices

# 安装APK
adb install bin/hsrautomation-1.0-arm64-v8a-debug.apk
```

**方法2：直接传输**

将APK文件传输到手机，直接点击安装。

### ⚙️ Android特定配置

#### 权限说明

项目需要以下权限：

- `SYSTEM_ALERT_WINDOW` - 悬浮窗权限（用于覆盖游戏界面）
- `WRITE_EXTERNAL_STORAGE` - 写入存储（保存模板和日志）
- `READ_EXTERNAL_STORAGE` - 读取存储（加载模板图片）
- `INTERNET` - 网络权限（可选）
- `ACCESS_NETWORK_STATE` - 网络状态（可选）
- `WAKE_LOCK` - 保持唤醒（防止息屏）
- `FOREGROUND_SERVICE` - 前台服务（保持运行）

#### 在Android上的限制

**注意：** 当前代码主要为桌面环境设计，在Android上需要适配：

1. **屏幕截图**：需要使用MediaProjection API
2. **模拟点击**：需要使用Accessibility Service
3. **权限申请**：需要在运行时申请特殊权限

### 🚀 下一步优化

要让应用在Android上完全可用，需要：

1. **添加Android Service**：创建后台服务保持运行
2. **申请特殊权限**：无障碍服务、截屏权限
3. **优化UI**：适配Android屏幕尺寸
4. **添加通知**：显示运行状态

### 📝 版本信息

- **当前版本**：1.0
- **支持架构**：arm64-v8a
- **最低Android版本**：5.0 (API 21)
- **目标Android版本**：13 (API 33)

### 💡 提示

1. **首次构建**：第一次构建会下载约1-2GB的SDK/NDK，请确保网络稳定
2. **构建时间**：首次构建可能需要30分钟到1小时
3. **存储空间**：确保至少有5GB的可用空间
4. **Python版本**：建议使用Python 3.9-3.11

### 🆘 获取帮助

如果遇到问题，可以：

1. 查看构建日志：`.buildozer/android/platform/build-*/logs/`
2. 检查Buildozer文档：https://buildozer.readthedocs.io/
3. 查看Kivy Android文档：https://kivy.org/doc/stable/guide/packaging-android.html

---

## 快速开始（TL;DR）

```bash
# 在Linux/WSL2/Docker中执行
cd /path/to/project
buildozer android debug

# 安装到手机
adb install bin/hsrautomation-1.0-arm64-v8a-debug.apk
```





