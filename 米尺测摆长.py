# -- coding: utf-8 --
# @Time: 2021/8/15 18:01
# @Author: Zavijah  zavijah@qq.com
# @File: main.py
# @Software: PyCharm
# @Purpose:****
import csv
import os
import subprocess

import pygame
import pygame.freetype
import pygame_gui
from pygame import Color

WINDOW_SIZE = (1280, 720)

# 颜色的定义
WHITE: Color = pygame.Color("#ffffff")
RED_A: Color = pygame.Color("#ccd7dd")
BLUE_A: Color = pygame.Color("#1aafd0")
GREEN_A: Color = pygame.Color("#fffaec")
BLACK_A: Color = pygame.Color("#333333")

is_running = True

pygame.init()  # 初始化窗口
pygame.display.set_caption("单摆")  # 设置窗口标题
window_surface = pygame.display.set_mode(WINDOW_SIZE)  # 设置窗口

clock = pygame.time.Clock()  # 添加管理时钟

# 表面的创建
# experiment_equipment_surface = pygame.Surface(WINDOW_SIZE)
experiment_equipment_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
experiment_equipment_surface_enlarge_down = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
experiment_equipment_surface_enlarge_up = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
data_process_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
experiment_equipment_surface = experiment_equipment_surface.convert_alpha()
experiment_equipment_surface_enlarge_down = experiment_equipment_surface_enlarge_down.convert_alpha()
experiment_equipment_surface_enlarge_up = experiment_equipment_surface_enlarge_up.convert_alpha()
data_process_surface = data_process_surface.convert_alpha()

# 添加界面管理器
ui_manager = pygame_gui.UIManager(WINDOW_SIZE, r"ui_themes\json\theme.json")

# 加载图片
background_pic = pygame.image.load(r"dependent_files\pic\摆长测量.png")

fonts = pygame.freetype.Font(r".\dependent_files\font\STSONG.TTF", 18)
entry_fonts = pygame.freetype.Font(r".\dependent_files\font\华光标题黑_CNKI.TTF")

next_ = pygame_gui.elements.UIButton(pygame.Rect(1106, 633, 101, 67),
                                     text="",
                                     manager=ui_manager,
                                     object_id="next")


class Experiment:
    def __init__(self, x_loc: int, y_loc: int):
        self.manager = ui_manager
        self.ball_color = RED_A
        self.pendulum_color = BLUE_A

        self.surface = experiment_equipment_surface

        self.ball_radius = 5
        self.pendulum_length = 400
        self.location = [x_loc, y_loc]

        self.reset = pygame_gui.elements.UIButton(pygame.Rect(1100, 570, 100, 50),
                                                  text="重置",
                                                  manager=self.manager,
                                                  object_id='reset',
                                                  )

    def draw_pendulum(self, loc: list, length: int):
        pygame.draw.line(self.surface, self.pendulum_color, loc, (loc[0], loc[1] + length), 5)

    def draw_ball(self, loc: tuple, r: int):
        pygame.draw.circle(self.surface, self.ball_color, loc, r, 0)

    def draw(self):
        self.draw_pendulum(self.location, self.pendulum_length)
        self.draw_ball((self.location[0] + 1, self.location[1] + self.pendulum_length + 2), self.ball_radius)


