import pygame
import random
from pygame.math import Vector2
from enum import Enum
from sys import exit
from os.path import join

GAME_NAME = "Slime Hunter"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

TILE_SIZE = 16

COLORS = {
    "white": "#ffffff",
    "black": "#000000",
}


class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class WorldLayers(Enum):
    BACKGROUND = 1
    BUILDING = 2
    SHADOW = 3
    ITEM = 4
    ENTITY = 5
    AIR = 6


def WorldLayersValues():
    return [WorldLayers.BACKGROUND, WorldLayers.BUILDING, WorldLayers.SHADOW, WorldLayers.ITEM, WorldLayers.ENTITY,
            WorldLayers.AIR]

