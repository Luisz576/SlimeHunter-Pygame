from game.settings import Enum, join
from game.level.item import Item

class Items(Enum):
    HEALTH_POTION = Item(1, "health_potion", join('assets', 'objects', 'red-potion.png'))
