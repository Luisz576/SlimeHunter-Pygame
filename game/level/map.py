from ..settings import *
from game.components import Sprite
from pytmx.util_pygame import load_pygame


class Map:
    def __init__(self, path, layers, collision_layers, group):
        self.path = path
        self.layers = layers
        self.collision_layers = collision_layers
        self.tmx_map = load_pygame(self.path)
        self.sprites = []
        self._setup(group)

    def _setup(self, group):
        if self.tmx_map is None:
            raise Exception("Map not loaded!")
        for layer in self.layers:
            for x, y, surf in self.tmx_map.get_layer_by_name(layer).tiles():
                self.sprites.append(Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, group, z=WorldLayers.BACKGROUND))
        for collision_layer in self.collision_layers:
            pass
            # for x, y, surf in self.tmx_map.get_layer_by_name(collision_layer).tiles():
            #   Body2D((x * TILE_SIZE, y * TILE_SIZE), surf, group))?
