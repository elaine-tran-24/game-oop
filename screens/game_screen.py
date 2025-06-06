"""
Game Screen for When Cows Fly
Main gameplay screen with cow, obstacles, and game logic
"""

import random
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.app import App
from kivy.vector import Vector

class Cow(Widget):
    """Cow player character"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity_y = 0
        self.gravity = -800
        self.jump_strength = 400
        self.size = (40, 40)
        self.ground_level = 60
        
        # Draw the cow (simple representation)
        with self.canvas:
            Color(1, 1, 1, 1)  # White cow
            self.cow_shape = Ellipse(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_graphics)
    
    def update_graphics(self, *args):
        """Update cow graphics position"""
        self.cow_shape.pos = self.pos
    
    def update(self, dt):
        """Update cow physics"""
        # Apply gravity
        self.velocity_y += self.gravity * dt
        
        # Update position
        self.y += self.velocity_y * dt
        
        # Ground collision
        if self.y <= self.ground_level:
            self.y = self.ground_level
            self.velocity_y = 0
        
        # Ceiling collision
        if self.y >= Window.height - self.height - 10:
            self.y = Window.height - self.height - 10
            self.velocity_y = 0
    
    def jump(self):
        """Make the cow jump"""
        self.velocity_y = self.jump_strength

class Obstacle(Widget):
    """Base obstacle class"""
    
    def __init__(self, obstacle_type, **kwargs):
        super().__init__(**kwargs)
        self.obstacle_type = obstacle_type
        self.speed = 200
        self.setup_obstacle()
    
    def setup_obstacle(self):
        """Setup obstacle based on type"""
        with self.canvas:
            if self.obstacle_type == 'electric_wire':
                Color(1, 1, 0, 1)  # Yellow
                self.size = (Window.width, 10)
                self.pos = (Window.width, Window.height - 30)
                self.shape = Rectangle(pos=self.pos, size=self.size)
            
            elif self.obstacle_type == 'hole':
                Color(0, 0, 0, 1)  # Black
                self.size = (80, 60)
                self.pos = (Window.width, 0)
                self.shape = Rectangle(pos=self.pos, size=self.size)
            
            elif self.obstacle_type == 'kite':
                Color(1, 0.5, 0, 1)  # Orange
                self.size = (30, 30)
                self.pos = (Window.width, random.randint(100, Window.height - 100))
                self.shape = Ellipse(pos=self.pos, size=self.size)
            
            elif self.obstacle_type == 'barrier':
                Color(0.5, 0.3, 0.1, 1)  # Brown
                self.size = (20, random.randint(60, 120))
                self.pos = (Window.width, random.randint(60, Window.height - self.height - 60))
                self.shape = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_graphics)
    
    def update_graphics(self, *args):
        """Update obstacle graphics position"""
        self.shape.pos = self.pos
    
    def update(self, dt, speed_multiplier=1.0):
        """Update obstacle position"""
        self.x -= self.speed * speed_multiplier * dt
        return self.x < -self.width

class Collectible(Widget):
    """Collectible grass item"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 200
        self.size = (25, 25)
        self.pos = (Window.width, random.randint(80, Window.height - 80))
        
        with self.canvas:
            Color(0, 1, 0, 1)  # Green
            self.shape = Ellipse(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_graphics)
    
    def update_graphics(self, *args):
        """Update collectible graphics position"""
        self.shape.pos = self.pos
    
    def update(self, dt, speed_multiplier=1.0):
        """Update collectible position"""
        self.x -= self.speed * speed_multiplier * dt
        return self.x < -self.width

