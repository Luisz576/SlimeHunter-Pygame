from game.settings import *
from game.importer import import_named_animations, import_image
from game.level.entity import Entity
from game.components import FollowableSprite


hash_player_data = {}


def build_player_data(animations, start_animation_name):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Shadow.png'),
            "offset": Vector2(2, 17)
        }
    }


class Players(Enum):
    SOLDIER = 1


def get_player_data(player_key):
    if player_key in hash_player_data:
        return hash_player_data[player_key]
    # build player data
    if player_key == Players.SOLDIER:
        return build_player_data(
            animations=import_named_animations(
                [
                    (6, 1, "idle"),
                    (8, 1, "walking"),
                ],
                [
                    join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Idle.png'),
                    join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Walk.png'),
                ]
            ),
            start_animation_name="idle",
        )


class Player(Entity):
    def __init__(self, pos, group, player_data):
        super().__init__(pos, group, player_data['animations'], player_data['start_animation_name'])
        # shadow
        self.shadow = FollowableSprite(
            import_image(player_data['shadow']['path']),
            self,
            group,
            offset=player_data['shadow']['offset'],
            z=WorldLayers.SHADOW
        )

    def _input(self):
        keys = pygame.key.get_pressed()

        # moviment
        if keys[pygame.K_w]:
            self.velocity.y = -1
        elif keys[pygame.K_s]:
            self.velocity.y = 1
        else:
            self.velocity.y = 0

        if keys[pygame.K_a]:
            self.velocity.x = -1
        elif keys[pygame.K_d]:
            self.velocity.x = 1
        else:
            self.velocity.x = 0

    def update(self, delta):
        self._input()

        # animation
        if self.is_moving():
            self.animation_controller.change("walking")
        else:
            self.animation_controller.change("idle")

        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super().update(delta)
