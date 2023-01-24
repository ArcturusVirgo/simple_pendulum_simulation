# -- coding: utf-8 --
# @Time: 2021/8/15 18:01
# @Author: Zavijah  zavijah@qq.com
# @File: main.py
# @Software: PyCharm
# @Purpose:

import csv
import os
import subprocess

import pygame
import pygame.freetype
import pygame_gui
from pygame import Color

WINDOW_SIZE = (1280, 720)

# 颜色的定义
Ball: Color = pygame.Color("#ced7df")  # 小球的颜色
WHITE: Color = pygame.Color("#ffffff")
RED_A: Color = pygame.Color("#cfcfcf")  #fc636b # 主尺子
BLUE_A: Color = pygame.Color("#1aafd0")
GREEN_A: Color = pygame.Color("#f7f7f7") #ff4e00 # 副尺子
BLACK_A: Color = pygame.Color("#333333")

is_running = True

next_program = None

pygame.init()  # 初始化窗口
pygame.display.set_caption("单摆")  # 设置窗口标题
window_surface = pygame.display.set_mode(WINDOW_SIZE)  # 设置窗口

clock = pygame.time.Clock()  # 添加管理时钟

# 表面的创建
experiment_equipment_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
data_process_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA, 32)
experiment_equipment_surface = experiment_equipment_surface.convert_alpha()
data_process_surface = data_process_surface.convert_alpha()

ui_manager = pygame_gui.UIManager(WINDOW_SIZE, r"ui_themes\json\theme.json")

background_pic = pygame.image.load(r"dependent_files\pic\小球半径测量.png")

next_ = pygame_gui.elements.UIButton(pygame.Rect(1106, 633, 101, 67),
                                     text="",
                                     manager=ui_manager,
                                     object_id="next")
fonts = pygame.freetype.Font(r".\dependent_files\font\STSONG.TTF")
entry_fonts = pygame.freetype.Font(r".\dependent_files\font\华光标题黑_CNKI.TTF")





class Experiment:
    def __init__(self, x_loc: int, y_loc: int):
        self.ball_color = Ball

        self.surface = experiment_equipment_surface

        self.ball_radius = 50
        self.location = x_loc, y_loc

    def draw_ball(self, loc: tuple, r: int):
        pygame.draw.circle(self.surface, self.ball_color, loc, r, 0)

    def draw(self):
        # self.draw_pendulum(self.location, self.pendulum_length)
        self.draw_ball(self.location, self.ball_radius)


