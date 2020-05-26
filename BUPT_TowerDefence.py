import cocos
import pyglet
import math
import pygame
import time
import threading
from cocos.actions import *
from cocos.layer import Layer
from cocos.particle_systems import *
from cocos.director import director
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.sprite import Sprite
from cocos import scenes
from pyglet.window import key
from cocos import layer
import cocos.collision_model as cm
from cocos.actions import Driver
from cocos.actions import Move
from pyglet.window import mouse
from cocos.collision_model import *
from cocos.skeleton import Bone, Skeleton
from cocos import skeleton
from cocos.audio.pygame import mixer, music
import draw
import root_bone
import root_skin
import animation.my_walk_skeleton
import animation.myE_skeleton
import animation.myE_skin
import animation.turn_my_walk_skeleton
import animation.myE_skin
import animation.myE_skeleton
import animation.turn_my_walk_skin
import animation.my_walk_skin
import animation.model1_skeleton
import animation.model1_skin
import animation.model2_skeleton
import animation.model2_skin
import animation.test_skeleton
import animation.test_skin
import animation.test_skin1
import _pickle as cPickle

address = "D:\MyCode\MyPython\BUPT_TowerDefence\img"
address_2 = "D:\MyCode\MyPython\BUPT_TowerDefence"
address = "D:\CSHE\BUPT_TowerDefence\img"
address_2 = "D:\CSHE\BUPT_TowerDefence"
# address = "*****\BUPT_TowerDefence\img"
# address_2 = "***\BUPT_TowerDefence"

class MouseDisplay(cocos.layer.Layer):  # 现在有bug 超出虚拟屏幕移动就有问题

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.text = cocos.text.Label('Mouse @', font_size=18,
                                     x=100, y=240)
        self.add(self.text)

    def on_mouse_motion(self, x, y, dx, dy):
        # dx,dy为向量,表示鼠标移动方向
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        # 按下鼠标按键不仅更新鼠标位置,还改变标签的位置.这里使用director.get_virtual_coordinates(),用于保证即使窗口缩放过也能正确更新位置,如果直接用x,y会位置错乱,原因不明
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, buttons, modifiers)
        self.text.element.x, self.text.element.y = director.get_virtual_coordinates(x, y)
        global target_x, target_y
        target_x, target_y = director.get_virtual_coordinates(x, y)


class Main_menu(cocos.menu.Menu):
    def __init__(self):
        super(Main_menu, self).__init__()

        items = []

        items.append(cocos.menu.ImageMenuItem('img/start.png', self.on_start))
        items.append(cocos.menu.ImageMenuItem('img/setting.png', self.on_setting))
        items.append(cocos.menu.ImageMenuItem('img/help.png', self.on_help))

        for i in items:
            i.x = 550

        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_start(self):
        print("start")
        bg_2 = BG(bg_name="img/bg_2.png")
        scene_2 = cocos.scene.Scene(MouseDisplay(),bg_2)
        level_choose = Level_choose()
        car = p_layer()
        scene_2.add(car, 2)
        scene_2.add(level_choose)
        director.replace(scenes.transitions.SlideInBTransition(scene_2, duration=1))

    def on_setting(self):
        print('setting')

    def on_help(self):
        print('help')


