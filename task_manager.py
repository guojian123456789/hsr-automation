"""
任务管理器 - 管理自动化任务定义和执行顺序
"""

from kivy.logger import Logger

class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks = self.load_default_tasks()
        Logger.info(f"任务管理器初始化完成，加载 {len(self.tasks)} 个任务")
    
    def load_default_tasks(self):
        """加载默认任务定义"""
        tasks = [
            {
                'id': 'login',
                'name': '游戏登录',
                'type': 'login',
                'description': '自动检测登录界面并完成登录',
                'priority': 1,
                'required': True,
                'timeout': 60,
                'retry_count': 3
            },
            {
                'id': 'weituo_task',
                'name': '委托任务',
                'type': 'weituo_task',
                'description': '点击task按钮，检索weituo界面，然后点击qianwang',
                'priority': 2,
                'required': False,
                'timeout': 60,
                'retry_count': 2
            },
            {
                'id': 'daily_tasks',
                'name': '每日任务',
                'type': 'daily_tasks',
                'description': '完成各种每日任务',
                'priority': 4,
                'required': False,
                'timeout': 300,
                'retry_count': 1
            }
        ]
        
        return tasks
    
    def get_tasks(self):
        """获取按优先级排序的任务列表"""
        return sorted(self.tasks, key=lambda x: x.get('priority', 999))
    
    def get_task_by_id(self, task_id):
        """根据ID获取任务"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def add_task(self, task):
        """添加新任务"""
        if 'id' not in task:
            Logger.error("任务必须包含ID")
            return False
        
        # 检查ID是否已存在
        if self.get_task_by_id(task['id']):
            Logger.error(f"任务ID已存在: {task['id']}")
            return False
        
        # 设置默认值
        task.setdefault('priority', 999)
        task.setdefault('required', False)
        task.setdefault('timeout', 30)
        task.setdefault('retry_count', 1)
        
        self.tasks.append(task)
        Logger.info(f"添加任务: {task['name']}")
        return True
    
    def remove_task(self, task_id):
        """删除任务"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                removed_task = self.tasks.pop(i)
                Logger.info(f"删除任务: {removed_task['name']}")
                return True
        
        Logger.error(f"未找到任务: {task_id}")
        return False
    
    def update_task(self, task_id, updates):
        """更新任务"""
        task = self.get_task_by_id(task_id)
        if not task:
            Logger.error(f"未找到任务: {task_id}")
            return False
        
        task.update(updates)
        Logger.info(f"更新任务: {task['name']}")
        return True
    
    def get_enabled_tasks(self):
        """获取启用的任务"""
        return [task for task in self.get_tasks() if task.get('enabled', True)]
    
    def get_required_tasks(self):
        """获取必需的任务"""
        return [task for task in self.get_tasks() if task.get('required', False)]
    
    def validate_task(self, task):
        """验证任务配置"""
        required_fields = ['id', 'name', 'type']
        
        for field in required_fields:
            if field not in task:
                Logger.error(f"任务缺少必需字段: {field}")
                return False
        
        # 验证任务类型
        valid_types = ['login', 'click_task', 'weituo_task', 'daily_tasks', 'custom']
        if task['type'] not in valid_types:
            Logger.error(f"无效的任务类型: {task['type']}")
            return False
        
        return True
    
    def get_task_summary(self):
        """获取任务摘要信息"""
        total = len(self.tasks)
        enabled = len(self.get_enabled_tasks())
        required = len(self.get_required_tasks())
        
        return {
            'total': total,
            'enabled': enabled,
            'required': required,
            'optional': enabled - required
        }
    
    def export_tasks(self):
        """导出任务配置"""
        return {
            'version': '1.0',
            'tasks': self.tasks
        }
    
    def import_tasks(self, task_data):
        """导入任务配置"""
        try:
            if 'tasks' not in task_data:
                Logger.error("无效的任务数据格式")
                return False
            
            new_tasks = task_data['tasks']
            
            # 验证所有任务
            for task in new_tasks:
                if not self.validate_task(task):
                    return False
            
            # 替换现有任务
            self.tasks = new_tasks
            Logger.info(f"成功导入 {len(new_tasks)} 个任务")
            return True
            
        except Exception as e:
            Logger.error(f"导入任务失败: {e}")
            return False
