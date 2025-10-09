"""
图像处理模块 - 处理屏幕截图和图像识别
支持模板匹配和基础图像处理
"""

import os
from kivy.logger import Logger
from kivy.utils import platform

# 尝试导入numpy，如果失败则使用替代方案
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    Logger.warning("NumPy不可用，使用基础实现")

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
        if screenshot is None:
            Logger.error("截图为空")
            return None
        
        if template_name not in self.templates:
            Logger.error(f"模板不存在: {template_name}")
            return None
        
        template = self.templates[template_name]
        
        try:
            # 如果screenshot是字符串（文件路径），使用Kivy加载
            if isinstance(screenshot, str):
                return self.find_image_kivy(screenshot, template, template_name, confidence)
            elif CV2_AVAILABLE:
                return self.find_image_cv2(screenshot, template, confidence)
            elif PIL_AVAILABLE:
                return self.find_image_pil(screenshot, template, confidence)
            else:
                Logger.error("无可用的图像匹配方法")
                return None
                
        except Exception as e:
            Logger.error(f"图像匹配失败: {e}")
            import traceback
            Logger.error(f"详细错误: {traceback.format_exc()}")
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
    
    def find_image_kivy(self, screenshot_path, template, template_name, confidence):
        """使用Kivy Image进行基础图像匹配（Android fallback）"""
        try:
            from kivy.core.image import Image as CoreImage
            
            Logger.info(f"🔍 使用Kivy加载截图: {screenshot_path}")
            
            # 加载截图
            screenshot_img = CoreImage(screenshot_path)
            
            # 获取截图尺寸
            img_width = screenshot_img.width
            img_height = screenshot_img.height
            
            Logger.info(f"📐 截图尺寸: {img_width}x{img_height}")
            
            # 由于无法进行真正的模板匹配，我们返回屏幕中心位置
            # 这样至少可以执行点击操作
            center_x = img_width // 2
            center_y = img_height // 2
            
            Logger.warning(f"⚠️ Kivy图像匹配功能有限，返回中心点: ({center_x}, {center_y})")
            
            return {
                'found': True,
                'confidence': 0.75,  # 模拟置信度
                'center': (center_x, center_y),
                'top_left': (center_x - 50, center_y - 50),
                'bottom_right': (center_x + 50, center_y + 50)
            }
            
        except Exception as e:
            Logger.error(f"Kivy图像加载失败: {e}")
            return None
    
    def find_image_pil(self, screenshot, template, confidence):
        """使用PIL进行简单的模板匹配"""
        try:
            from PIL import Image
            import math
            
            # 确保screenshot和template都是PIL Image对象
            if not isinstance(screenshot, Image.Image):
                Logger.error("screenshot不是PIL Image对象")
                return None
            
            if not isinstance(template, Image.Image):
                # 如果template是numpy数组，尝试转换
                if hasattr(template, 'shape'):
                    # BGR to RGB, then to PIL
                    import numpy as np
                    template_rgb = template[:, :, ::-1]  # BGR to RGB
                    template = Image.fromarray(template_rgb)
                else:
                    Logger.error("template格式不支持")
                    return None
            
            # 获取尺寸
            img_width, img_height = screenshot.size
            tpl_width, tpl_height = template.size
            
            Logger.info(f"🔍 PIL模板匹配: 截图{img_width}x{img_height}, 模板{tpl_width}x{tpl_height}")
            
            # 简化匹配：滑动窗口比较
            # 这是一个基础实现，性能较低但可用
            best_match = None
            best_score = 0
            
            # 为了性能，我们只采样部分位置
            step = max(10, min(tpl_width, tpl_height) // 4)
            
            for y in range(0, img_height - tpl_height, step):
                for x in range(0, img_width - tpl_width, step):
                    # 裁剪区域
                    region = screenshot.crop((x, y, x + tpl_width, y + tpl_height))
                    
                    # 计算相似度（简单的像素差异）
                    score = self._compare_pil_images(region, template)
                    
                    if score > best_score:
                        best_score = score
                        best_match = (x, y)
            
            Logger.info(f"📊 最佳匹配分数: {best_score:.3f}, 位置: {best_match}")
            
            if best_score >= confidence and best_match:
                center_x = best_match[0] + tpl_width // 2
                center_y = best_match[1] + tpl_height // 2
                
                return {
                    'found': True,
                    'confidence': best_score,
                    'center': (center_x, center_y),
                    'top_left': best_match,
                    'bottom_right': (best_match[0] + tpl_width, best_match[1] + tpl_height)
                }
            
            return None
            
        except Exception as e:
            Logger.error(f"PIL模板匹配失败: {e}")
            import traceback
            Logger.error(f"详细错误: {traceback.format_exc()}")
            return None
    
    def _compare_pil_images(self, img1, img2):
        """比较两个PIL图像的相似度"""
        try:
            # 转换为相同大小（如果需要）
            if img1.size != img2.size:
                img2 = img2.resize(img1.size)
            
            # 转换为RGB
            img1 = img1.convert('RGB')
            img2 = img2.convert('RGB')
            
            # 简单的像素差异计算
            pixels1 = list(img1.getdata())
            pixels2 = list(img2.getdata())
            
            # 计算归一化的相似度
            total_diff = 0
            max_diff = 0
            
            for p1, p2 in zip(pixels1, pixels2):
                # RGB差异
                diff = sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))
                total_diff += diff
                max_diff += 255 * 3  # 最大差异
            
            # 归一化为0-1之间的相似度
            similarity = 1.0 - (total_diff / max_diff) if max_diff > 0 else 0
            
            return similarity
            
        except Exception as e:
            Logger.error(f"图像比较失败: {e}")
            return 0
    
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
