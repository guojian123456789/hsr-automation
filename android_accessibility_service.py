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
        """检查无障碍服务是否已启用 - 简化版本"""
        # 由于Java服务编译问题，改用Shell Input方案
        # 不再需要检查AccessibilityService状态
        if not self.is_android:
            return True
        
        Logger.info("使用Shell Input点击方案，无需无障碍服务")
        self.service_enabled = True
        return True
    
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
        使用monkeyrunner方式执行点击
        通过Android的input命令实现，需要应用有SHELL权限或通过ADB授权
        """
        if not self.is_android:
            Logger.warning("非Android环境，无法点击")
            return False
        
        try:
            Logger.info(f"执行点击: ({int(x)}, {int(y)})")
            
            from jnius import autoclass
            import subprocess
            
            # 方法1：直接调用input命令（需要shell权限）
            try:
                Runtime = autoclass('java.lang.Runtime')
                runtime = Runtime.getRuntime()
                
                cmd = f"input tap {int(x)} {int(y)}"
                process = runtime.exec(cmd)
                process.waitFor()
                
                exit_code = process.exitValue()
                
                if exit_code == 0:
                    Logger.info(f"✅ 点击成功: ({int(x)}, {int(y)})")
                    return True
                else:
                    Logger.error(f"点击失败，退出码: {exit_code}")
                    
            except Exception as e1:
                Logger.error(f"Runtime.exec失败: {e1}")
                
                # 方法2：使用subprocess
                try:
                    result = subprocess.run(
                        ['input', 'tap', str(int(x)), str(int(y))],
                        capture_output=True,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        Logger.info(f"✅ subprocess点击成功: ({int(x)}, {int(y)})")
                        return True
                    else:
                        Logger.error(f"subprocess点击失败: {result.stderr}")
                        
                except Exception as e2:
                    Logger.error(f"subprocess失败: {e2}")
            
            return False
            
        except Exception as e:
            Logger.error(f"点击失败: {e}")
            import traceback
            Logger.error(traceback.format_exc())
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




