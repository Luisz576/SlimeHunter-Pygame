from game.level.attack import AttackArea
from game.settings import *
from game.importer import import_named_animations, import_image
from game.level.entity import Entity
from game.components import FollowableSprite, Health
from game.components.animation import AnimationEvent
from game.level.inventory import PlayerInventory
from game.sound import Sounds


class PlayerAnimation(Enum):
    IDLE = "idle"
    WALKING = "walking"
    ATTACKING = "attacking"
    HURTING = "hurting"


hash_player_data = {}


def build_player_data(animations, start_animation_name, shadow_path, max_health, shadow_offset, speed, attack_range, base_attack_damage, shadow_scale=1):
    return {
        "animations": animations,
        "start_animation_name": start_animation_name,
        "shadow": {
            "path": shadow_path,
            "offset": shadow_offset,
            "scale": shadow_scale
        },
        "speed": speed,
        "max_health": max_health,
        "attack_range": attack_range,
        "base_attack_damage": base_attack_damage
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
                        (6, 1, PlayerAnimation.IDLE, 4),
                        (8, 1, PlayerAnimation.WALKING, 4),
                        (6, 1, PlayerAnimation.ATTACKING, 15),
                        # (6, 1, PlayerAnimation.HURTING, ?),
                    ],
                    [
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Idle.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Walk.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Attack01.png'),
                    ]
                ),
                max_health=3,
                start_animation_name=PlayerAnimation.IDLE,
                shadow_path=join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Shadow.png'),
                shadow_offset=Vector2(25, 63),
                shadow_scale=3,
                speed=300,
                attack_range=(60, 50),
                base_attack_damage=2,
            )
            # scale
            hash_player_data[player_key]["animations"][PlayerAnimation.IDLE].scale_frames(3)
            hash_player_data[player_key]["animations"][PlayerAnimation.WALKING].scale_frames(3)
            hash_player_data[player_key]["animations"][PlayerAnimation.ATTACKING].scale_frames(3)
            # hash_player_data[player_key]["animations"][PlayerAnimation.HURTING].scale_frames(3)
    # return data
    return hash_player_data[player_key]


class Player(Entity):
    def __init__(self, game, pos, group, collision_group, enemy_group, player_data_type):
        self.enemy_group = enemy_group
        # get data
        self.player_data = get_player_data(player_data_type)
        # super
        super().__init__(game, pos, self.player_data["speed"], group, collision_group, self.player_data['animations'],
                         self.player_data['start_animation_name'])
        # attack
        self.base_attack_damage = self.player_data['base_attack_damage']
        self.attack_range = self.player_data['attack_range']
        # player inventory
        self.inventory = PlayerInventory()
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
        self.player_data["animations"][PlayerAnimation.ATTACKING].set_listener("attack_listener", self.__attack_handler)

    def attack_damage(self):
        return self.base_attack_damage # + inventory....

    def give_damage(self, damage):
        self.health.hurt(damage)
        if self.health.health > 0:
            #self.receiving_damage = True
            print(f"Player receive damage: {damage}")
            self.game.sound_manager.play_sound(Sounds.PLAYER_HURTED)
        else:
            self.game.level.game_over()

    def __animations_handler(self, event, animation, animation_controller):
        if event == AnimationEvent.ANIMATION_CHANGED:
            if self.animation_controller.current_animation != PlayerAnimation.ATTACKING:
                self.attacking = False

    def __attack_handler(self, event, animation):
        if event == AnimationEvent.ENDS:
            self.attacking = False
        elif event == AnimationEvent.FRAME_CHANGED:
            if animation.index == 3:
                self.__attack_give_damage_handler()

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
            self._attack_input_handler()

    def _attack_input_handler(self):
        if not self.is_attacking() and not self.is_moving():
            if self.can_attack:
                self.attacking = True

    def __attack_give_damage_handler(self):
        self.game.sound_manager.play_sound(Sounds.SWORD_ATTACK)
        if self.flipped:
            AttackArea(self.attack_damage(),
                (self.rect.centerx, self.rect.centery),
                (-self.attack_range[0], self.attack_range[1]),
                self.enemy_group
            )
        else:
            AttackArea(self.attack_damage(),
                (self.rect.centerx, self.rect.centery),
                self.attack_range,
                self.enemy_group
            )

    def _animate(self, delta):
        # animation
        if self.is_attacking():
            self.animation_controller.change(PlayerAnimation.ATTACKING)
        #elif self.receiving_damage:
            #self.animation_controller.change(PlayerAnimation.HURTING)
        elif self.is_moving():
            self.animation_controller.change(PlayerAnimation.WALKING)
        else:
            self.animation_controller.change(PlayerAnimation.IDLE)

        # flip
        if self.velocity.x != 0:
            self.flipped = self.velocity.x < 0

        super()._animate(delta)

    def update(self, delta):
        self._input()
        super().update(delta)