class Calipers:
    def __init__(self, x_loc, y_loc):
        self.manager = ui_manager
        self.surface = experiment_equipment_surface
        self.font = fonts

        self.mainScale_color = RED_A
        self.calibration_color = BLACK_A
        self.cursor_color = GREEN_A


        self.cursor_size = [550, 30]
        self.main_size = [700, 70]
        self.main_location = [x_loc, y_loc]
        self.cursor_offset = 50

        self.temp_x: int = -1
        self.temp_y: int = -1

        self.main_moving = False
        self.cursor_moving = False

        self.main_scale, self.cursor = self.draw_ruler(self.main_location[0], self.main_location[1], self.cursor_offset)

        self.reset = pygame_gui.elements.UIButton(pygame.Rect(1100, 570, 100, 50),
                                                  text="重置",
                                                  manager=self.manager,
                                                  object_id='reset', )



    def draw_ruler(self, basic_x, basic_y, offset):
        # 主尺部分
        main_scale = pygame.draw.rect(self.surface, self.mainScale_color,
                                      (basic_x, basic_y, self.main_size[0], self.main_size[1]))
        pygame.draw.polygon(self.surface, self.mainScale_color, ((basic_x, basic_y + self.main_size[1]),
                                                                 (basic_x + 20, basic_y + self.main_size[1]),
                                                                 (basic_x + 20, basic_y + self.main_size[1] + 110)))
        pygame.draw.polygon(self.surface, self.mainScale_color, ((basic_x + 20, basic_y),
                                                                 (basic_x + 40, basic_y),
                                                                 (basic_x + 20, basic_y - 50)))
        # 主尺刻度
        for i in range(61):
            if i % 5 == 0:
                pygame.draw.line(self.surface, self.calibration_color,
                                 (basic_x + 50 + i * 10, basic_y + self.main_size[1]),
                                 (basic_x + 50 + i * 10, basic_y + self.main_size[1] - 20), 1)
            else:
                pygame.draw.line(self.surface, self.calibration_color,
                                 (basic_x + 50 + i * 10, basic_y + self.main_size[1]),
                                 (basic_x + 50 + i * 10, basic_y + self.main_size[1] - 10), 1)
            if i % 10 == 0:
                self.font.render_to(self.surface,
                                    (basic_x + 45 + i * 10, basic_y + self.main_size[1] - 35),
                                    "{}".format(int(i / 10)), fgcolor=BLACK_A, size=18)
        self.font.render_to(self.surface,
                            (basic_x + 55 + 61 * 10, basic_y + self.main_size[1] - 55),
                            "cm", fgcolor=BLACK_A, size=18)
        # 游标部分
        cursor = pygame.draw.rect(self.surface, self.cursor_color,
                                  (basic_x + offset + 20, basic_y + self.main_size[1] - 3, self.cursor_size[0],
                                   self.cursor_size[1]))

        pygame.draw.rect(self.surface, self.cursor_color,
                         (basic_x + offset + 20, basic_y - self.cursor_size[1], self.cursor_size[0],
                          self.cursor_size[1]))

        pygame.draw.polygon(self.surface, self.cursor_color, ((basic_x + offset + 20, basic_y + self.main_size[1] - 3),
                                                              (basic_x + offset + 40, basic_y + self.main_size[1] - 3),
                                                              (basic_x + offset + 20,
                                                               basic_y + self.main_size[1] + 110)))

        pygame.draw.polygon(self.surface, self.cursor_color, ((basic_x + offset + 20, basic_y - 1),
                                                              (basic_x + offset, basic_y - 1),
                                                              (basic_x + offset + 20, basic_y - 50)))
        # 游标刻度
        for i in range(51):
            if i % 5 == 0:
                pygame.draw.line(self.surface, self.calibration_color,
                                 (basic_x + offset + 50 + i * 9.8, basic_y + self.main_size[1] - 3),
                                 (basic_x + offset + 50 + i * 9.8, basic_y + self.main_size[1] - 3 + 20), 1)
            else:
                pygame.draw.line(self.surface, self.calibration_color,
                                 (basic_x + offset + 50 + i * 9.8, basic_y + self.main_size[1] - 3),
                                 (basic_x + offset + 50 + i * 9.8, basic_y + self.main_size[1] - 3 + 10), 1)
            if i % 10 == 0:
                self.font.render_to(self.surface,
                                    (basic_x + offset + 55 + i * 9.8, basic_y + self.main_size[1] + 13),
                                    "{}".format(i), fgcolor=BLACK_A, size=16)

        return main_scale, cursor

    def draw(self):
        self.main_scale, self.cursor = self.draw_ruler(self.main_location[0], self.main_location[1], self.cursor_offset)

    def main_get_temp(self, pos: tuple):
        self.temp_x = pos[0] - self.main_location[0]
        self.temp_y = pos[1] - self.main_location[1]

    def cursor_get_temp(self, pos: tuple):
        self.temp_x = pos[0] - self.cursor_offset

    def main_move(self, pos: tuple):
        self.main_location[0] = pos[0] - self.temp_x
        self.main_location[1] = pos[1] - self.temp_y
        self.draw()

    def cursor_move(self, pos: tuple):
        self.cursor_offset = pos[0] - self.temp_x
        self.draw()


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
        self.font.render_to(self.surface, [self.loc[0] + 10 + 4 * self.x_offset, self.loc[1] - 90 + 1 * self.y_offset],
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
            with open(r"data\直径.csv", mode="w", newline="", encoding="utf-8") as f:
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

experiment_equipment = Experiment(600, 400)
calipers = Calipers(500, 150)
data = Data()

while is_running:  # 主程序
    time_delta = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                calipers.cursor_offset -= 1
            elif event.key == pygame.K_RIGHT:
                calipers.cursor_offset += 1
        # 鼠标按下
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 主尺
            if event.button == 1 and calipers.main_scale.collidepoint(mouse_pos):
                calipers.main_get_temp(mouse_pos)
                calipers.main_moving = True
            # 游标
            elif event.button == 1 and calipers.cursor.collidepoint(mouse_pos):
                calipers.cursor_get_temp(mouse_pos)
                calipers.cursor_moving = True
        # 鼠标移动
        elif event.type == pygame.MOUSEMOTION:
            # 主尺
            if event.buttons[0] == 1 and calipers.main_moving:
                calipers.main_move(mouse_pos)
            # 游标
            if event.buttons[0] == 1 and calipers.cursor_moving:
                calipers.cursor_move(mouse_pos)
        # 鼠标抬起
        elif event.type == pygame.MOUSEBUTTONUP:
            # 主尺
            if event.button == 1 and calipers.main_moving:
                calipers.main_moving = False
            # 游标
            elif event.button == 1 and calipers.cursor_moving:
                calipers.cursor_moving = False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == calipers.reset:
                    calipers.main_location = [500, 150]
                    calipers.cursor_offset = 50
                elif event.ui_element == next_:
                    if data.save():
                        is_running = False
                        # subprocess.Popen('实验调控菜单.exe')
                        # subprocess.Popen(r".\venv\Scripts\python 实验调控菜单.py")
                        os.system(r"start .\venv\Scripts\python 实验调控菜单.py")
                        # os.popen(r"实验调控菜单.exe")
                elif event.ui_element == initial.OK_button:
                    initial.son_window.hide()
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if len(event.text) != 5:
                    initial = Initial(manager=ui_manager2, surface=message_surface)
        ui_manager.process_events(event)
        ui_manager2.process_events(event)

    window_surface.fill(BLACK_A)
    experiment_equipment_surface.fill((0, 0, 0, 0))
    data_process_surface.fill((0, 0, 0, 0))
    message_surface.fill((0, 0, 0, 0))

    experiment_equipment.draw()
    calipers.draw()
    data.draw()

    ui_manager.update(time_delta)
    ui_manager2.update(time_delta)

    window_surface.blit(experiment_equipment_surface, (0, 0))
    window_surface.blit(background_pic, (0, 0))
    ui_manager.draw_ui(window_surface)
    ui_manager2.draw_ui(message_surface)
    window_surface.blit(data_process_surface, (0, 0))
    window_surface.blit(message_surface, (0, 0))
    pygame.display.update()
