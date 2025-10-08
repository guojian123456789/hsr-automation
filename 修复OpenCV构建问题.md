# 🔧 OpenCV 构建失败 - 解决方案

## ❌ 问题

**错误**: OpenCV 在 Android 上构建失败
- OpenCV 需要复杂的 C++ 编译
- buildozer 对 OpenCV 支持不完善
- 构建时间过长，容易超时

---

## ✅ 解决方案

### **方案1: 移除 OpenCV（推荐）** ⭐

**原理**: 代码已经有 PIL fallback，直接移除 OpenCV 依赖

**优点**:
- ✅ 构建速度快（5-15分钟）
- ✅ APK 体积小（减少 ~30MB）
- ✅ 更稳定可靠

**缺点**:
- ⚠️ PIL 的模板匹配功能有限
- ⚠️ 识别精度可能略低

**已应用**: 
```diff
- requirements = python3,kivy,numpy,pillow,opencv,pyyaml,pyjnius
+ requirements = python3,kivy,numpy,pillow,pyyaml,pyjnius
```

---

### **方案2: 使用预编译的 OpenCV（复杂）**

创建自定义 recipe:

```python
# buildozer.spec
android.gradle_dependencies = org.opencv:opencv:4.5.3
```

**复杂度**: 高
**成功率**: 中等

---

### **方案3: 纯 NumPy 实现模板匹配**

使用 NumPy 实现简单的模板匹配：

```python
def find_image_numpy(screenshot, template):
    # 使用互相关进行匹配
    from scipy.signal import correlate2d
    result = correlate2d(screenshot, template)
    ...
```

**问题**: 需要 scipy（也难编译）

---

## 🎯 当前策略

**采用方案1**: 移除 OpenCV

### 步骤:
1. ✅ 从 buildozer.spec 移除 opencv
2. ⏳ 提交并推送
3. ⏳ 等待构建（预计 10-15 分钟）

### 构建成功后:
- 桌面版: 继续使用 OpenCV（如果已安装）
- Android 版: 使用 PIL fallback

---

## 📝 未来改进

如果需要更好的图像识别：

1. **使用服务器端识别**
   - Android 截图 → 上传到服务器
   - 服务器用 OpenCV 处理
   - 返回结果给 Android

2. **使用 TensorFlow Lite**
   - 训练模型识别游戏元素
   - 在 Android 上运行轻量模型

3. **坐标缓存**
   - 第一次手动标记位置
   - 后续直接点击固定坐标

---

**当前方案足够实现基本功能！** ✅

