"""
Android无障碍服务模块
使用AccessibilityService实现模拟点击和手势功能
"""

from kivy.logger import Logger
from kivy.utils import platform

class AndroidAccessibilityService:
    """Android无障碍服务类"""
    
    def __init__(self):
        self.is_android = platform == 'android'
        self.service_enabled = False
        self.gesture_description = None
        
        if self.is_android:
            self.init_accessibility_service()
        
        Logger.info(f"Android无障碍服务初始化，是否为Android: {self.is_android}")
    
    def init_accessibility_service(self):
        """初始化无障碍服务"""
        try:
            from jnius import autoclass, PythonJavaClass, java_method
            
            # 获取Android类
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.AccessibilityService = autoclass('android.accessibilityservice.AccessibilityService')
            self.GestureDescription = autoclass('android.accessibilityservice.GestureDescription')
            self.GestureDescriptionBuilder = autoclass('android.accessibilityservice.GestureDescription$Builder')
            self.Path = autoclass('android.graphics.Path')
            self.GestureResultCallback = autoclass('android.accessibilityservice.AccessibilityService$GestureResultCallback')
            self.Context = autoclass('android.content.Context')
            self.Settings = autoclass('android.provider.Settings')
            self.Intent = autoclass('android.content.Intent')
            self.AccessibilityManager = autoclass('android.view.accessibility.AccessibilityManager')
            
            self.activity = self.PythonActivity.mActivity
            
            Logger.info("无障碍服务类加载成功")
            
        except Exception as e:
            Logger.error(f"无障碍服务初始化失败: {e}")
            self.is_android = False
    
    def check_service_enabled(self):
        """检查无障碍服务是否已启用"""
        if not self.is_android:
            return True
        
        try:
            # 获取AccessibilityManager
            accessibility_manager = self.activity.getSystemService(
                self.Context.ACCESSIBILITY_SERVICE
            )
            
            # 检查服务是否启用
            enabled_services = self.Settings.Secure.getString(
                self.activity.getContentResolver(),
                self.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
            )
            
            if enabled_services:
                # 检查我们的服务是否在列表中
                package_name = self.activity.getPackageName()
                service_name = f"{package_name}/com.hsr.automation.HSRAccessibilityService"
                
                self.service_enabled = service_name in enabled_services
                Logger.info(f"无障碍服务状态: {'已启用' if self.service_enabled else '未启用'}")
            else:
                self.service_enabled = False
                Logger.info("无障碍服务未启用")
            
            return self.service_enabled
            
        except Exception as e:
            Logger.error(f"检查无障碍服务状态失败: {e}")
            return False
    
    def request_service_permission(self):
        """请求开启无障碍服务"""
        if not self.is_android:
            return True
        
        try:
            Logger.info("请求开启无障碍服务")
            
            # 打开无障碍设置页面
            intent = self.Intent(self.Settings.ACTION_ACCESSIBILITY_SETTINGS)
            self.activity.startActivity(intent)
            
            Logger.info("已打开无障碍服务设置页面")
            return True
            
        except Exception as e:
            Logger.error(f"请求无障碍服务失败: {e}")
            return False
    
    def click(self, x, y, duration=100):
        """
        在指定位置执行点击
        
        参数:
            x: X坐标
            y: Y坐标
            duration: 点击持续时间（毫秒）
        """
        if not self.is_android:
            Logger.warning("非Android环境，无法使用无障碍服务点击")
            return False
        
        if not self.service_enabled:
            Logger.warning("无障碍服务未启用")
            return False
        
        try:
            Logger.info(f"执行点击: ({x}, {y}), 持续时间: {duration}ms")
            
            # 创建点击手势路径
            path = self.Path()
            path.moveTo(float(x), float(y))
            
            # 创建手势描述
            builder = self.GestureDescriptionBuilder()
            
            # 添加手势
            from jnius import autoclass
            StrokeDescription = autoclass('android.accessibilityservice.GestureDescription$StrokeDescription')
            
            stroke = StrokeDescription(path, 0, duration)
            builder.addStroke(stroke)
            
            gesture = builder.build()
            
            # 执行手势
            # 注意：这需要在实际的AccessibilityService实例中调用
            # 这里我们通过广播或其他方式通知Service执行
            self.dispatch_gesture(gesture)
            
            Logger.info("点击手势已发送")
            return True
            
        except Exception as e:
            Logger.error(f"执行点击失败: {e}")
            return False
    
    def swipe(self, start_x, start_y, end_x, end_y, duration=300):
        """
        执行滑动手势
        
        参数:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
            duration: 滑动持续时间（毫秒）
        """
        if not self.is_android:
            Logger.warning("非Android环境，无法使用无障碍服务滑动")
            return False
        
        if not self.service_enabled:
            Logger.warning("无障碍服务未启用")
            return False
        
        try:
            Logger.info(f"执行滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
            
            # 创建滑动路径
            path = self.Path()
            path.moveTo(float(start_x), float(start_y))
            path.lineTo(float(end_x), float(end_y))
            
            # 创建手势描述
            builder = self.GestureDescriptionBuilder()
            
            from jnius import autoclass
            StrokeDescription = autoclass('android.accessibilityservice.GestureDescription$StrokeDescription')
            
            stroke = StrokeDescription(path, 0, duration)
            builder.addStroke(stroke)
            
            gesture = builder.build()
            
            # 执行手势
            self.dispatch_gesture(gesture)
            
            Logger.info("滑动手势已发送")
            return True
            
        except Exception as e:
            Logger.error(f"执行滑动失败: {e}")
            return False
    
    def dispatch_gesture(self, gesture):
        """
        分发手势到无障碍服务
        
        注意：这需要在实际的Service中实现
        这里通过广播或绑定服务的方式通知Service执行手势
        """
        try:
            # 方案1：通过广播发送
            from jnius import autoclass
            
            Intent = autoclass('android.content.Intent')
            Bundle = autoclass('android.os.Bundle')
            
            intent = Intent("com.hsr.automation.DISPATCH_GESTURE")
            intent.setPackage(self.activity.getPackageName())
            
            # 将手势信息放入Intent
            # 注意：实际实现需要序列化手势数据
            
            self.activity.sendBroadcast(intent)
            
            Logger.info("已通过广播发送手势")
            
        except Exception as e:
            Logger.error(f"分发手势失败: {e}")
    
    def is_ready(self):
        """检查服务是否已准备好"""
        return self.service_enabled




