from game.level.attack import AttackArea
from game.settings import *
from game.math import points_dis
from game.components import FollowableSprite
from game.components.animation import AnimationEvent
from game.level.entity import Entity
from game.importer import import_named_animations, import_image


class Slimes(Enum):
    NORMAL_SLIME = 1


def build_slime_data(animations, start_animation_name, shadow_path, shadow_offset, attack_min_distance,
                     attack_damage, speed, health, chasing_min_distance_to_change_direction):
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
        "health": health,
        "chasing_min_distance_to_change_direction": chasing_min_distance_to_change_direction
    }


hash_slime_data = {}


class SlimeAnimation(Enum):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"
    HURTING = "hurting"


def get_slime_data(slime):
    if slime not in hash_slime_data:
        # build data
        if slime == Slimes.NORMAL_SLIME:
            hash_slime_data[slime] = build_slime_data(
                animations=import_named_animations(
                    [
                        (4, 1, SlimeAnimation.IDLE, 4),
                        (4, 1, SlimeAnimation.WALKING, 5),
                        (7, 1, SlimeAnimation.ATTACKING, 6),
                        (3, 1, SlimeAnimation.HURTING, 4),
                    ],
                    [
                        join('assets', 'characters', 'Slime', 'Slime-Idle.png'),
                        join('assets', 'characters', 'Slime', 'Slime-Walking.png'),
                        join('assets', 'characters', 'Slime', 'Slime-Attacking.png'),
                        join('assets', 'characters', 'Slime', 'Slime-Hurting.png'),
                    ]
                ),
                start_animation_name=SlimeAnimation.IDLE,
                shadow_path=None,
                shadow_offset=None,
                speed=130,
                health=5,
                # ia
                attack_damage=1,
                attack_min_distance=40,
                chasing_min_distance_to_change_direction=20,
            )
            # scale
            hash_slime_data[slime]["animations"][SlimeAnimation.IDLE].scale_frames(3)
            hash_slime_data[slime]["animations"][SlimeAnimation.WALKING].scale_frames(3)
            hash_slime_data[slime]["animations"][SlimeAnimation.ATTACKING].scale_frames(3)
            hash_slime_data[slime]["animations"][SlimeAnimation.HURTING].scale_frames(3)
    # return data
    return hash_slime_data[slime]


class Slime(Entity):
    def __init__(self, game, pos, group, collision_group, slime_data_type):
        # target
        self.target = None
        # get slime data
        self.slime_data = get_slime_data(slime_data_type)
        self.health = self.slime_data["health"]
        # super
        super().__init__(game, pos, self.slime_data["speed"], group, collision_group, self.slime_data['animations'], self.slime_data['start_animation_name'])
        # shadow
        self.shadow = FollowableSprite(
            import_image(self.slime_data['shadow']['path']),
            self,
            group,
            offset=self.slime_data['shadow']['offset'],
            z=WorldLayers.SHADOW
        ) if self.slime_data['shadow']['path'] is not None else None
        # attributes
        self.attacking = False
        # animation
        self.animation_controller.set_listener("AnimationsHandler", self.__animations_handler)

    def give_damage(self, damage):
        # health
        print(f"Receive damage: {damage}")
        self.health -= damage
        if self.health > 0:
            self.receiving_damage = True
        else:
            self.kill_entity()

        # attacking
        if self.attacking:
            self.attacking = False

    def __animations_handler(self, event, animation, animation_controller):
        if event == AnimationEvent.ANIMATION_CHANGED:
            self.attacking = (self.animation_controller.current_animation == SlimeAnimation.ATTACKING)
        elif event == AnimationEvent.ENDS:
            if self.animation_controller.current_animation == SlimeAnimation.HURTING:
                self.receiving_damage = False

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

    def __attack_give_damage_handler(self):
        # if self.flipped:
        #     AttackArea(self.attack_damage(),
        #         (self.rect.x, self.rect.y),
        #         (-self.attack_range[0], self.attack_range[1]),
        #         self.player_group
        #     )
        # else:
        #     AttackArea(self.attack_damage(),
        #         (self.rect.x, self.rect.y),
        #         self.attack_range,
        #         self.player_group
        #     )
        pass

    def _attack_hanlder(self):
        if not self.is_attacking() and not self.is_moving():
            if self.can_attack:
                self.attacking = True

    def _animate(self, delta):
        # animation
        if self.receiving_damage:
            self.animation_controller.change(SlimeAnimation.HURTING)
        elif self.is_moving():
            self.animation_controller.change(SlimeAnimation.WALKING)
        else:
            if self.is_attacking():
                self.animation_controller.change(SlimeAnimation.ATTACKING)
            else:
                self.animation_controller.change(SlimeAnimation.IDLE)

        # flip
        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super()._animate(delta)

    def update(self, delta):
        if not self.receiving_damage:
            self._ia()
        super().update(delta)
