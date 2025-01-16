from game.components.sound_manager import SoundManager
from game.settings import Enum, join


class Sounds(Enum):
    PLAYER_HURTED = "player_hurted"
    SWORD_ATTACK = "sword_attack"
    ARROW_SHOOT = "arrow_shoot"


class SlimeHunterSoundManager(SoundManager):
    def __init__(self):
        super().__init__()

        self.register_sounds()

    def register_sounds(self):
        self.set_sound(Sounds.PLAYER_HURTED, join('assets', 'sounds', 'damage_grunt_male.wav'))
        self.set_sound(Sounds.SWORD_ATTACK, join('assets', 'sounds', 'sword_attack.wav'))
        self.set_sound(Sounds.ARROW_SHOOT, join('assets', 'sounds', 'arrow_shoot.wav'))
