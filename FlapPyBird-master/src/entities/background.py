from ..utils import GameConfig  # 导入游戏配置类，用于获取游戏设置
from .entity import Entity  # 导入实体基类，Background 类继承自该类


class Background(Entity):  # 定义背景类，负责管理游戏背景
    def __init__(self, config: GameConfig) -> None:  # 初始化背景类，接收游戏配置作为参数
        super().__init__(  # 调用父类构造函数
            config,
            config.images.background,  # 设置背景图像
            0,  # 背景的初始 x 坐标
            0,  # 背景的初始 y 坐标
            config.window.width,  # 背景的宽度
            config.window.height,  # 背景的高度
        )
