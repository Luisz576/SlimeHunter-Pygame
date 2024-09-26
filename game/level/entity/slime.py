from game.settings import *
from game.components import FollowableSprite
from game.level.entity import NPEntity
from game.importer import import_named_animations, import_image


class Slimes(Enum):
    NORMAL_SLIME = 1


def build_slime_data(animations, start_animation_name, shadow_path, shadow_offset):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": shadow_path,
            "offset": shadow_offset
        }
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
                    ],
                    [
                        join('assets', 'characters', 'Slime', 'Slime-Idle.png'),
                        join('assets', 'characters', 'Slime', 'Slime-Walking.png'),
                    ]
                ),
                start_animation_name="idle",
                shadow_path=None,
                shadow_offset=None,
            )
            # scale
            hash_slime_data[slime]["animations"]["idle"].scale_frames(2)
            hash_slime_data[slime]["animations"]["walking"].scale_frames(2)
    # return data
    return hash_slime_data[slime]


class Slime(NPEntity):
    def __init__(self, pos, group, collision_group, slime_data_type):
        # get slime data
        slime_data = get_slime_data(slime_data_type)
        # super
        super().__init__(pos, group, collision_group, slime_data['animations'], slime_data['start_animation_name'])
        # goals
        self._register_goals()
        # shadow
        self.shadow = FollowableSprite(
            import_image(slime_data['shadow']['path']),
            self,
            group,
            offset=slime_data['shadow']['offset'],
            z=WorldLayers.SHADOW
        ) if slime_data['shadow']['path'] is not None else None

    def _register_goals(self):
        # self._register_goal(goal)
        pass

    def update(self, delta):
        # animation
        if self.is_moving():
            self.animation_controller.change("walking")
        else:
            self.animation_controller.change("idle")

        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super().update(delta)
