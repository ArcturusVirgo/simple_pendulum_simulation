import csv
import os
import subprocess
import time as t
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pygame as p
import pygame_gui as pg
from numpy import *
import sys

p.init()
clock = p.time.Clock()
Width, Height = 1280, 720
Screen = p.display.set_mode((Width, Height), p.RESIZABLE)
Manager = pg.UIManager((Width, Height), r"./ui_themes/json/TextTime.json")
p.display.set_caption("复摆")  # 设置窗口标题

g = 9.8
l = 1
theta0 = 5 / 180 * pi

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

bg = p.image.load('dependent_files/pic/FuBaiBG .png')

font = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 24)
font2 = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 16)
font3 = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 12)
# 输入参数
angle0 = 0
cycle0 = 0
diamater0 = 0
lingth0 = 0
damping = 0



with open(r'./data/复摆摆长.csv', 'r', encoding='utf-8') as f:
    temp = f.read()
RotatingDistance = eval('[' + temp + ']')

# 周期输入框
# TextTime1 = pg.elements.UITextEntryLine(p.Rect(83,335,50-2,40),Manager, None, None, 'TextTime', None)
# TextTime1.font = font3
# TextTime2 = pg.elements.UITextEntryLine(p.Rect(83+50-3,335,50-2,40),Manager, None, None, 'TextTime', None)
# TextTime2.font = font3
# TextTime3 = pg.elements.UITextEntryLine(p.Rect(83+100-6,335,50-2-2,40),Manager, None, None, 'TextTime', None)
# TextTime4 = pg.elements.UITextEntryLine(p.Rect(83+150-9,335,50-2-2,40),Manager, None, None, 'TextTime', None)
# TextTime5 = pg.elements.UITextEntryLine(p.Rect(83+200-12,335,50-2-2,40),Manager, None, None, 'TextTime', None)
# TextTime6 = pg.elements.UITextEntryLine(p.Rect(83,474,50-2,40),Manager, None, None, 'TextTime', None)
# TextTime7 = pg.elements.UITextEntryLine(p.Rect(83+47,474,50-2,40),Manager, None, None, 'TextTime', None)
# TextTime8 = pg.elements.UITextEntryLine(p.Rect(83+100-6,474,50-4,40),Manager, None, None, 'TextTime', None)
# TextTime9 = pg.elements.UITextEntryLine(p.Rect(83+150-9,474,50-4,40),Manager, None, None, 'TextTime', None)
# TextTime10 = pg.elements.UITextEntryLine(p.Rect(83+200-12,474,50-4,40),Manager, None, None, 'TextTime', None)
# TextTime3.font = font3
# TextTime4.font = font3
# TextTime5.font = font3
# TextTime6.font = font3
# TextTime7.font = font3
# TextTime8.font = font3
# TextTime9.font = font3
# TextTime10.font = font3

T1 = pg.elements.UIButton(p.Rect(85 + 0 * 47, 325 + 0, 40, 50), '{:.2f}'.format(RotatingDistance[0]), Manager)
T2 = pg.elements.UIButton(p.Rect(85 + 1 * 47, 325 + 0, 40, 50), '{:.2f}'.format(RotatingDistance[1]), Manager)
T3 = pg.elements.UIButton(p.Rect(85 + 2 * 47, 325 + 0, 40, 50), '{:.2f}'.format(RotatingDistance[2]), Manager)
T4 = pg.elements.UIButton(p.Rect(85 + 3 * 47, 325 + 0, 40, 50), '{:.2f}'.format(RotatingDistance[3]), Manager)
T5 = pg.elements.UIButton(p.Rect(85 + 4 * 47, 325 + 0, 40, 50), '{:.2f}'.format(RotatingDistance[4]), Manager)
T6 = pg.elements.UIButton(p.Rect(85 + 0 * 47, 325 + 140, 40, 50), '{:.2f}'.format(RotatingDistance[5]), Manager)
T7 = pg.elements.UIButton(p.Rect(85 + 1 * 47, 325 + 140, 40, 50), '{:.2f}'.format(RotatingDistance[6]), Manager)
T8 = pg.elements.UIButton(p.Rect(85 + 2 * 47, 325 + 140, 40, 50), '{:.2f}'.format(RotatingDistance[7]), Manager)
T9 = pg.elements.UIButton(p.Rect(85 + 3 * 47, 325 + 140, 40, 50), '{:.2f}'.format(RotatingDistance[8]), Manager)
T10 = pg.elements.UIButton(p.Rect(85 + 4 * 47, 325 + 140, 40, 50), '{:.2f}'.format(RotatingDistance[9]), Manager)

