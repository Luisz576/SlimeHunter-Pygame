from ..settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, group, frame_index=0, animation_speed=4):
        self.frame_index = frame_index
        self.animation_speed = animation_speed
        self.frames = frames
        super().__init__(pos, frames[0], group)

    def update(self, delta):
        self.frame_index += self.animation_speed * delta
        if int(self.frame_index) > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