class My_base(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(address + "/base.png")
        spr = cocos.sprite.Sprite(img)
        spr.position = 50, 100
        self.add(spr)

        life_bar = cocos.sprite.Sprite("img/yellow_bar.png")
        life_bar.position = 50, 220
        self.add(life_bar)


class VF_Layer(Layer):
    def __init__(self,fail):
        super(VF_Layer, self).__init__()
        print(fail,"asfhgekghklsg")
        if fail == True:
            self.count = 0
            self.bg = BG(bg_name="img/fail_bg.jpg")
            self.fail_window=Sprite("img/f_window.png")
            self.fail_window.position=620,350
            self.lable1 = cocos.text.Label('就', font_name='Times New Roman', font_size=200)
            self.lable1.position = 10, 170
            self.lable2 = cocos.text.Label('这', font_name='Times New Roman', font_size=200)
            self.lable2.position = 900, 170
            self.add(self.bg)
            self.add(self.fail_window)
            #self.add(self.lable2)
            #self.add(self.lable1)

        else:
            self.count=0
            self.vic_bg=BG(bg_name="img/vic_bg.jpg")
            self.vic_word=Sprite("img/vic_word.png")
            self.vic_word.position=600,400

            self.A_word=Sprite("img/A_word.png")
            self.A_word.position=700,500
            self.add(self.vic_bg)
            self.add(self.vic_word)
            self.add(self.A_word)



class Enemy_base(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()
        self.dead = False
        img = pyglet.image.load(address + "/base.png")
        spr = cocos.sprite.Sprite(img)
        spr.position = 2300, 100
        self.add(spr)
        self.life=10
        self.life_bar = cocos.sprite.Sprite("img/yellow_bar.png")
        self.life_bar.position = 2300, 220
        self.add(self.life_bar)
        self.cshape = cm.AARectShape(eu.Vector2(*spr.position),spr.width/2,spr.height/2)

    def update_position(self, dt):
        self.life_bar.scale_x = self.life / 100

class MainLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        bg = cocos.sprite.Sprite("img/bg_3.jpg")
        bg.position = bg.width // 2, bg.height // 2

        self.px_width = bg.width
        self.px_height = bg.height

        self.enemy_num = 1

        self.my_base = My_base()
        self.enemy_base = Enemy_base()

        self.add(bg, 0)
        self.add(self.my_base, 1)
        self.add(self.enemy_base, 1)


class BG(cocos.layer.Layer):  # 看是否需要传入background.position
    def __init__(self, bg_name):
        super(BG, self).__init__()
        d_width, d_height = director.get_window_size()
        # 创建背景精灵
        background = cocos.sprite.Sprite(bg_name)
        background.position = d_width // 2, d_height // 2
        self.add(background)


class Game_menu(cocos.menu.Menu):
    def __init__(self):
        super(Game_menu, self).__init__()

        items = []

        items.append(cocos.menu.ImageMenuItem('img/return.png', self.on_back))
        items.append(cocos.menu.ToggleMenuItem('Show FPS: ', self.on_show_fps, director.show_FPS))
        items.append(cocos.menu.ImageMenuItem('img/quit.png', self.on_quit))


        items[0].position = 250, -390
        items[1].position = -400, 300
        items[2].position = 350, -300

        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_back(self):  # 有点Bug
        print("back")
        bg_2 = BG(bg_name="img/bg_2.png")
        scene_2 = cocos.scene.Scene(MouseDisplay(),bg_2)
        level_choose = Level_choose()
        car = p_layer()
        scene_2.add(level_choose)
        scene_2.add(car, 2)
        director.replace(scenes.transitions.SlideInBTransition(scene_2, duration=1))

    def on_quit(self):
        director.window.close()

    def on_show_fps(self, show_fps):
        director.show_FPS = show_fps

class Game_menu_f(cocos.menu.Menu):             #需要精简
    def __init__(self):
        super(Game_menu_f, self).__init__()

        items = []

        items.append(cocos.menu.ImageMenuItem('img/return.png', self.on_back))
        items.append(cocos.menu.ToggleMenuItem('Show FPS: ', self.on_show_fps, director.show_FPS))
        items.append(cocos.menu.ImageMenuItem('img/quit.png', self.on_quit))

        items[0].position = 20, -235
        items[1].position = -400, 300
        items[2].position = 350, -300
        items[0].scale_x=3
        items[0].scale_y = 3

        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_back(self):  # 有点Bug
        print("back")
        bg_2 = BG(bg_name="img/bg_2.png")
        scene_2 = cocos.scene.Scene(MouseDisplay(),bg_2)
        level_choose = Level_choose()
        car = p_layer()
        scene_2.add(level_choose)
        scene_2.add(car, 2)
        director.replace(scenes.transitions.SlideInBTransition(scene_2, duration=1))

    def on_quit(self):
        director.window.close()

    def on_show_fps(self, show_fps):
        director.show_FPS = show_fps


class Drag(cocos.layer.Layer):
    is_event_handler = True  #to detect the mouse
    def __init__(self):
        super().__init__()
        
        self.spr = cocos.sprite.Sprite("img/car.png",anchor = (0,0))  #anchor means the relative center  the defalt is the center of the picture 

        self.spr.position = 450,450

        self.add(self.spr)
        self.clicked = False

    def mouse_on_sprite(self, x, y):
        if x < self.spr.x + self.spr.width and x > self.spr.x and y < self.spr.y + self.spr.height and y > self.spr.y:
            return True
        return False

    def on_mouse_press(self,x,y,button,modifiers):
        if button & mouse.LEFT:         #只检测鼠标左键
            if self.mouse_on_sprite(x,y):
                self.clicked = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.clicked = False

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.clicked:
            self.spr.position = (x - self.spr.width // 2, y - self.spr.height // 2)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_on_sprite(x,y):
            cursor_img = pyglet.image.load(address + '/cursor.png')
            cursor_img.anchor_x = cursor_img.width // 2
            cursor_img.anchor_y = cursor_img.height //2
            cursor = pyglet.window.ImageMouseCursor(cursor_img,0,0)   #hotx hoty
            # cursor = director.window.get_system_mouse_cursor(director.window.CURSOR_HAND)
            director.window.set_mouse_cursor(cursor)
        else:
            cursor = director.window.get_system_mouse_cursor(director.window.CURSOR_DEFAULT)
            director.window.set_mouse_cursor(cursor)


class Level_choose(cocos.menu.Menu):
    def __init__(self):
        super(Level_choose, self).__init__()
        items = []

        items.append(cocos.menu.ImageMenuItem('img/level_1_icon.png', self.level_1_callback))
        items.append(cocos.menu.ImageMenuItem('img/level_2_icon.png', self.level_2_callback))

        items[0].position = 100, -110
        items[1].position = 300, -70

        self.create_menu(items, cocos.menu.zoom_in(), cocos.menu.zoom_out())
        # self.count = 0

    def level_1_callback(self):
        print("第一关")
        # 这次创建的窗口带调整大小的功能
        self.game_menu = Game_menu()

        img = pyglet.image.load(address + "\skill_1.png")
        self.skill_1 = cocos.sprite.Sprite(img)
        self.skill_1.position = (100,620)
        img = pyglet.image.load(address + "\skill_2.png")
        self.skill_2 = cocos.sprite.Sprite(img)
        self.skill_2.position = (220,620)
        img = pyglet.image.load(address + "\skill_3.png")
        self.skill_3 = cocos.sprite.Sprite(img)
        self.skill_3.position = (340,620)

        self.scene_3 = cocos.scene.Scene(MouseDisplay(),self.game_menu,self.skill_1,self.skill_2,self.skill_3)

        self.addable = False
        self.auto_new = 0
        global scroller,speed_1,block_1,block_1_R
        speed_1 = 1
        scroller = cocos.layer.ScrollingManager()
        self.e_list = []

        self.skill = [[True,0],[True,0],[True,0]]            #两个数组第一个是技能1 每一个有两个参数：参数1：现在是否可以释放 参数2：冷却时间计数

        self.player_damage = 5
        self.eb_count=0
        self.m_layer = MainLayer()
        self.player_1 = Player_1()
        self.t_list=[]
        self.t_list.append(Teammate(animation.myE_skeleton.skeleton,animation.myE_skin.skin,"/animation/q.anim","/animation/E_attack.anim","/animation/frozen.anim",0))
        # self.player_2 = Player_2()
        self.e_list.append([Enemy_1(animation.test_skeleton.skeleton,animation.test_skin.skin,"/animation/2t.anim","/animation/E_attack.anim","/animation/frozen.anim",0), False])   #第一个是对象 第二个是是否死亡 第三个是count（子弹击中）
        self.enemy_1_dead = False
        self.add_e_count=0
        self.coll_manager = cm.CollisionManagerBruteForce()
        self.coll_manager.add(self.player_1)
        self.coll_manager.add(self.t_list[0])
        # self.coll_manager.add(self.player_2)
        self.coll_manager.add(self.e_list[0][0])
        self.coll_manager.add(self.player_1.bullet)
        self.coll_manager.add(self.m_layer.enemy_base)
        self.fi = self.player_1

        scroller.add(self.m_layer)
        # scroller.add(self.player_2)
        scroller.add(self.e_list[0][0])
        scroller.add(self.player_1)
        scroller.add(self.t_list[0])

        self.scene_3.schedule_interval(self.player_1.status_detect, 1 / 30)
        self.scene_3.schedule_interval(self.player_1.update_position, 1 / 80)
        self.scene_3.schedule_interval(self.m_layer.enemy_base.update_position, 1 / 80)
        # scene_3.schedule_interval(self.player_2.status_detect, 1 / 30)
        # scene_3.schedule_interval(self.player_2.update_position, 1 / 80)
        if not self.e_list[0][1]:
            self.scene_3.schedule_interval(self.e_list[0][0].update_position, 1 / 80)
            self.scene_3.schedule_interval(self.e_list[0][0].status_detect, 1 / 30)
        self.scene_3.schedule_interval(self.t_list[0].update_position, 1 / 80)
        self.scene_3.schedule_interval(self.t_list[0].status_detect, 1 / 30)
        self.scene_3.schedule_interval(self.update, 1 / 80)

        self.scene_3.add(scroller, 0)

        director.replace(scenes.transitions.SlideInBTransition(self.scene_3, duration=1))

    def level_2_callback(self):
        print("DIY角色")
        global img_name
        img_name = draw.Draw()
        self.level_1_callback()

    def skill_detect(self):
        global speed_1
        if(self.skill[0][0]):
            if(keyboard[key._1]):
                self.skill_1.color = (125,125,125)
                self.skill[0][0] = False
                self.skill[0][1] = 0
                self.player_damage = 10
        else:
            if (self.skill[0][1] <= 200):
                self.skill[0][1] += 1
                if(self.skill[0][1] == 100):
                    self.player_damage = 5
            else:
                self.skill_1.color = (255,255,255)
                self.skill[0][0] = True
        if(self.skill[1][0]):
            if(keyboard[key._2]):
                self.skill_2.color = (125,125,125)
                self.skill[1][0] = False
                self.skill[1][1] = 0
                speed_1 = 2.5
        else:
            if (self.skill[1][1] <= 200):
                if (self.skill[1][1] == 100):
                    speed_1 = 1
                self.skill[1][1] += 1
            else:
                self.skill_2.color = (255,255,255)
                self.skill[1][0] = True
        if(self.skill[2][0]):
            if(keyboard[key._3]):
                self.skill_3.color = (125,125,125)
                self.skill[2][0] = False
                self.skill[2][1] = 0
                self.player_1.add(self.player_1.fi)
                self.player_1.protect = True
        else:
            if (self.skill[2][1] <= 200):
                if (self.skill[2][1] == 100):
                    self.player_1.remove(self.player_1.fi)
                    self.player_1.protect = False
                self.skill[2][1] += 1
            else:
                self.skill_3.color = (255,255,255)
                self.skill[2][0] = True        

    def ebase_detect(self):
        if self.eb_count != 0:
            self.eb_count += 1
        if self.eb_count >= 7:
            self.eb_count = 0
        if self.coll_manager.they_collide(self.player_1.bullet, self.m_layer.enemy_base):
            if self.eb_count == 0:
                self.eb_count += 1
                self.player_1.refresh()
                if self.m_layer.enemy_base.life <= 10:
                    self.m_layer.enemy_base.life = 0
                    self.m_layer.enemy_base.dead = True
                else:
                    self.m_layer.enemy_base.life = self.m_layer.enemy_base.life - self.player_damage

    def add_enemy(self):
        if self.addable==False:
            self.auto_new += 1
        if self.auto_new>=400:
            self.addable=True
            self.auto_new=0
            if len(self.e_list) < 5:
                a = Enemy_1(animation.test_skeleton.skeleton,animation.test_skin1.skin,"/animation/2t.anim","/animation/E_attack.anim",("/animation/frozen.anim"),len(self.e_list))
                self.e_list.append([a, False, 0])
                self.coll_manager.add(a)
                self.scene_3.schedule_interval(a.update_position, 1 / 80)
                self.scene_3.schedule_interval(a.status_detect, 1 / 30)
                scroller.add(a)
                self.addable=False
        if self.add_e_count == 0:
            if keyboard[key.P]:
                a = Enemy_1(animation.test_skeleton.skeleton,animation.test_skin.skin,"/animation/2t.anim","/animation/E_attack.anim",("/animation/frozen.anim"),len(self.e_list))
                self.e_list.append([a, False, 0])
                self.coll_manager.add(a)
                self.scene_3.schedule_interval(a.update_position, 1 / 80)
                self.scene_3.schedule_interval(a.status_detect, 1 / 30)
                scroller.add(a)
                self.add_e_count += 1
        else:
            self.add_e_count += 1
            if self.add_e_count>40:
                self.add_e_count=0

    def death_detect(self):
        global scroller
        if self.player_1.life <= 0:
            #bg_1 = BG(bg_name="img/fail_bg.png")  # 1.获取背景图片路径
            self.game_menu = Game_menu_f()
            scene_2 = cocos.scene.Scene(VF_Layer(True),Drag(),MouseDisplay(), self.game_menu)
            director.replace(scenes.transitions.SlideInBTransition(scene_2, duration=1))
        for enemy in self.e_list:
            if enemy[0].life <= 0:
                enemy[1] = True
                scroller.remove(enemy[0])
                self.scene_3.unschedule(enemy[0].update_position)
                self.scene_3.unschedule(enemy[0].status_detect)
                self.e_list.remove(enemy)
        for teammate in self.t_list:
            if teammate.life <= 0:
                scroller.remove(teammate)
                self.scene_3.unschedule(teammate.update_position)
                self.scene_3.unschedule(teammate.status_detect)
                self.t_list.remove(teammate)


    def enemy_detect(self):
        self.death_detect()
        global block_1,block_1_R,block
        for enemy in self.e_list:
            if not enemy[1]:           #没死的话
                if (not self.player_1.protect) and (self.coll_manager.they_collide(self.player_1, enemy[0])):     #主角和enemy检测
                    block_1_R = True
                    if enemy[0].status == 1 or enemy[0].status == 3:        #enemy可以进行攻击
                        enemy[0].Attack = True
                        self.player_1.beheat = True
                    if enemy[0].status == 4:        #enemy攻击态
                        block_1 = True
                        self.player_1.life -= 0.5
                        self.player_1.beheat = True
                    else:
                        block_1 = False
                else:
                    block_1_R = False

                for teammate in self.t_list:                                #敌人和小弟检测
                    if self.coll_manager.they_collide(teammate, enemy[0]):      #得random或者怎样 调整怪物先手顺序 或者用speed判断
                        if enemy[0].status == 1 or enemy[0].status == 3:
                            enemy[0].Attack = True
                            teammate.beheat = True
                        elif enemy[0].status == 5:
                            enemy[0].life -= 0.5  
                        if teammate.status == 1:
                            teammate.Attack = True
                            enemy[0].beheat = True 
                        elif teammate.status == 5:
                            teammate.life -= 0.5

                if self.coll_manager.they_collide(self.player_1.bullet, enemy[0]):  #子弹和敌人检测
                    enemy[0].beheat = True
                    enemy[0].life = enemy[0].life - self.player_damage
                    self.player_1.refresh()


    def update(self, dt):
        self.skill_detect()
        self.add_enemy()
        self.ebase_detect()
        self.enemy_detect()

        if self.m_layer.enemy_base.dead:
            self.m_layer.enemy_base.dead = False
            self.game_menu = Game_menu_f()
            scene_2 = cocos.scene.Scene(VF_Layer(False),Drag(),MouseDisplay(), self.game_menu)
            director.replace(scenes.transitions.SlideInBTransition(scene_2, duration=1))
            

class P_move(Driver):
    def step(self, dt):
        x, y = self.target.position
        self.target.speed = 200
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(pow(dx, 2) + pow(dy, 2))
        if dy > 0:
            if dx > 0:
                self.angle = 180 * math.atan(dx / dy) / math.pi
            elif dx < 0:
                self.angle = 360 - 180 * math.atan(-dx / dy) / math.pi
            else:
                self.angle = self.angle
        elif dy < 0:
            if dx > 0:
                self.angle = 180 - 180 * math.atan(dx / -dy) / math.pi
            elif dx < 0:
                self.angle = 180 + 180 * math.atan(-dx / -dy) / math.pi
            else:
                self.angle = self.angle
        else:
            self.angle = self.angle
        self.target.do(MoveTo((target_x, target_y), duration=distance / self.target.speed) | RotateTo(self.angle, 0))
        super(P_move, self).step(dt)


class p_layer(cocos.sprite.Sprite):
    def __init__(self):
        super(p_layer, self).__init__("img/car.png")
        self.position = 500, 300
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 2, self.height / 2)
        self.do(P_move())

    def stop(self):
        global target_x, target_y
        target_x, target_y = self.position


class draw_rec(cocos.layer.util_layers.ColorLayer):
    def __init__(self, w, h):
        super().__init__(255, 0, 0, 255, width=w, height=h)


class Mover_1(cocos.actions.BoundedMove):
    def __init__(self):
        super().__init__(2300, 1430)  # it should be bigger than the size of the picture
        global block_1,block_1_R,speed_1,scroller
    def step(self, dt):  # add block
        if not block_1:
            super().step(dt)
            vel_x = (keyboard[key.D] - keyboard[key.A]) * 400 * speed_1
            if block_1_R and vel_x > 0:
                vel_x = 0
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)
            scroller.set_focus(self.target.x, self.target.y)


class Mover_2(cocos.actions.BoundedMove):
    def __init__(self):
        super().__init__(2300, 1430)  # it should be bigger than the size of the picture
    
    def step(self, dt):  # add block
        if not block_2:
            super().step(dt)
            vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 400
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)
            # global scroller
            # scroller.set_focus(self.target.x,self.target.y)       #不能同时存在两个focus


