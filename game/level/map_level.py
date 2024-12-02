from game.settings import *
from game.level import Level
from .map import Map
from game.components import RenderSpritesGroup, CollisionSpritesGroup, EnemyGroup, PlayerGroup
from game.level.entity import Player, Players
from game.ui import PauseScreen, GameHud


class MapLevel(Level):
    def __init__(self, game, map_path, map_layers, map_collision_layers, tile_scale):
        super().__init__(game)
        # init
        self.pause_screen = None
        self.game_hud = None

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # pause
        self.paused = False
        self.paused_delay = 0
        self.load_pause_screen()
        if self.pause_screen is None:
            raise Exception("Pause screen not loaded!")

        self.load_game_hud()
        if self.game_hud is None:
            raise Exception("Game hud not loaded!")

        # sprite groups
        self.render_sprites = RenderSpritesGroup()
        self.collision_sprites = CollisionSpritesGroup()

        # map
        self.map = Map(map_path, map_layers, map_collision_layers, self.render_sprites,
                       collision_group=self.collision_sprites, tile_scale=tile_scale)
        # enemy
        self.enemies = []
        self.enemy_group = EnemyGroup()

        # player
        self.player_group = PlayerGroup()
        self.player = None
        self.spawn_player()

    def spawn_player(self):
        if self.player is None:
            self.player = Player(
                self.game,
                (400, 400),
                [self.render_sprites, self.player_group],
                self.collision_sprites,
                self.enemy_group,
                Players.SOLDIER
            )

    def kill_entity(self, entity):
        for enemy in self.enemies:
            if enemy.uuid == entity.uuid:
                self.enemies.remove(enemy)
                self.game.game_score += enemy.enemy_die_score
                return

    def load_pause_screen(self):
        self.pause_screen = PauseScreen(self.game)

    def load_game_hud(self):
        self.game_hud = GameHud(self.game)

    def _input(self, delta):
        keys = pygame.key.get_pressed()

        # pause
        if self.paused_delay > 0:
            self.paused_delay -= delta
        if keys[pygame.K_ESCAPE] and self.paused_delay <= 0:
            self.paused = not self.paused
            self.paused_delay = 0.2

    def run(self, delta):
        # input
        self._input(delta)
        # update
        if self.paused:
            self.pause_screen.update(delta)
        else:
            self.game_hud.update(delta)
        # clear
        self.display_surface.fill(COLORS['black'])
        # sprites
        if self.paused:
            self.pause_screen.render(delta)
        else:
            self._render(delta)

    def _render(self, delta):
        self.render_sprites.draw(self.player.rect.center)
        self.render_sprites.update(delta)
        self.game_hud.render(delta)
