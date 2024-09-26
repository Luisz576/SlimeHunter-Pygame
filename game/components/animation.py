from pygame.transform import scale


class Animation:
    def __init__(self, frames):
        self.index = 0
        self.frames = frames
        self._size = len(self.frames)

    def size(self):
        return self._size

    def next(self):
        self.index += 1
        if self.index >= self.size():
            self.index = 0

    def reset(self):
        self.index = 0

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.size()

    def frame(self):
        return self.frames[self.index]

    def scale_frames(self, new_scale):
        for i in range(self._size):
            sprite_size = self.frames[i].get_size()
            self.frames[i] = scale(self.frames[i], (sprite_size[0] * new_scale, sprite_size[1] * new_scale))


class AnimationController:
    def __init__(self, animations, start_animation_name, speed=4, stopped=True):
        self.animations = animations
        self.speed = speed
        self.current_animation = start_animation_name
        self._stopped = stopped
        self._animation_delta_frame = 0

    def animation(self):
        return self.animations[self.current_animation]

    def frame(self):
        return self.animation().frame()

    def change(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.reset()

    def reset(self):
        self.animation().reset()

    def play(self):
        self._stopped = False

    def stop(self):
        self._stopped = True

    def next_frame(self):
        self.animation().next()

    def previous_frame(self):
        self.animation().previous()

    def update(self, delta):
        if self._stopped:
            return
        self._animation_delta_frame += self.speed * delta
        if self._animation_delta_frame > 1:
            self._animation_delta_frame = 0
            self.next_frame()
