from game.components import Sprite
from game.level.item import Item
from game.importer import import_image

class ItemEntity(Sprite):
    def __init__(self, pos, data: Item, group):
        self.data = data
        super().__init__(pos, import_image(self.data.sprite_path), group)
