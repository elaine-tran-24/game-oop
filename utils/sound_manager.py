"""
Sound Manager for When Cows Fly
Handles loading and playing sound effects
"""

import os
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.app import App

class SoundManager:
    """Manages sound effects for the game"""
    
    def __init__(self):
        self.sounds = {}
        self.sound_files = {
            'fly': 'fly.wav',
            'hit': 'hit.wav',
            'collect': 'collect.wav',
            'game_over': 'game_over.wav',
            'button_click': 'button.wav'
        }
    
    def load_sounds(self):
        """Load all sound files"""
        # Get assets directory path
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sounds')
        
        for sound_name, filename in self.sound_files.items():
            sound_path = os.path.join(assets_dir, filename)
            
            # Create placeholder sound file if it doesn't exist
            if not os.path.exists(sound_path):
                self.create_placeholder_sound(sound_path)
            
            try:
                sound = SoundLoader.load(sound_path)
                if sound:
                    self.sounds[sound_name] = sound
                    Logger.info(f"SoundManager: Loaded {sound_name}")
                else:
                    Logger.warning(f"SoundManager: Failed to load {sound_name}")
            except Exception as e:
                Logger.error(f"SoundManager: Error loading {sound_name}: {e}")
    
    def create_placeholder_sound(self, sound_path):
        """Create a placeholder sound file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(sound_path), exist_ok=True)
            
            # Create a very simple WAV file (just header, no actual audio)
            # This is a minimal 44-byte WAV header for a silent sound
            wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
            
            with open(sound_path, 'wb') as f:
                f.write(wav_header)
            
            Logger.info(f"SoundManager: Created placeholder sound: {sound_path}")
        except Exception as e:
            Logger.error(f"SoundManager: Error creating placeholder sound: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        try:
            # Check if sound is enabled
            app = App.get_running_app()
            if app and hasattr(app, 'data_manager'):
                if not app.data_manager.get_sound_enabled():
                    return
                
                volume = app.data_manager.get_volume()
            else:
                volume = 0.8
            
            if sound_name in self.sounds and self.sounds[sound_name]:
                sound = self.sounds[sound_name]
                sound.volume = volume
                sound.play()
                Logger.debug(f"SoundManager: Played {sound_name}")
        except Exception as e:
            Logger.error(f"SoundManager: Error playing {sound_name}: {e}")
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds"""
        try:
            for sound in self.sounds.values():
                if sound:
                    sound.stop()
        except Exception as e:
            Logger.error(f"SoundManager: Error stopping sounds: {e}")
    
    def set_volume(self, volume):
        """Set volume for all sounds"""
        try:
            for sound in self.sounds.values():
                if sound:
                    sound.volume = max(0.0, min(1.0, volume))
        except Exception as e:
            Logger.error(f"SoundManager: Error setting volume: {e}")