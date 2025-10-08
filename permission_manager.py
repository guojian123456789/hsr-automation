"""
Android权限自动请求管理器
应用启动时自动弹窗申请必要权限
"""

from kivy.logger import Logger
from kivy.utils import platform
from kivy.clock import Clock

class PermissionManager:
    """权限管理器 - 自动请求和管理所有Android权限"""
    
    def __init__(self, app):
        self.app = app
        self.is_android = platform == 'android'
        
        # 权限状态
        self.permissions = {
            'storage': False,
            'overlay': False,
            'accessibility': False,
            'media_projection': False  # 截图权限
        }
        
        # Android API
        if self.is_android:
            self._init_android_api()
        
        Logger.info("权限管理器初始化完成")
    
    def _init_android_api(self):
        """初始化Android API"""
        try:
            from android.permissions import request_permissions, Permission, check_permission
            from android import autoclass
            
            self.request_permissions = request_permissions
            self.Permission = Permission
            self.check_permission = check_permission
            
            # Android类
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Intent = autoclass('android.content.Intent')
            self.Settings = autoclass('android.provider.Settings')
            self.Build = autoclass('android.os.Build')
            self.Uri = autoclass('android.net.Uri')
            
            Logger.info("Android API初始化成功")
            
        except Exception as e:
            Logger.error(f"Android API初始化失败: {e}")
            self.is_android = False
    
    def request_all_permissions(self, callback=None):
        """
        启动时自动请求所有必要权限
        
        Args:
            callback: 权限请求完成后的回调函数
        """
        if not self.is_android:
            Logger.info("桌面环境，跳过权限请求")
            if callback:
                callback(True)
            return
        
        Logger.info("开始自动权限请求流程...")
        
        # 步骤1: 请求存储权限（会弹窗）
        self._request_storage_permission()
        
        # 步骤2: 延迟1秒后请求其他权限（避免弹窗冲突）
        Clock.schedule_once(lambda dt: self._request_other_permissions(callback), 1.0)
    
    def _request_storage_permission(self):
        """请求存储权限 - 会自动弹窗"""
        if not self.is_android:
            return
        
        try:
            Logger.info("📂 请求存储权限（弹窗）...")
            
            permissions = [
                self.Permission.WRITE_EXTERNAL_STORAGE,
                self.Permission.READ_EXTERNAL_STORAGE
            ]
            
            # 这会触发Android系统弹窗
            self.request_permissions(permissions, self._on_storage_permission_result)
            
        except Exception as e:
            Logger.error(f"请求存储权限失败: {e}")
    
    def _on_storage_permission_result(self, permissions, grant_results):
        """存储权限请求结果回调"""
        granted = all(grant_results)
        self.permissions['storage'] = granted
        
        if granted:
            Logger.info("✅ 存储权限已授予")
        else:
            Logger.warning("❌ 存储权限被拒绝")
    
    def _request_other_permissions(self, callback=None):
        """请求其他权限（需要跳转设置页面）"""
        if not self.is_android:
            return
        
        # 检查悬浮窗权限
        if not self._check_overlay_permission():
            Logger.info("🔲 悬浮窗权限未授予，准备引导用户...")
            self._show_overlay_permission_dialog()
        else:
            self.permissions['overlay'] = True
        
        # 检查无障碍服务
        if not self._check_accessibility_service():
            Logger.info("♿ 无障碍服务未开启，准备引导用户...")
            # 延迟显示，避免与悬浮窗权限对话框冲突
            Clock.schedule_once(lambda dt: self._show_accessibility_dialog(), 2.0)
        else:
            self.permissions['accessibility'] = True
        
        # 完成回调
        if callback:
            Clock.schedule_once(lambda dt: callback(self.all_permissions_granted()), 3.0)
    
    def _check_overlay_permission(self):
        """检查悬浮窗权限"""
        if not self.is_android:
            return True
        
        try:
            if self.Build.VERSION.SDK_INT >= 23:  # Android 6.0+
                return self.Settings.canDrawOverlays(self.PythonActivity.mActivity)
            return True
        except Exception as e:
            Logger.error(f"检查悬浮窗权限失败: {e}")
            return False
    
    def _check_accessibility_service(self):
        """检查无障碍服务"""
        if not self.is_android:
            return True
        
        try:
            from android_accessibility_service import AndroidAccessibilityService
            
            accessibility_service = AndroidAccessibilityService()
            is_enabled = accessibility_service.is_service_enabled()
            
            Logger.info(f"无障碍服务状态: {'已启用' if is_enabled else '未启用'}")
            return is_enabled
            
        except Exception as e:
            Logger.error(f"检查无障碍服务失败: {e}")
            return False
    
    def _show_overlay_permission_dialog(self):
        """显示悬浮窗权限引导对话框"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 说明文字
        label = Label(
            text='[size=16]需要悬浮窗权限[/size]\n\n'
                 '悬浮窗权限用于显示控制界面\n'
                 '点击下方按钮前往设置\n\n'
                 '[color=999999][size=12]在设置中找到本应用并开启权限[/size][/color]',
            markup=True,
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        
        # 按钮
        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
        
        go_btn = Button(
            text='前往设置',
            background_color=[0.3, 0.6, 1, 1],
            background_normal=''
        )
        
        cancel_btn = Button(
            text='稍后',
            background_color=[0.6, 0.6, 0.6, 1],
            background_normal=''
        )
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(go_btn)
        
        content.add_widget(label)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='权限请求',
            content=content,
            size_hint=(0.85, 0.5),
            auto_dismiss=False
        )
        
        def open_settings(instance):
            self.open_overlay_permission_settings()
            popup.dismiss()
        
        def dismiss_popup(instance):
            popup.dismiss()
        
        go_btn.bind(on_press=open_settings)
        cancel_btn.bind(on_press=dismiss_popup)
        
        popup.open()
    
    def _show_accessibility_dialog(self):
        """显示无障碍服务引导对话框"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 说明文字
        label = Label(
            text='[size=16]需要无障碍服务权限[/size]\n\n'
                 '[b]这是最重要的权限！[/b]\n'
                 '无障碍服务用于自动点击游戏\n'
                 '点击下方按钮前往设置\n\n'
                 '[color=999999][size=12]在无障碍设置中找到\n'
                 '"HSR Automation"并开启[/size][/color]',
            markup=True,
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        
        # 按钮
        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
        
        go_btn = Button(
            text='前往设置',
            background_color=[1, 0.4, 0.4, 1],  # 红色强调重要性
            background_normal=''
        )
        
        cancel_btn = Button(
            text='稍后',
            background_color=[0.6, 0.6, 0.6, 1],
            background_normal=''
        )
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(go_btn)
        
        content.add_widget(label)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='重要权限请求',
            content=content,
            size_hint=(0.85, 0.6),
            auto_dismiss=False
        )
        
        def open_settings(instance):
            self.open_accessibility_settings()
            popup.dismiss()
        
        def dismiss_popup(instance):
            popup.dismiss()
        
        go_btn.bind(on_press=open_settings)
        cancel_btn.bind(on_press=dismiss_popup)
        
        popup.open()
    
    def open_overlay_permission_settings(self):
        """打开悬浮窗权限设置页面"""
        if not self.is_android:
            Logger.warning("非Android环境，无法打开悬浮窗权限设置")
            return
        
        try:
            Logger.info("打开悬浮窗权限设置...")
            
            current_activity = self.PythonActivity.mActivity
            if current_activity is None:
                Logger.error("无法获取当前Activity")
                return
            
            # Android 6.0+ (API 23+) 需要特殊权限
            if self.Build.VERSION.SDK_INT >= 23:
                package_name = current_activity.getPackageName()
                Logger.info(f"应用包名: {package_name}")
                
                intent = self.Intent(self.Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
                intent.setData(self.Uri.parse(f"package:{package_name}"))
                
                # 添加FLAG_ACTIVITY_NEW_TASK标志
                intent.addFlags(0x10000000)  # Intent.FLAG_ACTIVITY_NEW_TASK
                
                current_activity.startActivity(intent)
                Logger.info("✅ 已打开悬浮窗权限设置")
            else:
                Logger.info("Android版本低于6.0，无需悬浮窗权限")
            
        except Exception as e:
            Logger.error(f"打开悬浮窗权限设置失败: {e}")
            import traceback
            Logger.error(traceback.format_exc())
    
    def open_accessibility_settings(self):
        """打开无障碍服务设置页面"""
        if not self.is_android:
            Logger.warning("非Android环境，无法打开无障碍服务设置")
            return
        
        try:
            Logger.info("打开无障碍服务设置...")
            
            current_activity = self.PythonActivity.mActivity
            if current_activity is None:
                Logger.error("无法获取当前Activity")
                return
            
            intent = self.Intent(self.Settings.ACTION_ACCESSIBILITY_SETTINGS)
            
            # 添加FLAG_ACTIVITY_NEW_TASK标志
            intent.addFlags(0x10000000)  # Intent.FLAG_ACTIVITY_NEW_TASK
            
            current_activity.startActivity(intent)
            
            Logger.info("✅ 已打开无障碍服务设置")
            
        except Exception as e:
            Logger.error(f"打开无障碍服务设置失败: {e}")
            import traceback
            Logger.error(traceback.format_exc())
    
    def request_media_projection(self):
        """请求截图权限（MediaProjection）"""
        if not self.is_android:
            return
        
        try:
            from android_screen_capture import AndroidScreenCapture
            
            screen_capture = AndroidScreenCapture()
            screen_capture.request_permission()
            
            Logger.info("已请求截图权限")
            
        except Exception as e:
            Logger.error(f"请求截图权限失败: {e}")
    
    def all_permissions_granted(self):
        """检查是否所有权限都已授予"""
        # 存储权限和无障碍服务是必需的
        required = ['storage', 'accessibility']
        return all(self.permissions.get(p, False) for p in required)
    
    def get_permission_status_text(self):
        """获取权限状态文本"""
        if not self.is_android:
            return "桌面环境，无需权限"
        
        status = []
        
        icons = {
            True: '✅',
            False: '❌'
        }
        
        status.append(f"{icons[self.permissions.get('storage', False)]} 存储权限")
        status.append(f"{icons[self.permissions.get('overlay', False)]} 悬浮窗权限")
        status.append(f"{icons[self.permissions.get('accessibility', False)]} 无障碍服务")
        
        return '\n'.join(status)
    
    def refresh_permissions(self):
        """刷新权限状态"""
        if not self.is_android:
            Logger.info("桌面环境，无需刷新权限")
            return
        
        Logger.info("🔄 开始刷新权限状态...")
        
        # 检查存储权限
        try:
            storage_granted = (
                self.check_permission(self.Permission.WRITE_EXTERNAL_STORAGE) and
                self.check_permission(self.Permission.READ_EXTERNAL_STORAGE)
            )
            self.permissions['storage'] = storage_granted
            Logger.info(f"存储权限: {'✅' if storage_granted else '❌'}")
        except Exception as e:
            Logger.error(f"检查存储权限失败: {e}")
        
        # 检查悬浮窗权限
        overlay_granted = self._check_overlay_permission()
        self.permissions['overlay'] = overlay_granted
        Logger.info(f"悬浮窗权限: {'✅' if overlay_granted else '❌'}")
        
        # 检查无障碍服务
        accessibility_enabled = self._check_accessibility_service()
        self.permissions['accessibility'] = accessibility_enabled
        Logger.info(f"无障碍服务: {'✅' if accessibility_enabled else '❌'}")
        
        Logger.info(f"✅ 权限状态刷新完成: {self.permissions}")
        
        return self.permissions

