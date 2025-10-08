# 🐋 Docker Desktop 安装指南 (Windows)

## 当前状态

```
[X] Docker is NOT installed!
```

**不用担心！按照以下步骤安装即可。**

---

## 📥 步骤1: 下载 Docker Desktop

### 方法A: 官方网站（推荐）

1. **访问官网**
   ```
   https://www.docker.com/products/docker-desktop
   ```

2. **点击 "Download for Windows"**
   - 文件名：`Docker Desktop Installer.exe`
   - 大小：约 500MB

### 方法B: 直接下载链接

```
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
```

---

## 💿 步骤2: 安装 Docker Desktop

### 2.1 运行安装程序

1. **双击** `Docker Desktop Installer.exe`

2. **用户账户控制（UAC）**
   - 点击 "是"

### 2.2 安装选项

安装向导会显示：

```
Configuration
☑ Use WSL 2 instead of Hyper-V (recommended)
☐ Add shortcut to desktop
```

**建议配置**:
- ✅ 勾选 "Use WSL 2 instead of Hyper-V"
- ✅ 勾选 "Add shortcut to desktop"（可选）

点击 **"OK"** 继续

### 2.3 等待安装

```
Installing Docker Desktop...
[████████████████████████] 100%
```

**时间**: 约 5-10 分钟（取决于电脑速度）

### 2.4 完成安装

```
Installation succeeded

Docker Desktop requires a logout or a restart.
```

**重要**: 点击 **"Close and restart"** 重启电脑

---

## 🔧 步骤3: 首次启动配置

### 3.1 启动 Docker Desktop

重启后：

1. **从开始菜单启动**
   - 开始菜单 → Docker Desktop

2. **或双击桌面图标**
   - Docker Desktop（蓝色鲸鱼图标）

### 3.2 服务条款

```
Docker Subscription Service Agreement

[ ] I accept the terms
```

- 勾选 "I accept the terms"
- 点击 **"Accept"**

### 3.3 Docker 使用调查（可选）

```
Help us improve Docker Desktop
```

- 可以跳过（点击 "Skip"）
- 或填写后点击 "Continue"

### 3.4 等待启动

```
Starting Docker Desktop...

Docker Desktop is starting...
```

**首次启动需要**: 2-5 分钟

**启动完成标志**:
- 右下角任务栏出现鲸鱼图标
- 图标不再旋转，变为稳定状态
- 鼠标悬停显示 "Docker Desktop is running"

---

## ✅ 步骤4: 验证安装

### 4.1 检查 Docker 版本

1. **打开 PowerShell 或 CMD**
   - 按 `Win + R`
   - 输入 `powershell`
   - 按 Enter

2. **运行命令**
   ```powershell
   docker --version
   ```

3. **期望输出**
   ```
   Docker version 24.0.6, build ed223bc
   ```

### 4.2 检查 Docker 是否运行

```powershell
docker ps
```

**期望输出**:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

（空列表是正常的，说明Docker在运行）

### 4.3 运行测试容器（可选）

```powershell
docker run hello-world
```

**期望输出**:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 🎯 步骤5: 返回项目构建

### 5.1 再次检查环境

回到项目目录，运行：

```batch
check_docker_en.bat
```

**现在应该看到**:
```
[OK] Docker is installed
[OK] Docker is running
[OK] All checks passed!
```

### 5.2 开始构建 APK

```batch
build_android_en.bat
```

---

## ⚠️ 常见问题

### 问题1: WSL 2 需要更新

**错误信息**:
```
WSL 2 installation is incomplete
```

**解决方法**:

1. **下载 WSL 2 内核更新**
   ```
   https://aka.ms/wsl2kernel
   ```

2. **安装更新包**
   - 双击 `wsl_update_x64.msi`
   - 完成安装

3. **重启 Docker Desktop**

---

### 问题2: 虚拟化未启用

**错误信息**:
```
Hardware assisted virtualization and data execution protection 
must be enabled in the BIOS
```

**解决方法**:

