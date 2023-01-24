import os
import subprocess

import pygame as p
import sys
import pygame_gui as pg
import numpy as np
import pandas as pd

import csv


p.init()
clock = p.time.Clock()
p.display.set_caption("单摆")  # 设置窗口标题
Width, Height = 1280, 720
Screen = p.display.set_mode((Width, Height), p.RESIZABLE)
Manager = pg.UIManager((Width,Height), r'./ui_themes/json/data_processing.json')
font = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 16)
font10 = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF', 13)

CycleFile = pd.read_excel('data\\周期.xlsx')
CycleData = CycleFile['avgtime'].to_list()
CycleData.append(np.average(CycleData))

# 主页按钮
enterbutton = pg.elements.UIButton(p.Rect(1106, 633, 101, 67),
                                         text='',
                                         manager=Manager,
                                         object_id='next')

data = []
with open(r"data\摆长.csv", mode="r", encoding="utf-8") as f:
    lines = csv.reader(f)
    for line in lines:
        data.append(line)
with open(r"data\直径.csv", mode="r", encoding="utf-8") as f:
    lines = csv.reader(f)
    for line in lines:
        data.append(line)

length = pd.Series(data[0], name="摆长", dtype="float64")
diameter = pd.Series(data[1], name="直径", dtype="float64")
diameter = diameter.to_list()
diameter.append(np.average(diameter))
length = length.to_list()
length.append(np.average(length))

def Init():
    Screen.blit(p.image.load('dependent_files/pic/ShujuBG.png'), (0, 0))
    clearance = 0
    for i in CycleData:
        Screen.blit(font.render('{:.2f}'.format(i),True,(255,255,255),None),(143+47*clearance,329))
        clearance+=1
    clearance = 0
    for i in diameter:
        Screen.blit(font10.render('{:.2f}'.format(i * 10), True, (255, 255, 255), None), (140 + 47 * clearance, 276))
        clearance += 1
    clearance = 0
    for i in length:
        Screen.blit(font10.render('{:.4f}'.format(i / 100), True, (255, 255, 255), None), (143 + 47 * clearance -2, 218))
        clearance += 1
    Screen.blit(font.render('{:.4f} m'.format(LengthUncertainty),True,(255,255,255),None),(933,362))
    Screen.blit(font.render('{:.2f} mm'.format(DiameterUncertainty*100),True,(255,255,255),None),(933,431))
    Screen.blit(font.render('{:.2f} s'.format(TimeUncertainty),True,(255,255,255),None),(933,497))
    Screen.blit(font.render('{:.2f}  m/s^2'.format(GUncertainty / 100),True,(255,255,255),None),(933,562))
    # Screen.blit(font.render('{:.2} m/s^2'.format(0.02),True,(255,255,255),None),(933,562))
    # Screen.blit(font.render('{:.3} m/s^2'.format(9.7962),True,(255,255,255),None),(854,631))
    Screen.blit(font.render('{:.2f} m/s^2'.format(g / 100),True,(255,255,255),None),(854,631))
    Screen.blit(font.render("{:.2f} m/s^2".format(GUncertainty / 100),True,(255,255,255),None),(1012,631))
    # Screen.blit(font.render("{:.2} m/s^2".format(0.02),True,(255,255,255),None),(1012,631))


    Manager.draw_ui(Screen)

def DealError(data):
    n = len(data)
    values = 0
    average = np.average(data)
    for i in data:
        values += (i - average)**2
    A = np.sqrt(1/(n-1)/n*values)
    if 90<data[0]<110:#摆长
        B = 0.01/np.sqrt(3)
    elif 0.5<data[0]<1.5:#直径
        B = 0.02e-3/np.sqrt(3)
        values = values
        A = np.sqrt(1 / (n - 1) / n * values)
    else:
        B = 0.01/np.sqrt(3)#时间
    return np.sqrt(A**2+B**2)



def Event():
    for i in p.event.get():
        if i.type == p.QUIT:
            sys.exit()
        elif i.type == p.USEREVENT:
            pass
        elif i.type ==p.MOUSEBUTTONDOWN:
            print(p.mouse.get_pos())
            if 1131<p.mouse.get_pos()[0]<1131+60 and 644<p.mouse.get_pos()[1]<644+50:
                # subprocess.Popen("主页UI.exe")
                os.system(r"start .\venv\Scripts\python 主页UI.py")
                # os.popen(r"主页UI.exe")
                sys.exit()
        Manager.process_events(i)



def Update():
    global Width, Height
    Width, Height = p.display.get_window_size()
    Manager.update(clock.tick(60)/1000.)
    p.display.update()
    Screen.fill((255, 255, 255))

LengthUncertainty  = DealError(length)
DiameterUncertainty = DealError(diameter)
TimeUncertainty = DealError(CycleData)
g = 4*np.pi**2 * (np.average(length)+np.average(diameter)/2)/np.average(CycleData)**2
GUncertainty = g*np.sqrt(
    1/(np.average(length) + np.average(diameter)/2)**2*LengthUncertainty**2 +
    (0.5/(np.average(length) + np.average(diameter)/2))**2*DiameterUncertainty**2+
    (2/np.average(CycleData))**2*TimeUncertainty**2
     )


while True:
    Init()
    Event()
    Update()
