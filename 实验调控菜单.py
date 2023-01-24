import csv
import time as t

import matplotlib.pyplot as plt
import pandas as pd
import pygame as p
import pygame_gui as pg
import pygame_gui
from numpy import *
import numpy as np
import os
import sys

p.init()
clock = p.time.Clock()
Width, Height = 1280, 720
WINDOW_SIZE = (Width, Height)
Screen = p.display.set_mode((Width, Height))
Manager = pg.UIManager((Width, Height), r"./ui_themes/json/TextTime.json")
p.display.set_caption("单摆")  # 设置窗口标题

g = 9.8
l = 1
theta0 = 5 / 180 * pi

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

bg = p.image.load('dependent_files/pic/DanbaiBG.png')
font = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 24)
font2 = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 16)
font3 = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 12)
# 输入参数
angle0 = 0
cycle0 = 0
diamater0 = 0
lingth0 = 0
damping = 0
length = 420

data = []
with open(r"./data/摆长.csv", mode="r", encoding="utf-8") as f:
    lines = csv.reader(f)
    for line in lines:
        data.append(line)
length = pd.Series(data[0], name="摆长", dtype="float64")
length = length.to_list()

data = []
with open(r"./data/直径.csv", mode="r", encoding="utf-8") as f:
    lines = csv.reader(f)
    for line in lines:
        data.append(line)
ReadDiameter = pd.Series(data[0], name="直径", dtype="float64")
ReadDiameter = ReadDiameter.to_list()
MaxMovex = sin(5 / 180 * pi) * 420
MaxMovey = (1 - cos(5 / 180)) * 420

cal = pg.elements.UIButton(p.Rect(1106, 633, 101, 67),
                           text="",
                           manager=Manager,
                           object_id="cal")

