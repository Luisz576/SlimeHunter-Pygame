from game.components import Animation
from game.settings import *
from pygame.transform import scale


def import_image(path, alpha=True):
    surf = pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()
    return surf


def import_tilemap(cols, rows, path, tilemap_scale=1):
    frames = {}
    surf = import_image(path)
    cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
    for col in range(cols):
        for row in range(rows):
            cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            cutout_surf = pygame.Surface((cell_width, cell_height))
            cutout_surf.fill('green')
            cutout_surf.set_colorkey('green')
            cutout_surf.blit(surf, (0, 0), cutout_rect)
            frames[(col, row)] = scale(cutout_surf, (cell_width * tilemap_scale, cell_height * tilemap_scale))
    return frames


def import_frames(cols, rows, path):
    frames = []
    surf = import_image(path)
    cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
    for col in range(cols):
        for row in range(rows):
            cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            cutout_surf = pygame.Surface((cell_width, cell_height))
            cutout_surf.fill('green')
            cutout_surf.set_colorkey('green')
            cutout_surf.blit(surf, (0, 0), cutout_rect)
            frames.append(cutout_surf)
    return frames


def import_animation(cols, rows, path, speed):
    if speed is None:
        speed = 4
    return Animation(import_frames(cols, rows, path), speed=speed)


def import_animations(animations_config, paths):
    animations = []
    for i in range(len(animations_config)):
        animations.append(import_animation(animations_config[i][0], animations_config[i][1], paths[i], animations_config[2] if len(animations_config) > 2 else None))
    return animations


def import_named_animations(animations_config, paths):
    animations = {}
    for i in range(len(animations_config)):
        animations[animations_config[i][2]] = import_animation(animations_config[i][0], animations_config[i][1], paths[i], animations_config[i][3] if len(animations_config[i]) > 3 else None)
    return animations
