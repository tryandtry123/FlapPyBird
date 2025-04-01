from ..utils import GameConfig
from .entity import Entity


class Floor(Entity):
    """
    地面实体。
    """
    def __init__(self, config: GameConfig) -> None:
        """
        初始化地面实体。

        :param config: 游戏配置
        """
        super().__init__(config, config.images.base, 0, config.window.vh)
        self.vel_x = 4  # x轴速度
        self.x_extra = self.w - config.window.w  # x轴超出部分的宽度

    def stop(self) -> None:
        """
        停止地面移动。
        """
        self.vel_x = 0

    def draw(self) -> None:
        """
        绘制地面实体。
        """
        # 使地面实体循环绘制
        self.x = -((-self.x + self.vel_x) % self.x_extra)
        super().draw()
