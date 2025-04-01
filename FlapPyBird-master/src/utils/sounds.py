import sys

import pygame


class Sounds:
    die: pygame.mixer.Sound  # 死亡音效
    hit: pygame.mixer.Sound  # 撞击音效
    point: pygame.mixer.Sound  # 得分音效
    swoosh: pygame.mixer.Sound  # 翅膀音效
    wing: pygame.mixer.Sound  # 拍打音效

    def __init__(self) -> None:
        """
        初始化音效
        """
        if "win" in sys.platform:
            ext = "wav"  # Windows平台使用wav格式
        else:
            ext = "ogg"  # 其他平台使用ogg格式

        self.die = pygame.mixer.Sound(f"assets/audio/die.{ext}")  # 加载死亡音效
        self.hit = pygame.mixer.Sound(f"assets/audio/hit.{ext}")  # 加载撞击音效
        self.point = pygame.mixer.Sound(f"assets/audio/point.{ext}")  # 加载得分音效
        self.swoosh = pygame.mixer.Sound(f"assets/audio/swoosh.{ext}")  # 加载翅膀音效
        self.wing = pygame.mixer.Sound(f"assets/audio/wing.{ext}")  # 加载拍打音效
