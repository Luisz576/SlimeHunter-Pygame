from ..settings import *


class AllSpritesGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2(0, 0)

    def draw(self, center):
        self.offset.x = -(center[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(center[1] - WINDOW_HEIGHT / 2)

        sprites_by_layer = {}
        for layer in WorldLayersValues():
            sprites_by_layer[layer] = []
        for sprite in self:
            sprites_by_layer[sprite.z].append(sprite)

        for layer in WorldLayersValues():
            sprites_by_layer[layer] = sorted(sprites_by_layer[layer], key=lambda s: s.y_sort)
            for sprite in sprites_by_layer[layer]:
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