cal = pg.elements.UIButton(p.Rect(1116, 633, 101, 67),
                             text="",
                             manager=Manager,
                             object_id="cal")

# new = pg.elements.UIButton(p.Rect(450, 450, 50, 30), '', Manager)

num = 0

# 输入量
Theta0Entry = pg.elements.UITextEntryLine(p.Rect(468, 87, 50, 0), Manager)
CycleEntry = pg.elements.UITextEntryLine(p.Rect(468, 118, 50, 0), Manager)
DistanceEntry = pg.elements.UITextEntryLine(p.Rect(468, 118 + 35, 50, 0), Manager)
Distance = 110
FirstEntry = pg.elements.UITextEntryLine(p.Rect(448, 362, 50, 0), Manager)
SecondEntry = pg.elements.UITextEntryLine(p.Rect(448, 394, 50, 0), Manager)
ThirdEntry = pg.elements.UITextEntryLine(p.Rect(448, 423, 50, 0), Manager)
AveageEntry = pg.elements.UITextEntryLine(p.Rect(448, 456, 50, 0), Manager)
# LengthBox = pg.elements.UIButton(p.Rect(468,118+62,50,31),'{:.2}'.format(np.average(length)),Manager)
# DampingEntry =  pg.elements.UITextEntryLine(p.Rect(468,118+93,50,0),Manager)
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
InImg = p.image.load('dependent_files\\pic\\FuBaiInput .png')
InImg2 = p.image.load('dependent_files\\pic\\FuBaiInput2.png')

# 状态量
RunState = -1  # 正数运行
ReStartState = False

'''
计算过程
'''
g = 9.8
h = 0.001  # 步长
I = 1  # 转动惯量
theta_0 = 5 / 180 * pi  # 初始角度
omiga_0 = 0  # 初始角速度
m = 1  # 质量
r = 0.5  # 转轴质心距离
k = m * g * r / I
O = []  # 角速度
T = []  # 角度
shijian = []


def Clear():
    global g, h, I, theta_0, omiga_0, m, r, O, T, shijian, k
    g = 9.8
    h = 0.001  # 步长
    I = 1  # 转动惯量
    theta_0 = 5 / 180 * pi  # 初始角度
    omiga_0 = 0  # 初始角速度
    m = 1  # 质量
    r = 0.5  # 转轴质心距离
#    k = m * g * r / I
    O = []  # 角速度
    T = []  # 角度
    shijian = []

####################################################################################################
def Longgekuta(t, Theta, Omiga):
    global k,r
    k = m * g * r / I
    def K11(t, Theta, Omiga):
        return Omiga

    def K12(t, Theta, Omiga):
        return Omiga + h / 2 * K21(t, Theta, Omiga)

    def K13(t, Theta, Omiga):
        return Omiga + h / 2 * K22(t, Theta, Omiga)

    def K14(t, Theta, Omiga):
        return Omiga + h * K23(t, Theta, Omiga)

    def K21(t, Theta, Omiga):
        return -k * sin(Theta)

    def K22(t, Theta, Omiga):
        return -k * sin(Theta + h / 2 * K11(t, Theta, Omiga))

    def K23(t, Theta, Omiga):
        return -k * sin(Theta + h / 2 * K12(t, Theta, Omiga))

    def K24(t, Theta, Omiga):
        return -k * sin(Theta + h * K13(t, Theta, Omiga))

    Theta_ = Theta + h / 6 * (
                K11(t, Theta, Omiga) + 2 * K12(t, Theta, Omiga) + 2 * K13(t, Theta, Omiga) + K14(t, Theta, Omiga))
    Omiga_ = Omiga + h / 6 * (
                K21(t, Theta, Omiga) + 2 * K22(t, Theta, Omiga) + 2 * K23(t, Theta, Omiga) + K24(t, Theta, Omiga))
    return [Omiga_, Theta_]