class GameScreen(Screen):
    """Main game screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_running = False
        self.score = 0
        self.lives = 3
        self.speed_multiplier = 1.0
        self.obstacles = []
        self.collectibles = []
        self.spawn_timer = 0
        self.collectible_spawn_timer = 0
        self.build_ui()
    
    def build_ui(self):
        """Build the game UI"""
        # Background
        with self.canvas.before:
            Color(0.5, 0.8, 1.0, 1)  # Light blue sky
            self.bg_rect = Rectangle(size=Window.size, pos=(0, 0))
            
            # Ground
            Color(0.2, 0.8, 0.2, 1)  # Green ground
            self.ground_rect = Rectangle(size=(Window.width, 60), pos=(0, 0))
        
        # Bind to update background
        self.bind(size=self.update_bg)
        Window.bind(size=self.update_bg)
        
        # UI Layout
        ui_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'top': 1})
        
        # Lives display
        self.lives_label = Label(
            text='❤️ ❤️ ❤️',
            font_size='24sp',
            size_hint=(0.3, 1),
            halign='left'
        )
        ui_layout.add_widget(self.lives_label)
        
        # Score display
        self.score_label = Label(
            text='Score: 0',
            font_size='20sp',
            size_hint=(0.7, 1),
            halign='right'
        )
        ui_layout.add_widget(self.score_label)
        
        self.add_widget(ui_layout)
        
        # Create cow
        self.cow = Cow()
        self.cow.pos = (100, self.cow.ground_level)
        self.add_widget(self.cow)
        
        # Bind touch events
        self.bind(on_touch_down=self.on_touch_down)
    
    def update_bg(self, *args):
        """Update background size"""
        self.bg_rect.size = Window.size
        self.ground_rect.size = (Window.width, 60)
    
    def on_enter(self):
        """Called when entering the game screen"""
        self.start_game()
    
    def on_leave(self):
        """Called when leaving the game screen"""
        self.stop_game()
    
    def start_game(self):
        """Start the game"""
        self.game_running = True
        self.score = 0
        self.lives = 3
        self.speed_multiplier = 1.0
        self.spawn_timer = 0
        self.collectible_spawn_timer = 0
        
        # Reset cow position
        self.cow.pos = (100, self.cow.ground_level)
        self.cow.velocity_y = 0
        
        # Clear obstacles and collectibles
        for obstacle in self.obstacles:
            self.remove_widget(obstacle)
        for collectible in self.collectibles:
            self.remove_widget(collectible)
        self.obstacles.clear()
        self.collectibles.clear()
        
        # Update UI
        self.update_ui()
        
        # Start game loop
        Clock.schedule_interval(self.update_game, 1.0/60.0)
    
    def stop_game(self):
        """Stop the game"""
        self.game_running = False
        Clock.unschedule(self.update_game)
    
    def pause_game(self):
        """Pause the game"""
        if self.game_running:
            Clock.unschedule(self.update_game)
            self.game_running = False
    
    def update_game(self, dt):
        """Main game update loop"""
        if not self.game_running:
            return
        
        # Update cow
        self.cow.update(dt)
        
        # Update speed based on score
        self.speed_multiplier = 1.0 + (self.score // 50) * 0.2
        
        # Spawn obstacles
        self.spawn_timer += dt
        if self.spawn_timer >= 2.0 / self.speed_multiplier:
            self.spawn_obstacle()
            self.spawn_timer = 0
        
        # Spawn collectibles
        self.collectible_spawn_timer += dt
        if self.collectible_spawn_timer >= 3.0:
            self.spawn_collectible()
            self.collectible_spawn_timer = 0
        
        # Update obstacles
        for obstacle in self.obstacles[:]:
            if obstacle.update(dt, self.speed_multiplier):
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
            else:
                self.check_collision(obstacle)
        
        # Update collectibles
        for collectible in self.collectibles[:]:
            if collectible.update(dt, self.speed_multiplier):
                self.remove_widget(collectible)
                self.collectibles.remove(collectible)
            else:
                self.check_collectible_collision(collectible)
    
    def spawn_obstacle(self):
        """Spawn a random obstacle"""
        obstacle_types = ['electric_wire', 'hole', 'kite', 'barrier']
        obstacle_type = random.choice(obstacle_types)
        obstacle = Obstacle(obstacle_type)
        self.obstacles.append(obstacle)
        self.add_widget(obstacle)
    
    def spawn_collectible(self):
        """Spawn a collectible grass"""
        collectible = Collectible()
        self.collectibles.append(collectible)
        self.add_widget(collectible)
    
    def check_collision(self, obstacle):
        """Check collision between cow and obstacle"""
        if self.cow.collide_widget(obstacle):
            app = App.get_running_app()
            
            if obstacle.obstacle_type == 'electric_wire':
                # Instant game over
                if app and hasattr(app, 'sound_manager'):
                    app.sound_manager.play_sound('game_over')
                self.game_over()
            elif obstacle.obstacle_type == 'hole' and self.cow.y <= obstacle.y + obstacle.height:
                # Fall into hole
                if app and hasattr(app, 'sound_manager'):
                    app.sound_manager.play_sound('hit')
                self.lose_life()
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
            else:
                # Other obstacles
                if app and hasattr(app, 'sound_manager'):
                    app.sound_manager.play_sound('hit')
                self.lose_life()
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
    
    def check_collectible_collision(self, collectible):
        """Check collision between cow and collectible"""
        if self.cow.collide_widget(collectible):
            app = App.get_running_app()
            if app and hasattr(app, 'sound_manager'):
                app.sound_manager.play_sound('collect')
            
            self.score += 1
            self.update_ui()
            self.remove_widget(collectible)
            self.collectibles.remove(collectible)
    
    def lose_life(self):
        """Lose a life"""
        self.lives -= 1
        self.update_ui()
        
        if self.lives <= 0:
            self.game_over()
    
    def game_over(self):
        """Handle game over"""
        self.stop_game()
        
        # Save score data
        app = App.get_running_app()
        if app and hasattr(app, 'data_manager'):
            app.data_manager.add_points(self.score)
            is_new_high_score = self.score > app.data_manager.get_best_score()
            app.data_manager.set_best_score(self.score)
            
            # Pass data to game over screen
            game_over_screen = self.manager.get_screen('game_over')
            game_over_screen.set_score_data(self.score, is_new_high_score)
        
        self.manager.current = 'game_over'
    
    def update_ui(self):
        """Update UI elements"""
        # Update lives display
        heart_text = '❤️ ' * self.lives + '🖤 ' * (3 - self.lives)
        self.lives_label.text = heart_text.strip()
        
        # Update score
        self.score_label.text = f'Score: {self.score}'
    
    def on_touch_down(self, touch):
        """Handle touch input"""
        if self.game_running:
            self.cow.jump()
            app = App.get_running_app()
            if app and hasattr(app, 'sound_manager'):
                app.sound_manager.play_sound('fly')
        return True
    
    def on_space_press(self):
        """Handle space bar press"""
        if self.game_running:
            self.cow.jump()
            app = App.get_running_app()
            if app and hasattr(app, 'sound_manager'):
                app.sound_manager.play_sound('fly')