"""
游戏启动器 - 自动启动和切换到游戏
"""

from kivy.logger import Logger
from kivy.utils import platform
import time

class GameLauncher:
    """游戏启动器 - 自动打开游戏应用"""
    
    def __init__(self):
        self.is_android = platform == 'android'
        self.game_package_name = None  # 游戏包名
        
        if self.is_android:
            self._init_android_api()
        
        Logger.info("游戏启动器初始化完成")
    
    def _init_android_api(self):
        """初始化Android API"""
        try:
            from android import autoclass
            
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.Intent = autoclass('android.content.Intent')
            self.PackageManager = autoclass('android.content.pm.PackageManager')
            
            Logger.info("游戏启动器 Android API初始化成功")
            
        except Exception as e:
            Logger.error(f"Android API初始化失败: {e}")
            self.is_android = False
    
    def set_game_package_name(self, package_name):
        """
        设置游戏包名
        
        Args:
            package_name: 游戏的Android包名
        """
        self.game_package_name = package_name
        Logger.info(f"已设置游戏包名: {package_name}")
    
    def is_game_installed(self):
        """
        检查游戏是否已安装
        
        Returns:
            bool: 游戏是否已安装
        """
        if not self.is_android or not self.game_package_name:
            return False
        
        try:
            activity = self.PythonActivity.mActivity
            pm = activity.getPackageManager()
            
            # 尝试获取应用信息
            try:
                pm.getPackageInfo(self.game_package_name, 0)
                Logger.info(f"✅ 游戏已安装: {self.game_package_name}")
                return True
            except:
                Logger.warning(f"❌ 游戏未安装: {self.game_package_name}")
                return False
                
        except Exception as e:
            Logger.error(f"检查游戏安装状态失败: {e}")
            return False
    
    def launch_game(self):
        """
        启动游戏
        
        Returns:
            bool: 是否成功启动
        """
        if not self.is_android:
            Logger.warning("非Android环境，无法启动游戏")
            return False
        
        if not self.game_package_name:
            Logger.error("未设置游戏包名")
            return False
        
        try:
            Logger.info(f"🚀 正在启动游戏: {self.game_package_name}")
            
            activity = self.PythonActivity.mActivity
            Logger.info(f"Activity获取成功: {activity}")
            
            pm = activity.getPackageManager()
            Logger.info(f"PackageManager获取成功: {pm}")
            
            # 获取游戏的启动Intent
            launch_intent = pm.getLaunchIntentForPackage(self.game_package_name)
            Logger.info(f"LaunchIntent: {launch_intent}")
            
            if launch_intent:
                # 设置标志：清除任务栈并创建新任务
                launch_intent.addFlags(self.Intent.FLAG_ACTIVITY_NEW_TASK)
                launch_intent.addFlags(self.Intent.FLAG_ACTIVITY_CLEAR_TOP)
                
                Logger.info(f"Intent flags已设置")
                
                # 启动游戏
                activity.startActivity(launch_intent)
                
                Logger.info("✅ 游戏启动命令已发送")
                return True
            else:
                Logger.error(f"❌ 无法获取游戏启动Intent: {self.game_package_name}")
                Logger.error("可能原因：1.包名错误 2.游戏未安装 3.游戏无启动Activity")
                return False
                
        except Exception as e:
            import traceback
            Logger.error(f"❌ 启动游戏失败: {e}")
            Logger.error(f"详细错误: {traceback.format_exc()}")
            return False
    
    def launch_game_and_wait(self, wait_seconds=3):
        """
        启动游戏并等待加载
        
        Args:
            wait_seconds: 等待游戏加载的秒数
            
        Returns:
            bool: 是否成功启动
        """
        if self.launch_game():
            Logger.info(f"⏰ 等待游戏加载 {wait_seconds} 秒...")
            time.sleep(wait_seconds)
            return True
        return False
    
    def get_installed_games(self):
        """
        获取已安装的常见游戏列表
        
        Returns:
            list: 游戏信息列表 [(name, package_name), ...]
        """
        if not self.is_android:
            return []
        
        # 常见游戏包名列表
        common_games = [
            ("崩坏：星穹铁道", "com.HoYoverse.hkrpgoversea"),  # 国际服
            ("崩坏：星穹铁道", "com.miHoYo.hkrpg"),  # 国服
            ("原神", "com.miHoYo.Yuanshen"),  # 国服
            ("原神", "com.miHoYo.GenshinImpact"),  # 国际服
            ("崩坏3", "com.miHoYo.bh3oversea"),  # 国际服
            ("崩坏3", "com.miHoYo.enterprise.NGHSoD"),  # 国服
        ]
        
        installed_games = []
        
        try:
            activity = self.PythonActivity.mActivity
            pm = activity.getPackageManager()
            
            Logger.info(f"开始检测游戏，共 {len(common_games)} 个候选")
            
            for game_name, package_name in common_games:
                try:
                    Logger.info(f"检测: {package_name}")
                    pm.getPackageInfo(package_name, 0)
                    installed_games.append((game_name, package_name))
                    Logger.info(f"✅ 发现已安装游戏: {game_name} ({package_name})")
                except Exception as e:
                    Logger.info(f"❌ {package_name} 未安装: {e}")
            
            Logger.info(f"检测完成，找到 {len(installed_games)} 个游戏")
            return installed_games
            
        except Exception as e:
            import traceback
            Logger.error(f"获取游戏列表失败: {e}")
            Logger.error(f"详细错误: {traceback.format_exc()}")
            return []
    
    def auto_detect_game(self):
        """
        自动检测并设置游戏包名
        
        Returns:
            str: 检测到的游戏名称，未检测到返回None
        """
        installed_games = self.get_installed_games()
        
        if installed_games:
            # 优先选择第一个（通常是星穹铁道）
            game_name, package_name = installed_games[0]
            self.set_game_package_name(package_name)
            Logger.info(f"✅ 自动检测到游戏: {game_name}")
            return game_name
        else:
            Logger.warning("❌ 未检测到已安装的游戏")
            return None
    
    def switch_to_game(self):
        """
        切换到已运行的游戏（如果游戏已在后台）
        
        Returns:
            bool: 是否成功切换
        """
        # 实际上就是重新启动游戏Intent
        # Android会自动恢复已存在的Activity
        return self.launch_game()
    
    def get_game_info(self):
        """
        获取当前设置的游戏信息
        
        Returns:
            dict: 游戏信息
        """
        return {
            'package_name': self.game_package_name,
            'installed': self.is_game_installed(),
            'platform': 'android' if self.is_android else 'desktop'
        }


