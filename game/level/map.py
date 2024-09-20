from ..settings import *
from game.components import Sprite
from pytmx.util_pygame import load_pygame


class Map:
    def __init__(self, path, layers, group):
        self.path = path
        self.layers = layers
        self.tmx_map = load_pygame(self.path)
        self._setup(group)

    def _setup(self, group):
        if self.tmx_map is None:
            raise Exception("Map not loaded!")
        for layer in self.layers:
            for x, y, surf in self.tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, group)
