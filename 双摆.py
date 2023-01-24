# -- coding: utf-8 --
# @Time: 2021/6/14 20:29
# @Author: Zavijah
# @File: test.py
# @Software: PyCharm
# @Purpose:
import hashlib
import math
import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import pygame
import pygame_gui
import pymunk
from pygame import Color

# 颜色的定义
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BALL = "#18ffff"
STRING = "#ced6e0"
BLACK_A: Color = pygame.Color("#333333")

# 相关物理量的定义
SCREEN_SIZE_X = 1280  # 屏幕尺寸
SCREEN_SIZE_Y = 720  # 屏幕尺寸
WINDOW_SIZE = SCREEN_SIZE_X, SCREEN_SIZE_Y
FPS = 60  # 帧率

# pymunk坐标
FIXED_X = 687
FIXED_Y = SCREEN_SIZE_Y - 200

DRAW_LEFT = 420
DRAW_RIGHT = 945
DRAW_TOP = 58
DRAW_BOTTOM = 630

is_running = True

# pygame初始化
pygame.init()  # 初始化窗口
pygame.display.set_caption("多摆")  # 设置窗口标题
window_surface = pygame.display.set_mode(WINDOW_SIZE)  # 设置窗口
clock = pygame.time.Clock()  # 添加管理时钟
# 表面的创建
experiment_equipment_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32).convert_alpha()
data_processing_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32).convert_alpha()
# 加载图片
background_pic = pygame.image.load(r"dependent_files\pic\多摆UI.png")

# pymunk初始化
# space.damping = 1  # 阻尼值
space = pymunk.Space()  # 创建一个约束空间
space.gravity = (0, -980)  # 设置重力
# 添加界面管理器
ui_manager = pygame_gui.UIManager(WINDOW_SIZE, r"ui_themes\json\Double pendulum.json")

# matplotlib初始化
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 负号显示的相关设置
plt.style.use('dark_background')  # 画图时使用黑色背景
plt.figure(figsize=(2.64, 5.5))

# UI的定义
next_ = pygame_gui.elements.UIButton(pygame.Rect(1106, 633, 101, 67),
                                     text="",
                                     manager=ui_manager,
                                     object_id="next")
start = pygame_gui.elements.UIButton(pygame.Rect(141, 437, 195, 41),
                                     text="开始",
                                     manager=ui_manager,
                                     object_id="start",
                                     allow_double_clicks=True)
reset = pygame_gui.elements.UIButton(pygame.Rect(141, 517, 195, 41),
                                     text="重置",
                                     manager=ui_manager,
                                     object_id="reset")
entry_line_1 = pygame_gui.elements.UITextEntryLine(pygame.Rect(304, 92, 88, 30),
                                                   manager=ui_manager, )
entry_line_2 = pygame_gui.elements.UITextEntryLine(pygame.Rect(304, 151, 88, 30),
                                                   manager=ui_manager, )
entry_line_3 = pygame_gui.elements.UITextEntryLine(pygame.Rect(304, 210, 88, 30),
                                                   manager=ui_manager, )
entry_line_4 = pygame_gui.elements.UITextEntryLine(pygame.Rect(304, 269, 88, 30),
                                                   manager=ui_manager, )
entry_line_5 = pygame_gui.elements.UITextEntryLine(pygame.Rect(304, 328, 88, 30),
                                                   manager=ui_manager, )


def difference(x, y, t_):
    # print(x)
    N = len(t_) - 1  # 数据个数
    X = np.array(x)  # X坐标
    Y = np.array(y)  # Y坐标
    phi = np.arcsin(X / (Y ** 2 + X ** 2) ** 0.5)  # 计算角度
    T = np.array(t_)  # 对应时间
    dphi = []  # 记录角速度
    for i in range(N):
        dphi.append((phi[i + 1] - phi[i]) / (T[i + 1] - T[i]))  # 差分计算，若有N组数据，则会生成N-1个角速度
    dphi = np.array(dphi)  # 整理数据格式
    return dphi.tolist(), phi[1:].tolist()


def calculate(t_, time_fps, parameter, *args):
    if len(args) == 4:
        x1, y1, x2, y2 = args
        xx1, yy1 = difference(x1, y1, t_)
        xx2, yy2 = difference(x2, y2, t_)
        plot(xx1, yy1, xx2, yy2, time_fps, parameter)
    elif len(args) == 6:
        x1, y1, x2, y2, xx3, yy3 = args
        xx1, yy1 = difference(x1, y1, t_)
        xx2, yy2 = difference(x2, y2, t_)
        xx3, yy3 = difference(x2, y2, t_)
        plot2(xx1, yy1, xx2, yy2, xx3, yy3, time_fps, parameter)


