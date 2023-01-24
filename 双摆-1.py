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
FIXED_X = SCREEN_SIZE_X / 2
FIXED_Y = SCREEN_SIZE_Y / 2 + 100

DRAW_LEFT = 0
DRAW_RIGHT = SCREEN_SIZE_X
DRAW_TOP = 0
DRAW_BOTTOM = SCREEN_SIZE_Y



# pygame初始化
pygame.init()  # 初始化窗口
pygame.display.set_caption("多摆")  # 设置窗口标题
window_surface = pygame.display.set_mode(WINDOW_SIZE)  # 设置窗口
clock = pygame.time.Clock()  # 添加管理时钟
# 表面的创建
experiment_equipment_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32).convert_alpha()



# pymunk初始化
# space.damping = 1  # 阻尼值
space = pymunk.Space()  # 创建一个约束空间
space.gravity = (0, -980)  # 设置重力


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

times = 0
max_time = 10

initial_data = [2, [100, 100], [60, 120], [1, 1], 'None']
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

while True:
    display = True

    # 一些变量的获取
    mouse_pos = pygame.mouse.get_pos()
    time_delta = clock.tick(FPS) / 1000

    # 获取事件并逐类响应
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.fill(BLACK_A)
    experiment_equipment_surface.fill((0, 0, 0, 0))

    grid.draw_grid()

    for obj in objects:
        obj.draw()

    space.step(1 / FPS)

    window_surface.blit(experiment_equipment_surface, (0, 0))
    pygame.display.update()
