from enum import Enum
from itertools import cycle

import pygame

from ..utils import GameConfig, clamp
from .entity import Entity
from .floor import Floor
from .pipe import Pipe, Pipes
from .powerup import PowerUpType


class PlayerMode(Enum):
    """玩家模式枚举"""
    NORMAL = "NORMAL"  # 正常模式
    SHM = "SHM"  # 静止模式
    CRASH = "CRASH"  # 撞击模式
    CRASHED = "CRASHED"  # 撞击模式


class Player(Entity):
    def __init__(self, config: GameConfig) -> None:
        image = config.images.player[0]
        x = int(config.window.width * 0.2)
        y = int((config.window.height - image.get_height()) / 2)
        super().__init__(config, image, x, y)
        self.min_y = -2 * self.h
        self.max_y = config.window.viewport_height - self.h * 0.75
        self.img_idx = 0
        self.img_gen = cycle([0, 1, 2, 1])
        self.frame = 0
        self.crashed = False
        self.crash_entity = None
        # 道具效果相关属性
        self.speed_modifier = 1.0  # 速度修改器
        self.invincible = False    # 无敌状态
        self.size_modifier = 1.0   # 大小修改器
        self.original_image = None # 保存原始图像
        self.set_mode(PlayerMode.SHM)
        
    def apply_powerup_effect(self, powerup_type: PowerUpType) -> None:
        """应用道具效果"""
        if powerup_type == PowerUpType.SPEED_BOOST:
            self.speed_modifier = 1.5
        elif powerup_type == PowerUpType.INVINCIBLE:
            self.invincible = True
        elif powerup_type == PowerUpType.SLOW_MOTION:
            self.speed_modifier = 0.5
        elif powerup_type == PowerUpType.SMALL_SIZE:
            # 缩小玩家
            if self.size_modifier == 1.0:
                self.original_image = self.image
                self.size_modifier = 0.6
                self._resize_player()
    
    def remove_powerup_effect(self, powerup_type: PowerUpType) -> None:
        """移除道具效果"""
        if powerup_type == PowerUpType.SPEED_BOOST or powerup_type == PowerUpType.SLOW_MOTION:
            self.speed_modifier = 1.0
        elif powerup_type == PowerUpType.INVINCIBLE:
            self.invincible = False
        elif powerup_type == PowerUpType.SMALL_SIZE:
            if self.original_image:
                self.size_modifier = 1.0
                self.image = self.original_image
                self.w = self.image.get_width()
                self.h = self.image.get_height()
                self.original_image = None
    
    def _resize_player(self) -> None:
        """根据size_modifier调整玩家大小"""
        if self.size_modifier != 1.0:
            new_width = int(self.image.get_width() * self.size_modifier)
            new_height = int(self.image.get_height() * self.size_modifier)
            self.image = pygame.transform.scale(self.image, (new_width, new_height))
            self.w = self.image.get_width()
            self.h = self.image.get_height()

    def set_mode(self, mode: PlayerMode) -> None:
        self.mode = mode
        if mode == PlayerMode.NORMAL:
            self.reset_vals_normal()
            self.config.sounds.wing.play()
        elif mode == PlayerMode.SHM:
            self.reset_vals_shm()
        elif mode == PlayerMode.CRASH:
            self.stop_wings()
            self.config.sounds.hit.play()
            if self.crash_entity == "pipe":
                self.config.sounds.die.play()
            self.reset_vals_crash()

    def reset_vals_normal(self) -> None:
        self.vel_y = -9  # player's velocity along Y axis
        self.max_vel_y = 10  # max vel along Y, max descend speed
        self.min_vel_y = -8  # min vel along Y, max ascend speed
        self.acc_y = 1  # players downward acceleration

        self.rot = 80  # player's current rotation
        self.vel_rot = -3  # player's rotation speed
        self.rot_min = -90  # player's min rotation angle
        self.rot_max = 20  # player's max rotation angle

        self.flap_acc = -9  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_shm(self) -> None:
        self.vel_y = 1  # player's velocity along Y axis
        self.max_vel_y = 4  # max vel along Y, max descend speed
        self.min_vel_y = -4  # min vel along Y, max ascend speed
        self.acc_y = 0.5  # players downward acceleration

        self.rot = 0  # player's current rotation
        self.vel_rot = 0  # player's rotation speed
        self.rot_min = 0  # player's min rotation angle
        self.rot_max = 0  # player's max rotation angle

        self.flap_acc = 0  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_crash(self) -> None:
        self.acc_y = 2
        self.vel_y = 7
        self.max_vel_y = 15
        self.vel_rot = -8

    def update_image(self):
        self.frame += 1
        if self.frame % 5 == 0:
            self.img_idx = next(self.img_gen)
            orig_image = self.config.images.player[self.img_idx]
            
            # 应用大小修改
            if self.size_modifier != 1.0:
                new_width = int(orig_image.get_width() * self.size_modifier)
                new_height = int(orig_image.get_height() * self.size_modifier)
                self.image = pygame.transform.scale(orig_image, (new_width, new_height))
            else:
                self.image = orig_image
                
            self.w = self.image.get_width()
            self.h = self.image.get_height()

    def tick_shm(self) -> None:
        if self.vel_y >= self.max_vel_y or self.vel_y <= self.min_vel_y:
            self.acc_y *= -1
        self.vel_y += self.acc_y
        self.y += self.vel_y

    def tick_normal(self) -> None:
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False

        # 应用速度修改器
        adjusted_vel_y = self.vel_y * self.speed_modifier
        self.y = clamp(self.y + adjusted_vel_y, self.min_y, self.max_y)
        self.rotate()

    def tick_crash(self) -> None:
        if self.min_y <= self.y <= self.max_y:
            self.y = clamp(self.y + self.vel_y, self.min_y, self.max_y)
            # rotate only when it's a pipe crash and bird is still falling
            if self.crash_entity != "floor":
                self.rotate()

        # player velocity change
        if self.vel_y < self.max_vel_y:
            self.vel_y += self.acc_y

    def rotate(self) -> None:
        self.rot = clamp(self.rot + self.vel_rot, self.rot_min, self.rot_max)

    def draw(self) -> None:
        self.update_image()
        if self.mode == PlayerMode.SHM:
            self.tick_shm()
        elif self.mode == PlayerMode.NORMAL:
            self.tick_normal()
        elif self.mode == PlayerMode.CRASH:
            self.tick_crash()

        self.draw_player()

    def draw_player(self) -> None:
        rotated_image = pygame.transform.rotate(self.image, self.rot)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        
        # 无敌状态时添加闪烁效果
        if self.invincible and pygame.time.get_ticks() % 200 < 100:
            # 创建一个带有透明度的副本
            alpha_image = rotated_image.copy()
            alpha_image.set_alpha(150)
            self.config.screen.blit(alpha_image, rotated_rect)
            
            # 添加光环效果
            glow_size = max(rotated_rect.width, rotated_rect.height) + 10
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface, 
                (255, 215, 0, 100),  # 金色光环
                (glow_size//2, glow_size//2), 
                glow_size//2
            )
            glow_rect = glow_surface.get_rect(center=rotated_rect.center)
            self.config.screen.blit(glow_surface, glow_rect)
            
        # 绘制玩家
        self.config.screen.blit(rotated_image, rotated_rect)

    def stop_wings(self) -> None:
        self.img_gen = cycle([self.img_idx])

    def flap(self) -> None:
        if self.y > self.min_y:
            self.vel_y = self.flap_acc
            self.flapped = True
            self.rot = 80
            self.config.sounds.wing.play()

    def crossed(self, pipe: Pipe) -> bool:
        return pipe.cx <= self.cx < pipe.cx - pipe.vel_x

    def collided(self, pipes: Pipes, floor: Floor) -> bool:
        """returns True if player collides with floor or pipes."""
        
        # 如果处于无敌状态，不检测碰撞
        if self.invincible:
            return False

        # if player crashes into ground
        if self.collide(floor):
            self.crashed = True
            self.crash_entity = "floor"
            return True

        for pipe in pipes.upper:
            if self.collide(pipe):
                self.crashed = True
                self.crash_entity = "pipe"
                return True
        for pipe in pipes.lower:
            if self.collide(pipe):
                self.crashed = True
                self.crash_entity = "pipe"
                return True

        return False
