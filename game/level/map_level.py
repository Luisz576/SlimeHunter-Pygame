from game.settings import *
from game.level import Level
from game.level.hud import Hud
from .map import Map
from game.components import RenderSpritesGroup, CollisionSpritesGroup, EnemyGroup
from game.level.entity import Player, Players
from game.ui import PauseScreen


class MapLevel(Level):
    def __init__(self, game, map_path, map_layers, map_collision_layers, tile_scale):
        super().__init__(game)
        # init
        self.pause_screen = None

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.render_sprites = RenderSpritesGroup()
        self.collision_sprites = CollisionSpritesGroup()

        # map
        self.map = Map(map_path, map_layers, map_collision_layers, self.render_sprites,
                       collision_group=self.collision_sprites, tile_scale=tile_scale)
        self.enemies = []
        # player
        self.enemy_group = EnemyGroup()
        self.player = Player(
            self.game,
            (400, 400),
            self.render_sprites,
            self.collision_sprites,
            self.enemy_group,
            Players.SOLDIER
        )
        # hud
        self.hud = Hud(self)

        # pause
        self.paused = False
        self.load_pause_screen()
        if self.pause_screen is None:
            raise Exception("Pause screen not loaded!")

    def load_pause_screen(self):
        self.pause_screen = PauseScreen(self)

    def _input(self):
        # TODO: FIX PRESS (IF YOU PRESS SO MUCH IT PAUSE AND UNPAUSE)
        keys = pygame.key.get_pressed()

        # pause
        if keys[pygame.K_ESCAPE]:
            self.paused = not self.paused

    def run(self, delta):
        # input
        self._input()
        # update
        if self.paused:
            self.pause_screen.update(delta)
        else:
            self._update(delta)
        # clear
        self.display_surface.fill(COLORS['black'])
        # sprites
        if self.paused:
            self.pause_screen.render(delta)
        else:
            self._render(delta)

    def _update(self, delta):
        self.hud.update(delta)

    def _render(self, delta):
        self.render_sprites.draw(self.player.rect.center)
        self.render_sprites.update(delta)
        self.hud.draw()
