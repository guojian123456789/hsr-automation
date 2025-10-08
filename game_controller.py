"""
游戏控制模块 - 处理点击、滑动等操作
支持桌面和Android环境
"""

import time
import random
from kivy.logger import Logger
from kivy.utils import platform

# 根据平台导入不同的控制库
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    Logger.info("PyAutoGUI可用")
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    Logger.warning("PyAutoGUI不可用")

class GameController:
    """游戏控制器"""
    
    def __init__(self):
        self.platform = platform
        self.screen_size = (1920, 1080)  # 默认屏幕尺寸
        
        if self.platform == 'android':
            self.init_android_controller()
        else:
            self.init_desktop_controller()
        
        Logger.info(f"游戏控制器初始化完成，平台: {self.platform}")
    
    def init_android_controller(self):
        """初始化Android控制器"""
        try:
            # TODO: 初始化Android无障碍服务
            Logger.info("初始化Android控制器")
            
            # 这里应该初始化无障碍服务连接
            # 获取屏幕尺寸等信息
            
        except Exception as e:
            Logger.error(f"Android控制器初始化失败: {e}")
    
    def init_desktop_controller(self):
        """初始化桌面控制器"""
        try:
            if PYAUTOGUI_AVAILABLE:
                # 设置PyAutoGUI参数
                pyautogui.FAILSAFE = True
                pyautogui.PAUSE = 0.1
                
                # 获取屏幕尺寸
                self.screen_size = pyautogui.size()
                Logger.info(f"桌面屏幕尺寸: {self.screen_size}")
            
        except Exception as e:
            Logger.error(f"桌面控制器初始化失败: {e}")
    
    def click_position(self, position):
        """点击指定位置"""
        try:
            x, y = position
            
            # 添加随机偏移
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            
            final_x = max(0, min(self.screen_size[0], x + offset_x))
            final_y = max(0, min(self.screen_size[1], y + offset_y))
            
            Logger.info(f"点击位置: ({final_x}, {final_y})")
            
            if self.platform == 'android':
                return self.android_click(final_x, final_y)
            else:
                return self.desktop_click(final_x, final_y)
                
        except Exception as e:
            Logger.error(f"点击操作失败: {e}")
            return False
    
    def click_center(self):
        """点击屏幕中央"""
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2
        
        return self.click_position((center_x, center_y))
    
    def android_click(self, x, y):
        """Android点击实现 - 使用无障碍服务"""
        try:
            Logger.info(f"Android点击: ({x}, {y})")
            
            # 使用无障碍服务执行点击
            from android_accessibility_service import AndroidAccessibilityService
            from jnius import autoclass
            
            if not hasattr(self, 'android_accessibility'):
                self.android_accessibility = AndroidAccessibilityService()
            
            # 检查服务是否已启用
            if not self.android_accessibility.check_service_enabled():
                Logger.warning("无障碍服务未启用，无法执行点击")
                return False
            
            # 通过广播发送点击指令
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent("com.hsr.automation.CLICK")
            intent.setPackage(PythonActivity.mActivity.getPackageName())
            intent.putExtra("x", float(x))
            intent.putExtra("y", float(y))
            intent.putExtra("duration", 100)
            
            PythonActivity.mActivity.sendBroadcast(intent)
            
            Logger.info(f"Android点击指令已发送: ({x}, {y})")
            time.sleep(0.1)  # 等待点击完成
            return True
            
        except Exception as e:
            Logger.error(f"Android点击失败: {e}")
            return False
    
    def desktop_click(self, x, y):
        """桌面点击实现 - 针对桌面游戏优化"""
        try:
            Logger.info(f"点击位置: ({x}, {y})")
            
            # 方法1: 尝试Windows API点击（对桌面游戏最有效）
            try:
                import win32api
                import win32con
                
                # 移动鼠标到目标位置
                win32api.SetCursorPos((x, y))
                time.sleep(0.1)
                
                # 执行点击
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                time.sleep(0.05)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                
                Logger.info(f"Windows API点击成功: ({x}, {y})")
                return True
                
            except ImportError:
                Logger.warning("win32api不可用，尝试PyAutoGUI")
            except Exception as e:
                Logger.warning(f"Windows API点击失败: {e}，尝试PyAutoGUI")
            
            # 方法2: 备用PyAutoGUI点击
            if PYAUTOGUI_AVAILABLE:
                pyautogui.FAILSAFE = False
                pyautogui.PAUSE = 0
                
                # 多次点击确保生效
                for i in range(3):
                    pyautogui.click(x, y, duration=0)
                    time.sleep(0.05)
                
                Logger.info(f"PyAutoGUI点击成功: ({x}, {y})")
                return True
            else:
                Logger.error("所有点击方法都不可用")
                return False
                
        except Exception as e:
            Logger.error(f"桌面点击失败: {e}")
            return False
    
    def swipe(self, start_pos, end_pos, duration=1.0):
        """滑动操作"""
        try:
            start_x, start_y = start_pos
            end_x, end_y = end_pos
            
            Logger.info(f"滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
            
            if self.platform == 'android':
                return self.android_swipe(start_x, start_y, end_x, end_y, duration)
            else:
                return self.desktop_swipe(start_x, start_y, end_x, end_y, duration)
                
        except Exception as e:
            Logger.error(f"滑动操作失败: {e}")
            return False
    
    def android_swipe(self, start_x, start_y, end_x, end_y, duration):
        """Android滑动实现"""
        try:
            # TODO: 使用无障碍服务执行滑动
            Logger.info(f"Android滑动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
            
            # 模拟滑动成功
            time.sleep(duration)
            return True
            
        except Exception as e:
            Logger.error(f"Android滑动失败: {e}")
            return False
    
    def desktop_swipe(self, start_x, start_y, end_x, end_y, duration):
        """桌面滑动实现（拖拽）"""
        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.drag(end_x - start_x, end_y - start_y, duration, button='left')
                Logger.info(f"桌面拖拽成功")
                return True
            else:
                Logger.error("PyAutoGUI不可用，无法执行拖拽")
                return False
                
        except Exception as e:
            Logger.error(f"桌面拖拽失败: {e}")
            return False
    
    def long_press(self, position, duration=2.0):
        """长按操作"""
        try:
            x, y = position
            
            Logger.info(f"长按: ({x}, {y})，持续 {duration} 秒")
            
            if self.platform == 'android':
                return self.android_long_press(x, y, duration)
            else:
                return self.desktop_long_press(x, y, duration)
                
        except Exception as e:
            Logger.error(f"长按操作失败: {e}")
            return False
    
    def android_long_press(self, x, y, duration):
        """Android长按实现"""
        try:
            # TODO: 使用无障碍服务执行长按
            Logger.info(f"Android长按: ({x}, {y})")
            
            # 模拟长按成功
            time.sleep(duration)
            return True
            
        except Exception as e:
            Logger.error(f"Android长按失败: {e}")
            return False
    
    def desktop_long_press(self, x, y, duration):
        """桌面长按实现"""
        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.mouseDown(x, y, button='left')
                time.sleep(duration)
                pyautogui.mouseUp(x, y, button='left')
                Logger.info(f"桌面长按成功")
                return True
            else:
                Logger.error("PyAutoGUI不可用，无法执行长按")
                return False
                
        except Exception as e:
            Logger.error(f"桌面长按失败: {e}")
            return False
    
    def wait(self, seconds):
        """等待指定时间"""
        Logger.info(f"等待 {seconds} 秒")
        time.sleep(seconds)
    
    def get_screen_size(self):
        """获取屏幕尺寸"""
        return self.screen_size