class Mover_3(cocos.actions.BoundedMove):
    def __init__(self,num):
        super().__init__(2300, 1430)  # it should be bigger than the size of the picture
        global block
        self.num = num
    def step(self, dt):  # add block
        if not block[self.num]:
            super().step(dt)
            vel_x = -100
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)

class Mover_4(Mover_3):
    def step(self, dt):  # add block
        if not block[self.num]:
            super().step(dt)
            vel_x = 100
            vel_y = 0
            self.target.velocity = (vel_x, vel_y)

class Spirite1(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(address + "/man.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 4, item_width=100, item_height=100)  # 1row 4col each one is 100*100

        anim = pyglet.image.Animation.from_image_sequence(img_grid[0:], 0.2,
                                                          loop=True)  # define the range of the photo and the second parameter is to descibe the period

        spr = cocos.sprite.Sprite(anim)
        spr.position = 200, 500
        self.add(spr)


class PeopleLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(address + "\girl.png")

        img_grid = pyglet.image.ImageGrid(img, 4, 8, item_width=120, item_height=150)

        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)

        spr = cocos.sprite.Sprite(anim)
        spr.position = 640, 500

        self.add(spr)


class Mr_cai(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(Mr_cai, self).__init__()

        x, y = director.get_window_size()
        self.skin = skeleton.BitmapSkin(animation.model1_skeleton.skeleton, animation.model1_skin.skin)
        self.add(self.skin)
        x, y = director.get_window_size()
        self.skin.position = 300, 150
        fp0 = open((address_2 + "/animation/Mr_cai.anim"), "rb+")
        anim = cPickle.load(fp0)
        self.skin.do(cocos.actions.Repeat(skeleton.Animate(anim)))


class Player_1(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(Player_1, self).__init__()
        # self.do(Repeat(MoveTo((600, 200), 5) + MoveTo((100, 200), 5)))

        animation.model2_skin.refresh()
        self.skin = skeleton.BitmapSkin(animation.model2_skeleton.skeleton, animation.model2_skin.skin)
        self.add(self.skin,1)
        # self.width,self.height = 0,0        #可能有bug
        self.position = 100, 100
        self.skin.position = 100, 100
        self.life = 100
        self.protect = False

        img = pyglet.image.load(address + "\dot.png")
        self.spr = cocos.sprite.Sprite(img, opacity=0)
        self.spr.position = 100, 100
        self.spr.velocity = (0, 0)
        self.mover = Mover_1()
        self.spr.do(self.mover)
        self.add(self.spr)
        self.life_bar = cocos.sprite.Sprite("img/yellow_bar.png")
        self.add(self.life_bar)
        self.fi = Fire()  # ParticleSystem 
        self.fi.auto_remove_on_finish = True
        self.fi.position = (100, 50)

        self.status = 1  # 1:stop 2:walk 3:保持态 4:attack
        self.change = False
        self.bullet_move = False
        self.count = 0
        self.beheat = False

        fp_1 = open((address_2 + "/animation/MOOOOVE1.anim"), "rb+")
        self.walk = cPickle.load(fp_1)

        fp_2 = open((address_2 + "/animation/gun_shot.anim"), "rb+")
        self.attack = cPickle.load(fp_2)

        fp_3 = open((address_2 + "/animation/my_frozen.anim"), "rb+")
        self.frozen = cPickle.load(fp_3)

        mixer.init()
        music.load((address_2 + r"/sound/bgm.mp3").encode())
        music.play()
        music.set_volume(0.4)

        # self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)
        self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)

        self.fire()
        self.bullet.cshape = cm.AARectShape(eu.Vector2(*self.bullet.position), self.bullet.width / 2,
                                            self.bullet.height / 2)

    def remove_all(self):
        if len(self.skin.actions) > 0:
            for i in range(0, len((self.skin.actions))):
                self.skin.remove_action(self.skin.actions[0])

    def update_position(self, dt):
        if not block_1:
            self.skin.position = self.spr.position  # !!!!!!! self.position = -(self.skin.position-600)
            x, y = self.skin.position
            self.life_bar.position = (x, y + 160)
            self.fi.position = (x,y-50)
            self.life_bar.scale_x = self.life / 100
            self.cshape.center = eu.Vector2(*self.skin.position)
            self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)

    def fire(self):  # 有个bug
        self.bullet = cocos.sprite.Sprite("img/bullet.png")
        self.bullet.position = -100, -100  # 初始在屏幕外
        self.add(self.bullet)

    def refresh(self):
        self.count = 0
        self.bullet.position = -100,-100
        global block_1
        block_1 = False
        self.bullet_move = False

    def recover(self):
        self.status = 1
        self.remove_all()
        global block_1
        block_1 = False

    def status_detect(self, dt):
        self.bullet.cshape.center = self.bullet.position
        if self.bullet_move:
            if self.count <= 4:
                self.count += 1
                x, y = self.bullet.position
                self.bullet.position = x + 40, y
            else:
                self.refresh()
        elif self.status == 1:
            if (keyboard[key.J]):
                self.status = 4
                global block_1
                block_1 = True
                self.skin.do(skeleton.Animate(self.attack))
                timer = threading.Timer(0.2, self.recover)
                timer.start()
                bullet_sound = pygame.mixer.Sound(address_2+'/sound/bullet.wav')
                bullet_sound.set_volume(0.5)
                bullet_sound.play()
                x, y = self.skin.position
                self.bullet.position = x + 110, y + 70
                self.bullet_move = True
            elif ((keyboard[key.D] and not block_1_R)or(keyboard[key.A])):  # key right and not attack  得改成状态保持
                self.status = 2
                self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
        if(self.status == 2 and not(keyboard[key.D] or keyboard[key.A])):
                self.recover()
        if self.beheat and self.status != 3:
            self.remove_all()
            self.status = 3
            self.beheat = False
            block_1 = True
            self.skin.do(skeleton.Animate(self.frozen))
            timer = threading.Timer(0.5, self.recover)
            timer.start()
                
        if self.life<=0:
            del self        #这里确定没有问题？？
            game_menu = Game_menu_f()
            scene_2 = cocos.scene.Scene(VF_Layer(True),Drag(),MouseDisplay(), game_menu)
            director.replace(scenes.transitions.SlideInBTransition(scene_2, duration=1))



class Player_2(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(Player_2, self).__init__()
        # self.do(Repeat(MoveTo((600, 200), 5) + MoveTo((100, 200), 5)))
        self.skin = skeleton.BitmapSkin(animation.my_walk_skeleton.skeleton, animation.my_walk_skin.skin)
        self.add(self.skin)

        self.skin.position = 500, 100
        self.position = 500, 100
        self.life = 100

        img = pyglet.image.load(address + "\dot.png")
        self.spr = cocos.sprite.Sprite(img, opacity=0)  # hide the dot
        self.spr.position = 500, 100
        self.spr.velocity = (0, 0)
        self.spr.do(Mover_2())
        self.life_bar = cocos.sprite.Sprite("img/yellow_bar.png")

        self.add(self.spr)
        self.add(self.life_bar)

        self.status = 3  # 1:walk left 2:walk right 3:stop 4:attack
        self.change = False
        self.block = False  # True means the character is having a continuous movement
        self.near_attack = False
        self.count = 0

        self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)  # 136不够

        fp_1 = open((address_2 + "/animation/MOOOOVE.anim"), "rb+")
        self.walk = cPickle.load(fp_1)

        fp_2 = open((address_2 + "/animation/attack.anim"), "rb+")
        self.attack = cPickle.load(fp_2)

    def remove_all(self):
        if len(self.skin.actions) > 0:
            for i in range(0, len((self.skin.actions))):
                self.skin.remove_action(self.skin.actions[0])

    def update_position(self, dt):
        if not block_2:
            self.skin.position = self.spr.position
            x, y = self.skin.position
            self.life_bar.position = (x, y + 160)
            self.life_bar.scale_x = self.life / 100
            self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)


    def refresh(self):
        global block_2
        self.count = 0
        self.near_attack = False
        self.block = False
        block_2 = self.block

    def status_detect(self, dt):
        self.cshape.center = eu.Vector2(*self.skin.position)  # 优化其放置位置
        if self.block:
            if self.count <= 5:
                self.count += 1
                self.near_attack = True
            else:
                global block_2
                self.refresh()
        else:
            if (keyboard[key.NUM_1]):
                if self.status != 4:
                    self.remove_all()
                    self.status = 4
                    self.change = True
                else:
                    self.change = False
                    self.block = True
                    block_2 = self.block
            elif (keyboard[key.RIGHT]):  # key right and not attack
                if self.status != 2 and self.status != 1:
                    self.remove_all()
                    self.status = 2
                    self.change = True
                else:
                    self.change = False
            elif (keyboard[key.LEFT]):  # key right and not attack
                if self.status != 1:
                    self.remove_all()
                    self.status = 1
                    self.change = True
                else:
                    self.change = False
            else:
                self.remove_all()
                if self.status != 3:
                    self.status = 3
                    self.change = True
                else:
                    self.change = False
        if self.change:
            if self.status == 1:
                self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
            else:
                if self.status == 2:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))
                elif self.status == 4:
                    self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.attack)))  # there is a bug:return attack
                    self.block = True
                    block_2 = self.block
            self.change = False