def plot(x1: list, y1: list, x2: list, y2: list, time_fps, parameter):
    file_name = get_filename(time_fps, parameter)
    if os.path.exists(r".\cache\{}.png".format(file_name)):
        pass
    else:

        plt.clf()
        plt.subplot(2, 1, 1)
        plt.scatter(x1, y1, c="w", s=2)
        plt.subplot(2, 1, 2)
        plt.scatter(x2, y2, c="w", s=2)
        plt.savefig(r".\cache\{}.png".format(file_name))


def plot2(x1: list, y1: list, x2: list, y2: list, x3: list, y3: list, time_fps, parameter):
    file_name = get_filename(time_fps, parameter)
    if os.path.exists(r".\cache\{}.png".format(file_name)):
        pass
    else:
        plt.figure(figsize=(2.64, 1.80 * 3))
        plt.clf()
        plt.subplot(3, 1, 1)
        plt.scatter(x1, y1, c="w", s=2)
        plt.subplot(3, 1, 2)
        plt.scatter(x2, y2, c="w", s=2)
        plt.subplot(3, 1, 3)
        plt.scatter(x3, y3, c="w", s=2)
        plt.savefig(r".\cache\{}.png".format(file_name))


def get_filename(time_fps, parameter):
    temp = list(map(str, [parameter[0],
                          parameter[1][0], parameter[1][1],
                          parameter[2][0], parameter[2][1],
                          parameter[3][0], parameter[3][1],
                          parameter[4]]))
    temp_str = '{}_{}'.format(time_fps, '_'.join(temp))
    file_name = hashlib.md5(temp_str.encode()).hexdigest()
    return file_name


def get_data():
    try:
        count = int(entry_line_1.get_text())
        pendulum_length_s = list(map(lambda x: eval(x) * 100, entry_line_2.get_text().split(',')))
        initial_theta_s = list(map(eval, entry_line_3.get_text().split(',')))
        mass_s = list(map(eval, entry_line_4.get_text().split(',')))

        return [count, pendulum_length_s, initial_theta_s, mass_s, 'None']
    except:
        return [2, [100, 100], [60, 120], [1, 1], 'None']


class Grid:
    def __init__(self, screen, x, y, left, right, top, bottom, step=50):
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.screen = screen
        self.GRID_DEEP = (47, 60, 65)
        self.GRID = (15, 21, 24)
        self.BACKGROUND = (0, 0, 0)
        self.step = step

    def draw_grid(self):
        pygame.draw.rect(self.screen, self.BACKGROUND,
                         (self.left, self.top, self.right - self.left, self.bottom - self.top))
        for i in range(1, int((self.bottom - self.top) / self.step) + 1):
            if self.bottom > self.y + i * self.step > self.top:
                pygame.draw.line(self.screen, self.GRID, (self.left, self.y + i * self.step),
                                 (self.right - 1, self.y + i * self.step), width=2)
            if self.bottom > self.y - i * self.step > self.top:
                pygame.draw.line(self.screen, self.GRID, (self.left, self.y - i * self.step),
                                 (self.right - 1, self.y - i * self.step), width=2)
        for i in range(1, int((self.right - self.left) / self.step) + 1):
            if self.right > self.x + i * self.step > self.left:
                pygame.draw.line(self.screen, self.GRID, (self.x + i * self.step, self.top),
                                 (self.x + i * self.step, self.bottom - 1), width=2)
            if self.right > self.x - i * self.step > self.left:
                pygame.draw.line(self.screen, self.GRID, (self.x - i * self.step, self.top),
                                 (self.x - i * self.step, self.bottom - 1), width=2)
        # 画中心线
        pygame.draw.line(self.screen, self.GRID_DEEP, (self.left, self.y), (self.right - 1, self.y), width=2)
        pygame.draw.line(self.screen, self.GRID_DEEP, (self.x, self.top), (self.x, self.bottom - 1), width=2)


