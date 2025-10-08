"""
Kivy UI 快速预览示例
运行这个文件可以在桌面看到UI效果
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.core.text import LabelBase

# ============= 配置中文字体 =============
# 注册中文字体（使用Windows自带的微软雅黑）
LabelBase.register(
    name='Microsoft YaHei',
    fn_regular='C:/Windows/Fonts/msyh.ttc',  # 微软雅黑常规
    fn_bold='C:/Windows/Fonts/msyhbd.ttc',   # 微软雅黑粗体
)

# ============= 模拟手机屏幕尺寸 =============
Config.set('graphics', 'width', '360')   # 手机宽度
Config.set('graphics', 'height', '780')  # 手机高度
Config.set('graphics', 'resizable', False)  # 固定大小

class UIPreviewApp(App):
    """UI预览示例应用"""
    
    def build(self):
        """构建UI界面"""
        
        # 主布局
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[30, 40, 30, 30],
            spacing=20
        )
        
        # 添加浅色背景
        with main_layout.canvas.before:
            Color(0.96, 0.96, 0.98, 1)  # 浅灰蓝色
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # ========== 1. 标题区域 ==========
        header = BoxLayout(orientation='vertical', size_hint=(1, 0.25), spacing=8)
        
        title = Label(
            text='[size=24][color=2E5BBA]HSR[/color] [color=E67E22]自动化助手[/color][/size]',
            size_hint=(1, 0.7),
            markup=True,
            halign='center',
            valign='middle',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        title.bind(size=title.setter('text_size'))
        
        status = Label(
            text='[color=27AE60]>[/color] UI预览模式',
            size_hint=(1, 0.3),
            font_size='16sp',
            markup=True,
            halign='center',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        
        header.add_widget(title)
        header.add_widget(status)
        
        # ========== 2. 选项区域 ==========
        options = BoxLayout(orientation='vertical', size_hint=(1, 0.15), spacing=10)
        
        options_title = Label(
            text='[size=14][color=34495E]任务选项[/color][/size]',
            size_hint=(1, 0.4),
            markup=True,
            halign='left',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        options_title.bind(size=options_title.setter('text_size'))
        
        checkbox_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.6),
            spacing=15,
            padding=[10, 0]
        )
        
        checkbox = CheckBox(
            active=True,
            size_hint=(0.15, 1),
            color=[0.29, 0.56, 0.89, 1]
        )
        
        checkbox_label = Label(
            text='[size=15][color=2C3E50]每日委托[/color][/size]',
            size_hint=(0.85, 1),
            markup=True,
            halign='left',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        checkbox_label.bind(size=checkbox_label.setter('text_size'))
        
        checkbox_layout.add_widget(checkbox)
        checkbox_layout.add_widget(checkbox_label)
        
        options.add_widget(options_title)
        options.add_widget(checkbox_layout)
        
        # ========== 3. 按钮区域 ==========
        buttons = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing=12)
        
        # 主要按钮
        primary_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.4),
            spacing=15
        )
        
        start_btn = Button(
            text='[size=16]开始[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.29, 0.78, 0.29, 1],  # 绿色
            background_normal='',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        start_btn.bind(on_press=self.on_start_click)
        
        stop_btn = Button(
            text='[size=16]停止[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.85, 0.33, 0.33, 1],  # 红色
            background_normal='',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        stop_btn.bind(on_press=self.on_stop_click)
        
        primary_buttons.add_widget(start_btn)
        primary_buttons.add_widget(stop_btn)
        
        # 辅助按钮
        secondary_buttons = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.3),
            spacing=15
        )
        
        perm_btn = Button(
            text='[size=14]权限设置[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.95, 0.65, 0.31, 1],  # 橙色
            background_normal='',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        
        about_btn = Button(
            text='[size=14]关于[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.44, 0.56, 0.89, 1],  # 蓝色
            background_normal='',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        
        secondary_buttons.add_widget(perm_btn)
        secondary_buttons.add_widget(about_btn)
        
        # 页脚
        footer = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=5)
        
        version = Label(
            text='[size=12][color=7F8C8D]版本 1.0 - 预览模式[/color][/size]',
            size_hint=(1, 0.5),
            markup=True,
            halign='center',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        
        warning = Label(
            text='[size=11][color=E74C3C]修改代码后按 Ctrl+R 刷新[/color][/size]',
            size_hint=(1, 0.5),
            markup=True,
            halign='center',
            font_name='Microsoft YaHei'  # 使用中文字体
        )
        
        footer.add_widget(version)
        footer.add_widget(warning)
        
        buttons.add_widget(primary_buttons)
        buttons.add_widget(secondary_buttons)
        buttons.add_widget(footer)
        
        # ========== 组装所有部分 ==========
        main_layout.add_widget(header)
        main_layout.add_widget(options)
        main_layout.add_widget(buttons)
        
        return main_layout
    
    def _update_bg(self, instance, value):
        """更新背景"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def on_start_click(self, instance):
        """开始按钮回调"""
        print("✓ 开始按钮被点击")
        instance.text = '[size=16]运行中...[/size]'
    
    def on_stop_click(self, instance):
        """停止按钮回调"""
        print("× 停止按钮被点击")


if __name__ == '__main__':
    print("=" * 50)
    print("Kivy UI 预览模式 - 中文版")
    print("=" * 50)
    print("\n使用说明:")
    print("  1. 窗口会以手机尺寸 (360x780) 显示")
    print("  2. 修改此文件的UI代码")
    print("  3. 在窗口中按 Ctrl+R 刷新查看效果")
    print("  4. 点击按钮查看控制台输出")
    print("\n提示:")
    print("  - 修改颜色: background_color=[R, G, B, 透明度]")
    print("  - 修改大小: size_hint=(宽度比例, 高度比例)")
    print("  - 修改文本: text='[markup标签]内容[/markup]'")
    print("  - 所有Label和Button都要加: font_name='Microsoft YaHei'")
    print("\n" + "=" * 50 + "\n")
    
    UIPreviewApp().run()