class Ruler:
    def __init__(self, x_loc: int, y_loc: int):
        # 常量的定义
        self.manager = ui_manager
        self.surface = experiment_equipment_surface
        self.main_color = GREEN_A
        self.calibration_color = BLACK_A
        self.font = fonts

        # 基础量
        self.location = [x_loc, y_loc]
        self.size = [50, 451]
        self.rect = [0, 0, 0, 0]

        # 偏移量
        self.moving = False
        self.offset = [0, 0]
        self.temp_x: int = -1
        self.temp_y: int = -1

        # 其他量
        self.update()
        self.ruler_ = self.draw_main(self.rect)

    def update(self):
        self.rect = self.location + self.size
        self.rect = [self.rect[0] + self.offset[0], self.rect[1] + self.offset[1], self.rect[2], self.rect[3]]

    def draw_main(self, rect: list):
        temp = pygame.draw.rect(self.surface, self.main_color, rect, 0)
        return temp

    def draw_calibration(self, rect: list, interval: int, count: int):
        for i in range(count):
            if i % 5 == 0:
                pygame.draw.line(self.surface, self.calibration_color,
                                 (rect[0], rect[1] + i * interval + 10),
                                 (rect[0] + 15, rect[1] + i * interval + 10), 1)
            else:
                pygame.draw.line(self.surface, self.calibration_color,
                                 (rect[0], rect[1] + i * interval + 10),
                                 (rect[0] + 8, rect[1] + i * interval + 10), 1)
            if i % 25 == 0:
                self.font.render_to(self.surface,
                                    (rect[0] + 20, rect[1] + i * interval + 5),
                                    "{}".format(i), fgcolor=BLACK_A, size=18)
        self.font.render_to(self.surface,
                            (rect[0] + 26, rect[1] + 100 * interval + 40),
                            "cm", fgcolor=BLACK_A, size=18)

    def get_temp(self, pos: tuple):
        self.temp_x = pos[0] - self.offset[0]
        self.temp_y = pos[1] - self.offset[1]

    def move(self, pos: tuple):
        self.offset[0] = pos[0] - self.temp_x
        self.offset[1] = pos[1] - self.temp_y

    def draw(self):
        self.update()
        self.ruler_ = self.draw_main(self.rect)
        self.draw_calibration(self.rect, 4, 106)


