import os
import subprocess
import sys
from math import cos, sin

import matplotlib.pyplot as plt
import numpy as np
import pygame as p
import pygame_gui as pg

# 初始化
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
p.init()
p.display.set_caption('球面摆')
Width, Height = 1280, 720
Screen = p.display.set_mode((Width, Height), p.RESIZABLE)
font = p.font.Font('dependent_files\\Font\\华光标题黑_CNKI.TTF',15)
# 👇--------------------------------------------------------------------------------------------------------------------
# 使用pygamegui主题
Manager = pg.UIManager((Width, Height), r"ui_themes\json\data_processing.json")
# 👆--------------------------------------------------------------------------------------------------------------------
clock = p.time.Clock()
UpTime = clock.tick(60) / 1000.

ProRuning = True

# 依赖文件导入
BgImage = p.image.load('dependent_files\\pic\\QiuMianBG.png')

# UI
TextLength = pg.elements.UITextEntryLine(p.Rect(304, 90.8, 90, 15), Manager)
TextTheta = pg.elements.UITextEntryLine(p.Rect(304, 126, 90, 10), Manager)
TextThetaW = pg.elements.UITextEntryLine(p.Rect(304, 161, 90, 10), Manager)
TextPhi = pg.elements.UITextEntryLine(p.Rect(304, 197, 90, 10), Manager)
TextPhiW = pg.elements.UITextEntryLine(p.Rect(304, 232.8, 90, 10), Manager)
ButtonStart = pg.elements.UIButton(p.Rect(68, 269, 112, 42), 'Start', Manager)
ButtonRestart = pg.elements.UIButton(p.Rect(281, 269, 112, 42), 'Restat', Manager)

PlaySpeed = 50
RunState = 0

# 摆的计算
# 以下所有角速度导数以及初始位置无特别指出取弧度制
v0 = 1.2  # 初始速度，米每秒
l = 0.85  # 摆长，以米做单位
g = 9.8  # 以米做单位
theta0 = 1.57  # theta初始值
theta_v0 = 0  # theta导数初始值
phi0 = 0  # 默认为零
phi_v0 = 0.855  # phi角初始导数
deltat = 0.0001  # 单位步长

v_0 = l * phi_v0
C = v_0 * sin(theta0) / l

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = l * np.outer(np.cos(u), np.sin(v))
y = l * np.outer(np.sin(u), np.sin(v))
z = l * np.outer(np.ones(np.size(u)), np.cos(v))

Theta_shuju = [theta0]
Theta_v_shuju = [theta_v0]
Phi_shuju = [phi0]
Phi_v_shuju = [phi_v0]
T = [0]
X = [l * sin(theta0) * cos(phi0)]  # 球坐标公式
Y = [l * sin(theta0) * sin(phi0)]
Z = [l * cos(theta0)]
s = 0


def forward(theta_, theta_0, phi_, phi_0, delta):  # 依次为θ导数，θ，φ导数，φ
    global C, g, l
    theta_div2 = sin(theta_0) * cos(theta_0) * phi_ ** 2 - g / l * sin(theta_0)
    theta_div1 = theta_ + theta_div2 * delta
    theta = theta_div1 * delta + theta_0

    phi_div2 = -2 * cos(theta_0) / sin(theta_0) * theta_ * phi_
    phi_div1 = phi_ + phi_div2 * delta
    phi = phi_div1 * delta + phi_0
    return [theta_div1, theta, phi_div1, phi]


for i in range(200000):
    s += 1  # 防止数据过多，每循环10次取1个数据
    A = forward(theta_v0, theta0, phi_v0, phi0, deltat)
    theta_v0, theta0, phi_v0, phi0 = A[0], A[1], A[2], A[3]
    if s % 10 == 0:
        X.append(l * sin(theta0) * cos(phi0))
        Y.append(l * sin(theta0) * sin(phi0))
        Z.append(-l * cos(theta0))
        T.append(deltat * i)
        Theta_shuju.append(theta0)
        Theta_v_shuju.append(theta_v0)
        Phi_shuju.append(phi0)
        Phi_v_shuju.append(phi_v0)


def OutData():
    global theta_v0, theta0, phi_v0, phi0, s, deltat
    for i in range(200000):
        s += 1  # 防止数据过多，每循环10次取1个数据
        A = forward(theta_v0, theta0, phi_v0, phi0, deltat)
        theta_v0, theta0, phi_v0, phi0 = A[0], A[1], A[2], A[3]
        if s % 10 == 0:
            X.append(l * sin(theta0) * cos(phi0))
            Y.append(l * sin(theta0) * sin(phi0))
            Z.append(-l * cos(theta0))
            T.append(deltat * i)
            Theta_shuju.append(theta0)
            Theta_v_shuju.append(theta_v0)
            Phi_shuju.append(phi0)
            Phi_v_shuju.append(phi_v0)


def ReStartDeal():
    global v, v_0, C, x, y, z, Theta_shuju, Theta_v_shuju, Phi_shuju, Phi_v_shuju, T, X, Y, Z, s,PlaySpeed,RunState
    v_0 = l * phi_v0
    C = v_0 * sin(theta0) / l
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = l * np.outer(np.cos(u), np.sin(v))
    y = l * np.outer(np.sin(u), np.sin(v))
    z = l * np.outer(np.ones(np.size(u)), np.cos(v))
    Theta_shuju = [theta0]
    Theta_v_shuju = [theta_v0]
    Phi_shuju = [phi0]
    Phi_v_shuju = [phi_v0]
    T = [0]
    X = [l * sin(theta0) * cos(phi0)]  # 球坐标公式
    Y = [l * sin(theta0) * sin(phi0)]
    Z = [l * cos(theta0)]
    s = 0
    PlaySpeed = 50
    OutData()
    RunState = False


