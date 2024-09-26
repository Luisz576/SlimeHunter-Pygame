from game.settings import *
from game.importer import import_named_animations, import_image
from game.level.entity import Entity
from game.components import FollowableSprite


hash_player_data = {}


def build_player_data(animations, start_animation_name, shadow_path, shadow_offset):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": shadow_path,
            "offset": shadow_offset
        }
    }


class Players(Enum):
    SOLDIER = 1


def get_player_data(player_key):
    if player_key not in hash_player_data:
        # build player data
        if player_key == Players.SOLDIER:
            hash_player_data[player_key] = build_player_data(
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
                shadow_path=join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Shadow.png'),
                shadow_offset=Vector2(2, 17)
            )
            # scale
            hash_player_data[player_key]["animations"]["idle"].scale_frames(2)
            hash_player_data[player_key]["animations"]["walking"].scale_frames(2)
    # return data
    return hash_player_data[player_key]


class Player(Entity):
    def __init__(self, pos, group, collision_group, player_data_type):
        # get data
        player_data = get_player_data(player_data_type)
        # super
        super().__init__(pos, group, collision_group, player_data['animations'], player_data['start_animation_name'])
        # shadow
        self.shadow = FollowableSprite(
            import_image(player_data['shadow']['path']),
            self,
            group,
            offset=player_data['shadow']['offset'],
            z=WorldLayers.SHADOW
        ) if player_data['shadow']['path'] is not None else None

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
