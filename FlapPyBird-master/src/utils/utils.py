from functools import wraps
from typing import List

import pygame

HitMaskType = List[List[bool]]  # 碰撞掩码类型定义


def clamp(n: float, minn: float, maxn: float) -> float:
    """
    限制一个数值在两个值之间
    """
    return max(min(maxn, n), minn)  # 返回限制后的值


def memoize(func):
    """
    缓存函数结果
    """
    cache = {}  # 创建缓存字典

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))  # 创建唯一键
        if key not in cache:
            cache[key] = func(*args, **kwargs)  # 缓存函数结果
        return cache[key]  # 返回缓存结果

    return wrapper


@memoize
def get_hit_mask(image: pygame.Surface) -> HitMaskType:
    """
    根据图像的透明度返回碰撞掩码
    """
    return list(
        (
            list(
                (
                    bool(image.get_at((x, y))[3])  # 获取像素的alpha值
                    for y in range(image.get_height())  # 遍历图像高度
                )
            )
            for x in range(image.get_width())  # 遍历图像宽度
        )
    )


def pixel_collision(
    rect1: pygame.Rect,
    rect2: pygame.Rect,
    hitmask1: HitMaskType,
    hitmask2: HitMaskType,
):
    """
    检查两个对象是否碰撞，而不仅仅是它们的矩形
    """
    rect = rect1.clip(rect2)  # 获取两个矩形的交集

    if rect.width == 0 or rect.height == 0:
        return False  # 如果没有交集，返回False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y  # 计算相对位置
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    # 安全检查：确保碰撞掩码存在且不为None
    if not hitmask1 or not hitmask2:
        return rect1.colliderect(rect2)  # 如果没有掩码，退回到矩形碰撞检测
    
    # 获取碰撞掩码的维度
    width1, height1 = len(hitmask1), len(hitmask1[0]) if hitmask1 else 0
    width2, height2 = len(hitmask2), len(hitmask2[0]) if hitmask2 else 0
    
    for x in range(rect.width):
        for y in range(rect.height):
            # 添加边界检查
            if (0 <= x1 + x < width1 and 0 <= y1 + y < height1 and
                0 <= x2 + x < width2 and 0 <= y2 + y < height2):
                # 只有在范围内的索引才检查碰撞
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True  # 如果两个碰撞掩码都为True，返回True
    return False  # 没有碰撞，返回False
