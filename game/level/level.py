from game.settings import *


# class Levels(Enum):
#     WORLD_1 = join('..', 'maps', 'world.tmx')


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # sprite groups
        self.all_sprites = pygame.sprite.Group()

    def run(self, delta):
        self.display_surface.fill(COLORS['black'])
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()