def DrawPic():
    plt.style.use('seaborn-paper')  # dark_background'
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.figure(figsize=(5.18, 5.6))
    ax = plt.subplot(projection='3d', alpha=0.1, )  # 创建一个三维的绘图工程np.array(T),
    A = ax.scatter(X[0:PlaySpeed], Y[0:PlaySpeed], Z[0:PlaySpeed], c=T[0:PlaySpeed], alpha=1,
                   cmap=plt.cm.get_cmap('winter'), s=10)  # 绘制数据点 c: ‘r‘红色，‘y‘黄色，等颜色
    B = ax.plot_surface(x, y, z, rstride=4, cstride=4, cmap='PuBu', alpha=0.2)
    ax.set_xlabel('X', fontsize=10)  # 设置x坐标轴
    ax.set_ylabel('Y', fontsize=10)  # 设置y坐标轴
    ax.set_zlabel('Z', fontsize=10)  # 设置z坐标轴
    ax.set_title("球面摆实时模拟", fontsize=15, alpha=1, verticalalignment='top')
    Color = plt.colorbar(A)
    Color.set_label('Time', fontsize=15)
    plt.savefig('cache\\pic\\pic1.png')
    f2 = plt.figure(figsize=(2.8, 2.8))
    plt.scatter(Theta_shuju[0:PlaySpeed], Theta_v_shuju[0:PlaySpeed], s=0.2, c='darkcyan', marker='^', alpha=0.8)
    plt.xlabel('Angular -Theta')
    plt.ylabel('Angular Speed-Theta')
    plt.savefig('cache\\pic\\pic2.png')
    f3 = plt.figure(figsize=(2.8, 2.8))
    plt.scatter(Phi_shuju[0:PlaySpeed], Phi_v_shuju[0:PlaySpeed], marker='p', c='blue', s=2)
    plt.xlabel('Angular -Phi')
    plt.ylabel('Angular Speed-Phi')
    plt.savefig('cache\\pic\\pic3.png')
    plt.close()



def LoadImage():
    p.time.wait(100)
    p1 = p.image.load('cache\\pics\\1pic{}.png'.format(PlaySpeed))
    p2 = p.image.load('cache\\pics\\2pic{}.png'.format(PlaySpeed))
    p3 = p.image.load('cache\\pics\\3pic{}.png'.format(PlaySpeed))
    Screen.blit(p1, (425, 58))
    Screen.blit(p2, (948, 58))
    Screen.blit(p3, (948, 344))
    with open('cache\\angle\\{}.txt'.format(PlaySpeed),'r') as file:
        temp = eval(file.read())
        theta_temp,phi_temp = temp[0],temp[1]
        Screen.blit(font.render('{}'.format(theta_temp),True,(0,0,0),None),(273,450))
        Screen.blit(font.render('{:.2e}'.format(phi_temp), True, (0, 0, 0), None), (273, 522))

def Init():
    Screen.blit(BgImage, (0, 0))
    Manager.draw_ui(Screen)


def Event():
    global l, theta0, theta_v0, phi0, phi_v0, RunState, ProRuning
    for i in p.event.get():
        if i.type == p.QUIT:
            sys.exit()
        elif i.type == p.MOUSEBUTTONDOWN:
            print(p.mouse.get_pos())
            if 1105<p.mouse.get_pos()[0]<1105+70 and 646<p.mouse.get_pos()[1]<646+50:
                pass
                #回主菜单
        elif i.type == p.USEREVENT:
            if i.user_type == pg.UI_BUTTON_START_PRESS:
                if i.ui_element == ButtonStart:
                    if TextLength.text != '':
                        l = TextLength.text  # 摆长，以米做单位
                    if TextTheta.text != '':
                        theta0 = TextTheta.text  # theta初始值
                    if TextThetaW.text != '':
                        theta_v0 = TextThetaW.text  # theta导数初始值
                    if TextPhi.text != '':
                        phi0 = TextPhi.text  # 默认为零
                    if TextPhiW.text != '':
                        phi_v0 = TextPhiW.text  # phi角初始导数
                    RunState = True
                elif i.ui_element == ButtonRestart:
                    l = 0.85  # 摆长，以米做单位
                    theta0 = 1.57  # theta初始值
                    theta_v0 = 0  # theta导数初始值
                    phi0 = 0  # 默认为零
                    phi_v0 = 0.855  # phi角初始导数
                    DrawPic()
                    ReStartDeal()

                # 👇----------------------------------------------------------------------------------------------
                # 新加了一个按钮
                elif i.ui_element == next_:
                    # 👇----------------------------------------------------------------------------------------------
                    # 程序的跳转部分
                    ProRuning = False
                    # subprocess.Popen('主页UI.exe')
                    # subprocess.Popen(r".\venv\Scripts\python 主页UI.py")
                    os.system(r"start .\venv\Scripts\python 主页UI.py")  # 调试时使用
                    # os.popen(r"主页UI.exe")  # 打包时使用
                    # 👆----------------------------------------------------------------------------------------------
                # 👆---------------------------------------------------------------------------------------------------
        Manager.process_events(i)


def Update():
    global Width, Height, PlaySpeed
    if RunState:
        LoadImage()
        PlaySpeed += 50
    Width, Height = p.display.get_window_size()
    Manager.update(UpTime)
    p.display.update()
    Screen.fill((255, 255, 255))


# 👇-------------------------------------------------------------------------------------------------------------------
# 新增跳转按钮
next_ = pg.elements.UIButton(p.Rect(1106, 633, 101, 67),
                             text="",
                             manager=Manager,
                             object_id="next")
# 👆-------------------------------------------------------------------------------------------------------------------

while ProRuning:
    Init()
    Event()
    Update()