# 周期输入框
TextTime1 = pg.elements.UITextEntryLine(p.Rect(83, 324, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime1.font = font3
TextTime2 = pg.elements.UITextEntryLine(p.Rect(83 + 50 - 3, 324, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime2.font = font3
TextTime3 = pg.elements.UITextEntryLine(p.Rect(83 + 100 - 6, 324, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime4 = pg.elements.UITextEntryLine(p.Rect(83 + 150 - 9, 324, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime5 = pg.elements.UITextEntryLine(p.Rect(83 + 200 - 13, 324, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime6 = pg.elements.UITextEntryLine(p.Rect(83, 441, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime7 = pg.elements.UITextEntryLine(p.Rect(83 + 47, 441, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime8 = pg.elements.UITextEntryLine(p.Rect(83 + 100 - 6, 441, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime9 = pg.elements.UITextEntryLine(p.Rect(83 + 150 - 9, 441, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime10 = pg.elements.UITextEntryLine(p.Rect(83 + 200 - 13, 441, 50 - 2, 40), Manager, None, None, 'TextTime', None)
TextTime3.font = font3
TextTime4.font = font3
TextTime5.font = font3
TextTime6.font = font3
TextTime7.font = font3
TextTime8.font = font3
TextTime9.font = font3
TextTime10.font = font3

# 输入量
Theta0Entry = pg.elements.UITextEntryLine(p.Rect(468, 87, 50, 0), Manager)
CycleEntry = pg.elements.UITextEntryLine(p.Rect(468, 118, 50, 0), Manager)
DiameterBox = pg.elements.UIButton(p.Rect(468, 118 + 31, 50, 31), '{:.2f}'.format(np.average(ReadDiameter)), Manager,
                                   object_id='button', )
LengthBox = pg.elements.UIButton(p.Rect(468, 118 + 62, 50, 31), '{:.4f}'.format(np.average(length)/100), Manager,
                                 object_id='button', )
DampingEntry = pg.elements.UITextEntryLine(p.Rect(468, 118 + 93, 50, 0), Manager)
CycleList = []

# 按钮
# StartButton = pg.elements.UIButton(p.Rect(140,150,60,50),'Start',Manager)
# StartButton.font = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF',40)
# ReStartButton = pg.elements.UIButton(p.Rect(120,220,110,50),'ReStart',Manager)
# 时间
StartTime = 0
ShowTime = 0
TouchTime = -1
StopTime = 0
OutTime = []
PicTime = 0
TimeImage = p.image.load('dependent_files\\pic\\time.png')
TimeImgPos = [371, 533 + 3]
ZeroTimeState  = False

# 位置
TouchTimePos = [419, 484]
StartPos = []
OutTimeMaxLength = 10

mp3 = p.mixer.Sound('dependent_files\\Sound\\di.mp3')
InImg = p.image.load('dependent_files\\pic\\input .png')

# 状态量
RunState = -1  # 正数运行
ReStartState = False
OutPutState = True

message_surface = p.Surface(WINDOW_SIZE, p.SRCALPHA, 32)
message_surface = message_surface.convert_alpha()
ui_manager2 = pygame_gui.UIManager(WINDOW_SIZE, r'./ui_themes/json/message.json')


class Initial:
    def __init__(self, manager, surface):
        self.manager = manager
        self.surface = surface

        self.son_window = pygame_gui.elements.ui_window.UIWindow(
            rect=p.Rect(((WINDOW_SIZE[0] - 500) / 2, (WINDOW_SIZE[1] - 300) / 2, 400, 200)),
            window_display_title="提示",
            manager=self.manager,
            object_id='window')

        self.text = pygame_gui.elements.UILabel(
            relative_rect=p.Rect(100, 20, 200, 50),
            text="有效数字位数不对！",
            manager=self.manager,
            container=self.son_window,
            object_id='message')

        self.OK_button = pygame_gui.elements.UIButton(
            relative_rect=p.Rect((150, 80, 100, 30)),
            text="确认",
            manager=self.manager,
            container=self.son_window,
            object_id='button')


def DrawLines(num):
    if num == 1:
        n = 20
        x = np.linspace(345, 811, n)
        for i in range(n):
            p.draw.line(Screen, (155, 155, 155), (x[i], 72), (x[i], 621))
    else:
        n = 25
        y = np.linspace(72, 621, n)
        for i in range(n):
            p.draw.line(Screen, (155, 155, 155), (345, y[i]), (811, y[i]))


class Ball():
    def __init__(self):
        self.pos = [640, 163]
        self.color = (248, 90, 64)


ball = Ball()


def OutPutPic():
    time = linspace(0, 3, 31)
    for i in time:
        # i = round(i,2)
        # print(i)
        ti = np.linspace(0, i, 40)
        w2 = damping ** 2 - (g / l)
        # ti = t.perf_counter() - PicTime
        if w2 < 0:
            num = pow(w2, 0.5)
            # a = round(np.real(num) - damping,4)
            b = np.imag(num)
            theta = theta0 * np.cos(b * ti) * np.e ** (
                    -damping * ti)
        else:
            a = np.sqrt(w2)
            c1 = (-damping + a) / 2 / a * theta0
            c2 = (damping + a) / 2 / a * theta0
            theta = c1 * e ** ((-damping - a) * ti) + c2 * e ** ((-damping + a) * ti)
        # theta = theta0 * np.cos(np.sqrt(g / l) * ti) * np.e ** (-damping * ti)
        w = -theta0 * np.sqrt(g / l) * np.sin(np.sqrt(g / l) * ti) * np.e ** (
                -damping * ti) - damping * theta0 * np.cos(
            np.sqrt(g / l) * ti) * np.e ** (-damping * ti)
        plt.figure(figsize=(3.9, 1.84))
        plt.grid()
        plt.ylim([-0.2,0.2])
        plt.plot(ti, theta)
        plt.title('θ - t')
        plt.savefig('cache\\1pic{:.2}.png'.format(i))
        plt.close()
        plt.figure(figsize=(3.9, 1.84))
        plt.grid()
        plt.ylim([-0.3, 0.3])
        plt.plot(theta, w, 'r')
        plt.title('θ - w')
        plt.savefig('cache\\2pic{:.2}.png'.format(i))
        plt.close()
        plt.figure(figsize=(3.9, 1.84))
        plt.grid()
        plt.ylim([-0.3, 0.3])
        plt.plot(ti, w, 'y')
        plt.title('w - t')
        plt.savefig('cache\\3pic{:.2}.png'.format(i))
        plt.close()


def Restart():
    global RunState, StartTime, ShowTime, TouchTime, StopTime, OutTime, PicTime, \
        angle0, cycle0, diamater0, lingth0, damping, length, CycleList, TouchTimePos, OutTimeMaxLength, \
        g, l, theta0, RunState,ReStartState,OutPutState
    g = 9.8
    l = 1
    theta0 = 5 / 180 * pi
    RunState = -1
    StartTime = 0
    ShowTime = 0
    TouchTime = -1
    StopTime = 0
    OutTime = []
    angle0 = 0
    cycle0 = 0
    diamater0 = 0
    lingth0 = 0
    damping = 0
    length = 420
    CycleList = []
    TouchTimePos = [419, 484]
    StartPos = []
    OutTimeMaxLength = 10
    OutPutState = True


def DrawPic():
    if t.perf_counter() - PicTime <= 3:
        ti = round(t.perf_counter() - PicTime, 1)
        # print('cache\\1pic{}.png'.format(ti))
        pic1 = p.image.load('cache\\1pic{}.png'.format(ti))
        Screen.blit(pic1, (814, 71))
        pic2 = p.image.load('cache\\2pic{}.png'.format(ti))
        Screen.blit(pic2, (814, 255))
        pic3 = p.image.load('cache\\3pic{}.png'.format(ti))
        Screen.blit(pic3, (814, 440))
    else:
        ti = np.linspace(0, 4.1, 40)
        pic1 = p.image.load('cache\\1pic3.0.png')
        Screen.blit(pic1, (814, 71))
        pic2 = p.image.load('cache\\2pic3.0.png')
        Screen.blit(pic2, (814, 255))
        pic3 = p.image.load('cache\\3pic3.0.png')
        Screen.blit(pic3, (814, 440))


def DrawPendulum():
    global OutPutState, PicTime
    center = [640, 163]
    length = 420
    if RunState == 1:
        if OutPutState:
            OutPutPic()
            OutPutState = False
            PicTime = t.perf_counter()
        w2 = damping**2 - (g / l)
        temptime = t.perf_counter() - PicTime
        if w2 < 0:
            num = pow(w2,0.5)
            # a = round(np.real(num) - damping,4)
            b = np.imag(num)
            theta = theta0 * np.cos(b * temptime) * np.e ** (
                        -damping * temptime)
        else:
            a = np.sqrt(w2)
            c1 = (-damping + a ) / 2 / a*theta0
            c2 = (damping + a) / 2 / a*theta0
            theta = c1 * e **((-damping - a)*temptime)  + c2 * e **((-damping + a)*temptime)
            # theta = c1 * e ** (-g/l*np.imag(np.sqrt(-1/(2*g/l + 1))) * temptime) + c2 * e ** (g/l*np.imag(np.sqrt(-1/(2*g/l + 1))) * temptime)
            # theta = theta0 * np.cos(np.imag(np.sqrt(damping**2 - (g / l))) * t.perf_counter()) * np.e ** (-damping * t.perf_counter())
        # ball.pos = [center[0] + length * np.sin(theta), center[1] + length * np.cos(theta)]
        p.draw.line(Screen, (255, 204, 153), center,
                    (center[0] + length * np.sin(theta), center[1] + length * np.cos(theta)), 3)
        p.draw.circle(Screen, ball.color, (center[0] + length * np.sin(theta), center[1] + length * np.cos(theta)), 10)
        DrawPic()
        Screen.blit(font.render('θ = {:.2f}°'.format(theta * 180 / pi), True, (255, 255, 255), None), (600, 131))
    else:
        if Theta0Entry.text != '':
            theta = float(Theta0Entry.text) / 180 * pi
        else:
            theta = theta0
        # p.draw.line(Screen,(255, 204,153),center,(ball.pos[0],ball.pos[1]+length),3)
        # p.draw.circle(Screen, ball.color, (ball.pos[0], ball.pos[1]+length), 10)
        p.draw.line(Screen, (255, 204, 153), center,
                    (center[0] + length * np.sin(theta), center[1] + length * np.cos(theta)), 3)
        p.draw.circle(Screen, ball.color, (center[0] + length * np.sin(theta), center[1] + length * np.cos(theta)), 10)
        Screen.blit(font.render('θ = {:.2f}°'.format(theta * 180 / pi), True, (255, 255, 255), None), (600, 131))
    p.draw.line(Screen, (244, 137, 36), (center[0] - 80, center[1]), (center[0] + 80, center[1]), 3)
    p.draw.circle(Screen, (255, 255, 255), center, 5)


def Init():
    Screen.blit(bg, (0, 0))
    DrawLines(1)
    DrawLines(2)
    Screen.blit(InImg, (342, 70))
    Screen.blit(TimeImage, (354, 484))
    if RunState == 1:
        Screen.blit(font.render('开始', True, (177, 82, 204), None), (146, 167))
    else:
        Screen.blit(font.render('开始', True, (255, 255, 255), None), (146, 167))
    DrawPendulum()
    if ZeroTimeState:
        Screen.blit(
            font2.render(
                '{}:{}:{}'.format(int(0), int(0 % 60), '{}'.format(round(0, 3))[-2:]),
                True, (0, 0, 0), None), TimeImgPos)
    else:
        Screen.blit(
            font2.render('{}:{}:{}'.format(int(ShowTime // 60), int(ShowTime % 60), '{}'.format(round(ShowTime, 3))[-2:]),
                         True, (0, 0, 0), None), TimeImgPos)
    Manager.draw_ui(Screen)


def Event():
    global RunState, TouchTime, StartTime, StopTime, theta0, PicTime, damping,ZeroTimeState,initial
    length = 420
    for i in p.event.get():
        if i.type == p.QUIT:
            sys.exit()
        elif i.type == p.MOUSEBUTTONDOWN:
            print(p.mouse.get_pos())
            if 146 <= p.mouse.get_pos()[0] <= 146 + 50 and 167 <= p.mouse.get_pos()[1] <= 167 + 50:
                RunState = -RunState
            elif 123 <= p.mouse.get_pos()[0] < 123 + 90 and 211 < p.mouse.get_pos()[1] <= 211 + 50:
                Restart()
            elif 355<= p.mouse.get_pos()[0] < 355 + 40 and 483 <p.mouse.get_pos()[1]<= 483 + 40:
                ZeroTimeState = True
                # print(1)
                # pass
            elif 640 - MaxMovex <= p.mouse.get_pos()[0] <= 640 + MaxMovex and 500 < p.mouse.get_pos()[1] < 600:
                theta0 = arcsin((p.mouse.get_pos()[0] - 640) / 420)
            elif 1135 < p.mouse.get_pos()[0] < 1135 + 50 and 651 < p.mouse.get_pos()[1] <= 651 + 50:
                os.system(r"start .\venv\Scripts\python 数据处理菜单.py")
                # os.popen(r"数据处理菜单.exe")
                exit()
            elif TouchTimePos[0] <= p.mouse.get_pos()[0] <= TouchTimePos[0] + 30 and TouchTimePos[1] <= \
                    p.mouse.get_pos()[1] <= TouchTimePos[1] + 30:
                ZeroTimeState = False
                TouchTime = -TouchTime
                mp3.play()
                if TouchTime == 1:
                    StartTime = t.perf_counter()
                elif TouchTime == -1:
                    StopTime = t.perf_counter()
                    if len(OutTime) < OutTimeMaxLength:
                        OutTime.append(ShowTime)

        elif i.type == p.USEREVENT:
            if i.user_type == pg.UI_TEXT_ENTRY_FINISHED:
                if i.ui_element == TextTime1 and CycleEntry.text != '':
                    AverageTime1 = pg.elements.UIButton(p.Rect(84 + 0 * 47, 370, 45, 60),
                                                        '{:.2f}'.format(float(TextTime1.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                    CycleList.append(float(TextTime1.text) / int(eval(CycleEntry.text)))
                elif i.ui_element == TextTime2 and CycleEntry.text != '':
                    CycleList.append(float(TextTime2.text) / int(eval(CycleEntry.text)))
                    AverageTime2 = pg.elements.UIButton(p.Rect(84 + 1 * 47, 370, 45, 60),
                                                        '{:.2f}'.format(float(TextTime2.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime3 and CycleEntry.text != '':
                    CycleList.append(float(TextTime3.text) / int(eval(CycleEntry.text)))
                    AverageTime3 = pg.elements.UIButton(p.Rect(84 + 2 * 47, 370, 45, 60),
                                                        '{:.2f}'.format(float(TextTime3.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime4 and CycleEntry.text != '':
                    CycleList.append(float(TextTime4.text) / int(eval(CycleEntry.text)))
                    AverageTime4 = pg.elements.UIButton(p.Rect(84 + 3 * 47, 370, 45, 60),
                                                        '{:.2f}'.format(float(TextTime4.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime5 and CycleEntry.text != '':
                    CycleList.append(float(TextTime5.text) / int(eval(CycleEntry.text)))
                    AverageTime5 = pg.elements.UIButton(p.Rect(84 + 4 * 47, 370, 45, 60),
                                                        '{:.2f}'.format(float(TextTime5.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime6 and CycleEntry.text != '':
                    CycleList.append(float(TextTime6.text) / int(eval(CycleEntry.text)))
                    AverageTime6 = pg.elements.UIButton(p.Rect(84 + 0 * 47, 370 + 120, 45, 60),
                                                        '{:.2f}'.format(float(TextTime6.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime7 and CycleEntry.text != '':
                    CycleList.append(float(TextTime7.text) / int(eval(CycleEntry.text)))
                    AverageTime7 = pg.elements.UIButton(p.Rect(84 + 1 * 47, 370 + 120, 45, 60),
                                                        '{:.2f}'.format(float(TextTime7.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime8 and CycleEntry.text != '':
                    CycleList.append(float(TextTime8.text) / int(eval(CycleEntry.text)))
                    AverageTime8 = pg.elements.UIButton(p.Rect(84 + 2 * 47, 370 + 120, 45, 60),
                                                        '{:.2f}'.format(float(TextTime8.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime9 and CycleEntry.text != '':
                    CycleList.append(float(TextTime9.text) / int(eval(CycleEntry.text)))
                    AverageTime9 = pg.elements.UIButton(p.Rect(84 + 3 * 47, 370 + 120, 45, 60),
                                                        '{:.2f}'.format(float(TextTime9.text) / int(eval(CycleEntry.text))),
                                                        Manager, object_id='button')
                elif i.ui_element == TextTime10 and CycleEntry.text != '':
                    CycleList.append(float(TextTime10.text) / int(eval(CycleEntry.text)))
                    AverageTime10 = pg.elements.UIButton(p.Rect(84 + 4 * 47, 370 + 120, 45, 60),
                                                         '{:.2f}'.format(float(TextTime10.text) / int(eval(CycleEntry.text))),
                                                         Manager, object_id='button')
                elif i.ui_element == Theta0Entry:
                    theta0 = float(Theta0Entry.text) / 180 * pi
                elif i.ui_element == DampingEntry:
                    damping = float(DampingEntry.text)


                if i.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if len(i.text) != 5:
                        initial = Initial(manager=ui_manager2, surface=Screen)
            if i.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if i.ui_element == initial.OK_button:
                    initial.son_window.hide()

        Manager.process_events(i)
        ui_manager2.process_events(i)


def Update():
    global Width, Height, ShowTime
    time_delta = clock.tick(60) / 1000
    Manager.update(time_delta)
    message_surface.fill((0, 0, 0, 0))
    ui_manager2.update(time_delta)
    ui_manager2.draw_ui(message_surface)
    Screen.blit(message_surface, (0, 0))
    p.display.update()
    Screen.fill((255, 255, 255))
    if TouchTime == 1:
        ShowTime = t.perf_counter() - StartTime
    elif TouchTime == -1:
        ShowTime = StopTime - StartTime
    if len(CycleList) == 10:
        df = pd.DataFrame(data=CycleList, columns=['avgtime'])
        df.to_excel('data\\周期.xlsx')






while True:
    Init()
    Event()
    Update()