class Ball:
    def __init__(self, ball, num, r, theta, color, track_color, density=1, radius=10):
        self.num = num
        self.radius = radius
        self.color = color
        self.track_length = 180  # 轨迹长度
        self.surface = experiment_equipment_surface
        self.r = r
        if self.num:  # 判断是否是悬挂点
            self.track = track_color
            self.history_x = []
            self.history_y = []
            self.body = pymunk.Body()  # 刚体
            self.shape = pymunk.Circle(self.body, self.radius)
            self.body.position = ball.body.position[0] + r * np.sin(theta * math.pi / 180), ball.body.position[
                1] - r * np.cos(theta * math.pi / 180)
            self.shape.density = density  # 密度
            self.shape.elasticity = 1.0  # 碰撞类型为完全弹性碰撞
            self.shape.friction = 0  # 无摩擦力
            space.add(self.body, self.shape)  # 向空间中添加这两个对象
        else:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body.position = ball

    def draw(self):
        if self.num:
            self.history(self.history_x, self.history_y, self.body.position[0], self.body.position[1])
            index = int(self.body.position[0]), SCREEN_SIZE_Y - int(self.body.position[1])
            r = 2
            for i in range(len(self.history_x)):
                translucence_surface = pygame.Surface((2 * r, 2 * r))
                translucence_surface.fill(BLACK)
                translucence_surface.set_colorkey(BLACK)
                pygame.draw.circle(translucence_surface, self.track, (r, r), r)
                translucence_surface.set_alpha(i)
                self.surface.blit(translucence_surface,
                                  (self.history_x[i] - r, SCREEN_SIZE_Y - (self.history_y[i] + r)))
            pygame.draw.circle(self.surface, self.color, index, self.radius)  # 绘制圆圈

    def history(self, h_x, h_y, x, y):
        if len(h_x) < self.track_length:
            h_x.append(x)
            h_y.append(y)
        else:
            del h_x[0]
            del h_y[0]
            h_x.append(x)
            h_y.append(y)


class String:
    def __init__(self, body1, body2):
        self.body1 = body1
        self.body2 = body2
        self.surface = experiment_equipment_surface
        self.joint = pymunk.PinJoint(self.body1, self.body2)
        self.joint.error_bias = 0
        space.add(self.joint)

    def draw(self):
        index_s = int(self.body1.position[0]), SCREEN_SIZE_Y - int(self.body1.position[1])  # 起点坐标
        index_e = int(self.body2.position[0]), SCREEN_SIZE_Y - int(self.body2.position[1])  # 终点坐标
        pygame.draw.line(self.surface, STRING, index_s, index_e, width=3)  # 画线


fixed_point = Ball((FIXED_X, FIXED_Y), 0, -1, -1, -1, -1)
grid = Grid(experiment_equipment_surface, FIXED_X, SCREEN_SIZE_Y - FIXED_Y, DRAW_LEFT, DRAW_RIGHT, DRAW_TOP,
            DRAW_BOTTOM)

# 初始数据的定义
objects = None  # 场景中是否存在摆
status = False  # 是否开始
display = False  # 摆是否显示
stop = False  # 是否停止
data_list = [[], [[], []], [[], []], [[], []]]  # 时间， 第一个小球， 第二个小球， 第三个小球
phase_diagrams_name = None
reset.disable()
times = 0
max_time = 10

