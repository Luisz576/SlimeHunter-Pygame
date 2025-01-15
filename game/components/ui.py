import pygame

from game.settings import Enum
from pygame.font import SysFont


class UIComponent:
    def __init__(self, pos):
        self.pos = pos

    def update(self, delta):
        pass

    def render(self, screen):
        pass


# FONTS
def create_font(font, size):
    return SysFont(font, size)


def font_comic_sans_ms(size):
    return create_font('Comic Sans MS', size)


# Label
class Label(UIComponent):
    def __init__(self, text, pos, color, size, font=None):
        super().__init__(pos)
        self.text = text
        self.color = color
        self.size = size
        self.font = font
        if self.font is None:
            self.font = font_comic_sans_ms(self.size)
        self.surface = None
        self.update_surface()

    def change_color(self, color):
        self.color = color
        self.update_surface()

    def change_size(self, size):
        self.size = size
        self.update_surface()

    def change_text(self, text):
        self.text = text
        self.update_surface()

    def update_surface(self):
        self.surface = self.font.render(self.text, False, self.color)

    def render(self, screen):
        screen.blit(self.surface, self.pos)


class ButtonLabel(Label):
    def __init__(self, text, pos, not_selected_color, selected_color, size, time_selected=1, selected=False, font=None):
        super().__init__(text, pos, not_selected_color, size, font)
        self.not_selected_color = not_selected_color
        self.selected_color = selected_color
        self.selected = selected
        self.time_selected = time_selected
        self.time_selected_delta = 0

    def _is_color_selected(self):
        return self.color[0] != self.not_selected_color[0] or self.color[1] != self.not_selected_color[1] or self.color[2] != self.not_selected_color[2]

    def update(self, delta):
        if self.selected:
            self.time_selected_delta = self.time_selected_delta + delta
            if self.time_selected_delta > self.time_selected:
                self.time_selected_delta = 0
                if self._is_color_selected():
                    self.change_color(self.not_selected_color)
                else:
                    self.change_color(self.selected_color)
        else:
            self.time_selected_delta = 0
            if self._is_color_selected():
                self.change_color(self.not_selected_color)

# InlineComponents
class InlineComponents(UIComponent):
    def __init__(self, pos_x, pos_y, offset_x, offset_y, icons):
        super().__init__(pos_x)
        self.icons = icons
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.amount = len(icons)
        self.__MAX__ = len(icons)

    def set_render_amount(self, amount):
        self.amount = max(0, min(amount, self.__MAX__))

    def update(self, delta):
        for i in range(len(self.icons)):
            icon_pos_x = self.pos_x + (i * self.offset_x)
            icon_pos_y = self.pos_y + (i * self.offset_y)
            self.icons[i].pos = (icon_pos_x, icon_pos_y)
            self.icons[i].update(delta)
            i += 1

    def render(self, screen):
        for i in range(self.__MAX__):
            if i < self.amount:
                self.icons[i].render(screen)

class Image(UIComponent):
    def __init__(self, pos, path):
        super().__init__(pos)
        self.path = path
        self.img = pygame.image.load(path)

    def update(self, delta):
        pass

    def render(self, screen):
        screen.blit(self.img, self.pos)
