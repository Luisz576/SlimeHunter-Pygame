from game.settings import *
from game.math import points_dis
from game.components import FollowableSprite
from game.level.entity import Entity
from game.importer import import_named_animations, import_image


class Slimes(Enum):
    NORMAL_SLIME = 1


def build_slime_data(animations, start_animation_name, shadow_path, shadow_offset, attack_min_distance,
                     attack_damage, speed, chasing_min_distance_to_change_direction):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": shadow_path,
            "offset": shadow_offset
        },
        "attack_min_distance": attack_min_distance,
        "attack_damage": attack_damage,
        "speed": speed,
        "chasing_min_distance_to_change_direction": chasing_min_distance_to_change_direction
    }


hash_slime_data = {}


def get_slime_data(slime):
    if slime not in hash_slime_data:
        # build data
        if slime == Slimes.NORMAL_SLIME:
            hash_slime_data[slime] = build_slime_data(
                animations=import_named_animations(
                    [
                        (4, 1, "idle"),
                        (4, 1, "walking"),
                        # (4, 1, "attacking"),
                    ],
                    [
                        join('assets', 'characters', 'Slime', 'Slime-Idle.png'),
                        join('assets', 'characters', 'Slime', 'Slime-Walking.png'),
                        # join('assets', 'characters', 'Slime', 'Slime-Attacking.png'),
                    ]
                ),
                start_animation_name="idle",
                shadow_path=None,
                shadow_offset=None,
                speed=170,
                # ia
                attack_damage=1,
                attack_min_distance=40,
                chasing_min_distance_to_change_direction=20,
            )
            # scale
            hash_slime_data[slime]["animations"]["idle"].scale_frames(3)
            hash_slime_data[slime]["animations"]["walking"].scale_frames(3)
    # return data
    return hash_slime_data[slime]


class Slime(Entity):
    def __init__(self, pos, group, collision_group, slime_data_type):
        # target
        self.target = None
        # get slime data
        self.slime_data = get_slime_data(slime_data_type)
        # super
        super().__init__(pos, self.slime_data["speed"], group, collision_group, self.slime_data['animations'], self.slime_data['start_animation_name'])
        # shadow
        self.shadow = FollowableSprite(
            import_image(self.slime_data['shadow']['path']),
            self,
            group,
            offset=self.slime_data['shadow']['offset'],
            z=WorldLayers.SHADOW
        ) if self.slime_data['shadow']['path'] is not None else None

    def _ia(self):
        self.velocity.x = 0
        self.velocity.y = 0
        if self.target is not None:
            dis_target = (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
            dis = points_dis((self.target.rect.x, self.target.rect.y), (self.rect.x, self.rect.y))
            if dis > self.slime_data["attack_min_distance"]:
                # moviment
                # move x
                if dis_target[0] > self.slime_data["chasing_min_distance_to_change_direction"]:
                    self.velocity.x = 1
                elif dis_target[0] < -1 * self.slime_data["chasing_min_distance_to_change_direction"]:
                    self.velocity.x = -1
                # move y
                if dis_target[1] > self.slime_data["chasing_min_distance_to_change_direction"]:
                    self.velocity.y = 1
                elif dis_target[1] < -1 * self.slime_data["chasing_min_distance_to_change_direction"]:
                    self.velocity.y = -1
            else:
                # attack
                self._attack_hanlder()

    def _attack_hanlder(self):
        # TODO: start attack animation
        # TODO: subscribe animation attack
        # TODO: create func attack_damage and spawn AttackArea
        pass

    def update(self, delta):
        self._ia()

        # animation
        if self.is_moving():
            self.animation_controller.change("walking")
        else:
            self.animation_controller.change("idle")

        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super().update(delta)
