# 游戏结束画面模块，定义游戏结束时的显示界面

from ..utils import GameConfig
from .entity import Entity


class GameOver(Entity):
    """
    游戏结束画面
    """

    def __init__(self, config: GameConfig) -> None:
        """
        初始化游戏结束画面

        :param config: 游戏配置
        """
        super().__init__(
            config=config,
            image=config.images.game_over,
            x=(config.window.width - config.images.game_over.get_width()) // 2,
            y=int(config.window.height * 0.2),
        )
