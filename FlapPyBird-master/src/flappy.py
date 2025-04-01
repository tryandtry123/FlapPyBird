import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .entities.powerup import PowerUpManager, PowerUpType
from .utils import GameConfig, Images, Sounds, Window


class Flappy:
    def __init__(self):
        """
        初始化Flappy Bird游戏
        """
        pygame.init()  # 初始化pygame
        pygame.display.set_caption("Flappy Bird")  # 设置窗口标题
        window = Window(288, 512)  # 创建窗口对象
        screen = pygame.display.set_mode((window.width, window.height))  # 设置屏幕大小
        images = Images()  # 加载图像资源

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )
        # 记录上一帧的时间，用于计算delta_time
        self.last_frame_time = pygame.time.get_ticks()

    async def start(self):
        """
        启动游戏循环
        """
        while True:
            self.background = Background(self.config)  # 创建背景对象
            self.floor = Floor(self.config)  # 创建地面对象
            self.player = Player(self.config)  # 创建玩家对象
            self.welcome_message = WelcomeMessage(self.config)  # 创建欢迎信息对象
            self.game_over_message = GameOver(self.config)  # 创建游戏结束信息对象
            self.pipes = Pipes(self.config)  # 创建管道对象
            self.score = Score(self.config)  # 创建得分对象
            self.powerup_manager = PowerUpManager(self.config)  # 创建道具管理器
            await self.splash()  # 显示欢迎界面
            await self.play()  # 开始游戏
            await self.game_over()  # 游戏结束

    async def splash(self):
        """
        显示欢迎界面动画
        """
        self.player.set_mode(PlayerMode.SHM)  # 设置玩家模式为SHM（静止模式）

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)  # 检查退出事件
                if self.is_tap_event(event):
                    return  # 如果有点击事件，退出欢迎界面

            self.background.tick()  # 更新背景
            self.floor.tick()  # 更新地面
            self.player.tick()  # 更新玩家
            self.welcome_message.tick()  # 更新欢迎信息

            pygame.display.update()  # 刷新显示
            await asyncio.sleep(0)  # 等待下一帧
            self.config.tick()  # 更新游戏配置

    def check_quit_event(self, event):
        """
        检查退出事件
        """
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()  # 退出pygame
            sys.exit()  # 退出程序

    def is_tap_event(self, event):
        """
        检查点击事件
        """
        m_left, _, _ = pygame.mouse.get_pressed()  # 检查鼠标左键是否按下
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )  # 检查空格键或上箭头是否按下
        screen_tap = event.type == pygame.FINGERDOWN  # 检查触摸事件
        return m_left or space_or_up or screen_tap  # 返回是否有点击事件

    def calculate_delta_time(self):
        """
        计算两帧之间的时间差
        """
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        return delta_time

    def check_powerup_collisions(self):
        """
        检查玩家与道具的碰撞
        """
        # 创建一个要删除的道具列表
        powerups_to_remove = []
        
        # 检查所有道具
        for powerup in self.powerup_manager.powerups:
            # 如果玩家碰到了道具
            if self.player.collide(powerup):
                # 应用道具效果
                self.player.apply_powerup_effect(powerup.power_type)
                # 激活道具在管理器中的效果
                self.powerup_manager.activate_effect(powerup.power_type)
                # 播放得分声音
                self.config.sounds.point.play()
                # 添加到要删除的列表
                powerups_to_remove.append(powerup)
        
        # 从管理器中删除已收集的道具
        for powerup in powerups_to_remove:
            if powerup in self.powerup_manager.powerups:
                self.powerup_manager.powerups.remove(powerup)

    def update_player_effects(self):
        """
        根据当前激活的效果更新玩家状态
        """
        # 检查每种效果是否已过期
        for power_type in list(PowerUpType):
            if self.powerup_manager.has_effect(power_type):
                # 效果仍然激活，确保效果被应用
                self.player.apply_powerup_effect(power_type)
            else:
                # 效果已过期，移除
                self.player.remove_powerup_effect(power_type)
    
    def render_active_effects(self):
        """
        在屏幕上显示当前激活的效果及其剩余时间# 修改前
        if self.powerup_manager.has_effect(power_type):
            # 效果仍然激活
            pass  # 效果在激活时已经应用到玩家
        
        # 修改后
        if self.powerup_manager.has_effect(power_type):
            # 效果仍然激活，确保效果被应用
            self.player.apply_powerup_effect(power_type)
        """
        active_effects = []
        for power_type in PowerUpType:
            if self.powerup_manager.has_effect(power_type):
                remaining_ms = self.powerup_manager.get_remaining_time(power_type)
                if remaining_ms is not None:
                    active_effects.append((power_type, remaining_ms))
        
        # 如果有激活的效果，在屏幕上显示
        if active_effects:
            font = pygame.font.SysFont('Arial', 10)
            y_offset = 10
            
            for power_type, remaining_ms in active_effects:
                remaining_sec = remaining_ms / 1000
                
                # 根据道具类型选择显示文本和颜色
                if power_type == PowerUpType.SPEED_BOOST:
                    text = f"Speed Boost: {remaining_sec:.1f}s"
                    color = (255, 165, 0)  # 橙色
                elif power_type == PowerUpType.INVINCIBLE:
                    text = f"Invincible: {remaining_sec:.1f}s"
                    color = (255, 215, 0)  # 金色
                elif power_type == PowerUpType.SLOW_MOTION:
                    text = f"Slow Motion: {remaining_sec:.1f}s"
                    color = (0, 191, 255)  # 天蓝色
                elif power_type == PowerUpType.SMALL_SIZE:
                    text = f"Small Size: {remaining_sec:.1f}s"
                    color = (147, 112, 219)  # 紫色
                
                # 创建文本表面
                text_surface = font.render(text, True, color)
                text_rect = text_surface.get_rect()
                text_rect.topleft = (10, y_offset)
                
                # 绘制文本
                self.config.screen.blit(text_surface, text_rect)
                
                # 更新下一个文本的位置
                y_offset += 20

    async def play(self):
        """
        游戏主循环
        """
        self.score.reset()  # 重置得分
        self.player.set_mode(PlayerMode.NORMAL)  # 设置玩家模式为正常

        while True:
            # 计算delta time
            delta_time = self.calculate_delta_time()
            
            if self.player.collided(self.pipes, self.floor):
                return  # 如果玩家与管道或地面碰撞，结束游戏

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()  # 玩家穿过管道，得分

            for event in pygame.event.get():
                self.check_quit_event(event)  # 检查退出事件
                if self.is_tap_event(event):
                    self.player.flap()  # 玩家点击，执行拍打动作

            # 更新道具管理器
            self.powerup_manager.tick(delta_time)
            
            # 检查道具碰撞
            self.check_powerup_collisions()
            
            # 更新玩家状态效果
            self.update_player_effects()

            self.background.tick()  # 更新背景
            self.floor.tick()  # 更新地面
            self.pipes.tick()  # 更新管道
            self.score.tick()  # 更新得分
            self.player.tick()  # 更新玩家
            
            # 绘制道具
            for powerup in self.powerup_manager.powerups:
                powerup.tick()
                
            # 绘制活跃效果提示
            self.render_active_effects()

            pygame.display.update()  # 刷新显示
            await asyncio.sleep(0)  # 等待下一帧
            self.config.tick()  # 更新游戏配置

    async def game_over(self):
        """
        玩家死亡并显示游戏结束界面
        """
        self.player.set_mode(PlayerMode.CRASH)  # 设置玩家模式为CRASH（死亡模式）
        self.pipes.stop()  # 停止管道
        self.floor.stop()  # 停止地面

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)  # 检查退出事件
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return  # 如果玩家落到地面，结束游戏

            self.background.tick()  # 更新背景
            self.floor.tick()  # 更新地面
            self.pipes.tick()  # 更新管道
            self.score.tick()  # 更新得分
            self.player.tick()  # 更新玩家
            self.game_over_message.tick()  # 更新游戏结束信息

            self.config.tick()  # 更新游戏配置
            pygame.display.update()  # 刷新显示
            await asyncio.sleep(0)  # 等待下一帧
