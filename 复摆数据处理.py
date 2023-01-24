import os
import subprocess

import pygame as p
import sys
import pygame_gui as pg
import numpy as np
from math import *
import matplotlib.pyplot as plt
import pandas as pd

p.display.set_caption("复摆")  # 设置窗口标题

with open(r'./data/复摆摆长.csv', 'r', encoding='utf-8') as f:
    temp = f.read()
r = eval('[' + temp + ']')
# r = pd.read_excel('data\\轴心距.xlsx')['轴心距'].to_list() #  r
T = pd.read_excel('data\\复摆导出的周期.xlsx')['周期'].to_list()  # Y数据 #  T

r2 = [i ** 2 for i in r]
T2r = [r[i] * T[i] ** 2 for i in range(len(r))]

plt.figure(figsize=(7, 5))
z1 = np.polyfit(r2, T2r, 1)  # 一次多项式拟合，相当于线性拟合
p1 = np.poly1d(z1)
print(p1)
theta = 5 / 180 * pi

g = (pi ** 2) * (16 + theta ** 2) / 4 / z1[1]  # 重力加速度
R = np.corrcoef(r2, T2r)  # 回转半径    #######################################
R = R[0][1]  #######################################
x = np.linspace(r2[0], r2[-1], 20)
y = z1[0] * x + z1[1]
plt.plot(x, y, 'r', label='Y = Ax+AB')
plt.scatter(r2, T2r)
plt.legend()
plt.savefig('data\\数据处理.png')
plt.close()
PicBg = p.image.load('data\\数据处理.png')

p.init()
clock = p.time.Clock()
Width, Height = 1280, 720
Screen = p.display.set_mode((Width, Height), p.RESIZABLE)
Manager = pg.UIManager((Width, Height), r'./ui_themes/json/data_processing.json')
font = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 20)
bg = p.image.load('dependent_files\\pic\\FubaiShujuBg.png')
A = z1[1]  #######################################
B = z1[0]  #######################################
# g = pi**2/A * (16+5/180*pi)/4
Kc = np.sqrt(A / B)  #######################################

# 主页按钮
enterbutton = pg.elements.UIButton(p.Rect(1106, 633, 101, 67),
                                   text='',
                                   manager=Manager,
                                   object_id='next')


def Init():
    Screen.blit(bg, (0, 0))
    Screen.blit(PicBg, (100, 135))
    Screen.blit(font.render('{:.3f}'.format(A), True, (255, 255, 255), None), (1076, 223))
    Screen.blit(font.render('{:.3f}'.format(B), True, (255, 255, 255), None), (977, 304))
    Screen.blit(font.render('{:.3f}'.format(R ** 2), True, (255, 255, 255), None), (926, 361))
    Screen.blit(font.render('{:.3f}'.format(g), True, (255, 255, 255), None), (1076, 429))
    Screen.blit(font.render('{:.3f}'.format(Kc), True, (255, 255, 255), None), (995, 505))

    Manager.draw_ui(Screen)


def Event():
    for i in p.event.get():
        if i.type == p.QUIT:
            sys.exit()
        elif i.type == p.USEREVENT:
            pass
        elif i.type == p.MOUSEBUTTONDOWN:
            print(p.mouse.get_pos())
            if 1126 <= p.mouse.get_pos()[0] <= 1126 + 40 and 647 <= p.mouse.get_pos()[1] < 647 + 40:
                # subprocess.Popen('主页UI.exe')
                # subprocess.Popen(r".\venv\Scripts\python 主页UI.py")
                os.system(r"start .\venv\Scripts\python 主页UI.py")
                # os.popen(r"主页UI.exe")
                sys.exit()
        Manager.process_events(i)


def Update():
    global Width, Height
    Width, Height = p.display.get_window_size()
    Manager.update(clock.tick(60) / 1000.)
    clock.tick(60)
    p.display.update()
    Screen.fill((255, 255, 255))


while True:
    Init()
    Event()
    Update()