class EnLargeDown:
    def __init__(self, e, r):
        # 常量的引入
        self.surface = experiment_equipment_surface_enlarge_down
        self.font = fonts

        # 两个对象
        self.ruler = r
        self.experiment = e

        # 基础参数
        self.ruler_loc = [564 - self.ruler.offset[0] * 20 + 277 * 20, 83 - self.ruler.offset[1] * 20 - 17 * 20]
        self.ruler_size = [90, 850]
        self.ruler_rect = [0, 0, 0, 0]

        self.ball_loc = [560, 520]
        self.ball_radius = 40

        self.pendulum_loc = [self.ball_loc[0], 360]
        self.pendulum_length = 520 - 360

        # 偏移量
        self.ruler_offset = [0, 0]

        # 更新数值
        self.update()

    def update(self):
        self.ruler_offset = [self.ruler.offset[0] * 20, self.ruler.offset[1] * 20]
        self.ruler_rect = self.ruler_loc + self.ruler_size
        self.ruler_rect = [self.ruler_rect[0] + self.ruler_offset[0], self.ruler_rect[1] + self.ruler_offset[1],
                           self.ruler_rect[2], self.ruler_rect[3]]

    def draw_ruler(self):
        if self.ruler.offset[1] < -6:
            pygame.draw.rect(self.surface, ruler.main_color, self.ruler_rect, 0)
        else:
            pygame.draw.rect(self.surface, ruler.main_color,
                             [self.ruler_rect[0], 360, self.ruler_rect[2], WINDOW_SIZE[1]], 0)

    def draw_tick_mark(self):
        pygame.draw.line(self.surface, self.ruler.calibration_color,
                         (self.ruler_rect[0], self.ruler_rect[1] + 438),
                         (self.ruler_rect[0] + 50, self.ruler_rect[1] + 438), 1)
        self.font.render_to(self.surface,
                            (self.ruler_rect[0] + 60, self.ruler_rect[1] + 438),
                            "{}".format(100), size=20)
        # 向上
        for i in range(1, 1000):
            if self.ruler_rect[1] + 438 - i * 8 < 360:
                break
            if i % 5 != 0 and i % 10 != 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 438 - i * 8),
                                 (self.ruler_rect[0] + 10, self.ruler_rect[1] + 438 - i * 8), 1)
            elif i % 5 == 0 and i % 10 != 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 438 - i * 8),
                                 (self.ruler_rect[0] + 20, self.ruler_rect[1] + 438 - i * 8), 1)
            elif i % 10 == 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 438 - i * 8),
                                 (self.ruler_rect[0] + 30, self.ruler_rect[1] + 438 - i * 8), 1)
                self.font.render_to(self.surface,
                                    (self.ruler_rect[0] + 60, self.ruler_rect[1] + 438 - i * 8),
                                    "{}".format(100 - i // 10), size=20)

        # 向下
        for i in range(1, 100):
            if self.ruler.offset[1] < 12:
                if self.ruler_rect[1] + 438 + i * 8 > self.ruler_rect[1] + self.ruler_rect[3] - 215:
                    break
            else:
                if self.ruler_rect[1] + 438 + i * 8 > WINDOW_SIZE[1]:
                    break
            if i % 5 != 0 and i % 10 != 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 438 + i * 8),
                                 (self.ruler_rect[0] + 10, self.ruler_rect[1] + 438 + i * 8), 1)
            elif i % 5 == 0 and i % 10 != 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 438 + i * 8),
                                 (self.ruler_rect[0] + 20, self.ruler_rect[1] + 438 + i * 8), 1)
            elif i % 10 == 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 438 + i * 8),
                                 (self.ruler_rect[0] + 30, self.ruler_rect[1] + 438 + i * 8), 1)
                self.font.render_to(self.surface,
                                    (self.ruler_rect[0] + 60, self.ruler_rect[1] + 438 + i * 8),
                                    "{}".format(100 + i // 10), size=20)

    def draw_ball(self):
        pygame.draw.circle(self.surface, self.experiment.ball_color, self.ball_loc, self.ball_radius, 0)

    def draw_cycloid(self):
        pygame.draw.line(self.surface, self.experiment.pendulum_color,
                         self.pendulum_loc, [self.pendulum_loc[0], self.pendulum_loc[1] + self.pendulum_length], 5)

    def draw(self):
        self.update()
        self.draw_cycloid()
        self.draw_ball()
        self.draw_ruler()
        self.draw_tick_mark()

        pygame.draw.rect(self.surface, (0, 0, 0, 0), (0, 0, WINDOW_SIZE[0], 364), 0)
        pygame.draw.rect(self.surface, (0, 0, 0, 0), (714, 0, WINDOW_SIZE[0] - 714, WINDOW_SIZE[1]), 0)


class EnLargeUp:
    def __init__(self, e, r):
        # 常量的引入
        self.surface = experiment_equipment_surface_enlarge_up
        self.font = fonts

        # 两个对象
        self.ruler = r
        self.experiment = e

        # 基础参数
        self.ruler_loc = [564 - self.ruler.offset[0] * 20 + 277 * 20, 80 - self.ruler.offset[1] * 20 - 17 * 20]
        self.ruler_size = [90, 400]
        self.ruler_rect = [0, 0, 0, 0]

        self.ball_loc = [560, 570]
        self.ball_radius = 40

        self.pendulum_loc = [self.ball_loc[0], 140]
        self.pendulum_length = 360 - 140

        # 偏移量
        self.ruler_offset = [0, 0]

        # 更新数值
        self.update()

    def update(self):
        self.ruler_offset = [self.ruler.offset[0] * 20, self.ruler.offset[1] * 20]
        self.ruler_rect = self.ruler_loc + self.ruler_size
        self.ruler_rect = [self.ruler_rect[0] + self.ruler_offset[0], self.ruler_rect[1] + self.ruler_offset[1],
                           self.ruler_rect[2], self.ruler_rect[3]]

    def draw_ruler(self):
        if self.ruler.offset[1] >= 13:
            pass
            pygame.draw.rect(self.surface, ruler.main_color, self.ruler_rect, 0)
        else:
            pygame.draw.rect(self.surface, ruler.main_color,
                             [self.ruler_rect[0], 0, self.ruler_rect[2], 360], 0)

    def draw_tick_mark(self):
        pygame.draw.line(self.surface, self.ruler.calibration_color,
                         (self.ruler_rect[0], self.ruler_rect[1] + 60),
                         (self.ruler_rect[0] + 50, self.ruler_rect[1] + 60), 1)
        if self.ruler_rect[1] + 60 > 0:
            self.font.render_to(self.surface,
                                (self.ruler_rect[0] + 60, self.ruler_rect[1] + 60),
                                "{}".format(0), size=20)
        # 向下
        for i in range(1, 10001):
            if self.ruler.offset[1] >= 13:
                if self.ruler_rect[1] + 60 + i * 8 > self.ruler_rect[1] + self.ruler_rect[3]:
                    break
            else:
                if self.ruler_rect[1] + 60 + i * 8 > 360:
                    break
            if i % 5 != 0 and i % 10 != 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 60 + i * 8),
                                 (self.ruler_rect[0] + 10, self.ruler_rect[1] + 60 + i * 8), 1)
            elif i % 5 == 0 and i % 10 != 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 60 + i * 8),
                                 (self.ruler_rect[0] + 20, self.ruler_rect[1] + 60 + i * 8), 1)
            elif i % 10 == 0:
                pygame.draw.line(self.surface, self.ruler.calibration_color,
                                 (self.ruler_rect[0], self.ruler_rect[1] + 60 + i * 8),
                                 (self.ruler_rect[0] + 30, self.ruler_rect[1] + 60 + i * 8), 1)
                if self.ruler_rect[1] + 60 + i * 8 > 0:
                    self.font.render_to(self.surface,
                                        (self.ruler_rect[0] + 60, self.ruler_rect[1] + 60 + i * 8),
                                        "{}".format(i // 10), size=20)

    def draw_cycloid(self):
        pygame.draw.line(self.surface, self.experiment.pendulum_color,
                         self.pendulum_loc, [self.pendulum_loc[0], self.pendulum_loc[1] + self.pendulum_length], 5)

    def draw(self):
        self.update()
        self.draw_cycloid()
        self.draw_ruler()
        self.draw_tick_mark()

        pygame.draw.rect(self.surface, (0, 0, 0, 0), (0, 360, WINDOW_SIZE[0], WINDOW_SIZE[1]), 0)
        pygame.draw.rect(self.surface, (0, 0, 0, 0), (714, 0, WINDOW_SIZE[0] - 714, WINDOW_SIZE[1]), 0)


class Data:
    def __init__(self):
        self.manager = ui_manager
        self.surface = data_process_surface
        self.font = entry_fonts

        self.data_list = []
        self.text = ""
        self.x_offset = 70
        self.y_offset = 181
        self.width = 67
        self.height = 30
        self.loc = [123, 385]

        self.entry_line_1 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0], self.loc[1], self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_2 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 1 * self.x_offset, self.loc[1], self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_3 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 2 * self.x_offset, self.loc[1], self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_4 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 3 * self.x_offset, self.loc[1], self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_5 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 4 * self.x_offset, self.loc[1], self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_6 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0], self.loc[1] + self.y_offset, self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_7 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 1 * self.x_offset, self.loc[1] + self.y_offset, self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_8 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 2 * self.x_offset, self.loc[1] + self.y_offset, self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_9 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 3 * self.x_offset, self.loc[1] + self.y_offset, self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_10 = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(self.loc[0] + 4 * self.x_offset, self.loc[1] + self.y_offset, self.width, -1),
            manager=self.manager, object_id="entry_line")
        self.entry_line_1.set_text('1.00')
        self.entry_line_2.set_text('1.00')
        self.entry_line_3.set_text('1.00')
        self.entry_line_4.set_text('1.00')
        self.entry_line_5.set_text('1.00')
        self.entry_line_6.set_text('1.00')
        self.entry_line_7.set_text('1.00')
        self.entry_line_8.set_text('1.00')
        self.entry_line_9.set_text('1.00')

    def draw(self):
        self.font.render_to(self.surface, [self.loc[0] + 25 + 0 * self.x_offset, self.loc[1] - 90 + 0 * self.y_offset],
                            text="1", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 1 * self.x_offset, self.loc[1] - 90 + 0 * self.y_offset],
                            text="2", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 2 * self.x_offset, self.loc[1] - 90 + 0 * self.y_offset],
                            text="3", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 3 * self.x_offset, self.loc[1] - 90 + 0 * self.y_offset],
                            text="4", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 4 * self.x_offset, self.loc[1] - 90 + 0 * self.y_offset],
                            text="5", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 0 * self.x_offset, self.loc[1] - 90 + 1 * self.y_offset],
                            text="6", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 1 * self.x_offset, self.loc[1] - 90 + 1 * self.y_offset],
                            text="7", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 2 * self.x_offset, self.loc[1] - 90 + 1 * self.y_offset],
                            text="8", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 25 + 3 * self.x_offset, self.loc[1] - 90 + 1 * self.y_offset],
                            text="9", fgcolor=WHITE, size=32)
        self.font.render_to(self.surface, [self.loc[0] + 12 + 4 * self.x_offset, self.loc[1] - 90 + 1 * self.y_offset],
                            text="10", fgcolor=WHITE, size=32)

    def save(self):
        result = []
        self.data_list = [self.entry_line_1.get_text(),
                          self.entry_line_2.get_text(),
                          self.entry_line_3.get_text(),
                          self.entry_line_4.get_text(),
                          self.entry_line_5.get_text(),
                          self.entry_line_6.get_text(),
                          self.entry_line_7.get_text(),
                          self.entry_line_8.get_text(),
                          self.entry_line_9.get_text(),
                          self.entry_line_10.get_text(), ]
        try:
            for value in self.data_list:
                result.append(float(value))
            with open(r"data\摆长.csv", mode="w", newline="", encoding="utf-8") as f:
                fw = csv.writer(f)
                fw.writerow(result)
            return True
        except:
            return False


