import os

import pygame

from .images import Images
from .sounds import Sounds
from .window import Window


class GameConfig:
    """
    游戏配置类，管理游戏的基本配置
    """
    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        fps: int,
        window: Window,
        images: Images,
        sounds: Sounds,
    ) -> None:
        """
        初始化游戏配置
        :param screen: 游戏屏幕
        :param clock: 游戏时钟
        :param fps: 帧率
        :param window: 窗口配置
        :param images: 图像配置
        :param sounds: 声音配置
        """
        self.screen = screen  # 游戏屏幕
        self.clock = clock  # 游戏时钟
        self.fps = fps  # 帧率
        self.window = window  # 窗口配置
        self.images = images  # 图像配置
        self.sounds = sounds  # 声音配置
        self.debug = os.environ.get("DEBUG", False)  # 调试模式

    def tick(self) -> None:
        """
        更新游戏时钟
        """
        self.clock.tick(self.fps)  # 控制游戏帧率
