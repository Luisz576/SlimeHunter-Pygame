import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {}

    def add_sound(self, key, path):
        if key in self.sounds.keys():
            return False
        self.sounds[key] = pygame.mixer.Sound(path)
        return True

    def set_background_music(self, music_path, volume=0.5):
        if music_path is None:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)

    def set_sound(self, key, path):
        self.sounds[key] = pygame.mixer.Sound(path)

    def remove_sound(self, key):
        return self.sounds.pop(key)

    def play_sound(self, key, volume=0.5):
        if key in self.sounds.keys():
            self.sounds[key].set_volume(volume)
            self.sounds[key].play()
