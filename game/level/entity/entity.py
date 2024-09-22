from game.components import AnimationController, Sprite
from game.settings import *


class Entity(Sprite):
    def __init__(self, pos, group, collision_group, animations, start_animation_name):
        # animations
        self.animation_controller = AnimationController(animations, start_animation_name)
        self.animation_controller.play()

        # super
        super().__init__(pos, self.animation_controller.frame(), group, use_rect_center=True, z=WorldLayers.ENTITY)

        # collision
        self.collision_group = collision_group
        self.hitbox = self.rect.inflate(-self.rect.width/2, -self.rect.height/2)
                                        # TODO: look here <- Maybe

        # render
        self.flipped = False

        # attributes
        self.speed = 200
        self.velocity = pygame.math.Vector2(0, 0)

    def _animate(self, delta):
        self.animation_controller.update(delta)
        self.image = pygame.transform.flip(self.animation_controller.frame(), self.flipped, False)

    def is_moving(self):
        return self.velocity.x != 0 or self.velocity.y != 0

    def _collisions(self, axis):
        for sprite in self.collision_group:
            if sprite.hitbox.colliderect(self.hitbox):
                print("COLLISION", axis)
                if axis == Axis.HORIZONTAL:
                    if self.velocity.x > 0:
                        self.hitbox.right = sprite.rect.left
                    elif self.velocity.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    if self.velocity.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    elif self.velocity.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    self.rect.centery = self.hitbox.centery

    def _move(self, delta):
        # normalizationws
        if self.velocity.magnitude() > 0:
            self.velocity = self.velocity.normalize()
        # move x
        self.rect.centerx = self.velocity.x * self.speed * delta
        self.hitbox.centerx = self.rect.centerx
        self._collisions(Axis.HORIZONTAL)
        # move y
        self.rect.centery = self.velocity.y * self.speed * delta
        self.hitbox.centery = self.rect.centery
        self._collisions(Axis.VERTICAL)

    def update(self, delta):
        self._move(delta)
        self.y_sort = self.rect.centery
        self._animate(delta)
