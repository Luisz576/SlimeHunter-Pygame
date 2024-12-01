from pygame.transform import scale
from game.settings import Enum


class AnimationEvent(Enum):
    FRAME_CHANGED = "frame_changed"
    RESETED = "reseted"
    ENDS = "ends"
    ANIMATION_CHANGED = "animation_changed"


class Animation:
    def __init__(self, frames, speed=4):
        self.index = 0
        self.frames = frames
        self.speed = speed
        self._size = len(self.frames)
        self._listeners = {}

    def set_listener(self, name, listener):
        self._listeners[name] = listener

    def remove_listener(self, name):
        self._listeners.pop(name)

    def size(self):
        return self._size

    def notify_all(self, event):
        for listener in self._listeners.values():
            listener(event, self)

    def next(self):
        self.index += 1
        if self.index >= self.size():
            self.index = 0
            self.notify_all(AnimationEvent.ENDS)
        self.notify_all(AnimationEvent.FRAME_CHANGED)

    def reset(self):
        self.index = 0
        self.notify_all(AnimationEvent.RESETED)

    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.size()
        self.notify_all(AnimationEvent.FRAME_CHANGED)

    def frame(self):
        return self.frames[self.index]

    def scale_frames(self, new_scale):
        for i in range(self._size):
            sprite_size = self.frames[i].get_size()
            self.frames[i] = scale(self.frames[i], (sprite_size[0] * new_scale, sprite_size[1] * new_scale))


class AnimationController:
    _ANIMATION_LISTENER_KEY = "__animation_controller__"

    def __init__(self, animations, start_animation_name, stopped=True):
        # animations
        self.animations = animations
        # listeners
        for anim in animations:
            animations[anim].set_listener(AnimationController._ANIMATION_LISTENER_KEY, self.__listener_handler)
        # configs
        self.speed = 0
        self.current_animation = start_animation_name
        self._stopped = stopped
        self._animation_delta_frame = 0
        # listener
        self._listeners = {}

    def set_listener(self, name, listener):
        self._listeners[name] = listener

    def remove_listener(self, name):
        self._listeners.pop(name)

    def __listener_handler(self, event, animation):
        for listener in self._listeners.values():
            listener(event, animation, self)

    def animation(self):
        return self.animations[self.current_animation]

    def frame(self):
        return self.animation().frame()

    def change(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.__listener_handler(AnimationEvent.ANIMATION_CHANGED, self.animation())
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
        self._animation_delta_frame += self.animation().speed * delta
        if self._animation_delta_frame > 1:
            self._animation_delta_frame = 0
            self.next_frame()
