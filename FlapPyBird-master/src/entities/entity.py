from typing import Optional  # 可选类型导入，用于类型注解

import pygame  # 导入 Pygame 库，处理游戏图形和声音

from ..utils import GameConfig, get_hit_mask, pixel_collision  # 导入游戏配置和碰撞检测工具


class Entity:  # 定义实体基类，所有游戏实体的父类
    """
    实体基类，所有游戏实体的父类。
    """

    def __init__(self, config: GameConfig, image: Optional[pygame.Surface] = None, x=0, y=0, w: int = None, h: int = None, **kwargs) -> None:  # 构造函数，初始化实体
        """
        构造函数，初始化实体。
        
        :param config: 游戏配置
        :param image: 实体图像
        :param x: 实体的 x 坐标
        :param y: 实体的 y 坐标
        :param w: 实体的宽度
        :param h: 实体的高度
        :param kwargs: 其他属性
        """
        self.config = config  # 保存游戏配置
        self.x = x  # 实体的 x 坐标
        self.y = y  # 实体的 y 坐标
        if w or h:  # 如果提供了宽度或高度
            self.w = w or config.window.ratio * h  # 计算宽度
            self.h = h or w / config.window.ratio  # 计算高度
            self.image = pygame.transform.scale(image, (self.w, self.h))  # 缩放图像
        else:  # 如果没有提供宽度和高度
            self.image = image  # 使用提供的图像
            self.w = image.get_width() if image else 0  # 获取图像宽度
            self.h = image.get_height() if image else 0  # 获取图像高度

        self.hit_mask = get_hit_mask(image) if image else None  # 获取碰撞掩码
        self.__dict__.update(kwargs)  # 更新其他属性

    def update_image(self, image: pygame.Surface, w: int = None, h: int = None) -> None:  # 更新实体图像
        """
        更新实体图像。
        
        :param image: 新图像
        :param w: 新宽度
        :param h: 新高度
        """
        self.image = image  # 设置新图像
        self.hit_mask = get_hit_mask(image)  # 更新碰撞掩码
        self.w = w or (image.get_width() if image else 0)  # 更新宽度
        self.h = h or (image.get_height() if image else 0)  # 更新高度

    @property  # 属性装饰器，计算中心 x 坐标
    def cx(self) -> float:
        """
        计算中心 x 坐标。
        
        :return: 中心 x 坐标
        """
        return self.x + self.w / 2  # 返回中心 x 坐标

    @property  # 属性装饰器，计算中心 y 坐标
    def cy(self) -> float:
        """
        计算中心 y 坐标。
        
        :return: 中心 y 坐标
        """
        return self.y + self.h / 2  # 返回中心 y 坐标

    @property  # 属性装饰器，返回实体的矩形区域
    def rect(self) -> pygame.Rect:
        """
        返回实体的矩形区域。
        
        :return: 矩形区域
        """
        return pygame.Rect(self.x, self.y, self.w, self.h)  # 返回矩形区域

    def collide(self, other) -> bool:  # 碰撞检测
        """
        碰撞检测。
        
        :param other: 另一个实体
        :return: 是否碰撞
        """
        if not self.hit_mask or not other.hit_mask:  # 如果没有碰撞掩码
            return self.rect.colliderect(other.rect)  # 使用矩形碰撞检测
        return pixel_collision(self.rect, other.rect, self.hit_mask, other.hit_mask)  # 使用像素碰撞检测

    def tick(self) -> None:  # 更新实体状态
        """
        更新实体状态。
        """
        self.draw()  # 绘制实体
        rect = self.rect  # 获取矩形区域
        if self.config.debug:  # 如果调试模式开启
            pygame.draw.rect(self.config.screen, (255, 0, 0), rect, 1)  # 绘制红色矩形框
            # 在矩形顶部写入 x 和 y 坐标
            font = pygame.font.SysFont("Arial", 13, True)  # 创建字体对象
            text = font.render(f"{self.x:.1f}, {self.y:.1f}, {self.w:.1f}, {self.h:.1f}", True, (255, 255, 255))  # 渲染文本
            self.config.screen.blit(text, (
                rect.x + rect.w / 2 - text.get_width() / 2,
                rect.y - text.get_height(),
            ))  # 在屏幕上绘制文本

    def draw(self) -> None:  # 绘制实体
        """
        绘制实体。
        """
        if self.image:  # 如果有图像
            self.config.screen.blit(self.image, self.rect)  # 在屏幕上绘制图像