class Enemy_1(cocos.layer.ScrollableLayer):
    def __init__(self,skele,skin,walk,attack,frozen,num):
        super(Enemy_1, self).__init__()
        self.skin = skeleton.BitmapSkin(skele,skin)
        self.add(self.skin)
        self.num = num
        global block
        block.append(False)

        self.life = 100

        img = pyglet.image.load(address + "\dot.png")
        self.spr = cocos.sprite.Sprite(img, opacity=0)  # hide the dot
        self.spr.velocity = (0, 0)
        self.private()              #私有函数 是它独有的部分
        self.life_bar = cocos.sprite.Sprite("img/yellow_bar.png")

        self.add(self.spr)
        self.add(self.life_bar)

        self.status = 1  # 1:walk left 2:walk right 3:保持态 4:attack 5：beheat
        self.Attack = False         #表示判定开始攻击这一瞬间
        self.auto_attack = False        #表示处于攻击这一整个状态  包括僵直
        self.dead = False
        self.count = 0
        self.beheat = False

        self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)  # 136不够

        fp_1 = open((address_2 + walk), "rb+")
        self.walk = cPickle.load(fp_1)

        fp_2 = open((address_2 + attack), "rb+")
        self.attack = cPickle.load(fp_2)

        fp_3 = open((address_2 + frozen), "rb+")
        self.frozen = cPickle.load(fp_3)

    def private(self):
        self.skin.position = 2300, 60
        self.position = self.skin.position
        self.spr.position = self.skin.position
        self.mover = Mover_3(self.num)
        self.spr.do(self.mover)

    def remove_all(self):
        if len(self.skin.actions) > 0:
            for i in range(0, len((self.skin.actions))):
                self.skin.remove_action(self.skin.actions[0])

    def recover(self):
        self.status = 1

    def update_position(self, dt):          #同步隐藏点的坐标到皮肤上
        if not block[self.num]:
            self.skin.position = self.spr.position
            x, y = self.skin.position
            self.life_bar.position = (x, y + 160)
            self.life_bar.scale_x = self.life / 100
            self.cshape = cm.AARectShape(eu.Vector2(*self.skin.position), 65, 136)

    def status_detect(self, dt):
        if self.life > 0:
            self.cshape.center = eu.Vector2(*self.skin.position)  # 优化其放置位置
            if self.beheat:
                self.remove_all()
                print(self.num)
                self.skin.do(skeleton.Animate(self.frozen))
                block[self.num] = True
                scream = pygame.mixer.Sound(address_2+'/sound/beheat_2.wav')
                scream.set_volume(0.5)
                scream.play()
                self.beheat = False
                self.status = 5
                timer = threading.Timer(1, self.recover)
                timer.start()
            elif self.Attack:
                block[self.num] = True
                self.remove_all()
                self.skin.do(skeleton.Animate(self.attack))
                self.status = 4
                self.Attack = False
                timer = threading.Timer(1, self.recover)
                timer.start()
            elif self.status == 1:
                block[self.num] = False
                self.remove_all()
                self.status = 3
                self.skin.do(cocos.actions.Repeat(skeleton.Animate(self.walk)))