while is_running:
    # 判定图片是否加载完毕
    # if times >= max_time * FPS:
    #     display = True
    # else:
    #     display = False

    # 一些变量的获取
    mouse_pos = pygame.mouse.get_pos()
    time_delta = clock.tick(FPS) / 1000

    # 获取事件并逐类响应
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            is_running = False
        # UI事件
        elif event.type == pygame.USEREVENT:
            # 按钮按下
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == next_:
                    is_running = False
                    # subprocess.Popen("主页UI.exe")
                    # subprocess.Popen(r".\venv\Scripts\python 主页UI.py")
                    os.system(r"start .\venv\Scripts\python 主页UI.py")
                    # os.popen(r"主页UI.exe")
                elif event.ui_element == start:
                    initial_data = get_data()  # 获取输入的参数
                    temp_balls = []
                    temp_strings = []
                    # 判断数据（小球个数）是否符合要求
                    if 2 <= initial_data[0] <= 3:
                        temp = fixed_point
                        for i in range(initial_data[0]):
                            temp_ball = Ball(temp, i + 1, initial_data[1][i], initial_data[2][i],
                                             BALL, GREEN, density=initial_data[3][i])
                            # 创建对象并储存在列表中
                            temp_string = String(temp_ball.body, temp.body)
                            temp_balls.append(temp_ball)
                            temp_strings.append(temp_string)
                            temp = temp_ball
                    objects = temp_strings + temp_balls
                    # 状态量的设置
                    status = True
                    start.disable()
                    reset.enable()
                elif event.ui_element == reset:
                    # 将约束空间清空
                    for obj in objects:
                        if type(obj) == String:
                            space.remove(obj.joint)
                        elif type(obj) == Ball:
                            space.remove(obj.shape, obj.body)
                    # 复原初始参数
                    objects = None
                    status = False
                    display = False
                    stop = False
                    data_list = [[], [[], []], [[], []], [[], []]]
                    phase_diagrams_name = None
                    times = 0
                    start.enable()
                    reset.disable()
                    data_processing_surface.fill((0, 0, 0, 0))
        ui_manager.process_events(event)  # 处理ui事件

    window_surface.fill(BLACK_A)
    experiment_equipment_surface.fill((0, 0, 0, 0))

    grid.draw_grid()

    if objects:
        # 恢复场景
        if times == max_time * 60:
            for obj in objects:
                if type(obj) == String:
                    space.remove(obj.joint)
                elif type(obj) == Ball:
                    space.remove(obj.shape, obj.body)
            objects = None

            initial_data = get_data()
            temp_balls = []
            temp_strings = []
            if initial_data:
                if 2 <= initial_data[0] <= 3:
                    temp = fixed_point
                    for i in range(initial_data[0]):
                        temp_ball = Ball(temp,
                                         i + 1,
                                         initial_data[1][i],
                                         initial_data[2][i],
                                         BALL,
                                         GREEN,
                                         density=initial_data[3][i])

                        temp_string = String(temp_ball.body, temp.body)

                        temp_balls.append(temp_ball)
                        temp_strings.append(temp_string)
                        temp = temp_ball
            objects = temp_strings + temp_balls

        # 加载图片（绘制图片）
        if not display:
            if len(objects) == 4:
                data_list[0].append(1 / FPS * times)

                pos_vec_1 = objects[2].body.position
                pos_vec_2 = objects[3].body.position

                data_list[1][0].append(pos_vec_1[0] - FIXED_X)
                data_list[1][1].append(pos_vec_1[1] - FIXED_Y)
                data_list[2][0].append(pos_vec_2[0] - FIXED_X)
                data_list[2][1].append(pos_vec_2[1] - FIXED_Y)

                calculate(data_list[0], times, get_data(),
                          data_list[1][0], data_list[1][1],
                          data_list[2][0], data_list[2][1])

            elif len(objects) == 6:
                data_list[0].append(1 / FPS * times)

                pos_vec_1 = objects[3].body.position
                pos_vec_2 = objects[4].body.position
                pos_vec_3 = objects[5].body.position

                data_list[1][0].append(pos_vec_1[0] - FIXED_X)
                data_list[1][1].append(pos_vec_1[1] - FIXED_Y)
                data_list[2][0].append(pos_vec_2[0] - FIXED_X)
                data_list[2][1].append(pos_vec_2[1] - FIXED_Y)
                data_list[3][0].append(pos_vec_3[0] - FIXED_X)
                data_list[3][1].append(pos_vec_3[1] - FIXED_Y)
                calculate(data_list[0], times, get_data(),
                          data_list[1][0], data_list[1][1],
                          data_list[2][0], data_list[2][1],
                          data_list[3][0], data_list[3][1])

        # 将加载好的相图画在屏幕上
        if display:
            for obj in objects:
                obj.draw()
            if not stop:
                if len(objects) == 4:
                    file_name = get_filename(times - max_time * FPS, get_data())
                    if os.path.exists(r".\cache\{}.png".format(file_name)):
                        phase_diagrams_name = file_name
                    else:
                        stop = True
                    pic_1 = pygame.image.load(r".\cache\{}.png".format(phase_diagrams_name))
                    data_processing_surface.blit(pygame.transform.scale(pic_1, (264, 550)), (956, 68))
                elif len(objects) == 6:
                    file_name_1 = get_filename(times - max_time * FPS, get_data())
                    file_name_2 = get_filename(times - max_time * FPS, get_data())
                    file_name_3 = get_filename(times - max_time * FPS, get_data())
                    if os.path.exists(r".\cache\{}.png".format(file_name_1)):
                        phase_diagrams_name = file_name_1

                    else:
                        stop = True
                    pic_1 = pygame.image.load(r".\cache\{}.png".format(phase_diagrams_name))
                    data_processing_surface.blit(pygame.transform.scale(pic_1, (264, 550)), (956, 68))

        # 将整个空间前进一点
        if not stop:
            space.step(1 / FPS)

    ui_manager.update(time_delta)

    window_surface.blit(experiment_equipment_surface, (0, 0))
    window_surface.blit(data_processing_surface, (0, 0))
    ui_manager.draw_ui(window_surface)
    window_surface.blit(background_pic, (0, 0))

    if status:
        times += 1
    pygame.display.update()
