from game.components import AnimationController, Sprite
from game.settings import *


class Entity(Sprite):
    def __init__(self, pos, group, animations, start_animation_name):
        self.animation_controller = AnimationController(animations, start_animation_name)
        self.animation_controller.play()

        super().__init__(pos, self.animation_controller.frame(), group, use_rect_center=True, z=WorldLayers.ENTITY)

        # render
        self.flipped = False

        # attributes
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
        self.velocity = pygame.math.Vector2(0, 0)

    def _animate(self, delta):
        self.animation_controller.update(delta)
        self.image = pygame.transform.flip(self.animation_controller.frame(), self.flipped, False)

    def is_moving(self):
        return self.velocity.x != 0 or self.velocity.y != 0

    def _move(self, delta):
        # normalizationws
        if self.velocity.magnitude() > 0:
            self.velocity = self.velocity.normalize()
        # moviment
        self.pos.x += self.velocity.x * self.speed * delta
        self.rect.centerx = self.pos.x
        self.pos.y += self.velocity.y * self.speed * delta
        self.rect.centery = self.pos.y

    def update(self, delta):
        self._move(delta)
        self.y_sort = self.rect.centery
        self._animate(delta)
