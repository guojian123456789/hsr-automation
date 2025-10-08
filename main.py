"""
Honkai Star Rail Automation Assistant - Mobile Version
Based on Kivy framework for Android applications
"""

import os
import sys
import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

# Import core modules
from automation_engine import AutomationEngine
from android_utils import AndroidUtils

class HSRAutomationApp(App):
    """Honkai Star Rail Automation Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.automation = None
        self.android_utils = AndroidUtils()
        self.is_running = False
        self.status_text = "Ready"
        self.daily_commission_enabled = True  # Default enabled
        
    def build(self):
        """Build application interface"""
        self.title = "HSR Automation Assistant"
        
        # Main layout with light background
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[30, 40, 30, 30],
            spacing=20
        )
        
        # Add light background to main layout
        with main_layout.canvas.before:
            Color(0.96, 0.96, 0.98, 1)  # Very light gray-blue background
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        # Bind to update background on layout resize
        main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # Header section
        header_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.25),
            spacing=8
        )
        
        # Title with enhanced styling for light background
        title_label = Label(
            text='[size=24][color=2E5BBA]HSR[/color] [color=E67E22]Automation[/color][/size]\n[size=16][color=27AE60]Assistant[/color][/size]',
            size_hint=(1, 0.7),
            markup=True,
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Status display with improved styling for light background
        self.status_label = Label(
            text=f'[color=27AE60]>[/color] {self.status_text}',
            size_hint=(1, 0.3),
            font_size='16sp',
            markup=True,
            halign='center',
            color=[0.2, 0.2, 0.2, 1]  # Dark text for light background
        )
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(self.status_label)
        
        # Options section with card-like appearance
        options_card = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            spacing=10
        )
        
        # Options title
        options_title = Label(
            text='[size=14][color=34495E]Options[/color][/size]',
            size_hint=(1, 0.4),
            markup=True,
            halign='left',
            valign='middle'
        )
        options_title.bind(size=options_title.setter('text_size'))
        
        # Daily Commission checkbox area
        commission_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.6),
            spacing=15,
            padding=[10, 0]
        )
        
        self.daily_commission_checkbox = CheckBox(
            active=self.daily_commission_enabled,
            size_hint=(0.15, 1),
            color=[0.29, 0.56, 0.89, 1]  # Nice blue
        )
        self.daily_commission_checkbox.bind(active=self.on_daily_commission_toggle)
        
        commission_label = Label(
            text='[size=15][color=2C3E50]Daily Commission[/color][/size]',
            size_hint=(0.85, 1),
            markup=True,
            halign='left',
            valign='middle'
        )
        commission_label.bind(size=commission_label.setter('text_size'))
        
        commission_layout.add_widget(self.daily_commission_checkbox)
        commission_layout.add_widget(commission_label)
        
        options_card.add_widget(options_title)
        options_card.add_widget(commission_layout)
        
        # Button section with improved styling
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.6),
            spacing=12,
            padding=[0, 10]
        )
        
        # Primary action buttons
        primary_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.4),
            spacing=15
        )
        
        self.start_btn = Button(
            text='[size=16]START[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.29, 0.78, 0.29, 1],  # Modern green
            background_normal='',
            bold=True
        )
        self.start_btn.bind(on_press=self.start_automation)
        
        self.stop_btn = Button(
            text='[size=16]STOP[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.85, 0.33, 0.33, 1],  # Modern red
            background_normal='',
            disabled=True,
            bold=True
        )
        self.stop_btn.bind(on_press=self.stop_automation)
        
        primary_layout.add_widget(self.start_btn)
        primary_layout.add_widget(self.stop_btn)
        
        # Secondary buttons
        secondary_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.3),
            spacing=15
        )
        
        perm_btn = Button(
            text='[size=14]Permissions[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.95, 0.65, 0.31, 1],  # Modern orange
            background_normal=''
        )
        perm_btn.bind(on_press=self.show_permissions)
        
        about_btn = Button(
            text='[size=14]About[/size]',
            size_hint=(0.5, 1),
            markup=True,
            background_color=[0.44, 0.56, 0.89, 1],  # Modern blue
            background_normal=''
        )
        about_btn.bind(on_press=self.show_about)
        
        secondary_layout.add_widget(perm_btn)
        secondary_layout.add_widget(about_btn)
        
        # Footer info
        footer_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            spacing=5
        )
        
        version_label = Label(
            text='[size=12][color=7F8C8D]Version 1.0 • Desktop Edition[/color][/size]',
            size_hint=(1, 0.5),
            markup=True,
            halign='center'
        )
        
        warning_label = Label(
            text='[size=11][color=E74C3C]! For educational purposes only[/color][/size]',
            size_hint=(1, 0.5),
            markup=True,
            halign='center'
        )
        
        footer_layout.add_widget(version_label)
        footer_layout.add_widget(warning_label)
        
        # Assemble all sections
        button_layout.add_widget(primary_layout)
        button_layout.add_widget(secondary_layout)
        button_layout.add_widget(footer_layout)
        
        main_layout.add_widget(header_layout)
        main_layout.add_widget(options_card)
        main_layout.add_widget(button_layout)
        
        # Initialize automation engine
        self.init_automation()
        
        return main_layout
    
    def _update_bg(self, instance, value):
        """Update background rectangle size"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def init_automation(self):
        """Initialize automation engine"""
        try:
            Logger.info("Initializing automation engine...")
            self.update_status("Initializing...")
            
            self.automation = AutomationEngine()
            
            # 设置初始选项
            self.automation.set_daily_commission_enabled(self.daily_commission_enabled)
            
            self.update_status("Ready")
            Logger.info("Automation engine initialized successfully")
            
        except Exception as e:
            Logger.error(f"Initialization failed: {e}")
            self.update_status(f"Init failed: {str(e)}")
    
    def start_automation(self, instance):
        """Start automation"""
        if self.is_running:
            return
        
        # Check permissions
        if platform == 'android' and not self.android_utils.check_permissions():
            self.update_status("Permissions required")
            return
            
        Logger.info("Starting automation tasks")
        self.is_running = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.update_status("Running...")
        
        # Run automation in background thread
        threading.Thread(target=self.run_automation_thread, daemon=True).start()
    
    def stop_automation(self, instance):
        """Stop automation"""
        if not self.is_running:
            return
            
        Logger.info("Stopping automation tasks")
        self.is_running = False
        
        if self.automation:
            self.automation.stop()
        
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.update_status("Stopped")
    
    def run_automation_thread(self):
        """Automation execution thread"""
        try:
            if self.automation:
                success = self.automation.run()
                if success:
                    Clock.schedule_once(lambda dt: self.update_status("Completed"), 0)
                else:
                    Clock.schedule_once(lambda dt: self.update_status("Failed"), 0)
            else:
                Clock.schedule_once(lambda dt: self.update_status("Engine not initialized"), 0)
                
        except Exception as e:
            Logger.error(f"Automation execution exception: {e}")
            Clock.schedule_once(lambda dt: self.update_status(f"Error: {str(e)}"), 0)
        
        finally:
            # Reset button states
            Clock.schedule_once(lambda dt: self.reset_buttons(), 0)
    
    def reset_buttons(self):
        """Reset button states"""
        self.is_running = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.update_status("Ready")
    
    def update_status(self, text):
        """Update status display"""
        self.status_text = text
        if hasattr(self, 'status_label'):
            # Format with color and icon based on status (darker colors for light background)
            if text.lower() in ['ready', 'completed']:
                formatted_text = f'[color=27AE60]>[/color] {text}'
            elif text.lower() in ['running', 'initializing']:
                formatted_text = f'[color=E67E22]>[/color] {text}'
            elif text.lower() in ['stopped', 'failed', 'error']:
                formatted_text = f'[color=E74C3C]>[/color] {text}'
            else:
                formatted_text = f'[color=27AE60]>[/color] {text}'
            
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', formatted_text), 0)
    
    def on_daily_commission_toggle(self, checkbox, value):
        """Handle daily commission checkbox toggle"""
        self.daily_commission_enabled = value
        Logger.info(f"Daily Commission {'enabled' if value else 'disabled'}")
        
        # Update automation engine if it exists
        if self.automation:
            self.automation.set_daily_commission_enabled(value)
    
    def show_permissions(self, instance):
        """Show permissions settings interface"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        if platform == 'android':
            # Android permissions settings
            title = Label(
                text='Android Permissions',
                size_hint=(1, 0.2),
                font_size='16sp'
            )
            content.add_widget(title)
            
            # Permission status
            perm_status = self.android_utils.get_permission_status()
            status_label = Label(
                text=perm_status,
                size_hint=(1, 0.3),
                text_size=(None, None),
                halign='left',
                font_size='14sp'
            )
            status_label.bind(size=status_label.setter('text_size'))
            content.add_widget(status_label)
            
            # Permission setting buttons
            btn_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=5)
            
            overlay_btn = Button(text='Enable Overlay Permission', size_hint=(1, 0.5))
            overlay_btn.bind(on_press=lambda x: self.android_utils.request_overlay_permission())
            
            accessibility_btn = Button(text='Enable Accessibility Service', size_hint=(1, 0.5))
            accessibility_btn.bind(on_press=lambda x: self.android_utils.request_accessibility_service())
            
            btn_layout.add_widget(overlay_btn)
            btn_layout.add_widget(accessibility_btn)
            content.add_widget(btn_layout)
        else:
            # Desktop environment
            content.add_widget(Label(
                text='Desktop environment, no special permissions needed',
                size_hint=(1, 0.6)
            ))
        
        # Close button
        close_btn = Button(text='Close', size_hint=(1, 0.2))
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Permissions',
            content=content,
            size_hint=(0.9, 0.8)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_about(self, instance):
        """Show about interface"""
        about_text = """HSR Automation Assistant

Version: 1.0 Mobile Edition
Platform: Android / Desktop

Game automation tool based on image recognition

Main Features:
• Auto game login
• Daily task execution  
• Resource collection

Important Notice:
For learning and research only
Risk of account ban exists
Please follow game terms of service

Tech Stack:
Kivy + OpenCV + Python"""
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        about_label = Label(
            text=about_text,
            size_hint=(1, 0.8),
            text_size=(None, None),
            halign='center',
            valign='middle',
            font_size='14sp'
        )
        about_label.bind(size=about_label.setter('text_size'))
        content.add_widget(about_label)
        
        close_btn = Button(text='Close', size_hint=(1, 0.2))
        content.add_widget(close_btn)
        
        popup = Popup(
            title='About',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

# Application entry point
if __name__ == '__main__':
    HSRAutomationApp().run()
