from game.settings import *
from game.importer import import_named_animations, import_image
from game.level.entity import Entity
from game.components import FollowableSprite, Health
from game.components.animation import AnimationEvent


hash_player_data = {}


def build_player_data(animations, start_animation_name, shadow_path, max_health, shadow_offset, speed, shadow_scale=1):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": shadow_path,
            "offset": shadow_offset,
            "scale": shadow_scale
        },
        "speed": speed,
        "max_health": max_health
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
                        (6, 1, "attacking"),
                    ],
                    [
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Idle.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Walk.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Attack01.png'),
                    ]
                ),
                max_health=6,
                start_animation_name="idle",
                shadow_path=join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Shadow.png'),
                shadow_offset=Vector2(25, 63),
                shadow_scale=3,
                speed=200,
            )
            # scale
            hash_player_data[player_key]["animations"]["idle"].scale_frames(3)
            hash_player_data[player_key]["animations"]["walking"].scale_frames(3)
            hash_player_data[player_key]["animations"]["attacking"].scale_frames(3)
            hash_player_data[player_key]["animations"]["attacking"].speed = 15
    # return data
    return hash_player_data[player_key]


class Player(Entity):
    def __init__(self, pos, group, collision_group, player_data_type):
        # get data
        self.player_data = get_player_data(player_data_type)
        # super
        super().__init__(pos, self.player_data["speed"], group, collision_group, self.player_data['animations'],
                         self.player_data['start_animation_name'])
        # health
        self.health = Health(self.player_data["max_health"])
        # shadow
        self.shadow = FollowableSprite(
            import_image(self.player_data['shadow']['path']),
            self,
            group,
            offset=self.player_data['shadow']['offset'],
            z=WorldLayers.SHADOW
        ).scale(self.player_data['shadow']['scale'] if self.player_data['shadow']['scale'] > 1 else 1)\
            if self.player_data['shadow']['path'] is not None else None
        # register listener
        self.animation_controller.set_listener("AnimationsHandler", self.__animations_handler)
        self.player_data["animations"]["attacking"].set_listener("attack_listener", self.__attack_handler)

    def __animations_handler(self, event, animation, animation_controller):
        if event == AnimationEvent.ANIMATION_CHANGED:
            if self.animation_controller.current_animation != "attacking":
                self.attacking = False

    def __attack_handler(self, event, animation):
        if event == AnimationEvent.ENDS:
            self.attacking = False

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

        # attack
        if keys[pygame.K_SPACE]:
            self._attack_handler()

    def _attack_handler(self):
        if not self.is_attacking():
            if self.can_attack:
                self.attacking = True

    def update(self, delta):
        self._input()

        # animation
        if self.is_moving():
            self.animation_controller.change("walking")
        else:
            if self.is_attacking():
                self.animation_controller.change("attacking")
            else:
                self.animation_controller.change("idle")

        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super().update(delta)
