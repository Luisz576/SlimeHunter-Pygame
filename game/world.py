from enum import Enum
from pytmx.util_pygame import load_pygame
from os.path import join


class Levels(Enum):
    WORLD_1 = join('..', 'maps', 'world.tmx')


class World:
    def __init__(self, world_path):
        self.path = world_path
        self.tmx_map = load_pygame(self.path)