class Teammate(Enemy_1):
    def private(self):
        self.skin.position = 200, 60
        self.position = self.skin.position
        self.spr.position = self.skin.position
        self.mover = Mover_4(self.num)
        self.spr.do(self.mover)


class BackgroundLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()
        bg = cocos.sprite.Sprite("img/bg_3.jpg")
        bg.position = bg.width // 2, bg.height // 2
        self.px_width = bg.width
        self.px_height = bg.height
        self.add(bg)


if __name__ == '__main__':
    # 全局变量
    target_x, target_y = (0, 0)
    block = []
    block_1 = False
    block_1_R = False
    block_2 = False
    img_name = ""
    pygame.mixer.init()
    # 初始化导演
    director.init(width=1201, height=686, caption="BUPT Tower Defence")
    director.window.pop_handlers()
    # 键盘
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    bg_1 = BG(bg_name="img/start_bg.png")  # 1.获取背景图片路径
    # mr_cai = Mr_cai()
    # people_layer = PeopleLayer()
    # spr1_layer = Spirite1()
    scene_1 = cocos.scene.Scene(bg_1)  # 2.把背景图片生成scene
    # scene_1.add(mr_cai, 1)
    # scene_1.add(people_layer, 1)
    # scene_1.add(spr1_layer, 1)
    scene_1_menu = Main_menu()
    scene_1.add(scene_1_menu)  # 4.把按钮加入到scene
    director.run(scene_1)  # 5.启动场景