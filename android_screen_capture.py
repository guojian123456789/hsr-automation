"""
Android屏幕截图模块
使用MediaProjection API实现屏幕截图功能
"""

from kivy.logger import Logger
from kivy.utils import platform
import numpy as np

class AndroidScreenCapture:
    """Android屏幕截图类"""
    
    def __init__(self):
        self.is_android = platform == 'android'
        self.media_projection = None
        self.virtual_display = None
        self.image_reader = None
        self.permission_granted = False
        
        if self.is_android:
            self.init_media_projection()
        
        Logger.info(f"Android截图模块初始化，是否为Android: {self.is_android}")
    
    def init_media_projection(self):
        """初始化MediaProjection"""
        try:
            from jnius import autoclass, cast
            
            # 获取Android类
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.MediaProjectionManager = autoclass('android.media.projection.MediaProjectionManager')
            self.Context = autoclass('android.content.Context')
            self.Intent = autoclass('android.content.Intent')
            self.ImageReader = autoclass('android.media.ImageReader')
            self.PixelFormat = autoclass('android.graphics.PixelFormat')
            self.DisplayMetrics = autoclass('android.util.DisplayMetrics')
            self.WindowManager = autoclass('android.view.WindowManager')
            
            # 获取Activity和Context
            self.activity = self.PythonActivity.mActivity
            self.context = cast('android.content.Context', self.activity)
            
            # 获取MediaProjectionManager
            self.projection_manager = self.context.getSystemService(
                self.Context.MEDIA_PROJECTION_SERVICE
            )
            
            # 获取屏幕尺寸
            self.get_screen_size()
            
            Logger.info("MediaProjection初始化成功")
            
        except Exception as e:
            Logger.error(f"MediaProjection初始化失败: {e}")
            self.is_android = False
    
    def get_screen_size(self):
        """获取屏幕尺寸"""
        try:
            window_manager = self.context.getSystemService(self.Context.WINDOW_SERVICE)
            display = window_manager.getDefaultDisplay()
            metrics = self.DisplayMetrics()
            display.getRealMetrics(metrics)
            
            self.screen_width = metrics.widthPixels
            self.screen_height = metrics.heightPixels
            self.screen_density = metrics.densityDpi
            
            Logger.info(f"屏幕尺寸: {self.screen_width}x{self.screen_height}, DPI: {self.screen_density}")
            
        except Exception as e:
            Logger.error(f"获取屏幕尺寸失败: {e}")
            self.screen_width = 1080
            self.screen_height = 1920
            self.screen_density = 320
    
    def request_permission(self):
        """请求屏幕录制权限"""
        if not self.is_android:
            return True
        
        try:
            Logger.info("请求屏幕录制权限")
            
            # 创建权限请求Intent
            capture_intent = self.projection_manager.createScreenCaptureIntent()
            
            # 启动权限请求Activity
            # 注意：这需要在自定义的Activity中处理onActivityResult
            self.activity.startActivityForResult(capture_intent, 1001)
            
            Logger.info("已发起屏幕录制权限请求")
            return True
            
        except Exception as e:
            Logger.error(f"请求屏幕录制权限失败: {e}")
            return False
    
    def start_capture(self, result_code, data_intent):
        """
        开始截图
        
        参数:
            result_code: Activity返回的结果代码
            data_intent: Activity返回的Intent数据
        """
        if not self.is_android:
            return False
        
        try:
            Logger.info("开始初始化屏幕截图")
            
            # 创建MediaProjection
            self.media_projection = self.projection_manager.getMediaProjection(
                result_code, 
                data_intent
            )
            
            if not self.media_projection:
                Logger.error("创建MediaProjection失败")
                return False
            
            # 创建ImageReader
            self.image_reader = self.ImageReader.newInstance(
                self.screen_width,
                self.screen_height,
                self.PixelFormat.RGBA_8888,
                2  # maxImages
            )
            
            # 创建VirtualDisplay
            self.virtual_display = self.media_projection.createVirtualDisplay(
                "ScreenCapture",
                self.screen_width,
                self.screen_height,
                self.screen_density,
                0,  # flags
                self.image_reader.getSurface(),
                None,  # callback
                None   # handler
            )
            
            self.permission_granted = True
            Logger.info("屏幕截图初始化成功")
            return True
            
        except Exception as e:
            Logger.error(f"开始截图失败: {e}")
            return False
    
    def capture_screen(self):
        """
        截取当前屏幕
        
        返回:
            numpy array: BGR格式的图像数据，与OpenCV兼容
        """
        if not self.is_android:
            Logger.warning("非Android环境，无法使用MediaProjection截图")
            return None
        
        if not self.permission_granted:
            Logger.warning("屏幕录制权限未授予")
            return None
        
        try:
            # 获取最新的Image
            image = self.image_reader.acquireLatestImage()
            
            if not image:
                Logger.warning("未能获取屏幕图像")
                return None
            
            # 获取Image的Plane
            planes = image.getPlanes()
            if not planes or len(planes) == 0:
                image.close()
                return None
            
            plane = planes[0]
            buffer = plane.getBuffer()
            
            # 获取图像数据
            pixel_stride = plane.getPixelStride()
            row_stride = plane.getRowStride()
            row_padding = row_stride - pixel_stride * self.screen_width
            
            # 将Buffer转换为numpy array
            # 注意：这里需要使用pyjnius的buffer转换功能
            from jnius import cast
            import array
            
            # 读取buffer数据
            buffer_size = buffer.remaining()
            byte_array = array.array('b', [0] * buffer_size)
            
            # 复制数据
            for i in range(buffer_size):
                byte_array[i] = buffer.get(i)
            
            # 转换为numpy array
            img_array = np.frombuffer(byte_array, dtype=np.uint8)
            
            # 重塑为图像格式 (height, width, channels)
            # RGBA格式，4个通道
            img_height = self.screen_height
            img_width = self.screen_width + row_padding // pixel_stride
            
            img_array = img_array.reshape((img_height, img_width, 4))
            
            # 裁剪到实际宽度
            img_array = img_array[:, :self.screen_width, :]
            
            # 转换RGBA到BGR（OpenCV格式）
            # RGBA -> BGR
            bgr_image = img_array[:, :, [2, 1, 0]]  # 只取RGB，转为BGR
            
            # 关闭Image
            image.close()
            
            Logger.info(f"成功截取屏幕: {bgr_image.shape}")
            return bgr_image
            
        except Exception as e:
            Logger.error(f"截取屏幕失败: {e}")
            return None
    
    def stop_capture(self):
        """停止截图"""
        try:
            if self.virtual_display:
                self.virtual_display.release()
                self.virtual_display = None
            
            if self.image_reader:
                self.image_reader.close()
                self.image_reader = None
            
            if self.media_projection:
                self.media_projection.stop()
                self.media_projection = None
            
            self.permission_granted = False
            Logger.info("已停止屏幕截图")
            
        except Exception as e:
            Logger.error(f"停止截图失败: {e}")
    
    def is_ready(self):
        """检查是否已准备好截图"""
        return self.permission_granted and self.media_projection is not None




