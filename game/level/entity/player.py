from game.level.attack import AttackArea
from game.level.entity.components.Shootable import Shootable, PROJECTILE_ARROW
from game.settings import *
from game.math import is_in_range
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
    ATTACK_ARROW = "attack_arrow"


hash_player_data = {}


def build_player_data(animations, start_animation_name, shadow_path, delay_to_shoot, max_health, inventory_config, shadow_offset, speed, attack_range, base_attack_damage, shadow_scale=1):
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
        "inventory_config": inventory_config,
        "base_attack_damage": base_attack_damage,
        "delay_to_shoot": delay_to_shoot,
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
                        (6, 1, PlayerAnimation.ATTACKING, 8),
                        # (6, 1, PlayerAnimation.HURTING, ?),
                        (9, 1, PlayerAnimation.ATTACK_ARROW, 20),
                    ],
                    [
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Idle.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Walk.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Attack01.png'),
                        join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Attack-Arrow.png'),
                    ]
                ),
                max_health=3,
                start_animation_name=PlayerAnimation.IDLE,
                shadow_path=join('assets', 'characters', 'Soldier', 'Soldier', 'Soldier-Shadow.png'),
                shadow_offset=Vector2(25, 63),
                shadow_scale=3,
                speed=300,
                attack_range=(80, 50),
                base_attack_damage=2,
                delay_to_shoot=2,
                inventory_config = {
                    "max_arrows": 2,
                }
            )
            # scale
            hash_player_data[player_key]["animations"][PlayerAnimation.IDLE].scale_frames(3)
            hash_player_data[player_key]["animations"][PlayerAnimation.WALKING].scale_frames(3)
            hash_player_data[player_key]["animations"][PlayerAnimation.ATTACKING].scale_frames(3)
            hash_player_data[player_key]["animations"][PlayerAnimation.ATTACK_ARROW].scale_frames(3)
            # hash_player_data[player_key]["animations"][PlayerAnimation.HURTING].scale_frames(3)
    # return data
    return hash_player_data[player_key]


class Player(Entity):
    def __init__(self, game, pos, group, collision_group, enemy_group, item_group, render_projectile_group, player_data_type):
        self.enemy_group = enemy_group
        self.item_group = item_group
        # get data
        self.player_data = get_player_data(player_data_type)
        # super
        super().__init__(game, pos, self.player_data["speed"], group, collision_group, self.player_data['animations'],
                         self.player_data['start_animation_name'])
        # attack
        self.base_attack_damage = self.player_data['base_attack_damage']
        self.attack_range = self.player_data['attack_range']
        self.delay_to_shoot = self.player_data["delay_to_shoot"]
        self.delay_to_shoot_delta = 0
        # player inventory
        self.inventory = PlayerInventory(
            max_arrows=self.player_data["inventory_config"]["max_arrows"]
        )
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
        # shootable
        self.shootable_arrow = Shootable(self.game, self, PROJECTILE_ARROW, render_projectile_group, self.enemy_group)
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

    def shoot(self):
        if self.delay_to_shoot_delta <= 0:
            if self.inventory.arrows() > 0:
                self.shootable_arrow.shoot(self.game.mouse_loc)
                self.inventory.use_arrow()
                self.delay_to_shoot_delta = self.delay_to_shoot

    def __attack_handler(self, event, animation):
        if event == AnimationEvent.ENDS:
            self.attacking = False
        elif event == AnimationEvent.FRAME_CHANGED:
            if animation.index == 3:
                self.__attack_give_damage_handler()

    def _input(self):
        keys = pygame.key.get_pressed()

        # moviment
        self.velocity.y = 0
        if keys[pygame.K_w]:
            self.velocity.y = -1
        elif keys[pygame.K_s]:
            self.velocity.y = 1

        self.velocity.x = 0
        if keys[pygame.K_a]:
            self.velocity.x = -1
        elif keys[pygame.K_d]:
            self.velocity.x = 1

        # attack
        if keys[pygame.K_SPACE]:
            self._attack_input_handler()
        elif self.game.is_mouse_clicking:
            self.shoot()

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

    def try_get_some_item(self):
        for item_entity in self.item_group:
            px = self.rect.centerx
            py = self.rect.centery
            if is_in_range(item_entity.rect.x, px - 15, px + 15) and is_in_range(item_entity.rect.y, py - 15, py + 15):
                item_entity.beGettedByPlayer(self)
                self.game.level.remove_dropped_item(item_entity)

    def update(self, delta):
        self._input()

        if self.delay_to_shoot_delta > 0:
            self.delay_to_shoot_delta -= delta

        self.try_get_some_item()

        super().update(delta)
