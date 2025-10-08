# Docker 镜像加速配置指南

## 问题症状

```
ERROR: failed to do request: Head "https://registry-1.docker.io/v2/library/ubuntu/manifests/22.04": 
dial tcp 128.242.240.93:443: connectex: A connection attempt failed
```

**原因**: Docker Hub 连接超时（网络问题）

---

## ✅ 解决方案：配置镜像加速器

### 步骤1：打开 Docker Desktop 设置

1. **右键点击** 任务栏的 Docker 图标（蓝色鲸鱼）🐋
2. **选择** "Settings" 或 "设置"

### 步骤2：配置 Docker Engine

1. **左侧菜单** → 点击 "Docker Engine"

2. **找到配置区域**（JSON格式）：
   ```json
   {
     "builder": {
       "gc": {
         "defaultKeepStorage": "20GB",
         "enabled": true
       }
     },
     "experimental": false
   }
   ```

3. **添加镜像源**，修改为：
   ```json
   {
     "builder": {
       "gc": {
         "defaultKeepStorage": "20GB",
         "enabled": true
       }
     },
     "experimental": false,
     "registry-mirrors": [
       "https://docker.mirrors.ustc.edu.cn",
       "https://hub-mirror.c.163.com",
       "https://mirror.baidubce.com"
     ]
   }
   ```

4. **点击** "Apply & Restart" 按钮

5. **等待** Docker 重启（约30秒-1分钟）

### 步骤3：验证配置

打开 PowerShell 或 CMD：

```powershell
docker info | findstr "Registry Mirrors"
```

**应该看到**:
```
Registry Mirrors:
  https://docker.mirrors.ustc.edu.cn/
  https://hub-mirror.c.163.com/
  https://mirror.baidubce.com/
```

---

## 🎯 可用的国内镜像源

| 镜像源 | 地址 | 速度 |
|--------|------|------|
| 中科大 | `https://docker.mirrors.ustc.edu.cn` | ⭐⭐⭐⭐⭐ |
| 网易 | `https://hub-mirror.c.163.com` | ⭐⭐⭐⭐ |
| 百度云 | `https://mirror.baidubce.com` | ⭐⭐⭐⭐ |
| 阿里云 | `https://<你的ID>.mirror.aliyuncs.com` | ⭐⭐⭐⭐⭐ |
| 腾讯云 | `https://mirror.ccs.tencentyun.com` | ⭐⭐⭐⭐ |

**注意**：阿里云镜像需要注册账号获取专属ID

---

## 🔄 配置后重新构建

配置完成并重启Docker后：

```batch
# 清理之前的构建缓存（可选）
docker system prune -a

# 重新构建
.\build_android_auto.bat debug
```

---

## ⚠️ 其他解决方案

### 方案2：使用代理

如果有VPN或代理：

1. **Docker Desktop Settings** → **Resources** → **Proxies**

2. **配置代理**：
   ```
   Web Server (HTTP): http://127.0.0.1:端口号
   Secure Web Server (HTTPS): http://127.0.0.1:端口号
   ```

3. **勾选** "Manual proxy configuration"

4. **Apply & Restart**

### 方案3：离线导入镜像

如果网络始终不通：

1. **在其他有网络的电脑**下载镜像：
   ```bash
   docker pull ubuntu:22.04
   docker save ubuntu:22.04 -o ubuntu-22.04.tar
   ```

2. **复制到当前电脑**

3. **导入镜像**：
   ```powershell
   docker load -i ubuntu-22.04.tar
   ```

---

## 📊 网络测试

### 测试 Docker Hub 连接

```powershell
# 测试连接
Test-NetConnection -ComputerName registry-1.docker.io -Port 443

# 或使用 curl
curl -I https://registry-1.docker.io
```

### 测试镜像源

```powershell
# 测试中科大镜像
curl -I https://docker.mirrors.ustc.edu.cn

# 测试网易镜像
curl -I https://hub-mirror.c.163.com
```

---

## ✅ 完整流程（推荐）

```batch
1. 配置 Docker 镜像加速器
   └─> Docker Desktop Settings
       └─> Docker Engine
           └─> 添加 registry-mirrors
               └─> Apply & Restart

2. 验证配置
   └─> docker info | findstr "Registry Mirrors"

3. 重新构建
   └─> .\build_android_auto.bat debug
```

---

## 🆘 如果仍然失败

1. **检查网络连接**
   - 确保能访问互联网
   - 关闭防火墙测试
   - 尝试使用VPN

2. **检查 Docker 设置**
   - 重启 Docker Desktop
   - 重启电脑

3. **查看详细日志**
   - 查看最新的 `build_log_*.txt` 文件

4. **联系支持**
   - Docker 官方文档：https://docs.docker.com/desktop/
   - 项目文档：`START_HERE.md`

---

**配置镜像加速器后，下载速度会从几KB/s提升到几MB/s！** 🚀

