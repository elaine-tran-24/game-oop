"""
Main Menu Screen for When Cows Fly
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class MainMenuScreen(Screen):
    """Main menu screen with title, buttons, and score display"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the main menu UI"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Add background
        with self.canvas.before:
            Color(0.3, 0.8, 1.0, 1)  # Sky blue background
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))
        
        # Bind to update background on window resize
        self.bind(size=self.update_bg)
        Window.bind(size=self.update_bg)
        
        # Title
        title_label = Label(
            text='[size=48][color=ffffff]When Cows Fly[/color][/size]',
            markup=True,
            size_hint=(1, 0.3),
            halign='center'
        )
        main_layout.add_widget(title_label)
        
        # Spacer
        main_layout.add_widget(Widget(size_hint=(1, 0.1)))
        
        # Score display
        self.score_label = Label(
            text='',
            markup=True,
            size_hint=(1, 0.15),
            halign='center'
        )
        main_layout.add_widget(self.score_label)
        
        # Button layout
        button_layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(1, 0.4))
        
        # Play button
        play_btn = Button(
            text='PLAY',
            size_hint=(1, 0.25),
            font_size='24sp',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        play_btn.bind(on_press=self.start_game)
        button_layout.add_widget(play_btn)
        
        # Tutorial button
        tutorial_btn = Button(
            text='TUTORIAL',
            size_hint=(1, 0.25),
            font_size='20sp',
            background_color=(0.8, 0.6, 0.2, 1)
        )
        tutorial_btn.bind(on_press=self.show_tutorial)
        button_layout.add_widget(tutorial_btn)
        
        # Settings button
        settings_btn = Button(
            text='SETTINGS',
            size_hint=(1, 0.25),
            font_size='20sp',
            background_color=(0.6, 0.6, 0.8, 1)
        )
        settings_btn.bind(on_press=self.show_settings)
        button_layout.add_widget(settings_btn)
        
        main_layout.add_widget(button_layout)
        
        # Spacer
        main_layout.add_widget(Widget(size_hint=(1, 0.05)))
        
        self.add_widget(main_layout)
    
    def update_bg(self, *args):
        """Update background size"""
        self.bg_rect.size = Window.size
    
    def on_enter(self):
        """Called when entering this screen"""
        self.update_score_display()
    
    def update_score_display(self):
        """Update the score display"""
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            best_score = app.data_manager.get_best_score()
            total_points = app.data_manager.get_total_points()
            
            self.score_label.text = (
                f'[size=18][color=ffffff]Best Score: {best_score}[/color][/size]\n'
                f'[size=16][color=ffffaa]Total Points: {total_points}[/color][/size]'
            )
    
    def start_game(self, button):
        """Start the game"""
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        
        self.manager.current = 'game'
    
    def show_tutorial(self, button):
        """Show tutorial screen"""
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        
        self.manager.current = 'tutorial'
    
    def show_settings(self, button):
        """Show settings screen"""
        app = App.get_running_app()
        if app and hasattr(app, 'sound_manager'):
            app.sound_manager.play_sound('button_click')
        
        self.manager.current = 'settings'