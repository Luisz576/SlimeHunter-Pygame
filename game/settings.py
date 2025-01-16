import math

import pygame
import random
from pygame.math import Vector2
from enum import Enum
from sys import exit
from os.path import join

pygame.font.init()
pygame.mixer.init()

GAME_NAME = "Slime Hunter"

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TILE_SIZE = 16

COLORS = {
    "white": "#ffffff",
    "black": "#000000",
}


ENEMIES_TO_GIVE_ARROW = 5

class Axis(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class WorldLayers(Enum):
    BACKGROUND = 1
    BUILDING = 2
    SHADOW = 3
    ITEM = 4
    ENTITY = 5
    ATTACK=6
    AIR = 7


def WorldLayersValues():
    return [WorldLayers.BACKGROUND, WorldLayers.BUILDING, WorldLayers.SHADOW, WorldLayers.ITEM, WorldLayers.ENTITY,
            WorldLayers.AIR]


def calc_points_angle(p_start, p_end):
    delta_y = p_end[1] - p_start[1]
    delta_x = p_end[0] - p_start[0]

    angulo_rad = math.atan2(delta_y, delta_x)
    angulo_deg = math.degrees(angulo_rad)

    return angulo_deg

def calc_point_angle(vec):
    return math.degrees(math.atan2(-vec[1], vec[0]))

def calc_points_vector_look(p_start, p_end):
    delta_x = p_end[0] - p_start[0]
    delta_y = p_end[1] - p_start[1]

    mag = math.sqrt(delta_x**2 + delta_y**2)

    vec = (delta_x / mag, delta_y / mag)
    return vec

MAX_DIFFICULT = 10
SLIME_CHANCES_TO_SPAWN_BASED_ON_TIME = {
    0: 0.0015,
    1: 0.002,
    2: 0.0025,
    3: 0.003,
    4: 0.0035,
    5: 0.004,
    6: 0.005,
    7: 0.006,
    8: 0.007,
    9: 0.008,
    10: 0.01,
    100: 0.08
}
