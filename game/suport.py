from settings import *


def import_image(*path, alpha=True, format='png'):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf


def import_tilemap(*path, cols, rows):
    frames = {}
    surf = import_image(*path)
    cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
    for col in range(cols):
        for row in range(rows):
            cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            cutout_surf = pygame.Surface((cell_width, cell_height))
            cutout_surf.fill('green')
            cutout_surf.set_colorkey('green')
            cutout_surf.blit(surf, (0, 0), cutout_rect)
            frames[(col, row)] = cutout_surf
    return frames
