# 🚀 使用 GitHub Actions 构建 Android APK

## ✅ 优势

- ✨ **完全云端构建** - 不受本地网络限制
- 🆓 **完全免费** - GitHub Actions 免费额度充足
- ⚡ **自动化** - 推送代码自动构建
- 📦 **可下载 APK** - 构建完成后直接下载

---

## 📋 准备工作

### 1. 创建 GitHub 账号

如果还没有 GitHub 账号：
1. 访问：https://github.com/signup
2. 填写邮箱、密码、用户名
3. 验证邮箱

---

## 🎯 详细步骤

### 步骤 1: 初始化 Git 仓库

在项目目录打开 PowerShell：

```powershell
# 检查是否已有 git
git --version

# 如果没有，从这里下载：https://git-scm.com/download/win

# 初始化仓库
git init

# 配置用户信息（首次使用）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - HSR Automation"
```

---

### 步骤 2: 在 GitHub 创建仓库

1. **访问 GitHub**：https://github.com/new

2. **填写仓库信息**：
   ```
   Repository name: hsr-automation
   Description: HSR Automation Assistant (可选)
   Public ✅ (推荐，免费无限构建)
   或 Private (每月 2000 分钟)
   
   ❌ 不要勾选 "Add README"
   ❌ 不要勾选 "Add .gitignore"
   ❌ 不要勾选 "Choose a license"
   ```

3. **点击** "Create repository"

---

### 步骤 3: 关联远程仓库并推送

GitHub 会显示命令，复制并在 PowerShell 运行：

```powershell
# 关联远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/hsr-automation.git

# 推送代码
git branch -M main
git push -u origin main
```

**如果需要登录**：
- 用户名：你的 GitHub 用户名
- 密码：使用 Personal Access Token (不是密码)
  - 创建 Token：https://github.com/settings/tokens
  - 权限选择：`repo` (full control)

---

### 步骤 4: 验证工作流文件

确认以下文件已存在并已推送：

```
.github/
└── workflows/
    └── build-android.yml  ✅ 已创建
```

检查：

```powershell
# 查看文件
cat .github\workflows\build-android.yml

# 确认文件已添加到 git
git status
```

如果文件未提交：

```powershell
git add .github/workflows/build-android.yml
git commit -m "Add GitHub Actions workflow"
git push
```

---

### 步骤 5: 查看构建进度

1. **访问 Actions 页面**：
   ```
   https://github.com/你的用户名/hsr-automation/actions
   ```

2. **查看构建状态**：
   - 🟡 黄色圆圈：正在构建
   - ✅ 绿色勾：构建成功
   - ❌ 红色叉：构建失败

3. **点击构建** 查看详细日志

---

### 步骤 6: 下载 APK

构建成功后：

1. **点击最新的成功构建**

2. **滚动到页面底部**，找到 "Artifacts" 部分

3. **点击下载**：
   ```
   📦 hsr-automation-apk
   ```

4. **解压 ZIP 文件**，得到：
   ```
   hsrautomation-1.0-arm64-v8a-debug.apk
   ```

---

## ⏱️ 构建时间

| 阶段 | 时间 |
|------|------|
| 设置环境 | 2-3 分钟 |
| 安装依赖 | 3-5 分钟 |
| 下载 Android SDK/NDK | 5-10 分钟 |
| 编译 APK | 5-15 分钟 |
| **总计** | **15-30 分钟** |

---

## 🔄 后续更新

每次修改代码后：

```powershell
# 1. 查看修改
git status

# 2. 添加修改的文件
git add .

# 3. 提交
git commit -m "描述你的修改"

# 4. 推送
git push

# 5. 自动触发构建
# 访问 Actions 页面查看
```

---

## 🎯 手动触发构建

如果只想手动构建，不想每次推送都构建：

1. **访问 Actions 页面**

2. **左侧点击** "Build Android APK"

3. **点击右侧** "Run workflow" 按钮

4. **选择分支** (通常是 main)

5. **点击** "Run workflow"

---

## 🐛 常见问题

### Q1: 推送时提示 "permission denied"

**解决**：使用 Personal Access Token

1. 生成 Token：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 复制 Token（只显示一次！）
5. 推送时：
   - 用户名：你的 GitHub 用户名
   - 密码：粘贴 Token

---

### Q2: 构建失败，显示 "buildozer.spec not found"

**解决**：确保 `buildozer.spec` 已提交

```powershell
git add buildozer.spec
git commit -m "Add buildozer.spec"
git push
```

---

### Q3: 构建成功但没有 APK

**解决**：检查 `bin/` 目录

在构建日志中搜索：
- "Build completed"
- "Successfully built"
- 查看 bin 目录内容

---

### Q4: 免费额度用完了

**公开仓库**：无限制 ✅

**私有仓库**：
- 每月 2000 分钟
- 单次构建约 15-30 分钟
- 约可构建 60-130 次/月
- **完全够用！**

---

## 📊 构建日志示例

成功的构建日志应该包含：

```
✅ Set up Python
✅ Install system dependencies
✅ Install Python dependencies
✅ Build APK with Buildozer
   - Downloading Android SDK
   - Downloading Android NDK
   - Building APK
   - APK created successfully
✅ Upload APK artifact
```

---

## 🎉 成功标志

构建成功后：

```
Actions 页面：
✅ "Build Android APK" - 绿色勾

Artifacts 部分：
📦 hsr-automation-apk
   Size: ~30-50 MB
   Expires in: 30 days
```

下载并解压后：

```
hsrautomation-1.0-arm64-v8a-debug.apk
Size: ~30-50 MB
```

---

## 📱 安装到手机

### 方法 1: ADB 安装

```powershell
# 连接手机，开启 USB 调试
adb devices

# 安装 APK
adb install hsrautomation-1.0-arm64-v8a-debug.apk
```

### 方法 2: 直接安装

1. 将 APK 复制到手机
2. 使用文件管理器打开
3. 点击安装
4. 允许安装未知来源的应用

---

## 🔗 相关链接

- **GitHub 注册**：https://github.com/signup
- **Git 下载**：https://git-scm.com/download/win
- **Personal Access Token**：https://github.com/settings/tokens
- **GitHub Actions 文档**：https://docs.github.com/en/actions

---

## 📞 获取帮助

遇到问题？检查：

1. **Actions 日志**：查看详细错误
2. **buildozer.spec**：确认配置正确
3. **Git 状态**：`git status` 确认文件已提交
4. **网络连接**：确保能访问 GitHub

---

## ✅ 快速检查清单

开始前确认：

- [ ] 有 GitHub 账号
- [ ] 安装了 Git
- [ ] 项目目录中有 `buildozer.spec`
- [ ] 项目目录中有 `main.py`
- [ ] `.github/workflows/build-android.yml` 已创建

推送前确认：

- [ ] `git init` 已运行
- [ ] `git add .` 已运行
- [ ] `git commit` 已运行
- [ ] 已创建 GitHub 仓库
- [ ] `git remote add origin` 已运行

构建时确认：

- [ ] Actions 页面可访问
- [ ] 构建已开始（黄色圆圈）
- [ ] 等待 15-30 分钟
- [ ] 构建成功（绿色勾）
- [ ] Artifacts 可下载

---

**祝构建顺利！** 🎉

有任何问题随时查看 Actions 日志或询问帮助。