1. **重启电脑进入 BIOS**
   - 重启时按 `F2`, `Del`, 或 `F10`（取决于主板）

2. **启用虚拟化**
   - Intel CPU: 启用 "Intel VT-x"
   - AMD CPU: 启用 "AMD-V" 或 "SVM Mode"

3. **保存并退出 BIOS**

4. **重启后启动 Docker Desktop**

---

### 问题3: Hyper-V 冲突

**错误信息**:
```
Hyper-V is not available
```

**解决方法** (Windows 10/11 Home):

使用 WSL 2 模式（已在安装时选择）：
- 不需要 Hyper-V
- WSL 2 是更好的选择

**如果是 Windows 10/11 Pro**:

1. **启用 Hyper-V**
   - 控制面板 → 程序 → 启用或关闭 Windows 功能
   - 勾选 "Hyper-V"
   - 重启电脑

---

### 问题4: 端口占用

**错误信息**:
```
Port is already allocated
```

**解决方法**:

1. **检查占用端口的程序**
   ```powershell
   netstat -ano | findstr :XXXX
   ```

2. **关闭占用的程序**
   - 或重启电脑

---

## 📊 系统要求

### 最低要求

- **操作系统**: Windows 10 64-bit (Build 19041+) 或 Windows 11
- **内存**: 4GB RAM（建议 8GB+）
- **硬盘**: 至少 10GB 可用空间
- **CPU**: 支持虚拟化的 64-bit 处理器

### 检查 Windows 版本

```powershell
winver
```

**需要**: 
- Windows 10: 版本 2004 或更高
- Windows 11: 任意版本

---

## 🎓 Docker Desktop 界面说明

### 主要功能

```
┌─────────────────────────────────┐
│  Docker Desktop                 │
├─────────────────────────────────┤
│  ▶ Containers  (运行的容器)     │
│  📦 Images     (镜像列表)       │
│  🔧 Settings   (设置)           │
└─────────────────────────────────┘
```

### 右下角托盘图标

- **绿色鲸鱼**: Docker 正在运行 ✅
- **旋转鲸鱼**: Docker 正在启动 🔄
- **红色鲸鱼**: Docker 已停止 ❌

---

## 🚀 快速开始清单

安装完成后：

- [ ] Docker Desktop 已安装
- [ ] 电脑已重启
- [ ] Docker Desktop 已启动（托盘图标是绿色）
- [ ] 运行 `docker --version` 成功
- [ ] 运行 `docker ps` 成功
- [ ] 运行 `check_docker_en.bat` 显示全部 OK
- [ ] 准备运行 `build_android_en.bat`

---

## 📞 获取帮助

### 官方资源

- **Docker 文档**: https://docs.docker.com/desktop/install/windows-install/
- **WSL 2 文档**: https://docs.microsoft.com/en-us/windows/wsl/install
- **社区论坛**: https://forums.docker.com/

### 项目文档

- **构建指南**: `BUILD_ANDROID_GUIDE.md`
- **问题排查**: `构建问题排查指南.md`
- **快速开始**: `START_HERE.md`

---

## 💡 小提示

### Docker Desktop 资源使用

Docker Desktop 会占用系统资源：

- **内存**: 默认 2GB（可在设置中调整）
- **CPU**: 默认 2 核心（可在设置中调整）
- **硬盘**: WSL 2 会动态分配空间

### 调整资源（可选）

1. 打开 Docker Desktop
2. 点击 ⚙️ Settings
3. 选择 Resources
4. 调整 CPU、Memory、Disk

**建议配置（如果电脑配置较好）**:
- Memory: 4-6GB
- CPU: 4 cores
- Disk: 20GB+

---

## ✅ 安装完成

完成以上步骤后，Docker 就安装好了！

**下一步**:

```batch
cd D:\插件
check_docker_en.bat
```

应该显示：
```
[OK] Docker is installed
[OK] Docker is running
```

然后就可以开始构建了：
```batch
build_android_en.bat
```

---

**祝安装顺利！** 🎉




