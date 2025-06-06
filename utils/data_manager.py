"""
Data Manager for When Cows Fly
Handles saving and loading game data using JSON
"""

import json
import os
from kivy.logger import Logger
from kivy.app import App

class DataManager:
    """Manages game data persistence"""
    
    def __init__(self):
        self.data_file = self.get_data_path()
        self.default_data = {
            'best_score': 0,
            'total_points': 0,
            'settings': {
                'sound_enabled': True,
                'volume': 0.8
            }
        }
        self.data = self.default_data.copy()
    
    def get_data_path(self):
        """Get the path to save data file"""
        try:
            # Try to use user data directory
            app = App.get_running_app()
            if app:
                user_data_dir = app.user_data_dir
                if not os.path.exists(user_data_dir):
                    os.makedirs(user_data_dir)
                return os.path.join(user_data_dir, 'game_data.json')
        except Exception as e:
            Logger.warning(f"DataManager: Could not access user data dir: {e}")
        
        # Fallback to current directory
        return 'game_data.json'
    
    def load_data(self):
        """Load game data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with defaults to handle missing keys
                    self.data = {**self.default_data, **loaded_data}
                    # Ensure settings exist
                    if 'settings' not in self.data:
                        self.data['settings'] = self.default_data['settings']
                    else:
                        self.data['settings'] = {**self.default_data['settings'], **self.data['settings']}
                    
                Logger.info(f"DataManager: Data loaded successfully")
            else:
                Logger.info("DataManager: No save file found, using defaults")
                self.data = self.default_data.copy()
        except Exception as e:
            Logger.error(f"DataManager: Error loading data: {e}")
            self.data = self.default_data.copy()
    
    def save_data(self):
        """Save game data to file"""
        try:
            # Ensure directory exists
            data_dir = os.path.dirname(self.data_file)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
            Logger.info("DataManager: Data saved successfully")
        except Exception as e:
            Logger.error(f"DataManager: Error saving data: {e}")
    
    def get_best_score(self):
        """Get the best score"""
        return self.data.get('best_score', 0)
    
    def set_best_score(self, score):
        """Set the best score"""
        self.data['best_score'] = max(score, self.data.get('best_score', 0))
        self.save_data()
    
    def get_total_points(self):
        """Get total accumulated points"""
        return self.data.get('total_points', 0)
    
    def add_points(self, points):
        """Add points to total"""
        self.data['total_points'] = self.data.get('total_points', 0) + points
        self.save_data()
    
    def get_setting(self, key, default=None):
        """Get a setting value"""
        return self.data.get('settings', {}).get(key, default)
    
    def set_setting(self, key, value):
        """Set a setting value"""
        if 'settings' not in self.data:
            self.data['settings'] = {}
        self.data['settings'][key] = value
        self.save_data()
    
    def get_sound_enabled(self):
        """Check if sound is enabled"""
        return self.get_setting('sound_enabled', True)
    
    def set_sound_enabled(self, enabled):
        """Enable/disable sound"""
        self.set_setting('sound_enabled', enabled)
    
    def get_volume(self):
        """Get volume level"""
        return self.get_setting('volume', 0.8)
    
    def set_volume(self, volume):
        """Set volume level"""
        self.set_setting('volume', max(0.0, min(1.0, volume)))