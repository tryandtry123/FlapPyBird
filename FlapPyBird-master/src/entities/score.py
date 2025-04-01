import pygame

from ..utils import GameConfig
from .entity import Entity


class Score(Entity):
    """
    分数显示类
    """
    def __init__(self, config: GameConfig) -> None:
        """
        初始化分数
        :param config: 游戏配置
        """
        super().__init__(config)
        self.y = self.config.window.height * 0.1  # 分数显示y坐标
        self.score = 0  # 初始分数

    def reset(self) -> None:
        """
        重置分数
        """
        self.score = 0  # 分数重置为0

    def add(self) -> None:
        """
        增加分数
        """
        self.score += 1  # 分数加1
        self.config.sounds.point.play()  # 播放得分音效

    @property
    def rect(self) -> pygame.Rect:
        """
        获取分数矩形区域
        """
        score_digits = [int(x) for x in list(str(self.score))]  # 将分数转换为数字列表
        images = [self.config.images.numbers[digit] for digit in score_digits]  # 获取数字图像
        w = sum(image.get_width() for image in images)  # 计算总宽度
        x = (self.config.window.width - w) / 2  # 计算x坐标
        h = max(image.get_height() for image in images)  # 计算高度
        return pygame.Rect(x, self.y, w, h)  # 返回矩形区域

    def draw(self) -> None:
        """displays score in center of screen"""
        score_digits = [int(x) for x in list(str(self.score))]  # 将分数转换为数字列表
        images = [self.config.images.numbers[digit] for digit in score_digits]  # 获取数字图像
        digits_width = sum(image.get_width() for image in images)  # 计算数字总宽度
        x_offset = (self.config.window.width - digits_width) / 2  # 计算x轴偏移量

        for image in images:
            self.config.screen.blit(image, (x_offset, self.y))  # 绘制数字
            x_offset += image.get_width()  # 更新x轴偏移量