message_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
message_surface = message_surface.convert_alpha()
ui_manager2 = pygame_gui.UIManager(WINDOW_SIZE, r'./ui_themes/json/message.json')


class Initial:
    def __init__(self, manager, surface):
        self.manager = manager
        self.surface = surface

        self.son_window = pygame_gui.elements.ui_window.UIWindow(
            rect=pygame.Rect(((WINDOW_SIZE[0] - 500) / 2, (WINDOW_SIZE[1] - 300) / 2, 400, 200)),
            window_display_title="提示",
            manager=self.manager,
            object_id='window')

        self.text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(100, 20, 200, 50),
            text="有效数字位数不对！",
            manager=self.manager,
            container=self.son_window,
            object_id='message')

        self.OK_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 80, 100, 30)),
            text="确认",
            manager=self.manager,
            container=self.son_window,
            object_id='button')


experiment_equipment = Experiment(850, 150)
ruler = Ruler(1130, 124)
# ruler.offset = [-277, 17]
data = Data()
en_large_down = EnLargeDown(experiment_equipment, ruler)
en_large_up = EnLargeUp(experiment_equipment, ruler)

while is_running:  # 主程序
    time_delta = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and ruler.ruler_.collidepoint(mouse_pos):
                ruler.get_temp(mouse_pos)
                ruler.moving = True

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1 and ruler.moving:
                ruler.move(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and ruler.moving:
                ruler.moving = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ruler.offset[1] -= 0.1
            elif event.key == pygame.K_DOWN:
                ruler.offset[1] += 0.1
            elif event.key == pygame.K_LEFT:
                ruler.offset[0] -= 0.1
            elif event.key == pygame.K_RIGHT:
                ruler.offset[0] += 0.1

        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == experiment_equipment.reset:
                    ruler.offset = [0, 0]
                elif event.ui_element == next_:
                    if data.save():
                        is_running = False
                        # subprocess.Popen("游标卡尺测直径.exe")
                        # subprocess.Popen(r".\venv\Scripts\python 游标卡尺测直径.py")
                        os.system(r"start .\venv\Scripts\python 游标卡尺测直径.py")
                        # os.popen(r"游标卡尺测直径.exe")
                elif event.ui_element == initial.OK_button:
                    initial.son_window.hide()
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if len(event.text) != 5:
                    initial = Initial(manager=ui_manager2, surface=message_surface)

        ui_manager.process_events(event)
        ui_manager2.process_events(event)

    message_surface.fill((0, 0, 0, 0))
    window_surface.fill(BLACK_A)
    experiment_equipment_surface.fill((0, 0, 0, 0))
    experiment_equipment_surface_enlarge_down.fill((0, 0, 0, 0))
    experiment_equipment_surface_enlarge_up.fill((0, 0, 0, 0))

    experiment_equipment.draw()
    ruler.draw()
    en_large_down.draw()
    en_large_up.draw()
    data.draw()

    ui_manager.update(time_delta)
    ui_manager2.update(time_delta)

    window_surface.blit(experiment_equipment_surface, (0, 0))
    window_surface.blit(experiment_equipment_surface_enlarge_down, (0, 0))
    window_surface.blit(experiment_equipment_surface_enlarge_up, (0, 0))

    window_surface.blit(background_pic, (0, 0))
    ui_manager.draw_ui(window_surface)
    ui_manager2.draw_ui(message_surface)
    window_surface.blit(data_process_surface, (0, 0))
    window_surface.blit(message_surface, (0, 0))

    pygame.display.update()
