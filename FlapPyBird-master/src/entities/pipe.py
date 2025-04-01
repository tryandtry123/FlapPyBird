import random
from typing import List

from ..utils import GameConfig
from .entity import Entity


class Pipe(Entity):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vel_x = -5  # 管道的水平速度

    def draw(self) -> None:
        self.x += self.vel_x  # 更新管道位置
        super().draw()  # 调用父类的绘制方法


class Pipes(Entity):
    upper: List[Pipe]  # 上方管道列表
    lower: List[Pipe]  # 下方管道列表

    def __init__(self, config: GameConfig) -> None:
        super().__init__(config)
        self.pipe_gap = 120  # 管道间隙
        self.top = 0  # 顶部位置
        self.bottom = self.config.window.viewport_height  # 底部位置
        self.upper = []  # 初始化上方管道列表
        self.lower = []  # 初始化下方管道列表
        self.spawn_initial_pipes()  # 生成初始管道

    def tick(self) -> None:
        if self.can_spawn_pipes():  # 检查是否可以生成管道
            self.spawn_new_pipes()  # 生成新管道
        self.remove_old_pipes()  # 移除旧管道

        for up_pipe, low_pipe in zip(self.upper, self.lower):
            up_pipe.tick()  # 更新上方管道状态
            low_pipe.tick()  # 更新下方管道状态

    def stop(self) -> None:
        for pipe in self.upper + self.lower:
            pipe.vel_x = 0  # 停止管道移动

    def can_spawn_pipes(self) -> bool:
        last = self.upper[-1]  # 获取最后一个上方管道
        if not last:
            return True

        return self.config.window.width - (last.x + last.w) > last.w * 2.5  # 检查是否可以生成新管道

    def spawn_new_pipes(self):
        # 当第一个管道即将触碰屏幕左侧时生成新管道
        upper, lower = self.make_random_pipes()  # 生成随机管道
        self.upper.append(upper)  # 添加上方管道
        self.lower.append(lower)  # 添加下方管道

    def remove_old_pipes(self):
        # 移除超出屏幕的管道
        for pipe in self.upper:
            if pipe.x < -pipe.w:
                self.upper.remove(pipe)  # 移除上方管道

        for pipe in self.lower:
            if pipe.x < -pipe.w:
                self.lower.remove(pipe)  # 移除下方管道

    def spawn_initial_pipes(self):
        upper_1, lower_1 = self.make_random_pipes()  # 生成初始管道
        upper_1.x = self.config.window.width + upper_1.w * 3  # 设置初始上方管道位置
        lower_1.x = self.config.window.width + upper_1.w * 3  # 设置初始下方管道位置
        self.upper.append(upper_1)  # 添加初始上方管道
        self.lower.append(lower_1)  # 添加初始下方管道

        upper_2, lower_2 = self.make_random_pipes()  # 生成第二组初始管道
        upper_2.x = upper_1.x + upper_1.w * 3.5  # 设置第二个上方管道位置
        lower_2.x = upper_1.x + upper_1.w * 3.5  # 设置第二个下方管道位置
        self.upper.append(upper_2)  # 添加第二个上方管道
        self.lower.append(lower_2)  # 添加第二个下方管道

    def make_random_pipes(self):
        """返回随机生成的管道"""
        # 上下管道之间的间隙y坐标
        base_y = self.config.window.viewport_height

        gap_y = random.randrange(0, int(base_y * 0.6 - self.pipe_gap))  # 随机生成间隙y坐标
        gap_y += int(base_y * 0.2)  # 调整间隙y坐标
        pipe_height = self.config.images.pipe[0].get_height()  # 获取管道高度
        pipe_x = self.config.window.width + 10  # 设置管道x坐标

        # 随机生成特殊管道
        if random.random() < 0.2:  # 20% 概率生成特殊管道
            pipe_type = random.choice(['speed_up', 'speed_down'])
            if pipe_type == 'speed_up':
                upper_pipe = Pipe(
                    self.config,
                    self.config.images.pipe[0],
                    pipe_x,
                    gap_y - pipe_height,
                    speed_up=True
                )
                lower_pipe = Pipe(
                    self.config,
                    self.config.images.pipe[1],
                    pipe_x,
                    gap_y + self.pipe_gap,
                    speed_up=True
                )
            else:
                upper_pipe = Pipe(
                    self.config,
                    self.config.images.pipe[0],
                    pipe_x,
                    gap_y - pipe_height,
                    speed_down=True
                )
                lower_pipe = Pipe(
                    self.config,
                    self.config.images.pipe[1],
                    pipe_x,
                    gap_y + self.pipe_gap,
                    speed_down=True
                )
        else:
            upper_pipe = Pipe(
                self.config,
                self.config.images.pipe[0],
                pipe_x,
                gap_y - pipe_height,
            )  # 创建上方管道

            lower_pipe = Pipe(
                self.config,
                self.config.images.pipe[1],
                pipe_x,
                gap_y + self.pipe_gap,
            )  # 创建下方管道

        return upper_pipe, lower_pipe  # 返回上方和下方管道
