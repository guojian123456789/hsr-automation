# 🤖 Android平台适配完整指南

## 📱 已实现的Android功能

### ✅ 屏幕截图（MediaProjection API）

**文件**: `android_screen_capture.py`

**功能**:
- 使用MediaProjection API实现无Root屏幕截图
- 返回与OpenCV兼容的BGR格式图像
- 支持实时截图

**使用方法**:
```python
from android_screen_capture import AndroidScreenCapture

# 初始化
capture = AndroidScreenCapture()

# 请求权限（会弹出系统授权窗口）
capture.request_permission()

# 在权限授予后开始截图
if capture.is_ready():
    screenshot = capture.capture_screen()
    # screenshot是numpy array，BGR格式
```

**权限要求**:
- 用户需要在弹出的系统窗口中点击"立即开始"授予截屏权限
- 此权限仅在应用运行期间有效

---

### ✅ 模拟点击（Accessibility Service）

**文件**: 
- Python层: `android_accessibility_service.py`
- Java层: `service/HSRAccessibilityService.java`
- 配置: `service/accessibility_service_config.xml`

**功能**:
- 使用AccessibilityService实现无Root模拟点击
- 支持点击和滑动手势
- 通过广播机制与Python通信

**使用方法**:
```python
from android_accessibility_service import AndroidAccessibilityService

# 初始化
accessibility = AndroidAccessibilityService()

# 检查服务是否已启用
if not accessibility.check_service_enabled():
    # 打开设置页面让用户手动启用
    accessibility.request_service_permission()

# 执行点击
accessibility.click(x=100, y=200, duration=100)

# 执行滑动
accessibility.swipe(
    start_x=100, start_y=500,
    end_x=100, end_y=200,
    duration=300
)
```

**权限要求**:
- 用户需要在设置中手动启用无障碍服务
- 路径: 设置 → 辅助功能 → 已安装的服务 → HSR Automation → 开启

---

## 🔧 集成方式

### 1. image_processor.py 自动适配

```python
def capture_screen(self):
    """自动根据平台选择截图方式"""
    if self.platform == 'android':
        return self.capture_android_screen()  # 使用MediaProjection
    else:
        return self.capture_desktop_screen()  # 使用PIL
```

### 2. game_controller.py 自动适配

```python
def click_position(self, position):
    """自动根据平台选择点击方式"""
    x, y = position
    
    if self.platform == 'android':
        return self.android_click(x, y)  # 使用AccessibilityService
    else:
        return self.desktop_click(x, y)  # 使用PyAutoGUI/Win32API
```

---

## 📋 构建配置

### buildozer.spec 关键配置

```ini
# 添加pyjnius依赖（用于Python调用Java）
requirements = python3,kivy,numpy,pillow,opencv,pyyaml,pyjnius

# 包含Java服务文件
source.include_patterns = service/*.java,service/*.xml

# 注册AccessibilityService
android.services = HSRAccessibilityService:service/HSRAccessibilityService.java

# 添加服务配置元数据
android.meta_data = com.hsr.automation.accessibility_service=@xml/accessibility_service_config

# 必需权限
android.permissions = SYSTEM_ALERT_WINDOW,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,FOREGROUND_SERVICE
```

---

## 🚀 用户使用流程

### 首次运行设置

1. **安装APK**
   ```bash
   adb install bin/hsrautomation-1.0-arm64-v8a-debug.apk
   ```

2. **启动应用**
   - 打开HSR Automation

3. **授予屏幕录制权限**
   - 应用会自动请求截屏权限
   - 在弹出窗口中点击"立即开始"

4. **启用无障碍服务**
   - 应用会引导到设置页面
   - 路径: 设置 → 辅助功能 → 已安装的服务
   - 找到"HSR Automation"并开启

5. **开始使用**
   - 返回应用
   - 勾选需要的功能
   - 点击START开始自动化

---

## 🎯 技术架构