####################################################################################################
def Calculation():
    global theta_0, omiga_0,shijian,K,O,T,k,r,I
    I = I + r**2
    k = m * g * r / I

    for i in range(1, 100000):
        K = Longgekuta(t=i * h, Theta=theta_0, Omiga=omiga_0)
        omiga_0, theta_0 = K[0], K[1]
        O.append(omiga_0)
        T.append(theta_0)
        shijian.append(round(i * h, 2))


CalculationState = True
CalcuStartTime = 0
Measure = []


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
        # self.color = (248,90,64)
        self.color = (255, 204, 153)


ball = Ball()

####################################################################################################
def DrawPic(index):
    if index <= 4000:
        plt.clf()
        plt.figure(figsize=(3.9, 1.84))
        plt.grid()
        plt.plot(shijian[0:index:60], T[0:index:60])
        plt.title('t - θ')
        plt.savefig('cache\\fupic1.png')
        plt.close()
        pic1 = p.image.load('cache\\fupic1.png')
        Screen.blit(pic1, (814, 71))
        plt.figure(figsize=(3.9, 1.84))
        plt.grid()
        plt.plot(T[0:index:60], O[0:index:60], 'r')
        plt.title('θ - w')
        plt.savefig('cache\\fupic2.png')
        plt.close()
        pic2 = p.image.load('cache\\fupic2.png')
        Screen.blit(pic2, (814, 255))
        plt.figure(figsize=(3.9, 1.84))
        plt.grid()
        plt.scatter(shijian[0:index:60], O[0:index:60])
        plt.title('t - w')
        plt.savefig('cache\\fupic3.png')
        plt.close()
        pic3 = p.image.load('cache\\fupic3.png')
        Screen.blit(pic3, (814, 440))
        plt.close('all')
        plt.close('all')
    else:
        pic1 = p.image.load('cache\\fupic1.png')
        Screen.blit(pic1, (814, 71))
        pic2 = p.image.load('cache\\fupic2.png')
        Screen.blit(pic2, (814, 255))
        pic3 = p.image.load('cache\\fupic3.png')
        Screen.blit(pic3, (814, 440))


def DealDraw(pos2, theta):
    length = 200
    pos1 = [640, pos2[1] - Distance * np.cos(theta)]  # 转轴
    # if pos1[0] == pos2[0]:
    #     x = np.linspace(640, ball.pos[0], 10)
    #     y = np.linspace(163, ball.pos[1] + length - 50, 10)
    #     return x,y
    # else:
    s = [pos1[0] - (110 - Distance) * np.sin(theta), pos1[1] - (110 - Distance) * np.cos(theta)]
    x = np.linspace(s[0], s[0] + 150 * np.sin(theta), 10)
    y = np.linspace(s[1], s[1] + 150 * np.cos(theta), 10)
    return x, y


