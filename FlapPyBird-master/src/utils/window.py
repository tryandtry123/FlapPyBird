class Window:
    def __init__(self, width, height):
        """
        初始化窗口配置
        :param width: 窗口宽度
        :param height: 窗口高度
        """
        self.width = width  # 窗口宽度
        self.height = height  # 窗口高度
        self.ratio = width / height  # 宽高比
        self.w = width  # 窗口宽度（别名）
        self.h = height  # 窗口高度（别名）
        self.r = width / height  # 宽高比（别名）
        self.viewport_width = width  # 视口宽度
        self.viewport_height = height * 0.79  # 视口高度（79% 的窗口高度）
        self.vw = width  # 视口宽度（别名）
        self.vh = height * 0.79  # 视口高度（别名）
        self.viewport_ratio = self.vw / self.vh  # 视口宽高比
        self.vr = self.vw / self.vh  # 视口宽高比（别名）