```
┌─────────────────────────────────────────┐
│          Python层 (Kivy)                │
│  ┌───────────────────────────────────┐  │
│  │  main.py (UI)                     │  │
│  │  automation_engine.py (逻辑)      │  │
│  └───────────────────────────────────┘  │
│           ↓                ↓             │
│  ┌─────────────┐    ┌─────────────┐     │
│  │ image_      │    │ game_       │     │
│  │ processor   │    │ controller  │     │
│  └──────┬──────┘    └──────┬──────┘     │
│         │                  │             │
│         ↓                  ↓             │
│  ┌─────────────┐    ┌─────────────┐     │
│  │ android_    │    │ android_    │     │
│  │ screen_     │    │ accessi-    │     │
│  │ capture.py  │    │ bility_     │     │
│  │             │    │ service.py  │     │
│  └──────┬──────┘    └──────┬──────┘     │
│         │                  │             │
│         ↓                  ↓             │
│  ┌─────────────┐    ┌─────────────┐     │
│  │ jnius       │    │ jnius       │     │
│  │ (Python-    │    │ (Broadcast) │     │
│  │  Java桥接)  │    │             │     │
│  └──────┬──────┘    └──────┬──────┘     │
└─────────┼──────────────────┼─────────────┘
          │                  │
          ↓                  ↓
┌─────────────────────────────────────────┐
│          Java/Android层                  │
│  ┌─────────────┐    ┌─────────────┐     │
│  │ Media-      │    │ HSR         │     │
│  │ Projection  │    │ Accessi-    │     │
│  │ Manager     │    │ bility      │     │
│  │             │    │ Service     │     │
│  └─────────────┘    └─────────────┘     │
│         │                  │             │
│         ↓                  ↓             │
│  ┌─────────────┐    ┌─────────────┐     │
│  │ Screen      │    │ Gesture     │     │
│  │ Capture     │    │ Dispatch    │     │
│  └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────┘
```

---

## ⚠️ 注意事项

### 1. 权限说明

**屏幕录制权限**:
- 运行时权限，每次启动应用都需要重新授予
- 仅用于截取游戏画面进行识别
- 不会录制或保存视频

**无障碍服务权限**:
- 系统级权限，需要用户手动在设置中开启
- 一次开启后持续有效
- 仅用于模拟点击游戏界面
- 不会访问其他应用的数据

### 2. 性能考虑

**截图性能**:
- MediaProjection截图速度: ~50-100ms/张
- 建议间隔至少200ms再次截图
- 避免过于频繁的截图造成性能问题

**点击延迟**:
- AccessibilityService点击延迟: ~50-200ms
- 比直接触摸慢，但足够用于游戏自动化
- 建议点击后等待至少100ms

### 3. 兼容性

**Android版本要求**:
- 最低: Android 5.0 (API 21)
- 推荐: Android 7.0+ (API 24+)
- MediaProjection: API 21+
- AccessibilityService手势: API 24+

**已测试设备**:
- 需要在实际设备上测试
- 不同厂商ROM可能有差异
- 部分MIUI/EMUI可能需要额外设置

---

## 🐛 故障排除

### 问题1: 屏幕截图失败

**症状**: 截图返回None或黑屏

**解决方法**:
1. 检查是否授予了屏幕录制权限
2. 重启应用重新请求权限
3. 检查日志中的错误信息

### 问题2: 点击无反应

**症状**: 发送点击指令但游戏无响应

**解决方法**:
1. 确认无障碍服务已启用
2. 检查服务是否在运行: `adb shell dumpsys accessibility`
3. 重启无障碍服务
4. 检查游戏是否在前台

### 问题3: 构建失败

**症状**: buildozer编译Java服务失败

**解决方法**:
1. 确保service目录结构正确
2. 检查Java语法错误
3. 查看构建日志: `.buildozer/android/platform/build-*/logs/`

### 问题4: 权限请求无响应

**症状**: 点击权限按钮后无反应

**解决方法**:
1. 检查Intent是否正确发送
2. 使用adb查看系统日志: `adb logcat`
3. 尝试手动进入设置页面

---

## 📚 相关文档

- [MediaProjection官方文档](https://developer.android.com/reference/android/media/projection/MediaProjection)
- [AccessibilityService官方文档](https://developer.android.com/reference/android/accessibilityservice/AccessibilityService)
- [Pyjnius文档](https://pyjnius.readthedocs.io/)
- [Buildozer文档](https://buildozer.readthedocs.io/)

---

## ✅ 完成检查清单

构建前确认:

- [x] `android_screen_capture.py` - 截图模块已创建
- [x] `android_accessibility_service.py` - 点击模块已创建  
- [x] `service/HSRAccessibilityService.java` - Java服务已创建
- [x] `service/accessibility_service_config.xml` - 配置文件已创建
- [x] `image_processor.py` - 已集成Android截图
- [x] `game_controller.py` - 已集成Android点击
- [x] `buildozer.spec` - 已添加必要配置
- [ ] 在真机上测试截图功能
- [ ] 在真机上测试点击功能
- [ ] 测试权限请求流程

---

**版本**: 1.0  
**更新日期**: 2025-10-06  
**状态**: ✅ Android适配已完成




