"""
Android工具模块 - 处理Android特定功能
包括权限管理、无障碍服务等
"""

from kivy.logger import Logger
from kivy.utils import platform

class AndroidUtils:
    """Android工具类"""
    
    def __init__(self):
        self.is_android = platform == 'android'
        self.permissions = {
            'overlay': False,
            'accessibility': False,
            'storage': False
        }
        
        if self.is_android:
            self.init_android_services()
        
        Logger.info(f"Android工具初始化完成，是否为Android: {self.is_android}")
    
    def init_android_services(self):
        """初始化Android服务"""
        try:
            # 尝试导入Android相关模块
            from android.permissions import request_permissions, Permission
            from android import autoclass
            
            self.request_permissions = request_permissions
            self.Permission = Permission
            
            # 获取Android类
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Context = autoclass('android.content.Context')
            self.Intent = autoclass('android.content.Intent')
            self.Settings = autoclass('android.provider.Settings')
            
            Logger.info("Android服务初始化成功")
            
        except ImportError as e:
            Logger.error(f"Android模块导入失败: {e}")
            self.is_android = False
    
    def check_permissions(self):
        """检查所有必要权限 - 使用Runtime.exec方案，只需存储权限"""
        if not self.is_android:
            return True
        
        try:
            # 只检查存储权限
            self.permissions['storage'] = self.check_storage_permission()
            
            # Runtime.exec方案不需要悬浮窗和无障碍服务
            self.permissions['overlay'] = True
            self.permissions['accessibility'] = True
            
            Logger.info(f"权限检查结果: 存储={self.permissions['storage']}")
            
            # 只要有存储权限就可以运行
            return self.permissions['storage']
            
        except Exception as e:
            Logger.error(f"权限检查失败: {e}")
            return False
    
    def check_overlay_permission(self):
        """检查悬浮窗权限"""
        if not self.is_android:
            return True
        
        try:
            # TODO: 实现悬浮窗权限检查
            Logger.info("检查悬浮窗权限")
            return False  # 默认返回False，需要用户手动授权
            
        except Exception as e:
            Logger.error(f"检查悬浮窗权限失败: {e}")
            return False
    
    def check_accessibility_service(self):
        """检查无障碍服务是否开启"""
        if not self.is_android:
            return True
        
        try:
            # TODO: 实现无障碍服务状态检查
            Logger.info("检查无障碍服务状态")
            return False  # 默认返回False，需要用户手动开启
            
        except Exception as e:
            Logger.error(f"检查无障碍服务失败: {e}")
            return False
    
    def check_storage_permission(self):
        """检查存储权限"""
        if not self.is_android:
            return True
        
        try:
            # TODO: 实现存储权限检查
            Logger.info("检查存储权限")
            return True  # 存储权限通常在安装时已授予
            
        except Exception as e:
            Logger.error(f"检查存储权限失败: {e}")
            return False
    
    def request_overlay_permission(self):
        """请求悬浮窗权限"""
        if not self.is_android:
            return True
        
        try:
            Logger.info("请求悬浮窗权限")
            
            # 打开悬浮窗权限设置页面
            intent = self.Intent(self.Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
            self.PythonActivity.mActivity.startActivity(intent)
            
            Logger.info("已打开悬浮窗权限设置页面")
            return True
            
        except Exception as e:
            Logger.error(f"请求悬浮窗权限失败: {e}")
            return False
    
    def request_accessibility_service(self):
        """请求无障碍服务权限"""
        if not self.is_android:
            return True
        
        try:
            Logger.info("请求无障碍服务权限")
            
            # 打开无障碍服务设置页面
            intent = self.Intent(self.Settings.ACTION_ACCESSIBILITY_SETTINGS)
            self.PythonActivity.mActivity.startActivity(intent)
            
            Logger.info("已打开无障碍服务设置页面")
            return True
            
        except Exception as e:
            Logger.error(f"请求无障碍服务权限失败: {e}")
            return False
    
    def request_storage_permission(self):
        """请求存储权限"""
        if not self.is_android:
            return True
        
        try:
            Logger.info("请求存储权限")
            
            # 请求存储权限
            self.request_permissions([
                self.Permission.WRITE_EXTERNAL_STORAGE,
                self.Permission.READ_EXTERNAL_STORAGE
            ])
            
            Logger.info("已请求存储权限")
            return True
            
        except Exception as e:
            Logger.error(f"请求存储权限失败: {e}")
            return False
    
    def get_permission_status(self):
        """获取权限状态文本"""
        if not self.is_android:
            return "桌面环境，无需特殊权限"
        
        status_lines = []
        
        # 悬浮窗权限
        overlay_status = "✅ 已授予" if self.permissions['overlay'] else "❌ 未授予"
        status_lines.append(f"悬浮窗权限: {overlay_status}")
        
        # 无障碍服务
        accessibility_status = "✅ 已开启" if self.permissions['accessibility'] else "❌ 未开启"
        status_lines.append(f"无障碍服务: {accessibility_status}")
        
        # 存储权限
        storage_status = "✅ 已授予" if self.permissions['storage'] else "❌ 未授予"
        status_lines.append(f"存储权限: {storage_status}")
        
        return "\n".join(status_lines)
    
    def get_permission_guide(self):
        """获取权限设置指南"""
        if not self.is_android:
            return "桌面环境无需特殊权限设置"
        
        guide = """📱 Android权限设置指南

🔹 悬浮窗权限
• 用途: 允许应用在其他应用上显示界面
• 设置: 点击"开启悬浮窗权限"按钮
• 操作: 在设置中找到本应用并开启权限

🔹 无障碍服务  
• 用途: 允许应用模拟点击和获取界面信息
• 设置: 点击"开启无障碍服务"按钮
• 操作: 在无障碍设置中找到本应用并开启服务

🔹 存储权限
• 用途: 保存配置文件和日志
• 设置: 通常在安装时已自动授予

⚠️ 重要提醒:
• 这些权限仅用于游戏自动化功能
• 不会收集或上传任何个人信息
• 可以随时在设置中关闭权限"""
        
        return guide
    
    def is_permission_granted(self, permission_type):
        """检查特定权限是否已授予"""
        return self.permissions.get(permission_type, False)
    
    def refresh_permissions(self):
        """刷新权限状态"""
        Logger.info("刷新权限状态")
        return self.check_permissions()
