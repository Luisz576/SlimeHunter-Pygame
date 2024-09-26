from game.settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, use_rect_center=False, z=WorldLayers.BUILDING):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(center=pos) if use_rect_center else self.image.get_rect(topleft=pos)
        self.z = z
        self.y_sort = self.rect.bottom
        self.hitbox = self.rect.copy()


class FollowableSprite(Sprite):
    def __init__(self, surf, target, group, offset=Vector2(0, 0), use_rect_center=False, z=WorldLayers.BUILDING):
        super().__init__((0, 0), surf, group, use_rect_center=use_rect_center, z=z)
        self.target = target
        self.offset = offset


class CollidableSprite(Sprite):
    def __init__(self, pos, surf, group, use_rect_center=False, z=WorldLayers.BUILDING):
        super().__init__(pos, surf, group, use_rect_center=use_rect_center, z=z)


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, group, frame_index=0, animation_speed=4, use_rect_center=False,
                 z=WorldLayers.BUILDING):
        self.frame_index = frame_index
        self.animation_speed = animation_speed
        self.frames = frames
        super().__init__(pos, frames[0], group, use_rect_center=use_rect_center, z=z)

    def update(self, delta):
        self.frame_index += self.animation_speed * delta
        if int(self.frame_index) > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
