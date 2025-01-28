from game.level.item import Items
from game.settings import *
from game.math import points_dis
from game.components import FollowableSprite
from game.components.animation import AnimationEvent
from game.level.entity import EnemyEntity
from game.level.entity.slime import Slimes
from game.level.attack import AttackArea
from game.importer import import_named_animations, import_image


def build_slime_data(animations, start_animation_name, shadow_path, shadow_offset, attack_min_distance, loot_chances,
                     attack_damage, speed, health, chasing_min_distance_to_change_direction, attack_range, slime_die_score):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": shadow_path,
            "offset": shadow_offset
        },
        "attack_min_distance": attack_min_distance,
        "attack_damage": attack_damage,
        "attack_range": attack_range,
        "speed": speed,
        "health": health,
        "chasing_min_distance_to_change_direction": chasing_min_distance_to_change_direction,
        "slime_die_score": slime_die_score,
        "loot_chances": loot_chances,
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
            slime_data = build_slime_data(
                animations=import_named_animations(
                    [
                        (4, 1, SlimeAnimation.IDLE, 4),
                        (4, 1, SlimeAnimation.WALKING, 3),
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
                speed=150,
                health=5,
                # ia
                attack_damage=1,
                attack_range=(50, 50),
                attack_min_distance=20,
                chasing_min_distance_to_change_direction=15,
                slime_die_score = 1,
                loot_chances = {
                    '1': 0.06
                }
            )
            # scale
            slime_data["animations"][SlimeAnimation.IDLE].scale_frames(3)
            slime_data["animations"][SlimeAnimation.WALKING].scale_frames(3)
            slime_data["animations"][SlimeAnimation.ATTACKING].scale_frames(3)
            slime_data["animations"][SlimeAnimation.HURTING].scale_frames(3)
            return slime_data
        elif slime == Slimes.FAST_SLIME:
            slime_data = build_slime_data(
                animations=import_named_animations(
                    [
                        (4, 1, SlimeAnimation.IDLE, 4),
                        (4, 1, SlimeAnimation.WALKING, 3),
                        (7, 1, SlimeAnimation.ATTACKING, 6),
                        (3, 1, SlimeAnimation.HURTING, 4),
                    ],
                    [
                        join('assets', 'characters', 'FastSlime', 'Slime-Idle.png'),
                        join('assets', 'characters', 'FastSlime', 'Slime-Walking.png'),
                        join('assets', 'characters', 'FastSlime', 'Slime-Attacking.png'),
                        join('assets', 'characters', 'FastSlime', 'Slime-Hurting.png'),
                    ]
                ),
                start_animation_name=SlimeAnimation.IDLE,
                shadow_path=None,
                shadow_offset=None,
                speed=280,
                health=3,
                # ia
                attack_damage=1,
                attack_range=(50, 50),
                attack_min_distance=20,
                chasing_min_distance_to_change_direction=15,
                slime_die_score=2,
                loot_chances={
                    '1': 0.08
                }
            )
            # scale
            slime_data["animations"][SlimeAnimation.IDLE].scale_frames(3)
            slime_data["animations"][SlimeAnimation.WALKING].scale_frames(3)
            slime_data["animations"][SlimeAnimation.ATTACKING].scale_frames(3)
            slime_data["animations"][SlimeAnimation.HURTING].scale_frames(3)
            return slime_data
        elif slime == Slimes.TANK_SLIME:
            slime_data = build_slime_data(
                animations=import_named_animations(
                    [
                        (4, 1, SlimeAnimation.IDLE, 4),
                        (4, 1, SlimeAnimation.WALKING, 3),
                        (7, 1, SlimeAnimation.ATTACKING, 6),
                        (3, 1, SlimeAnimation.HURTING, 4),
                    ],
                    [
                        join('assets', 'characters', 'TankSlime', 'Slime-Idle.png'),
                        join('assets', 'characters', 'TankSlime', 'Slime-Walking.png'),
                        join('assets', 'characters', 'TankSlime', 'Slime-Attacking.png'),
                        join('assets', 'characters', 'TankSlime', 'Slime-Hurting.png'),
                    ]
                ),
                start_animation_name=SlimeAnimation.IDLE,
                shadow_path=None,
                shadow_offset=None,
                speed=150,
                health=11,
                # ia
                attack_damage=1,
                attack_range=(70, 60),
                attack_min_distance=24,
                chasing_min_distance_to_change_direction=14,
                slime_die_score=3,
                loot_chances={
                    '1': 0.12
                }
            )
            # scale
            slime_data["animations"][SlimeAnimation.IDLE].scale_frames(3)
            slime_data["animations"][SlimeAnimation.WALKING].scale_frames(3)
            slime_data["animations"][SlimeAnimation.ATTACKING].scale_frames(3)
            slime_data["animations"][SlimeAnimation.HURTING].scale_frames(3)
            return slime_data
        # none
        return None


class Slime(EnemyEntity):
    def __init__(self, game, pos, group, collision_group, player_group, slime_data_type):
        # target
        self.target = None
        self.player_group = player_group
        # get slime data
        self.slime_data = get_slime_data(slime_data_type)
        self.health = self.slime_data["health"]
        # super
        super().__init__(game, pos, self.slime_data["speed"], group, collision_group, self.slime_data['animations'],
                         self.slime_data['start_animation_name'], self.slime_data['slime_die_score'])
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
        self.attack_damage = self.slime_data['attack_damage']
        self.attack_range = self.slime_data['attack_range']
        # animation
        self.animation_controller.set_listener("AnimationsHandler", self.__animations_handler)

    def give_damage(self, damage):
        # health
        print(f"Receive damage: {damage}")
        self.health -= damage
        if self.health > 0:
            self.receiving_damage = True
        else:
            self.maybe_give_loot()
            self.kill_entity()

        # attacking
        if self.attacking:
            self.attacking = False

    def maybe_give_loot(self):
        for item_id in self.slime_data["loot_chances"]:
            percent = self.slime_data["loot_chances"][item_id]
            if random.random() <= percent:
                self.game.level.spawn_item((self.rect.centerx, self.rect.centery), Items.HEALTH_POTION.value)
                break

    def __animations_handler(self, event, animation, animation_controller):
        if event == AnimationEvent.ANIMATION_CHANGED:
            if animation_controller.current_animation != SlimeAnimation.ATTACKING:
                self.attacking = False
        elif event == AnimationEvent.ENDS:
            self.receiving_damage = False
        elif event == AnimationEvent.FRAME_CHANGED:
            if animation.index == 5 and animation_controller.current_animation == SlimeAnimation.ATTACKING:
                self.__attack_give_damage_handler()

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
        if self.flipped:
            AttackArea(self.attack_damage,
                (self.rect.centerx + 10, self.rect.centery),
                (-self.attack_range[0], self.attack_range[1]),
                self.player_group
            )
        else:
            AttackArea(self.attack_damage,
                (self.rect.centerx - 10, self.rect.centery),
                self.attack_range,
                self.player_group
            )

    def _attack_hanlder(self):
        if not self.is_attacking() and not self.is_moving():
            if self.can_attack:
                self.attacking = True
        elif not self.is_moving():
            dis_target = (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
            if abs(dis_target[0]) > 5:
                self.flipped = dis_target[0] < 0

    def _animate(self, delta):
        # animation
        if self.receiving_damage:
            self.animation_controller.change(SlimeAnimation.HURTING)
        elif self.is_attacking():
            self.animation_controller.change(SlimeAnimation.ATTACKING)
        elif self.is_moving():
            self.animation_controller.change(SlimeAnimation.WALKING)
        else:
            self.animation_controller.change(SlimeAnimation.IDLE)

        # flip
        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super()._animate(delta)

    def update(self, delta):
        if self.receiving_damage:
            self.velocity.x = 0
            self.velocity.y = 0
        else:
            self._ia()
        super().update(delta)
