from game.settings import Enum, join
from game.level.item import Item

class Items(Enum):
    HEALTH_POTION = Item("health_potion", join('assets', 'objects', 'objects.png'))
