from ..settings import *


class AllSpritesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2(0, 0)

    def draw(self, center):
        self.offset.x = -(center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(center[1] - WINDOW_HEIGHT / 2)

        for sprite in self:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