class GamePackageNames:
    """常见游戏包名常量"""
    
    # 崩坏：星穹铁道
    HSR_GLOBAL = "com.HoYoverse.hkrpgoversea"  # 国际服
    HSR_CN = "com.miHoYo.hkrpg"  # 国服
    HSR_BILIBILI = "com.miHoYo.hkrpg.bilibili"  # B服
    
    # 原神
    GENSHIN_GLOBAL = "com.miHoYo.GenshinImpact"  # 国际服
    GENSHIN_CN = "com.miHoYo.Yuanshen"  # 国服
    GENSHIN_BILIBILI = "com.miHoYo.Yuanshen.bilibili"  # B服
    
    # 崩坏3
    HONKAI_GLOBAL = "com.miHoYo.bh3oversea"  # 国际服
    HONKAI_CN = "com.miHoYo.enterprise.NGHSoD"  # 国服
    
    # 绝区零
    ZZZ_GLOBAL = "com.HoYoverse.Nap"  # 国际服
    ZZZ_CN = "com.miHoYo.Nap"  # 国服
    
    @classmethod
    def get_all_hsr_packages(cls):
        """获取所有星穹铁道包名"""
        return [cls.HSR_GLOBAL, cls.HSR_CN, cls.HSR_BILIBILI]
    
    @classmethod
    def get_all_packages(cls):
        """获取所有游戏包名"""
        return [
            cls.HSR_GLOBAL, cls.HSR_CN, cls.HSR_BILIBILI,
            cls.GENSHIN_GLOBAL, cls.GENSHIN_CN, cls.GENSHIN_BILIBILI,
            cls.HONKAI_GLOBAL, cls.HONKAI_CN,
            cls.ZZZ_GLOBAL, cls.ZZZ_CN
        ]

