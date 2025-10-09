"""
自动化引擎 - 核心自动化逻辑
支持桌面和Android环境
"""

import time
import threading
from kivy.logger import Logger
from kivy.utils import platform

# 导入图像处理和控制模块
from image_processor import ImageProcessor
from game_controller import GameController
from task_manager import TaskManager
from android_screen_capture import AndroidScreenCapture

class AutomationEngine:
    """自动化引擎主类"""
    
    VERSION = "1.0.5-enable-pillow-matching"  # 版本标记
    
    def __init__(self):
        self.is_running = False
        self.current_task = None
        self.platform = platform
        self.daily_commission_enabled = True  # Default enabled
        
        # 初始化子模块
        self.image_processor = ImageProcessor()
        self.game_controller = GameController()
        self.task_manager = TaskManager()
        
        # 初始化截图模块（Android专用）
        if platform == 'android':
            self.screen_capture = AndroidScreenCapture()
            Logger.info(f"✅ AndroidScreenCapture 已初始化")
        else:
            self.screen_capture = None
        
        Logger.info(f"🚀 自动化引擎初始化完成 [版本: {self.VERSION}]，平台: {self.platform}")
    
    def set_daily_commission_enabled(self, enabled):
        """设置每日委托是否启用"""
        self.daily_commission_enabled = enabled
        Logger.info(f"每日委托设置为: {'启用' if enabled else '禁用'}")
    
    def run(self):
        """运行自动化流程"""
        try:
            Logger.info("开始执行自动化流程")
            self.is_running = True
            
            # 获取任务列表
            tasks = self.task_manager.get_tasks()
            
            for task in tasks:
                if not self.is_running:
                    Logger.info("自动化被中断")
                    return False
                
                Logger.info(f"执行任务: {task['name']}")
                self.current_task = task
                
                success = self.execute_task(task)
                
                if not success and task.get('required', True):
                    Logger.error(f"必需任务失败: {task['name']}")
                    return False
                
                # 任务间延迟
                time.sleep(2)
            
            Logger.info("✅ 自动化流程完成")
            return True
            
        except Exception as e:
            Logger.error(f"自动化执行异常: {e}")
            return False
        
        finally:
            self.is_running = False
            self.current_task = None
    
    def execute_task(self, task):
        """执行单个任务"""
        try:
            task_type = task.get('type')
            
            if task_type == 'login':
                return self.execute_login_task(task)
            elif task_type == 'click_task':
                return self.execute_click_task(task)
            elif task_type == 'weituo_task':
                if self.daily_commission_enabled:
                    Logger.info("🎯 开始执行每日委托任务")
                    return self.execute_weituo_task(task)
                else:
                    Logger.info("⏩ 每日委托已禁用，跳过委托任务")
                    return True  # 跳过但不视为失败
            elif task_type == 'daily_tasks':
                return self.execute_daily_tasks(task)
            else:
                Logger.warning(f"未知任务类型: {task_type}")
                return False
                
        except Exception as e:
            Logger.error(f"任务执行异常: {e}")
            return False
    
    def execute_login_task(self, task):
        """执行登录任务 - 智能持续检测模式"""
        Logger.info("开始执行登录流程 - 智能等待游戏加载")
        
        # 第一阶段：持续检测 first OR screen/button（无时间限制）
        # 因为游戏刚启动，可能需要较长时间加载
        Logger.info("🔍 第一阶段：检测登录界面...")
        
        check_count = 0
        first_button_clicked = False
        
        while True:
            if not self.is_running:
                return False
            
            check_count += 1
            if check_count % 5 == 0:  # 每5秒打印一次
                Logger.info(f"持续检测中... ({check_count}秒)")
            
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("⚠️ 无法截图，1秒后重试")
                time.sleep(1)
                continue
            
            # 优先检测 login_button_first
            result = self.image_processor.find_image(screenshot, 'login_button_first')
            if result:
                Logger.info("✅ 找到首次登录按钮！")
                center_x, center_y = result['center']
                Logger.info(f"坐标: ({center_x}, {center_y})")
                
                if self.game_controller.click_position((center_x, center_y)):
                    Logger.info("✅ 首次登录按钮点击成功")
                    time.sleep(2)
                    first_button_clicked = True
                    break
                else:
                    Logger.error("❌ 点击失败")
            
            # 如果没有first，检测screen或button（可能直接出现）
            for image_name in ['game_start_screen', 'login_button']:
                result = self.image_processor.find_image(screenshot, image_name)
                if result:
                    Logger.info(f"✅ 直接检测到: {image_name}")
                    # 直接进入第二阶段处理
                    break
            else:
                # 如果都没检测到，继续循环
                time.sleep(1)
                continue
            
            # 检测到screen或button，跳出循环
            break
        
        # 第二阶段：持续检测 game_start_screen 和 login_button（无时间限制）
        Logger.info("🔍 第二阶段：持续检测游戏开始界面和登录按钮（每秒检查一次，无时间限制）")
        second_stage_images = ['game_start_screen', 'login_button']
        second_stage_start = time.time()
        
        while True:  # 无时间限制，持续检测
            if not self.is_running:
                return False
            
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("无法获取屏幕截图，1秒后重试")
                time.sleep(1)
                continue
            
            # 检测第二阶段图像
            detected = False
            for image_name in second_stage_images:
                result = self.image_processor.find_image(screenshot, image_name)
                if result:
                    Logger.info(f"✅ 检测到: {image_name}")
                    center_x, center_y = result['center']
                    
                    # 等待2秒后再点击
                    Logger.info("等待2秒后点击...")
                    time.sleep(2)
                    
                    # 执行点击
                    if self.game_controller.click_position((center_x, center_y)):
                        Logger.info(f"点击成功: {image_name}")
                        detected = True
                        
                        # 等待进入游戏并检测登录奖励或task按钮
                        Logger.info("等待游戏加载...")
                        time.sleep(20)  # 等待20秒让游戏充分加载
                        
                        # 第三阶段：智能检测 yueka（登录奖励）或 task（主界面）
                        Logger.info("🔍 第三阶段：智能检测登录奖励(yueka)或主界面(task)...")
                        
                        yueka_handled = False
                        check_screenshot = self.screen_capture.capture_screen()
                        
                        if check_screenshot is not None:
                            # 同时检测 yueka 和 task，比较置信度
                            yueka_result = self.image_processor.find_image(check_screenshot, 'yueka')
                            task_result = self.image_processor.find_image(check_screenshot, 'task')
                            
                            yueka_confidence = yueka_result['confidence'] if yueka_result else 0
                            task_confidence = task_result['confidence'] if task_result else 0
                            
                            Logger.info(f"检测结果 - yueka置信度: {yueka_confidence:.2f}, task置信度: {task_confidence:.2f}")
                            
                            # 如果检测到 yueka 且置信度更高
                            if yueka_result and yueka_confidence > task_confidence:
                                Logger.info("✅ 检测到登录奖励弹窗(yueka)，准备关闭...")
                                center_x, center_y = yueka_result['center']
                                
                                # 第一次点击（领取奖励）
                                if self.game_controller.click_position((center_x, center_y)):
                                    Logger.info("✅ 第一次点击成功（领取奖励）")
                                    time.sleep(1)
                                    
                                    # 第二次点击（关闭弹窗）
                                    if self.game_controller.click_position((center_x, center_y)):
                                        Logger.info("✅ 第二次点击成功（关闭弹窗）")
                                        time.sleep(1)
                                        yueka_handled = True
                                    else:
                                        Logger.warning("⚠️ 第二次点击失败")
                                else:
                                    Logger.warning("⚠️ 第一次点击失败")
                            
                            # 如果检测到 task 且置信度更高（或没有yueka）
                            elif task_result and task_confidence >= yueka_confidence:
                                Logger.info("✅ 直接检测到task按钮，登录成功！")
                                return True
                        
                        # 第四阶段：持续检测task按钮（无时间限制）
                        task_check_start = time.time()
                        
                        Logger.info("🔍 第四阶段：持续检测task按钮（进入游戏成功标识，无时间限制）...")
                        while True:  # 无时间限制，持续检测
                            if not self.is_running:
                                return False
                            
                            check_screenshot = self.screen_capture.capture_screen()
                            if check_screenshot is not None:
                                task_result = self.image_processor.find_image(check_screenshot, 'task')
                                if task_result:
                                    Logger.info("✅ 检测到task按钮，登录成功！")
                                    return True
                            
                            task_elapsed = int(time.time() - task_check_start)
                            if task_elapsed % 10 == 0 and task_elapsed > 0:  # 每10秒显示一次进度
                                Logger.info(f"🔍 检测task按钮中... (已等待 {task_elapsed}s)")
                            
                            time.sleep(1)  # 每秒检查一次
                        
                        break  # 跳出当前循环，继续监控
                    else:
                        Logger.error(f"点击失败: {image_name}")
            
            if not detected:
                elapsed = int(time.time() - second_stage_start)
                if elapsed % 10 == 0 and elapsed > 0:  # 每10秒显示一次进度
                    Logger.info(f"🔍 第二阶段监控中... (已等待 {elapsed}s)")
            
            time.sleep(1)  # 每秒检查一次
    
    def execute_click_task(self, task):
        """执行点击任务按钮任务"""
        Logger.info("开始执行点击任务按钮")
        
        target_image = task.get('target_image', 'task')
        timeout = task.get('timeout', 15)
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if not self.is_running:
                return False
            
            # 截取屏幕
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                time.sleep(1)
                continue
            
            # 查找目标按钮
            result = self.image_processor.find_image(screenshot, target_image)
            if result:
                Logger.info(f"找到目标按钮: {target_image}")
                
                # 点击按钮
                if self.game_controller.click_position(result['center']):
                    Logger.info("✅ 任务按钮点击成功")
                    return True
            
            time.sleep(1)
        
        Logger.error("❌ 未找到任务按钮")
        return False
    
    def execute_weituo_task(self, task):
        """执行委托任务流程：点击task -> 等待 -> 检索weituo -> 检索qianwang -> 点击qianwang"""
        Logger.info("🎯 开始执行委托任务流程")
        
        # 第一步：点击task按钮
        Logger.info("📋 第一步：点击task按钮")
        task_timeout = 15
        task_start = time.time()
        
        while time.time() - task_start < task_timeout:
            if not self.is_running:
                return False
            
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("无法获取屏幕截图，1秒后重试")
                time.sleep(1)
                continue
            
            task_result = self.image_processor.find_image(screenshot, 'task')
            if task_result:
                Logger.info("✅ 检测到task按钮")
                center_x, center_y = task_result['center']
                
                # 等待7秒后再点击
                Logger.info("⏰ 等待7秒后点击task按钮...")
                time.sleep(7)
                
                if self.game_controller.click_position((center_x, center_y)):
                    Logger.info("✅ 成功点击task按钮")
                    break
                else:
                    Logger.error("❌ task按钮点击失败")
            
            time.sleep(1)
        else:
            Logger.error("❌ 未找到task按钮，委托任务失败")
            return False
        
        # 第二步：检索weituo.png
        Logger.info("🔍 第二步：检索weituo界面")
        weituo_timeout = 10
        weituo_start = time.time()
        
        while time.time() - weituo_start < weituo_timeout:
            if not self.is_running:
                return False
            
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("无法获取屏幕截图，1秒后重试")
                time.sleep(1)
                continue
            
            weituo_result = self.image_processor.find_image(screenshot, 'weituo')
            if weituo_result:
                Logger.info("✅ 找到weituo界面")
                
                # 第三步：在weituo区域内检索qianwang.png
                Logger.info("🔍 第三步：在weituo界面中检索qianwang按钮")
                qianwang_result = self.image_processor.find_image(screenshot, 'qianwang')
                if qianwang_result:
                    # 第四步：点击qianwang
                    Logger.info("🎯 第四步：点击qianwang按钮")
                    qw_x, qw_y = qianwang_result['center']
                    if self.game_controller.click_position((qw_x, qw_y)):
                        Logger.info("✅ 成功点击qianwang")
                        
                        # 第五步：等待2秒后处理后续逻辑
                        Logger.info("⏰ 第五步：等待2秒...")
                        time.sleep(2)
                        
                        # 第六步：检查paiqianzhong或lingqu
                        return self.handle_post_qianwang_logic()
                    else:
                        Logger.error("❌ qianwang按钮点击失败")
                        return False
                else:
                    Logger.info("⚠️ 在weituo界面中未找到qianwang按钮，继续搜索...")
            
            time.sleep(1)
        
        Logger.error("❌ 委托任务失败：未找到weituo界面或qianwang按钮")
        return False
    
    def handle_post_qianwang_logic(self):
        """处理点击qianwang后的逻辑：检查paiqianzhong或lingqu"""
        Logger.info("🔍 第六步：检查paiqianzhong或lingqu状态")
        
        # 获取当前屏幕截图
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
        
        # 优先检查paiqianzhong（排签中）
        paiqian_result = self.image_processor.find_image(screenshot, 'paiqianzhong')
        if paiqian_result:
            Logger.info("✅ 检测到paiqianzhong（排签中状态）")
            
            # 查找并点击close按钮
            close_result = self.image_processor.find_image(screenshot, 'close')
            if close_result:
                Logger.info("🎯 点击close按钮")
                close_x, close_y = close_result['center']
                if self.game_controller.click_position((close_x, close_y)):
                    Logger.info("✅ 成功点击close")
                    
                    # 等待3秒后继续120kaituoli流程
                    Logger.info("⏰ 等待3秒...")
                    time.sleep(3)
                    
                    # 执行120kaituoli流程
                    return self.execute_120kaituoli_flow()
                else:
                    Logger.error("❌ close按钮点击失败")
                    return False
            else:
                Logger.warning("⚠️ 检测到paiqianzhong但未找到close按钮")
                return False
        
        # 如果没有paiqianzhong，执行领取流程：yijianlingqu → zaicipaiqian → close
        Logger.info("🔍 未检测到paiqianzhong，开始执行领取流程")
        
        # 第二步：点击yijianlingqu
        Logger.info("🎯 第二步：点击yijianlingqu按钮")
        yijianlingqu_result = self.image_processor.find_image(screenshot, 'yijianlingqu', confidence=0.7)  # 提高置信度
        if yijianlingqu_result:
            Logger.info("✅ 检测到yijianlingqu按钮")
            yijianlingqu_x, yijianlingqu_y = yijianlingqu_result['center']
            if self.game_controller.click_position((yijianlingqu_x, yijianlingqu_y)):
                Logger.info("✅ 成功点击yijianlingqu")
                
                # 等待2秒
                Logger.info("⏰ 等待2秒...")
                time.sleep(2)
                
                # 第三步：点击zaicipaiqian
                Logger.info("🎯 第三步：点击zaicipaiqian按钮")
                screenshot2 = self.screen_capture.capture_screen()
                if screenshot2 is not None:
                    zaici_result = self.image_processor.find_image(screenshot2, 'zaicipaiqian')
                    if zaici_result:
                        Logger.info("✅ 检测到zaicipaiqian按钮")
                        zaici_x, zaici_y = zaici_result['center']
                        if self.game_controller.click_position((zaici_x, zaici_y)):
                            Logger.info("✅ 成功点击zaicipaiqian")
                            
                            # 等待3秒
                            Logger.info("⏰ 等待3秒...")
                            time.sleep(3)
                            
                            # 第四步：点击close
                            Logger.info("🎯 第四步：点击close按钮")
                            screenshot3 = self.screen_capture.capture_screen()
                            if screenshot3 is not None:
                                close_result = self.image_processor.find_image(screenshot3, 'close')
                                if close_result:
                                    Logger.info("✅ 检测到close按钮")
                                    close_x, close_y = close_result['center']
                                    if self.game_controller.click_position((close_x, close_y)):
                                        Logger.info("✅ 成功点击close")
                                        
                                        # 等待3秒后继续120kaituoli流程
                                        Logger.info("⏰ 等待3秒...")
                                        time.sleep(3)
                                        
                                        # 执行120kaituoli流程
                                        return self.execute_120kaituoli_flow()
                                    else:
                                        Logger.error("❌ close按钮点击失败")
                                        return False
                                else:
                                    Logger.warning("⚠️ 未找到close按钮")
                                    return False
                            else:
                                Logger.error("❌ 无法获取第三次屏幕截图")
                                return False
                        else:
                            Logger.error("❌ zaicipaiqian按钮点击失败")
                            return False
                    else:
                        Logger.warning("⚠️ 未找到zaicipaiqian按钮")
                        return False
                else:
                    Logger.error("❌ 无法获取第二次屏幕截图")
                    return False
            else:
                Logger.error("❌ yijianlingqu按钮点击失败")
                return False
        else:
            Logger.warning("⚠️ 未找到yijianlingqu按钮")
            return False
    
    def execute_120kaituoli_flow(self):
        """执行120kaituoli流程：搜索120kaituoli.png，然后在其区域内找到qianwang并点击"""
        Logger.info("🔍 开始120kaituoli流程")
        
        # 获取当前屏幕截图
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
        
        # 搜索120kaituoli.png
        Logger.info("🔍 搜索120kaituoli.png")
        kaituoli_result = self.image_processor.find_image(screenshot, '120kaituoli')
        if kaituoli_result:
            Logger.info("✅ 找到120kaituoli区域")
            
            # 在同一屏幕截图中搜索qianwang按钮
            Logger.info("🔍 在120kaituoli区域内搜索qianwang按钮")
            qianwang_result = self.image_processor.find_image(screenshot, 'qianwang')
            if qianwang_result:
                Logger.info("✅ 在120kaituoli区域内找到qianwang按钮")
                qianwang_x, qianwang_y = qianwang_result['center']
                
                # 点击qianwang按钮
                Logger.info("🎯 点击120kaituoli区域内的qianwang按钮")
                if self.game_controller.click_position((qianwang_x, qianwang_y)):
                    Logger.info("✅ 成功点击120kaituoli区域内的qianwang")
                    
                    # 执行后续的详细操作流程
                    return self.execute_detailed_challenge_flow()
                else:
                    Logger.error("❌ qianwang按钮点击失败")
                    return False
            else:
                Logger.warning("⚠️ 在120kaituoli区域内未找到qianwang按钮")
                return False
        else:
            Logger.warning("⚠️ 未找到120kaituoli区域")
            return False
    
    def execute_detailed_challenge_flow(self):
        """执行详细的挑战流程：等待5s → 点击jinru → 等待3s → 点击jiahao六次 → 等待1s → 点击tiaozhan → 等待3s → 点击kaishitiaozhan"""
        Logger.info("🚀 开始详细挑战流程")
        
        # 第一步：等待5秒
        Logger.info("⏰ 第一步：等待5秒...")
        time.sleep(5)
        
        # 第二步：点击jinru
        Logger.info("🔍 第二步：搜索并点击jinru按钮")
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
            
        jinru_result = self.image_processor.find_image(screenshot, 'jinru')
        if jinru_result:
            Logger.info("✅ 找到jinru按钮")
            jinru_x, jinru_y = jinru_result['center']
            if self.game_controller.click_position((jinru_x, jinru_y)):
                Logger.info("✅ 成功点击jinru按钮")
            else:
                Logger.error("❌ jinru按钮点击失败")
                return False
        else:
            Logger.warning("⚠️ 未找到jinru按钮")
            return False
        
        # 第三步：等待3秒
        Logger.info("⏰ 第三步：等待3秒...")
        time.sleep(3)
        
        # 第四步：点击jiahao五次
        Logger.info("🔍 第四步：搜索并点击jiahao按钮5次")
        for i in range(5):
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.error(f"❌ 第{i+1}次无法获取屏幕截图")
                return False
                
            jiahao_result = self.image_processor.find_image(screenshot, 'jiahao')
            if jiahao_result:
                Logger.info(f"✅ 第{i+1}次找到jiahao按钮")
                jiahao_x, jiahao_y = jiahao_result['center']
                if self.game_controller.click_position((jiahao_x, jiahao_y)):
                    Logger.info(f"✅ 第{i+1}次成功点击jiahao按钮")
                    time.sleep(0.5)  # 每次点击间隔0.5秒
                else:
                    Logger.error(f"❌ 第{i+1}次jiahao按钮点击失败")
                    return False
            else:
                Logger.warning(f"⚠️ 第{i+1}次未找到jiahao按钮")
                return False
        
        # 第五步：等待1秒
        Logger.info("⏰ 第五步：等待1秒...")
        time.sleep(1)
        
        # 第六步：点击tiaozhan
        Logger.info("🔍 第六步：搜索并点击tiaozhan按钮")
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
            
        tiaozhan_result = self.image_processor.find_image(screenshot, 'tiaozhan')
        if tiaozhan_result:
            Logger.info("✅ 找到tiaozhan按钮")
            tiaozhan_x, tiaozhan_y = tiaozhan_result['center']
            if self.game_controller.click_position((tiaozhan_x, tiaozhan_y)):
                Logger.info("✅ 成功点击tiaozhan按钮")
            else:
                Logger.error("❌ tiaozhan按钮点击失败")
                return False
        else:
            Logger.warning("⚠️ 未找到tiaozhan按钮")
            return False
        
        # 第七步：等待3秒
        Logger.info("⏰ 第七步：等待3秒...")
        time.sleep(3)
        
        # 第八步：点击kaishitiaozhan
        Logger.info("🔍 第八步：搜索并点击kaishitiaozhan按钮")
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
            
        kaishitiaozhan_result = self.image_processor.find_image(screenshot, 'kaishitiaozhan')
        if kaishitiaozhan_result:
            Logger.info("✅ 找到kaishitiaozhan按钮")
            kaishitiaozhan_x, kaishitiaozhan_y = kaishitiaozhan_result['center']
            if self.game_controller.click_position((kaishitiaozhan_x, kaishitiaozhan_y)):
                Logger.info("✅ 成功点击kaishitiaozhan按钮")
                
                # 执行倍速控制逻辑
                return self.execute_beisu_control()
            else:
                Logger.error("❌ kaishitiaozhan按钮点击失败")
                return False
        else:
            Logger.warning("⚠️ 未找到kaishitiaozhan按钮")
            return False
    
    def execute_beisu_control(self):
        """执行智能倍速控制：等待10s → 检测beisukai和beisuguan → 自动切换到开启状态"""
        Logger.info("🚀 开始智能倍速控制")
        
        # 第一步：等待10秒
        Logger.info("⏰ 等待10秒...")
        time.sleep(10)
        
        # 最大尝试次数，防止无限循环
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            Logger.info(f"🔍 第{attempt}次检测倍速状态")
            
            # 获取当前屏幕截图
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.error("❌ 无法获取屏幕截图")
                return False
            
            # 同时检测两种倍速状态
            beisukai_result = self.image_processor.find_image(screenshot, 'beisukai')
            beisuguan_result = self.image_processor.find_image(screenshot, 'beisuguan')
            
            # 获取置信度
            beisukai_confidence = beisukai_result['confidence'] if beisukai_result else 0.0
            beisuguan_confidence = beisuguan_result['confidence'] if beisuguan_result else 0.0
            
            Logger.info(f"📊 倍速状态检测结果：")
            Logger.info(f"   beisukai（亮/开启）置信度: {beisukai_confidence:.3f}")
            Logger.info(f"   beisuguan（暗/关闭）置信度: {beisuguan_confidence:.3f}")
            
            # 判断当前状态
            if beisukai_confidence > beisuguan_confidence:
                Logger.info("✅ 倍速已开启（beisukai置信度更高），无需操作")
                Logger.info("✅ 倍速控制成功，开始检测自动功能")
                # 继续执行自动功能控制
                return self.execute_zidong_control()
            elif beisuguan_confidence > beisukai_confidence:
                Logger.info("🔄 倍速未开启（beisuguan置信度更高），尝试点击开启")
                
                if beisuguan_result:
                    beisuguan_x, beisuguan_y = beisuguan_result['center']
                    if self.game_controller.click_position((beisuguan_x, beisuguan_y)):
                        Logger.info("✅ 成功点击beisuguan，尝试开启倍速")
                        time.sleep(1)  # 等待界面响应
                        
                        # 检查是否成功切换
                        check_screenshot = self.screen_capture.capture_screen()
                        if check_screenshot is not None:
                            check_beisukai = self.image_processor.find_image(check_screenshot, 'beisukai')
                            check_beisuguan = self.image_processor.find_image(check_screenshot, 'beisuguan')
                            
                            check_beisukai_conf = check_beisukai['confidence'] if check_beisukai else 0.0
                            check_beisuguan_conf = check_beisuguan['confidence'] if check_beisuguan else 0.0
                            
                            if check_beisukai_conf > check_beisuguan_conf:
                                Logger.info("✅ 倍速控制成功，开始检测自动功能")
                                return self.execute_zidong_control()
                        
                        continue  # 继续下一次检测
                    else:
                        Logger.error("❌ beisuguan点击失败")
                        return False
                else:
                    Logger.warning("⚠️ 检测到beisuguan置信度更高，但未找到具体位置")
                    return False
            else:
                Logger.warning("⚠️ 两种倍速状态置信度相同，可能检测异常")
                time.sleep(1)  # 等待后重试
                continue
        
        Logger.warning(f"⚠️ 达到最大尝试次数({max_attempts})，倍速控制可能未完全成功")
        Logger.info("🔄 倍速控制达到最大尝试次数，继续检测自动功能")
        # 即使倍速控制未完全成功，也继续执行自动功能控制
        return self.execute_zidong_control()
    
    def execute_zidong_control(self):
        """执行智能自动功能控制：检测zidongkai和zidongguan → 自动切换到开启状态"""
        Logger.info("🚀 开始智能自动功能控制")
        
        # 最大尝试次数，防止无限循环
        max_attempts = 5
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            Logger.info(f"🔍 第{attempt}次检测自动功能状态")
            
            # 获取当前屏幕截图
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.error("❌ 无法获取屏幕截图")
                return False
            
            # 同时检测两种自动功能状态
            zidongkai_result = self.image_processor.find_image(screenshot, 'zidongkai')
            zidongguan_result = self.image_processor.find_image(screenshot, 'zidongguan')
            
            # 获取置信度
            zidongkai_confidence = zidongkai_result['confidence'] if zidongkai_result else 0.0
            zidongguan_confidence = zidongguan_result['confidence'] if zidongguan_result else 0.0
            
            Logger.info(f"📊 自动功能状态检测结果：")
            Logger.info(f"   zidongkai（金色/开启）置信度: {zidongkai_confidence:.3f}")
            Logger.info(f"   zidongguan（灰色/关闭）置信度: {zidongguan_confidence:.3f}")
            
            # 判断当前状态
            if zidongkai_confidence > zidongguan_confidence:
                Logger.info("✅ 自动功能已开启（zidongkai置信度更高），无需操作")
                Logger.info("✅ 自动功能控制成功，开始持续检测循环")
                # 继续执行持续检测循环
                return self.execute_continuous_cycle_detection()
            elif zidongguan_confidence > zidongkai_confidence:
                Logger.info("🔄 自动功能未开启（zidongguan置信度更高），尝试点击开启")
                
                if zidongguan_result:
                    zidongguan_x, zidongguan_y = zidongguan_result['center']
                    if self.game_controller.click_position((zidongguan_x, zidongguan_y)):
                        Logger.info("✅ 成功点击zidongguan，尝试开启自动功能")
                        time.sleep(1)  # 等待界面响应
                        
                        # 检查是否成功切换
                        check_screenshot = self.screen_capture.capture_screen()
                        if check_screenshot is not None:
                            check_zidongkai = self.image_processor.find_image(check_screenshot, 'zidongkai')
                            check_zidongguan = self.image_processor.find_image(check_screenshot, 'zidongguan')
                            
                            check_zidongkai_conf = check_zidongkai['confidence'] if check_zidongkai else 0.0
                            check_zidongguan_conf = check_zidongguan['confidence'] if check_zidongguan else 0.0
                            
                            if check_zidongkai_conf > check_zidongguan_conf:
                                Logger.info("✅ 自动功能控制成功，开始持续检测循环")
                                return self.execute_continuous_cycle_detection()
                        
                        continue  # 继续下一次检测
                    else:
                        Logger.error("❌ zidongguan按钮点击失败")
                        return False
                else:
                    Logger.warning("⚠️ 检测到zidongguan置信度更高，但未找到具体位置")
                    return False
            else:
                Logger.warning("⚠️ 两种自动功能状态置信度相同，可能检测异常")
                time.sleep(1)  # 等待后重试
                continue
        
        Logger.warning(f"⚠️ 达到最大尝试次数({max_attempts})，自动功能控制可能未完全成功")
        Logger.info("🔄 自动功能控制达到最大尝试次数，继续持续检测循环")
        # 即使自动功能控制未完全成功，也继续执行持续检测循环
        return self.execute_continuous_cycle_detection()
    
    def execute_continuous_cycle_detection(self):
        """执行持续检测循环：无限循环检测zailaiyici和tuichuguanqia，检测到后等待2s并点击"""
        Logger.info("🔄 开始持续检测循环（无时间限制）")
        
        # 阶段1：持续检测"再来一次"
        Logger.info("🔍 阶段1：持续检测zailaiyici（再来一次）...")
        zailaiyici_detected = False
        check_count = 0
        
        while not zailaiyici_detected:
            check_count += 1
            if check_count % 10 == 0:  # 每10次检测输出一次日志，避免日志过多
                Logger.info(f"🔍 已检测zailaiyici {check_count}次，继续等待...")
            
            # 获取屏幕截图
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("⚠️ 无法获取屏幕截图，等待1秒后重试")
                time.sleep(1)
                continue
            
            # 检测zailaiyici
            zailaiyici_result = self.image_processor.find_image(screenshot, 'zailaiyici')
            if zailaiyici_result:
                Logger.info("✅ 检测到zailaiyici（再来一次）按钮")
                zailaiyici_detected = True
                
                # 等待2秒
                Logger.info("⏰ 等待2秒...")
                time.sleep(2)
                
                # 点击zailaiyici
                zailaiyici_x, zailaiyici_y = zailaiyici_result['center']
                if self.game_controller.click_position((zailaiyici_x, zailaiyici_y)):
                    Logger.info("✅ 成功点击zailaiyici按钮")
                    
                    # 点击后等待10秒再进入下一阶段
                    Logger.info("⏰ 等待10秒后开始检测退出关卡...")
                    time.sleep(10)
                else:
                    Logger.error("❌ zailaiyici按钮点击失败")
                    return False
            else:
                # 未检测到，等待1秒后继续
                time.sleep(1)
        
        # 阶段2：持续检测"退出关卡"
        Logger.info("🔍 阶段2：持续检测tuichuguanqia（退出关卡）...")
        tuichuguanqia_detected = False
        check_count = 0
        
        while not tuichuguanqia_detected:
            check_count += 1
            if check_count % 10 == 0:  # 每10次检测输出一次日志，避免日志过多
                Logger.info(f"🔍 已检测tuichuguanqia {check_count}次，继续等待...")
            
            # 获取屏幕截图
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("⚠️ 无法获取屏幕截图，等待1秒后重试")
                time.sleep(1)
                continue
            
            # 检测tuichuguanqia
            tuichuguanqia_result = self.image_processor.find_image(screenshot, 'tuichuguanqia')
            if tuichuguanqia_result:
                Logger.info("✅ 检测到tuichuguanqia（退出关卡）按钮")
                tuichuguanqia_detected = True
                
                # 等待2秒
                Logger.info("⏰ 等待2秒...")
                time.sleep(2)
                
                # 点击tuichuguanqia
                tuichuguanqia_x, tuichuguanqia_y = tuichuguanqia_result['center']
                if self.game_controller.click_position((tuichuguanqia_x, tuichuguanqia_y)):
                    Logger.info("✅ 成功点击tuichuguanqia按钮")
                    # 继续执行退出后的流程
                    return self.execute_post_exit_flow()
                else:
                    Logger.error("❌ tuichuguanqia按钮点击失败")
                    return False
            else:
                # 未检测到，等待1秒后继续
                time.sleep(1)
        
        return True
    
    def execute_post_exit_flow(self):
        """执行退出后的流程：检测close → 点击task → 持续点击所有lingqu"""
        Logger.info("🚀 开始执行退出后流程")
        
        # 阶段1：检测并点击close
        Logger.info("🔍 阶段1：检测close按钮...")
        close_detected = False
        check_count = 0
        
        while not close_detected:
            check_count += 1
            if check_count % 10 == 0:
                Logger.info(f"🔍 已检测close {check_count}次，继续等待...")
            
            # 获取屏幕截图
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("⚠️ 无法获取屏幕截图，等待1秒后重试")
                time.sleep(1)
                continue
            
            # 检测close
            close_result = self.image_processor.find_image(screenshot, 'close')
            if close_result:
                Logger.info("✅ 检测到close按钮")
                close_detected = True
                
                # 等待2秒
                Logger.info("⏰ 等待2秒...")
                time.sleep(2)
                
                # 点击close
                close_x, close_y = close_result['center']
                if self.game_controller.click_position((close_x, close_y)):
                    Logger.info("✅ 成功点击close按钮")
                else:
                    Logger.error("❌ close按钮点击失败")
                    return False
            else:
                # 未检测到，等待1秒后继续
                time.sleep(1)
        
        # 阶段2：等待1秒后点击task
        Logger.info("⏰ 阶段2：等待1秒...")
        time.sleep(1)
        
        Logger.info("🔍 阶段2：搜索并点击task按钮")
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
        
        task_result = self.image_processor.find_image(screenshot, 'task')
        if task_result:
            Logger.info("✅ 找到task按钮")
            task_x, task_y = task_result['center']
            if self.game_controller.click_position((task_x, task_y)):
                Logger.info("✅ 成功点击task按钮")
            else:
                Logger.error("❌ task按钮点击失败")
                return False
        else:
            Logger.warning("⚠️ 未找到task按钮")
            return False
        
        # 阶段3：等待3秒后持续检测并点击所有lingqu
        Logger.info("⏰ 阶段3：等待3秒...")
        time.sleep(3)
        
        Logger.info("🔍 阶段3：开始持续检测并点击所有lingqu...")
        lingqu_count = 0
        
        while True:
            # 获取屏幕截图
            screenshot = self.screen_capture.capture_screen()
            if screenshot is None:
                Logger.warning("⚠️ 无法获取屏幕截图，等待1秒后重试")
                time.sleep(1)
                continue
            
            # 检测lingqu
            lingqu_result = self.image_processor.find_image(screenshot, 'lingqu')
            if lingqu_result:
                lingqu_count += 1
                Logger.info(f"✅ 检测到第{lingqu_count}个lingqu按钮")
                
                # 点击lingqu
                lingqu_x, lingqu_y = lingqu_result['center']
                if self.game_controller.click_position((lingqu_x, lingqu_y)):
                    Logger.info(f"✅ 成功点击第{lingqu_count}个lingqu按钮")
                    
                    # 每次点击后等待1秒
                    Logger.info("⏰ 等待1秒...")
                    time.sleep(1)
                else:
                    Logger.error(f"❌ 第{lingqu_count}个lingqu按钮点击失败")
                    return False
            else:
                # 未检测到lingqu，说明已经全部领取完毕
                Logger.info(f"✅ 已完成所有lingqu点击，共点击了{lingqu_count}个")
                # 继续执行400/500判断流程
                return self.execute_gift_check_flow()
    
    def execute_gift_check_flow(self):
        """执行礼物检查流程：比较400和500的置信度，如果500更高则点击gift"""
        Logger.info("🎁 开始执行礼物检查流程")
        
        # 获取屏幕截图
        screenshot = self.screen_capture.capture_screen()
        if screenshot is None:
            Logger.error("❌ 无法获取屏幕截图")
            return False
        
        # 检测400和500
        Logger.info("🔍 检测400和500的置信度...")
        result_400 = self.image_processor.find_image(screenshot, '400')
        result_500 = self.image_processor.find_image(screenshot, '500')
        
        # 获取置信度（如果没有检测到，置信度为0）
        confidence_400 = result_400['confidence'] if result_400 else 0.0
        confidence_500 = result_500['confidence'] if result_500 else 0.0
        
        Logger.info("📊 礼物检测结果：")
        Logger.info(f"   400置信度: {confidence_400:.3f}")
        Logger.info(f"   500置信度: {confidence_500:.3f}")
        
        # 比较置信度
        if confidence_500 > confidence_400:
            Logger.info("✅ 500置信度更高，执行gift点击流程")
            
            # 检测gift位置
            gift_result = self.image_processor.find_image(screenshot, 'gift')
            if not gift_result:
                Logger.error("❌ 未找到gift按钮")
                return False
            
            gift_x, gift_y = gift_result['center']
            Logger.info(f"🎁 找到gift按钮位置: ({gift_x}, {gift_y})")
            
            # 第一次点击gift
            Logger.info("🎯 第一次点击gift...")
            if not self.game_controller.click_position((gift_x, gift_y)):
                Logger.error("❌ gift按钮第一次点击失败")
                return False
            Logger.info("✅ gift第一次点击成功")
            
            # 等待1秒
            Logger.info("⏰ 等待1秒...")
            time.sleep(1)
            
            # 第二次点击gift
            Logger.info("🎯 第二次点击gift...")
            if not self.game_controller.click_position((gift_x, gift_y)):
                Logger.error("❌ gift按钮第二次点击失败")
                return False
            Logger.info("✅ gift第二次点击成功")
            
            # 等待2秒
            Logger.info("⏰ 等待2秒...")
            time.sleep(2)
            
            # 点击close
            Logger.info("🔍 搜索并点击close按钮...")
            close_screenshot = self.screen_capture.capture_screen()
            if close_screenshot is None:
                Logger.error("❌ 无法获取屏幕截图")
                return False
            
            close_result = self.image_processor.find_image(close_screenshot, 'close')
            if not close_result:
                Logger.error("❌ 未找到close按钮")
                return False
            
            close_x, close_y = close_result['center']
            if self.game_controller.click_position((close_x, close_y)):
                Logger.info("✅ 成功点击close按钮")
                Logger.info("🎉 礼物检查流程完成！")
                Logger.info("🎉 委托任务完成！所有流程执行成功")
                return True
            else:
                Logger.error("❌ close按钮点击失败")
                return False
        else:
            Logger.info("ℹ️ 400置信度更高或相等，跳过gift点击流程")
            Logger.info("🎉 委托任务完成！所有流程执行成功")
            return True
    
    def execute_daily_tasks(self, task):
        """执行每日任务"""
        Logger.info("开始执行每日任务")
        
        # 这里可以添加具体的每日任务逻辑
        # 比如：领取奖励、完成副本等
        
        # 模拟任务执行
        time.sleep(5)
        
        Logger.info("✅ 每日任务完成")
        return True
    
    def stop(self):
        """停止自动化"""
        Logger.info("停止自动化引擎")
        self.is_running = False
    
    def get_status(self):
        """获取当前状态"""
        if not self.is_running:
            return "就绪"
        elif self.current_task:
            return f"执行中: {self.current_task['name']}"
        else:
            return "运行中"
