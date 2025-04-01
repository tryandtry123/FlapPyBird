from ..utils import GameConfig
from .entity import Entity


class WelcomeMessage(Entity):
    """
    欢迎信息类
    """
    def __init__(self, config: GameConfig) -> None:
        """
        初始化欢迎信息
        :param config: 游戏配置
        """
        image = config.images.welcome_message  # 获取欢迎信息图像
        super().__init__(
            config=config,
            image=image,
            x=(config.window.width - image.get_width()) // 2,  # 设置x坐标为屏幕中心
            y=int(config.window.height * 0.12),  # 设置y坐标为屏幕高度的12%
        )