def DrawPendulum():
    global CalculationState, CalcuStartTime
    length = 200
    b = ball.pos[1] + length - 90
    center = [640, 163]
    Rotating = b - Distance
    if RunState == 1:
        if CalculationState:
            Calculation()
            CalculationState = False
            CalcuStartTime = t.perf_counter()
        ti = round((t.perf_counter() - CalcuStartTime), 1)
        if ti in shijian:
            index = shijian.index(ti)
            theta = T[index]
            DrawPic(index)
        else:
            theta = 0
        # p.draw.circle(Screen, ball.color, (center[0] + (length-50) * np.sin(theta), center[1] +( length-50) * np.cos(theta)), 60)
        # x = np.linspace(center[0], ball.pos[0]+ (length-50) * np.sin(theta), 10)
        # y = np.linspace(center[1], ball.pos[1] + (length-50) * np.cos(theta), 10)
        x, y = DealDraw([center[0] + (length - 90) * np.sin(theta), center[1] + (length - 90) * np.cos(theta)], theta)
        p.draw.line(Screen, ball.color, (x[0], y[0]),
                    (center[0] + (length) * np.sin(theta), center[1] + (length) * np.cos(theta)), 10)
        p.draw.circle(Screen, (255, 255, 255),
                      [center[0] + length // 2 * sin(theta), center[1] + length // 2 * np.cos(theta)], 5)
        # for i in range(len(x)): p.draw.circle(Screen, (255, 204,153+i*5), (x[i], y[i]), 20+i*5) 质心 p.draw.circle(
        # Screen, (255, 255, 255), (s[0] + (length-90) * np.sin(theta), s[1] +( length-90) * np.cos(theta)), 5)

    else:
        # p.draw.line(Screen,(255, 204,153),center,(ball.pos[0],ball.pos[1]+length),10)
        # p.draw.circle(Screen, ball.color, (ball.pos[0], ball.pos[1]+length-50), 80)
        # x = np.linspace(center[0], ball.pos[0], 10)
        # y = np.linspace(center[1], ball.pos[1] + length-50, 10)
        # for i in range(len(x)):
        #     p.draw.circle(Screen, (255, 204, 153 + i * 5), (x[i], y[i]), 20 + i * 5)
        p.draw.line(Screen, ball.color, center, (center[0], center[1] + (length)), 10)
        p.draw.circle(Screen, (255, 255, 255), (ball.pos[0], ball.pos[1] + length // 2), 5)
    x = np.linspace(center[0] - 100, center[0] + 100, 52)
    for i in range(0, len(x), 4):
        p.draw.line(Screen, (244, 137, 36), (x[i], Rotating), (x[i + 1], Rotating), 3)
    p.draw.circle(Screen, (255, 255, 255), (center[0], Rotating), 5)


def Init():
    Screen.blit(bg, (0, 0))
    DrawLines(1)
    DrawLines(2)
    Screen.blit(InImg, (342, 70))
    Screen.blit(InImg2, (342, 360))
    Screen.blit(TimeImage, (354, 484))
    if RunState == 1:
        Screen.blit(font.render('开始', True, (177, 82, 204), None), (146, 172))
    else:
        Screen.blit(font.render('开始', True, (255, 255, 255), None), (146, 172))
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


def ReStart():
    global num, StartTime, ShowTime, TouchTime, OutTime, StopTime, PicTime, TimeImage,\
        TimeImgPos, RunState, CalculationState, CalcuStartTime, Measure, CycleList, index, \
        shijian, T, O, K,ZeroTimeState
    ZeroTimeState=False
    # num = 0
    Clear()
    StartTime = 0
    ShowTime = 0
    TouchTime = -1
    StopTime = 0
    OutTime = []
    PicTime = 0
    TimeImage = p.image.load('dependent_files\\pic\\time.png')
    TimeImgPos = [371, 533]
    # 状态量
    RunState = -1  # 正数运行
    CalculationState = True
    # CalculationState = True
    CalcuStartTime = 0
    # Measure = []
    # CycleList = []
    index = 0
    g = 9.8
    h = 0.001  # 步长
    I = 1  # 转动惯量
    theta_0 = 5 / 180 * pi  # 初始角度
    omiga_0 = 0  # 初始角速度
    m = 1  # 质量
    r = 2  # 转轴质心距离
    # k = m * g * r / I
    O = []  # 角速度
    T = []  # 角度
    shijian = []


def Event():
    global RunState, TouchTime, StartTime, StopTime, theta0, PicTime, Distance, theta_0, r, CalculationState, ZeroTimeState
    for i in p.event.get():
        if i.type == p.QUIT:
            sys.exit()
        elif i.type == p.MOUSEBUTTONDOWN:
            print(p.mouse.get_pos())
            if 146 <= p.mouse.get_pos()[0] <= 146 + 50 and 167 <= p.mouse.get_pos()[1] <= 167 + 50:
                RunState = -RunState
                PicTime = t.perf_counter()

            elif 123 < p.mouse.get_pos()[0] <= 123 + 80 and 231 < p.mouse.get_pos()[1] < 231 + 30:
                ReStart()
            elif 355<= p.mouse.get_pos()[0] < 355 + 40 and 483 <p.mouse.get_pos()[1]<= 483 + 40:
                ZeroTimeState = True
            elif TouchTimePos[0] <= p.mouse.get_pos()[0] <= TouchTimePos[0] + 40 and TouchTimePos[1] <= \
                    p.mouse.get_pos()[1] <= TouchTimePos[1] + 40:
                TouchTime = -TouchTime
                ZeroTimeState = False
                mp3.play()
                if TouchTime == 1:
                    StartTime = t.perf_counter()
                elif TouchTime == -1:
                    StopTime = t.perf_counter()
                    if len(OutTime) < OutTimeMaxLength:
                        OutTime.append(ShowTime)
        elif i.type == p.USEREVENT:
            if i.user_type == pg.UI_TEXT_ENTRY_FINISHED:
                if i.ui_element == Theta0Entry:
                    theta0 = float(Theta0Entry.text) / 180 * pi
                    theta_0 = theta0
                elif i.ui_element == DistanceEntry:
                    temp = float(DistanceEntry.text)
                    Distance = temp / 50 * 110
                    r = temp / 100               #######################################
                elif i.ui_element == FirstEntry and FirstEntry.text != '':
                    Measure.append(float(FirstEntry.text))
                elif i.ui_element == SecondEntry and SecondEntry.text != '':
                    Measure.append(float(SecondEntry.text))
                elif i.ui_element == ThirdEntry and ThirdEntry.text != '':
                    Measure.append(float(ThirdEntry.text))
            if i.user_type == pg.UI_BUTTON_PRESSED:
                if i.ui_element == cal:
                    # subprocess.Popen("复摆数据处理.exe")
                    # subprocess.Popen(r".\venv\Scripts\python 复摆数据处理.py")
                    os.system(r"start .\venv\Scripts\python 复摆数据处理.py")
                    # os.popen(r"复摆数据处理.exe")
                    sys.exit()
        Manager.process_events(i)


def Update():
    global Width, Height, ShowTime, Measure, num
    Width, Height = p.display.get_window_size()
    Manager.update(clock.tick(60) / 1000.)
    clock.tick(400)
    p.display.update()
    Screen.fill((255, 255, 255))
    if TouchTime == 1:
        ShowTime = t.perf_counter() - StartTime
    elif TouchTime == -1:
        ShowTime = StopTime - StartTime
    if len(CycleList) == 10:
        df = pd.DataFrame(data=CycleList, columns=['avgtime'])
        df.to_excel('data\\复摆周期.xlsx')
    if len(Measure) == 3:
        new = pg.elements.UIButton(p.Rect(450, 450, 50, 30), '{:.2f}'.format(average(Measure) / float(CycleEntry.text)),
                                   Manager, object_id='new')
        # new.set_text('{:.2f}'.format(average(Measure) / float(CycleEntry.text)))
        # Manager.update(0.1)
        if num == 0:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out1 = pg.elements.UIButton(p.Rect(85 + 0 * 47, 325 + 60, 40, 50), '{:.2f}'.format(average(Measure) / float(CycleEntry.text)),
                                        Manager)
            Measure = []
            num += 1
        elif num == 1:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out2 = pg.elements.UIButton(p.Rect(85 + 1 * 47, 325 + 60, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 2:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out3 = pg.elements.UIButton(p.Rect(85 + 2 * 47, 325 + 60, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 3:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out4 = pg.elements.UIButton(p.Rect(85 + 3 * 47, 325 + 60, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 4:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out5 = pg.elements.UIButton(p.Rect(85 + 4 * 47, 325 + 60, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 5:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out6 = pg.elements.UIButton(p.Rect(85 + 0 * 47, 325 + 200, 40, 50), '{:.2f}'.format(average(Measure) / float(CycleEntry.text)),
                                        Manager)
            Measure = []
            num += 1
        elif num == 6:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out7 = pg.elements.UIButton(p.Rect(85 + 1 * 47, 325 + 200, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 7:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out8 = pg.elements.UIButton(p.Rect(85 + 2 * 47, 325 + 200, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 8:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out9 = pg.elements.UIButton(p.Rect(85 + 3 * 47, 325 + 200, 40, 50),
                                        '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        elif num == 9:
            CycleList.append(average(Measure) / float(CycleEntry.text))
            out10 = pg.elements.UIButton(p.Rect(85 + 4 * 47, 325 + 200, 40, 50),
                                         '{:.2f}'.format(average(Measure) / float(CycleEntry.text)), Manager)
            Measure = []
            num += 1
        FirstEntry.text = ''
        SecondEntry.text = ''
        ThirdEntry.text = ''
        del new
    if len(CycleList) == 10:
        df = pd.DataFrame(data=CycleList, columns=['周期'])
        df.to_excel('data\\复摆导出的周期.xlsx')



while True:
    Init()
    Event()
    Update()
