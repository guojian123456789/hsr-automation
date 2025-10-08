# 🚀 HSR Automation - Quick Start Guide

## ✅ Project Ready to Build!

All Android adaptation is complete. You can now build a fully functional APK.

---

## 📂 Project Structure (Clean Version)

### 🎯 Core Files (Must Keep)
```
main.py                          - Application entry (Kivy UI)
automation_engine.py             - Core automation logic
image_processor.py               - Image recognition (OpenCV)
game_controller.py               - Game control (click/swipe)
task_manager.py                  - Task management
android_utils.py                 - Android utilities
android_screen_capture.py        - Android screenshot (MediaProjection)
android_accessibility_service.py - Android click (AccessibilityService)
```

### 📦 Build Files (Must Keep)
```
buildozer.spec                   - Android build configuration
requirements.txt                 - Python dependencies
Dockerfile                       - Docker build environment
build_android.sh                 - Linux/Mac build script
build_android_en.bat            ⭐ Windows build script (English, no garbled text)
check_docker_en.bat             ⭐ Environment check (English, no garbled text)
service/
  ├── HSRAccessibilityService.java        - Java accessibility service
  └── accessibility_service_config.xml    - Service configuration
```

### 🖼️ Templates (Must Keep)
```
templates/                       - 25 image template files
  ├── login_button_first.png
  ├── game_start_screen.png
  ├── task.png
  └── ... (22 more template files)
```

### 📚 Documentation
```
_Android适配完成_必读.md         ⭐ READ THIS FIRST!
README.md                        - Project overview
BUILD_ANDROID_GUIDE.md           - Detailed build guide
ANDROID_ADAPTATION_GUIDE.md      - Android adaptation technical guide
QUICK_START_ANDROID.md           - Quick start guide
如何使用构建脚本_无乱码版.txt     - How to use build scripts (no garbled text)
如何解决Android截图和点击.md      - How Android screenshot/click is solved
构建问题排查指南.md               - Build troubleshooting guide
打包前检查清单.md                 - Pre-build checklist
```

---

## 🎯 How to Build (3 Easy Steps)

### Step 1: Check Environment ✅
```batch
Double-click: check_docker_en.bat
```

Expected output:
```
[OK] Docker is installed
[OK] Docker is running
[OK] All checks passed!
```

If you see errors, follow the instructions shown.

---

### Step 2: Build APK 🔨
```batch
Double-click: build_android_en.bat
```

What will happen:
- Build Docker image (5 minutes, first time only)
- Download Android SDK/NDK (30-60 minutes, first time only)
- Build your APK

**Window will NOT close!** You'll see progress.

---

### Step 3: Install APK 📱
```batch
adb install bin\hsrautomation-1.0-arm64-v8a-debug.apk
```

Done! The app is now on your phone.

---

## 📖 Recommended Reading Order

### For Quick Build
1. **START_HERE.md** (this file) ⭐
2. **如何使用构建脚本_无乱码版.txt** - Build script usage

### For Understanding
3. **_Android适配完成_必读.md** - Android adaptation summary
4. **如何解决Android截图和点击.md** - How screenshot/click works

### For Troubleshooting
5. **构建问题排查指南.md** - Build troubleshooting
6. **BUILD_ANDROID_GUIDE.md** - Detailed build guide

### For Development
7. **ANDROID_ADAPTATION_GUIDE.md** - Technical details

---

## ✨ Key Features

### Desktop Version (Working Now)
- ✅ Auto login
- ✅ Daily commission (optional)
- ✅ Auto challenge (120 stamina)
- ✅ Smart speed control
- ✅ Smart auto-battle
- ✅ Loop farming
- ✅ Reward collection
- ✅ Gift check

### Android Version (Fully Adapted!)
- ✅ Screenshot (MediaProjection API)
- ✅ Click simulation (AccessibilityService)
- ✅ All desktop features supported
- ✅ Same codebase, cross-platform

---

## 🔧 Files You Can Delete (Optional)

These are documentation files. Deleting them won't affect functionality:

```
README_ANDROID.md                (info already in other docs)
使用说明.md                      (old manual, outdated)
项目文件清单.md                  (file list, for reference only)
Android适配完成总结.md           (summary, info in _Android适配完成_必读.md)
```

**But it's safe to keep them!** They contain useful information.

---

## ⚠️ Important Notes

### Permissions Required on Android

1. **Screen Recording Permission**
   - System will ask when app starts
   - Click "Start now"
   - Used for screenshot

2. **Accessibility Service**
   - Must enable manually in Settings
   - Settings → Accessibility → HSR Automation → Enable
   - Used for clicking

### First Build Takes Time

- **First build**: 30-60 minutes (downloads SDK/NDK)
- **Subsequent builds**: 5-10 minutes (much faster!)

---

## 🆘 Common Issues

### Issue: Window closes immediately
**Solution**: Use `check_docker_en.bat` to diagnose

### Issue: Garbled text in command window
**Solution**: Use English version scripts:
- `check_docker_en.bat`
- `build_android_en.bat`

### Issue: Build fails
**Solution**: 
1. Check error message
2. Read `构建问题排查指南.md`
3. Check log file: `build_log_*.txt`

---

## 📊 Quick Reference

```
┌─────────────────────────────────────────┐
│  Build Android APK - Quick Guide        │
├─────────────────────────────────────────┤
│  1. Check: check_docker_en.bat          │
│  2. Build: build_android_en.bat         │
│  3. Install: adb install bin\*.apk      │
└─────────────────────────────────────────┘

Requirements:
  ✓ Docker Desktop installed and running
  ✓ 5GB+ free disk space
  ✓ Stable internet connection

Build Time:
  First: 30-60 minutes
  Later: 5-10 minutes

Result:
  bin\hsrautomation-1.0-arm64-v8a-debug.apk
```

---

## 🎉 You're Ready!

Everything is prepared and ready to build. Just run:

1. `check_docker_en.bat` - Make sure everything is OK
2. `build_android_en.bat` - Build the APK
3. `adb install bin\*.apk` - Install to phone

**Good luck!** 🚀

---

**Last Updated**: 2025-10-06  
**Version**: 1.0  
**Status**: ✅ Production Ready




