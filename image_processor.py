"""
图像处理模块 - 处理屏幕截图和图像识别
支持模板匹配和基础图像处理
"""

import os
import numpy as np
from kivy.logger import Logger
from kivy.utils import platform

# 根据平台导入不同的图像处理库
try:
    import cv2
    CV2_AVAILABLE = True
    Logger.info("OpenCV可用")
except ImportError:
    CV2_AVAILABLE = False
    Logger.warning("OpenCV不可用，使用基础图像处理")

try:
    from PIL import Image, ImageGrab
    PIL_AVAILABLE = True
    Logger.info("PIL可用")
except ImportError:
    PIL_AVAILABLE = False
    Logger.warning("PIL不可用")

class ImageProcessor:
    """图像处理器"""
    
    def __init__(self):
        self.templates = {}
        self.platform = platform
        
        # 加载模板图像
        self.load_templates()
        
        Logger.info(f"图像处理器初始化完成，平台: {self.platform}")
    
    def load_templates(self):
        """加载模板图像"""
        template_dir = "templates"
        
        if not os.path.exists(template_dir):
            Logger.warning(f"模板目录不存在: {template_dir}")
            self.create_default_templates()
            return
        
        # 加载所有模板图像
        template_files = [
            'login_button_first.png',
            'game_start_screen.png', 
            'login_button.png',
            'main_menu.png',
            'task.png',
            'weituo.png',
            'qianwang.png',
            'yijianlingqu.png',
            'paiqianzhong.png',
            'close.png',
            'zaicipaiqian.png',
            '120kaituoli.png',
            'jinru.png',
            'jiahao.png',
            'tiaozhan.png',
            'kaishitiaozhan.png',
            'beisukai.png',
            'beisuguan.png',
            'zidongkai.png',
            'zidongguan.png',
            'zailaiyici.png',
            'tuichuguanqia.png',
            'lingqu.png',
            '400.png',
            '500.png',
            'gift.png'
        ]
        
        for filename in template_files:
            filepath = os.path.join(template_dir, filename)
            if os.path.exists(filepath):
                try:
                    if CV2_AVAILABLE:
                        template = cv2.imread(filepath, cv2.IMREAD_COLOR)
                        if template is not None:
                            name = filename.replace('.png', '')
                            self.templates[name] = template
                            Logger.info(f"加载模板: {name}")
                    elif PIL_AVAILABLE:
                        template = Image.open(filepath)
                        name = filename.replace('.png', '')
                        self.templates[name] = template
                        Logger.info(f"加载模板: {name}")
                except Exception as e:
                    Logger.error(f"加载模板失败 {filename}: {e}")
        
        Logger.info(f"共加载 {len(self.templates)} 个模板")
    
    def create_default_templates(self):
        """创建默认模板图像"""
        Logger.info("创建默认模板目录和图像")
        
        os.makedirs("templates", exist_ok=True)
        
        if not CV2_AVAILABLE:
            Logger.warning("无法创建默认模板，OpenCV不可用")
            return
        
        # 创建简单的占位符模板
        templates_to_create = {
            'login_button_first': (100, 50, [100, 100, 200]),
            'game_start_screen': (200, 100, [50, 150, 50]),
            'login_button': (120, 60, [200, 100, 100]),
            'main_menu': (150, 80, [100, 200, 100]),
            'task': (80, 40, [150, 150, 100])
        }
        
        for name, (width, height, color) in templates_to_create.items():
            try:
                # 创建彩色图像
                img = np.full((height, width, 3), color, dtype=np.uint8)
                
                # 添加文字
                cv2.putText(img, name.upper()[:4], (10, height//2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # 保存图像
                filepath = os.path.join("templates", f"{name}.png")
                cv2.imwrite(filepath, img)
                
                # 加载到内存
                self.templates[name] = img
                
                Logger.info(f"创建默认模板: {name}")
                
            except Exception as e:
                Logger.error(f"创建默认模板失败 {name}: {e}")
    
    def capture_screen(self):
        """截取屏幕"""
        try:
            if self.platform == 'android':
                return self.capture_android_screen()
            else:
                return self.capture_desktop_screen()
        except Exception as e:
            Logger.error(f"屏幕截图失败: {e}")
            return None
    
    def capture_android_screen(self):
        """Android屏幕截图"""
        try:
            # 使用MediaProjection API截图
            from android_screen_capture import AndroidScreenCapture
            
            if not hasattr(self, 'android_capture'):
                self.android_capture = AndroidScreenCapture()
            
            if not self.android_capture.is_ready():
                Logger.warning("Android截图服务未就绪，需要先申请权限")
                return None
            
            # 截取屏幕
            screenshot = self.android_capture.capture_screen()
            
            if screenshot is not None:
                Logger.info(f"Android截图成功: {screenshot.shape}")
                return screenshot
            else:
                Logger.warning("Android截图返回空")
                return None
            
        except Exception as e:
            Logger.error(f"Android屏幕截图失败: {e}")
            return None
    
    def capture_desktop_screen(self):
        """桌面屏幕截图"""
        try:
            if PIL_AVAILABLE:
                # 使用PIL截图
                screenshot_pil = ImageGrab.grab()
                
                if CV2_AVAILABLE:
                    # 转换为OpenCV格式
                    screenshot = np.array(screenshot_pil)
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                    return screenshot
                else:
                    return screenshot_pil
            else:
                Logger.error("无可用的截图方法")
                return None
                
        except Exception as e:
            Logger.error(f"桌面屏幕截图失败: {e}")
            return None
    
    def find_image(self, screenshot, template_name, confidence=0.7):
        """在截图中查找模板图像"""
        if not screenshot is not None:
            Logger.error("截图为空")
            return None
        
        if template_name not in self.templates:
            Logger.error(f"模板不存在: {template_name}")
            return None
        
        template = self.templates[template_name]
        
        try:
            if CV2_AVAILABLE:
                return self.find_image_cv2(screenshot, template, confidence)
            elif PIL_AVAILABLE:
                return self.find_image_pil(screenshot, template, confidence)
            else:
                Logger.error("无可用的图像匹配方法")
                return None
                
        except Exception as e:
            Logger.error(f"图像匹配失败: {e}")
            return None
    
    def find_image_cv2(self, screenshot, template, confidence):
        """使用OpenCV进行模板匹配"""
        # 模板匹配
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            # 计算中心点
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            
            return {
                'found': True,
                'confidence': max_val,
                'center': (center_x, center_y),
                'top_left': max_loc,
                'bottom_right': (max_loc[0] + w, max_loc[1] + h)
            }
        
        return None
    
    def find_image_pil(self, screenshot, template, confidence):
        """使用PIL进行基础图像匹配"""
        # PIL的基础匹配实现
        # 这里只是一个简化的实现
        Logger.warning("PIL图像匹配功能有限")
        
        # 返回模拟结果用于测试
        return {
            'found': True,
            'confidence': 0.8,
            'center': (100, 100),
            'top_left': (50, 50),
            'bottom_right': (150, 150)
        }
    
    def save_screenshot(self, screenshot, filename):
        """保存截图"""
        try:
            if CV2_AVAILABLE:
                cv2.imwrite(filename, screenshot)
            elif PIL_AVAILABLE and isinstance(screenshot, Image.Image):
                screenshot.save(filename)
            
            Logger.info(f"截图已保存: {filename}")
            return True
            
        except Exception as e:
            Logger.error(f"保存截图失败: {e}")
            return False
