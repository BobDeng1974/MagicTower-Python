# 作为新框架测试用

import pygame
import os
import json
import platform
import ctypes
from sysconf import *

pygame.init()

# 如果是Windows系统，在游戏中禁用显示缩放
# 注：通常高分屏用户在使用Windows系统时，都会把缩放调到100%以上，否则会瞎眼。
# 例如1920*1080屏幕，Windows推荐的缩放率就是125%。
# 这样会导致游戏窗口被严重放大，造成一部分游戏画面处在任务栏下方。
# 然而，在Linux系统下并没有这问题，所以这里只判定是否为Windows。
if platform.system() == "Windows":
    ctypes.windll.user32.SetProcessDPIAware()

# 设置游戏窗口大小
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# 设置窗口标题
pygame.display.set_caption(TOWER_NAME)

from lib.utools import *
from lib import CurrentMap, PlayerCon, WriteLog
from lib.ground import GroundSurface
from lib import global_var
from lib.event import EventFlow, Event
from project.block import BlockData

RootScreen = GroundSurface(mode="copy", surface=screen)
running = True
from lib import ui
from lib import actions

action_control = actions.ActionControl()

from lib import music

def init():
    global_var.set_value("font_name", FONT_NAME)
    global_var.set_value("RootScreen", RootScreen)
    global_var.set_value("action_control", action_control)
    
    # 设置PlayerCon为全局变量（必须要在CurrentMap.set_map之前完成）
    global_var.set_value("PlayerCon", PlayerCon)
    
    # 初始化地图
    CurrentMap.set_map(PLAYER_FLOOR)
    CurrentMap.add_sprite(PlayerCon)
    global_var.set_value("CurrentMap", CurrentMap)
    WriteLog.debug(__name__, "初始化地图完成")

    # 初始化BlockData（建立通过id反查地图编号的字典）
    BlockDataReverse = {}
    for map_obj in BlockData:
        block_id = BlockData[map_obj]["id"]
        BlockDataReverse[block_id] = map_obj
    global_var.set_value("BlockDataReverse", BlockDataReverse)

    # 状态栏占位（如果删除，会影响游戏内地图的位置）
    StatusBarArea = RootScreen.add_child("left", BLOCK_UNIT * 4)
    StatusBarArea.priority = 15
    RootScreen.add_child(CurrentMap)  
    
    # 初始化UI图层
    # --- UI0 - 状态栏
    STATUSBAR = ui.StatusBar(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    STATUSBAR.priority = 145
    RootScreen.add_child(STATUSBAR)  
    global_var.set_value("STATUSBAR", STATUSBAR)
    WriteLog.debug(__name__, "初始化状态栏图层完成")
    # --- UI1 - 怪物手册
    BOOK = ui.Book(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    BOOK.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(BOOK)
    global_var.set_value("BOOK", BOOK)
    WriteLog.debug(__name__, "初始化怪物手册图层完成")
    # --- UI2 - 开始界面
    STARTMENU = ui.StartMenu(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    STARTMENU.priority = 500  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(STARTMENU)
    global_var.set_value("STARTMENU", STARTMENU)
    WriteLog.debug(__name__, "初始化开始界面图层完成")
    # --- UI3 - 背包界面
    BACKPACK = ui.Backpack(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    BACKPACK.priority = 150  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(BACKPACK)
    global_var.set_value("BACKPACK", BACKPACK)
    WriteLog.debug(__name__, "初始化背包图层完成")
    # --- UI4 - 存档界面
    SAVE = ui.SaveMenu(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    SAVE.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(SAVE)
    global_var.set_value("SAVE", SAVE)
    WriteLog.debug(__name__, "初始化存档图层完成")
    # --- UI5 - 读档界面
    LOAD = ui.LoadMenu(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    LOAD.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(LOAD)
    global_var.set_value("LOAD", LOAD)
    WriteLog.debug(__name__, "初始化读档图层完成")
    # --- UI6 - 楼层传送器界面
    FLY = ui.Fly(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    FLY.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(FLY)
    global_var.set_value("FLY", FLY)
    WriteLog.debug(__name__, "初始化楼层传送器图层完成")
    # --- UI7 - 帮助界面
    HELP = ui.Help(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    HELP.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(HELP)
    global_var.set_value("HELP", HELP)
    WriteLog.debug(__name__, "初始化帮助图层完成")
    # --- UI8 - 商店1界面
    Shop1 = ui.Shop1(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    Shop1.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(Shop1)
    global_var.set_value("Shop1", Shop1)
    WriteLog.debug(__name__, "初始化商店1图层完成")
    # --- UI9 - 商店2界面
    Shop2 = ui.Shop2(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    Shop2.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(Shop2)
    global_var.set_value("Shop2", Shop2)
    WriteLog.debug(__name__, "初始化商店2图层完成")
    # --- UI10 - 文本框界面
    TEXTBOX = ui.TextBox(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    TEXTBOX.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(TEXTBOX)
    global_var.set_value("TEXTBOX", TEXTBOX)
    WriteLog.debug(__name__, "初始化文本框图层完成")
    # --- UI11 - 选择框界面
    CHOICEBOX = ui.ChoiceBox(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    CHOICEBOX.priority = 140  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(CHOICEBOX)
    global_var.set_value("CHOICEBOX", CHOICEBOX)
    WriteLog.debug(__name__, "初始化选择框图层完成")
    # --- UI12 - 显伤层
    SHOWDAMAGE = ui.ShowDamage(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    SHOWDAMAGE.priority = 65  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(SHOWDAMAGE)
    global_var.set_value("SHOWDAMAGE", SHOWDAMAGE)
    WriteLog.debug(__name__, "初始化显伤层完成")
    # --- UI13 - 色调层
    CURTAIN = ui.Curtain(mode='copy', surface=RootScreen) # 必须按ground的方式初始化
    CURTAIN.priority = 125  # 显示的优先级 高于地图 所以在地图上
    RootScreen.add_child(CURTAIN)
    global_var.set_value("CURTAIN", CURTAIN)
    WriteLog.debug(__name__, "初始化色调层完成")
    WriteLog.info(__name__, "初始化全部UI图层完成")


def init_actions():
    # QUIT:
    def quit(e):
        global running
        running = False
        return True
    
    # 注册事件
    action_control.register_action('QUIT', pygame.QUIT, quit)
    action_control.register_action('BOOK', pygame.KEYUP, global_var.get_value('BOOK').action)
    action_control.register_action('STARTMENU', pygame.KEYUP, global_var.get_value('STARTMENU').action)
    action_control.register_action('BACKPACK', pygame.KEYUP, global_var.get_value('BACKPACK').action)
    action_control.register_action('SAVE', pygame.KEYUP, global_var.get_value('SAVE').action)
    action_control.register_action('LOAD', pygame.KEYUP, global_var.get_value('LOAD').action)
    action_control.register_action('FLY', pygame.KEYUP, global_var.get_value('FLY').action)
    action_control.register_action('HELP', pygame.KEYUP, global_var.get_value('HELP').action)
    action_control.register_action('Shop1', pygame.KEYUP, global_var.get_value('Shop1').action)
    action_control.register_action('Shop2', pygame.KEYUP, global_var.get_value('Shop2').action)
    action_control.register_action('TEXTBOX', pygame.KEYUP, global_var.get_value('TEXTBOX').action)
    action_control.register_action('CHOICEBOX', pygame.KEYUP, global_var.get_value('CHOICEBOX').action)
    action_control.register_action('SHOWDAMAGE', pygame.KEYUP, global_var.get_value('SHOWDAMAGE').action)
    action_control.register_action('STATUSBAR', pygame.KEYUP, global_var.get_value('STATUSBAR').action)
    action_control.register_action('CURTAIN', pygame.KEYUP, global_var.get_value('CURTAIN').action)
    WriteLog.info(__name__, "事件全部注册完成")


def init_sound():
    Music = music.MusicWrapper()
    global_var.set_value("Music", Music)
    WriteLog.info(__name__, "初始化音效完成")

def init_event_flow():
    EVENTFLOW = EventFlow()
    global_var.set_value("EVENTFLOW", EVENTFLOW)
    EVENT = Event()
    global_var.set_value("EVENT", EVENT)
    EVENT.get_event_flow_module()
    EVENTFLOW.get_event_module()
    WriteLog.info(__name__, "初始化事件流完成")

def init_function():
    FUNCTION = global_var.get_value("FUNCTION")
    FUNCTION.init_var()
    WriteLog.info(__name__, "初始化function完成")

# DEBUG（开关在sysconf.py，如果开启将会启动控制台）
if DEBUG:
    import threading


    def console():
        while running:
            r = input()
            try:
                print(eval(r))
            except:
                try:
                    exec(r)
                except Exception as e:
                    print("error:", str(e))


    t = threading.Thread(target=console)
    t.start()

init()
init_actions()
init_sound()
init_event_flow()
init_function()
clock = pygame.time.Clock()

STARTMENU = global_var.get_value("STARTMENU")

# 主程序
while running:
    # a = pygame.time.get_ticks()
    # 展示开始菜单
    if STARTMENU.new_game == True:
        STARTMENU.open()
        STARTMENU.new_game = False
        # 默认开启显伤
        show_damage = global_var.get_value("SHOWDAMAGE")
        show_damage.open()
        # 默认开启状态栏
        status_bar = global_var.get_value("STATUSBAR")
        status_bar.open()
        # 地图确保为active状态
        CurrentMap.active = True
        # 载入初始事件
        EVENTFLOW = global_var.get_value("EVENTFLOW")
        with open(os.path.join(os.getcwd(),"project", "start_text.json")) as f:
            start_text = json.load(f)
        EVENTFLOW.insert_action(start_text["startText"])
    pygame.display.update()
    # 背景
    RootScreen.flush(screen)  # 显示刷新到屏幕
    action_control.action_render()  # 检查动作消息
    # b = pygame.time.get_ticks()
    # print(b - a)

