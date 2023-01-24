import os
import subprocess

import pygame
import pygame_gui.data
import pygame_gui

WINDOW_SIZE = (1280, 720)

is_running = True

pygame.init()  # 初始化窗口
pygame.display.set_caption("虚拟仿真软件")  # 设置窗口标题
window_surface = pygame.display.set_mode(WINDOW_SIZE)  # 设置窗口


clock = pygame.time.Clock()  # 添加管理时钟

# 添加界面管理器
ui_manager = pygame_gui.UIManager(WINDOW_SIZE, r'./ui_themes/json/dbbutton.json')


# 加载图片
background_pic = pygame.image.load(r"./dependent_files/pic/开始菜单第4版.png")

# 单摆介绍
intro_pic = pygame.image.load(r"./dependent_files/pic/单摆介绍.png")

# 单摆实验按钮
DBbutton = pygame_gui.elements.UIButton(pygame.Rect(107, 174, 213, 63),
                                        text='',
                                        manager=ui_manager,
                                        object_id='db'
                                        )

# 复摆实验按钮
FBbutton = pygame_gui.elements.UIButton(pygame.Rect(107, 257, 213, 63),
                                        text='',
                                        manager=ui_manager,
                                        object_id='fb'
                                        )
# 双摆实验按钮
SBbutton = pygame_gui.elements.UIButton(pygame.Rect(107, 340, 213, 63),
                                        text='',
                                        manager=ui_manager,
                                        object_id='double'
                                        )

# 球面摆实验按钮
QMBbutton = pygame_gui.elements.UIButton(pygame.Rect(107, 423, 213, 63),
                                         text='',
                                         manager=ui_manager,
                                         object_id='globe'
                                         )

# 进入按钮
enterbutton = pygame_gui.elements.UIButton(pygame.Rect(1106, 633, 101, 67),
                                           text='',
                                           manager=ui_manager,
                                           object_id='enter')

ls = [1, 0, 0, 0]  # 单摆，复摆，多摆，球面摆
DBbutton.select()

while is_running:  # 主程序
    time_delta = clock.tick(60) / 100.0
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == DBbutton:
                    ls[0] = 1
                    ls[1] = 0
                    ls[2] = 0
                    ls[3] = 0
                    DBbutton.select()
                    FBbutton.unselect()
                    SBbutton.unselect()
                    QMBbutton.unselect()
                    intro_pic = pygame.image.load(r"./dependent_files/pic/单摆介绍.png")
                elif event.ui_element == FBbutton:
                    ls[0] = 0
                    ls[1] = 1
                    ls[2] = 0
                    ls[3] = 0
                    FBbutton.select()
                    DBbutton.unselect()
                    SBbutton.unselect()
                    QMBbutton.unselect()
                    intro_pic = pygame.image.load(r"./dependent_files/pic/复摆介绍.png")
                elif event.ui_element == SBbutton:
                    ls[0] = 0
                    ls[1] = 0
                    ls[2] = 1
                    ls[3] = 0
                    SBbutton.select()
                    DBbutton.unselect()
                    FBbutton.unselect()
                    QMBbutton.unselect()
                    intro_pic = pygame.image.load(r"./dependent_files/pic/多摆介绍.png")
                elif event.ui_element == QMBbutton:
                    ls[0] = 0
                    ls[1] = 0
                    ls[2] = 0
                    ls[3] = 1
                    QMBbutton.select()
                    DBbutton.unselect()
                    FBbutton.unselect()
                    SBbutton.unselect()
                    intro_pic = pygame.image.load(r"./dependent_files/pic/球面摆介绍.png")
                elif event.ui_element == enterbutton:
                    if ls[0]:
                        # subprocess.Popen("米尺测摆长.exe")
                        # subprocess.Popen(r".\venv\Scripts\python 米尺测摆长.py")
                        os.system(r"start .\venv\Scripts\python 米尺测摆长.py")
                        # os.popen(r"米尺测摆长.exe")

                        is_running = False
                    elif ls[1]:
                        # subprocess.Popen("复摆测量.exe")
                        # subprocess.Popen(r".\venv\Scripts\python 复摆测量.py")
                        os.system(r"start .\venv\Scripts\python 复摆测量.py")
                        # os.popen(r"复摆测量.exe")
                        is_running = False
                    elif ls[2]:
                        # subprocess.Popen("双摆.exe")
                        # subprocess.Popen(r".\venv\Scripts\python 双摆.py")
                        os.system(r"start .\venv\Scripts\python 双摆.py")
                        # os.popen(r"双摆.exe")
                        is_running = False
                    elif ls[3]:
                        # subprocess.Popen("球面摆.exe")
                        # subprocess.Popen(r".\venv\Scripts\python 球面摆.py")
                        os.system(r"start .\venv\Scripts\python 球面摆.py")
                        # os.popen(r"球面摆.exe")
                        is_running = False
        ui_manager.process_events(event)
    ui_manager.update(time_delta)
    ui_manager.draw_ui(window_surface)
    window_surface.blit(intro_pic, (0, 0))
    window_surface.blit(background_pic, (0, 0))
    pygame.display.update()
