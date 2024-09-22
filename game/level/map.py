from game.settings import *
from game.components import Sprite, CollidableSprite
from pytmx.util_pygame import load_pygame


class Map:
    def __init__(self, path, layers, collision_layers, group, collision_group=None):
        self.path = path
        self.layers = layers
        self.collision_layers = collision_layers
        self.tmx_map = load_pygame(self.path)
        self.sprites = []
        self.collision_sprites = []
        if collision_group is None:
            collision_group = group
        self._setup(group, collision_group)

    def _setup(self, group, collision_group):
        if self.tmx_map is None:
            raise Exception("Map not loaded!")
        for layer in self.layers:
            for x, y, surf in self.tmx_map.get_layer_by_name(layer).tiles():
                self.sprites.append(Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, group, z=WorldLayers.BACKGROUND))
        for collision_layer in self.collision_layers:
            for obj in self.tmx_map.get_layer_by_name(collision_layer):
                self.collision_sprites.append(CollidableSprite((obj.x, obj.y),
                                                               pygame.Surface((obj.width, obj.height)),
                                                               collision_group))
