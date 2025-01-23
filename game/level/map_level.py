from game.settings import *
from game.level import Level
from .map import Map
from game.components import RenderSpritesGroup, CollisionSpritesGroup, EnemyGroup, PlayerGroup
from game.level.entity import Player, Players, ItemEntity
from game.ui import PauseScreen, GameHud
from ..components.groups import ItemSpritesGroup
from game.level.item import Item


class MapLevel(Level):
    def __init__(self, game, map_path, map_layers, map_collision_layers, tile_scale, background_music_path):
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
        self.item_sprites = ItemSpritesGroup()
        self.render_sprites = RenderSpritesGroup()
        self.collision_sprites = CollisionSpritesGroup()

        # map
        self.map = Map(map_path, map_layers, map_collision_layers, self.render_sprites,
                       collision_group=self.collision_sprites, tile_scale=tile_scale)
        # enemy
        self.enemies = []
        self.enemy_group = EnemyGroup()

        # items
        self.dropped_items = []

        # projectile
        self.projectiles = []

        # player
        self.player_group = PlayerGroup()
        self.player = None
        self.spawn_player()

        # bg sound
        self.background_music_path = background_music_path
        if self.background_music_path is not None:
            self.game.sound_manager.set_background_music(self.background_music_path)

    def unload_level(self):
        self.game.sound_manager.set_background_music(None)

    def spawn_player(self):
        if self.player is None:
            self.player = Player(
                self.game,
                (400, 400),
                [self.render_sprites, self.player_group],
                self.collision_sprites,
                self.enemy_group,
                self.item_sprites,
                self.render_sprites,
                Players.SOLDIER
            )

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def kill_entity(self, entity):
        for enemy in self.enemies:
            if enemy.uuid == entity.uuid:
                self.enemies.remove(enemy)
                self.add_score(enemy.enemy_die_score)
                return

    def spawn_item(self, pos, item: Item):
        item_entity = ItemEntity(pos, item, self.render_sprites, self.item_sprites)
        self.dropped_items.append(item_entity)

    def remove_dropped_item(self, item_entity):
        self.dropped_items.remove(item_entity)
        item_entity.kill()

    def clear_items(self):
        for item_entity in self.dropped_items:
            item_entity.kill()
        self.dropped_items.clear()

    def add_score(self, points):
        self.game.game_score += points
        if self.game.game_score % ENEMIES_TO_GIVE_ARROW == 0:
            self.player.inventory.give_arrow()

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
            self.pause_screen.page_index = 0
            self.paused = not self.paused
            self.paused_delay = 0.2
            # music
            if self.background_music_path is not None:
                if self.paused:
                    self.game.sound_manager.set_background_music(None)
                else:
                    self.game.sound_manager.set_background_music(self.background_music_path)

    def is_paused(self):
        return self.paused

    def run(self, delta):
        # input
        self._input(delta)
        # update
        if self.paused:
            self.pause_screen.update(delta)
        else:
            self.game_hud.update(delta)
        # projectiles
        to_remove = []
        for projectile in self.projectiles:
            if projectile.is_destroyed:
                to_remove.append(projectile)
            else:
                projectile.update(delta)
        for r in to_remove:
            self.projectiles.remove(r)
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
