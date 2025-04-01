import random
from typing import List, Tuple

import pygame

from .constants import BACKGROUNDS, PIPES, PLAYERS


class Images:
    numbers: List[pygame.Surface]  # 数字图像列表
    game_over: pygame.Surface  # 游戏结束图像
    welcome_message: pygame.Surface  # 欢迎信息图像
    base: pygame.Surface  # 地面图像
    background: pygame.Surface  # 背景图像
    player: Tuple[pygame.Surface]  # 玩家图像
    pipe: Tuple[pygame.Surface]  # 管道图像

    def __init__(self) -> None:
        """
        初始化图像资源
        """
        self.numbers = list(
            (
                pygame.image.load(f"assets/sprites/{num}.png").convert_alpha()  # 加载数字图像
                for num in range(10)
            )
        )

        # 游戏结束图像
        self.game_over = pygame.image.load(
            "assets/sprites/gameover.png"
        ).convert_alpha()
        # 欢迎信息图像
        self.welcome_message = pygame.image.load(
            "assets/sprites/message.png"
        ).convert_alpha()
        # 地面图像
        self.base = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.randomize()  # 随机化背景和玩家图像

    def randomize(self):
        """
        随机选择背景、玩家和管道图像
        """
        # 随机选择背景图像
        rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
        # 随机选择玩家图像
        rand_player = random.randint(0, len(PLAYERS) - 1)
        # 随机选择管道图像
        rand_pipe = random.randint(0, len(PIPES) - 1)

        self.background = pygame.image.load(BACKGROUNDS[rand_bg]).convert()  # 加载随机背景图像
        self.player = (
            pygame.image.load(PLAYERS[rand_player][0]).convert_alpha(),  # 加载玩家上拍图像
            pygame.image.load(PLAYERS[rand_player][1]).convert_alpha(),  # 加载玩家中拍图像
            pygame.image.load(PLAYERS[rand_player][2]).convert_alpha(),  # 加载玩家下拍图像
        )
        self.pipe = (
            pygame.transform.flip(
                pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
                False,
                True,
            ),  # 加载并翻转管道图像
            pygame.image.load(PIPES[rand_pipe]).convert_alpha(),  # 加载管道图像
        )
