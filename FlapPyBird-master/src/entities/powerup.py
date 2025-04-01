import random
from enum import Enum
from typing import Optional

import pygame

from ..utils import GameConfig
from .entity import Entity


class PowerUpType(Enum):
    """道具类型枚举"""
    SPEED_BOOST = "SPEED_BOOST"  # 加速
    INVINCIBLE = "INVINCIBLE"    # 无敌
    SLOW_MOTION = "SLOW_MOTION"  # 慢动作
    SMALL_SIZE = "SMALL_SIZE"    # 缩小玩家


class PowerUp(Entity):
    """道具实体类"""
    def __init__(self, config: GameConfig, power_type: PowerUpType, x: int, y: int) -> None:
        # 创建基本的圆形表示
        size = 30
        self.power_type = power_type
        
        # 根据道具类型选择颜色
        color_map = {
            PowerUpType.SPEED_BOOST: (255, 165, 0),   # 橙色
            PowerUpType.INVINCIBLE: (255, 215, 0),    # 金色
            PowerUpType.SLOW_MOTION: (0, 191, 255),   # 天蓝色
            PowerUpType.SMALL_SIZE: (147, 112, 219),  # 紫色
        }
        
        self.color = color_map[power_type]
        self.duration = 5000  # 道具持续时间(毫秒)
        self.vel_x = -4  # 水平移动速度
        
        # 创建道具表面
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, self.color, (size//2, size//2), size//2)
        
        # 根据道具类型绘制标志
        font = pygame.font.SysFont('Arial', 20)
        symbol_map = {
            PowerUpType.SPEED_BOOST: "S",
            PowerUpType.INVINCIBLE: "I",
            PowerUpType.SLOW_MOTION: "T",  # T for Time slow
            PowerUpType.SMALL_SIZE: "-",
        }
        text = font.render(symbol_map[power_type], True, (255, 255, 255))
        text_rect = text.get_rect(center=(size//2, size//2))
        surface.blit(text, text_rect)
        
        # 添加光晕效果
        glow_surface = pygame.Surface((size+10, size+10), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.color, 100), (size//2+5, size//2+5), size//2+5)
        
        # 合并图层
        final_surface = pygame.Surface((size+10, size+10), pygame.SRCALPHA)
        final_surface.blit(glow_surface, (0, 0))
        final_surface.blit(surface, (5, 5))
        
        super().__init__(config, final_surface, x, y)
        
        # 动画参数
        self.animation_tick = 0
        self.pulse_scale = 1.0
        self.pulse_direction = 0.01
        # 保存初始中心坐标
        self.center_x = self.x + self.w / 2
        self.center_y = self.y + self.h / 2
    
    def draw(self) -> None:
        self.x += self.vel_x  # 更新位置
        # 更新中心坐标
        self.center_x = self.x + self.w / 2
        self.center_y = self.y + self.h / 2
        self.animate()  # 更新动画
        super().draw()  # 调用父类绘制方法
    
    def animate(self) -> None:
        """使道具产生脉动动画效果"""
        self.animation_tick += 1
        
        # 每3帧更新一次脉动
        if self.animation_tick % 3 == 0:
            # 脉动效果
            self.pulse_scale += self.pulse_direction
            if self.pulse_scale > 1.1:
                self.pulse_direction = -0.01
            elif self.pulse_scale < 0.9:
                self.pulse_direction = 0.01
                
            # 创建缩放后的图像
            scaled_size = int(self.image.get_width() * self.pulse_scale)
            scaled_image = pygame.transform.scale(self.image, (scaled_size, scaled_size))
            
            # 更新图像和尺寸
            old_width = self.w
            old_height = self.h
            self.image = scaled_image
            self.w = self.image.get_width()
            self.h = self.image.get_height()
            
            # 更新位置以保持中心不变
            self.x = self.center_x - self.w / 2
            self.y = self.center_y - self.h / 2


class PowerUpManager:
    """道具管理器，负责道具的生成、更新和移除"""
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.powerups = []
        self.spawn_timer = 0
        self.spawn_interval = 3000  # 每3秒生成一次道具的机会
        self.spawn_chance = 0.6     # 60%概率生成道具
        self.active_effects = {}    # 当前激活的效果 {PowerUpType: end_time}
    
    def tick(self, delta_time: int) -> None:
        """更新所有道具状态"""
        # 更新生成计时器
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            if random.random() < self.spawn_chance:
                self.spawn_powerup()
        
        # 更新和移除道具
        for powerup in list(self.powerups):
            powerup.tick()
            # 移除超出屏幕的道具
            if powerup.x < -powerup.w:
                self.powerups.remove(powerup)
        
        # 更新激活效果的剩余时间
        current_time = pygame.time.get_ticks()
        expired_effects = []
        
        for effect_type, end_time in self.active_effects.items():
            if current_time >= end_time:
                expired_effects.append(effect_type)
                
        # 移除过期效果
        for effect in expired_effects:
            self.active_effects.pop(effect)
    
    def spawn_powerup(self) -> None:
        """生成一个随机道具"""
        # 从枚举中随机选择一个道具类型
        power_type = random.choice(list(PowerUpType))
        
        # 在合适的位置生成道具
        x = self.config.window.width + 10
        # 在屏幕中央区域随机生成
        min_y = int(self.config.window.height * 0.2)
        max_y = int(self.config.window.height * 0.7)
        y = random.randint(min_y, max_y)
        
        # 创建道具并添加到列表
        powerup = PowerUp(self.config, power_type, x, y)
        self.powerups.append(powerup)
    
    def activate_effect(self, power_type: PowerUpType) -> None:
        """激活道具效果"""
        current_time = pygame.time.get_ticks()
        end_time = current_time + PowerUp(self.config, power_type, 0, 0).duration
        self.active_effects[power_type] = end_time
        
        # 播放音效
        if power_type == PowerUpType.SPEED_BOOST:
            self.config.sounds.point.play()
        elif power_type == PowerUpType.INVINCIBLE:
            self.config.sounds.point.play()
        elif power_type == PowerUpType.SLOW_MOTION:
            self.config.sounds.point.play()
        elif power_type == PowerUpType.SMALL_SIZE:
            self.config.sounds.point.play()
    
    def has_effect(self, power_type: PowerUpType) -> bool:
        """检查指定的效果是否处于激活状态"""
        return power_type in self.active_effects
    
    def get_remaining_time(self, power_type: PowerUpType) -> Optional[int]:
        """获取效果剩余时间"""
        if not self.has_effect(power_type):
            return None
        
        current_time = pygame.time.get_ticks()
        end_time = self.active_effects[power_type]
        return max(0, end_time - current_time)
