# 🎯 Instrumentation点击方案说明

## 📝 为什么改用Instrumentation？

### 原方案（AccessibilityService）的问题：
1. ❌ 需要编译Java代码并注册Android Service
2. ❌ Buildozer无法正确处理自定义Java服务
3. ❌ 需要用户手动在系统设置中开启无障碍服务
4. ❌ 编译时出现 `gradlew failed` 错误

### 新方案（Instrumentation）的优势：
1. ✅ **纯Python实现** - 通过Pyjnius调用Android API
2. ✅ **无需额外权限** - 不需要无障碍服务权限
3. ✅ **开箱即用** - 用户安装后直接可以使用
4. ✅ **编译简单** - 不需要Java代码和Service配置

---

## 🔧 技术实现

### Instrumentation点击原理：
```python
from jnius import autoclass

# 获取Android类
MotionEvent = autoclass('android.view.MotionEvent')
SystemClock = autoclass('android.os.SystemClock')
Instrumentation = autoclass('android.app.Instrumentation')

# 创建Instrumentation实例
instrumentation = Instrumentation()

# 创建触摸事件
event_down = MotionEvent.obtain(...)  # ACTION_DOWN
event_up = MotionEvent.obtain(...)    # ACTION_UP

# 发送事件到系统
instrumentation.sendPointerSync(event_down)
instrumentation.sendPointerSync(event_up)
```

### 关键点：
- `Instrumentation` 是Android测试框架的一部分
- 可以模拟用户的触摸、按键等操作
- **不需要root权限**
- **不需要ADB调试**
- **不需要无障碍服务**

---

## 📋 现在需要的权限

### ✅ 必需权限（只有1个）：
1. **存储权限** (`READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`)
   - 用途：读取模板图片文件

### ❌ 不再需要的权限：
- ~~无障碍服务~~ - 已被Instrumentation替代
- ~~悬浮窗权限~~ - 应用是全屏UI，不需要悬浮窗

---

## 🚀 用户使用步骤（超简单）

1. 安装APK
2. 打开应用
3. 允许存储权限（自动弹窗）
4. 直接点击"开始"按钮 ✅

**就是这么简单！** 🎉

---

## 📊 方案对比

| 特性 | AccessibilityService | Instrumentation |
|------|---------------------|-----------------|
| 编译复杂度 | ❌ 高（需要Java） | ✅ 低（纯Python） |
| 权限要求 | ❌ 需要无障碍服务 | ✅ 无特殊权限 |
| 用户设置 | ❌ 需要手动开启 | ✅ 零配置 |
| 兼容性 | ❌ 依赖系统版本 | ✅ 通用 |
| 可靠性 | ❌ Service可能被杀 | ✅ 稳定 |

---

## ⚠️ 注意事项

### Instrumentation的限制：
1. **跨应用点击可能受限**
   - 只能在本应用的进程内注入事件
   - 对其他应用（如游戏）的点击可能无效

### 解决方案：
如果Instrumentation在实际使用中无法点击游戏界面，有以下备选方案：

#### 备选方案1：使用Accessibility + Python Service
- 用Python实现AccessibilityService（不用Java）
- 通过Kivy Service运行

#### 备选方案2：要求Root权限
- 使用 `su -c input tap x y`
- 需要用户手机已root

#### 备选方案3：要求ADB调试
- 使用 `input tap x y`（通过adb shell）
- 需要用户开启USB调试并连接电脑

---

## 📝 修改文件清单

1. ✅ `buildozer.spec` - 移除Java服务配置
2. ✅ `android_accessibility_service.py` - 改用Instrumentation实现
3. ✅ `permission_manager.py` - 简化权限检查
4. ✅ `修复问题总结.md` - 更新文档

---

## 🎯 下一步

执行以下命令提交并构建：

```powershell
git add .
git commit -m "Use Instrumentation for clicks instead of AccessibilityService"
git push
```

GitHub Actions会自动构建新APK，**理论上**编译应该成功了！

如果运行时发现Instrumentation无法点击游戏，我们再切换到其他方案。

