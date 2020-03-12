import cocos
import pyglet
import math
from cocos.actions import *
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
import root_bone
import root_skin
import my_sample_skeleton
import my_sample_skin
import model1_skeleton
import model1_skin
import _pickle as cPickle


class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.text = cocos.text.Label('Mouse @', font_size=18,
                                     x=100, y=240)
        self.add(self.text)

    def on_mouse_motion(self, x, y, dx, dy):
        #dx,dy为向量,表示鼠标移动方向
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        #按下鼠标按键不仅更新鼠标位置,还改变标签的位置.这里使用director.get_virtual_coordinates(),用于保证即使窗口缩放过也能正确更新位置,如果直接用x,y会位置错乱,原因不明
        self.text.element.text = 'Mouse @ {}, {}, {}, {}'.format(x, y,buttons, modifiers)
        self.text.element.x, self.text.element.y = director.get_virtual_coordinates(x, y)
        global target_x,target_y
        target_x,target_y = director.get_virtual_coordinates(x, y)

 
class main_menu(cocos.menu.Menu):
    def __init__(self):
        super(main_menu, self).__init__()
        #文本菜单项  （文字，回掉函数）
        item1=cocos.menu.MenuItem('开始',self.item1_callback)
        # 开关菜单项  （文字，回掉函数，状态）
        item2 = cocos.menu.ToggleMenuItem('音效', self.item2_callback,False)
        #创建菜单（添加项的列表，选中效果，未选中效果）
        self.create_menu([item1,item2],
                            selected_effect=cocos.menu.shake(),
                            unselected_effect=cocos.menu.shake_back(),
                                    )

        #改变字体
        self.font_item['font_size']=22
        #选中时
        self.font_item_selected['font_size']=33


    def item1_callback(self):
        print('item1')
        main_scence=cocos.scene.Scene(layer)
        director.run(main_scence)
    def item2_callback(self,value):
        print('item2')

class MainLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        self.player = p_layer()
        self.enemy = Enemy()
        self.life_bar=life_bar()
        self.enemy_num = 1
        self.add(self.player,1)
        self.add(self.enemy,0)
        self.add(self.life_bar,2)
        self.coll_manager = cm.CollisionManagerBruteForce()

    def update(self,dt):
        if self.enemy_num>0:
            if self.enemy.life>=0 :
                self.enemy.update_()
                self.life_bar.position = (enemy_x,enemy_y+50)
                self.life_bar.scale_x=self.enemy.life/100
                self.enemy.life-=0.2
                if self.coll_manager.they_collide(self.player,self.enemy):
                    self.player.color = [255,0,0]
                    self.player.stop()
                else:
                    self.player.color = [255,255,255]
            else:
                self.enemy_num -= 1
                self.remove(self.enemy)
                self.remove(self.life_bar)
                del self.enemy
                del self.life_bar


class BG(cocos.layer.Layer):        #看是否需要传入background.position
    def __init__(self,bg_name):
        super(BG,self).__init__()
        d_width, d_height = director.get_window_size()
        # 创建背景精灵
        background = cocos.sprite.Sprite(bg_name)
        background.position = d_width // 2, d_height // 2
        self.add(background)


class button(cocos.menu.Menu):      #button父类  传入图片 位置
    def __init__(self):
        super(button, self).__init__()
 
        # 也可以改变图片项的大小
        # 改变字体
        self.font_item['font_size'] = 66
        # 选中时
        self.font_item_selected['font_size'] = 66
        #改变颜色 rgba
        self.font_item['color'] = (255,255,255,25)
        # 选中时
        self.font_item_selected['color'] = (25,255,255,255)
 
class menu_button(button):      #button下的子类 专门写自己的回调函数
    def __init__(self,pic_1,pic_2,pic_3,poi):
        super(button, self).__init__()
        pic_1=cocos.menu.ImageMenuItem(pic_1,self.pic_1_callback)
        pic_2= cocos.menu.ImageMenuItem(pic_2, self.pic_2_callback)
        pic_3 = cocos.menu.ImageMenuItem(pic_3, self.pic_3_callback)
        #创建菜单（添加项的列表，自定义布局位置）
        self.create_menu([pic_1,pic_2,pic_3],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(poi),   #三个按钮的位置
                         selected_effect=cocos.menu.zoom_in(),
                         unselected_effect=cocos.menu.zoom_out())
    def pic_1_callback(self):
        print("start")
        bg_2 = BG(bg_name="img/bg_2.png")
        scence_2=cocos.scene.Scene(bg_2)
        mapbutton=map_button(pic_1='img/level_1_icon.png',pic_2='img/level_2_icon.png',poi=[(600,270),(800,270)])
        scence_2.add(mapbutton)
        director.replace(scenes.transitions.SlideInBTransition(scence_2, duration=1))
    def pic_3_callback(self):
        print("help")
    def pic_2_callback(self):
        print("setting")


class setting_button(button):
    def __init__(self,pic_1,poi,setting = 1):
        self.setting = setting
        super(button, self).__init__()
        pic_setting = BG(bg_name = "img/return.png")
        pic_1 = cocos.menu.ImageMenuItem(pic_1, self.pic_1_callback)
        self.create_menu([pic_1],
                    layout_strategy=cocos.menu.fixedPositionMenuLayout(poi))
    def pic_1_callback(self):
        if self.setting:
            print('show setting')
        else:
            print('hide setting')
        self.setting = 1-self.setting       #取反


class map_button(button):      #button下的子类 专门写自己的回调函数
    def __init__(self,pic_1,pic_2,poi):
        super(button, self).__init__()
        pic_1=cocos.menu.ImageMenuItem(pic_1,self.pic_1_callback)
        pic_2= cocos.menu.ImageMenuItem(pic_2, self.pic_2_callback)
        #创建菜单（添加项的列表，自定义布局位置）
        self.create_menu([pic_1,pic_2],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(poi),   #三个按钮的位置
                         selected_effect=cocos.menu.zoom_in(),
                         unselected_effect=cocos.menu.zoom_out())
    def pic_1_callback(self):
        print("第一关")
        #这次创建的窗口带调整大小的功能
        bg_3 = BG(bg_name="img/bg_3.jpg")
        scene_3 = cocos.scene.Scene(MouseDisplay(),setting_button(pic_1 = "img/setting.png", poi=[(964,30)]))
        scene_3.add(bg_3)

        spr1_layer = Sprite1()
        people_layer = PeopleLayer()
        bones = bone()
        moving_man = Moving_man()
        mr_cai = Mr_cai()
        walk=Mooooove()
        m_layer= MainLayer()
        scene_3.schedule_interval(m_layer.update, 1 / 70)
        scene_3.add(m_layer)

        scene_3.add(people_layer,1)
        scene_3.add(spr1_layer,0)
        scene_3.add(bones,2)
        scene_3.add(moving_man,3)
        scene_3.add(mr_cai,4)
        scene_3.add(walk,5)
        scene_3.add(MouseDisplay())


        director.replace(scenes.transitions.SlideInBTransition(scene_3, duration=1))
    def pic_2_callback(self):
        print("第二关")

class Enemy(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("img/sanjiguan.png")
        self.position = 700,600
        self.life=100
        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)

        self.do(Repeat(MoveTo((100,500),4) + MoveTo((1000,500),4)))

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)
        global enemy_x,enemy_y
        enemy_x,enemy_y = self.cshape.center


class P_move(Driver):
    def step(self,dt):
        x,y = self.target.position
        self.target.speed = 200
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(pow(dx,2) + pow(dy,2))
        if dy > 0 :
            if dx > 0:
                self.angle = 180*math.atan(dx/dy)/math.pi
            elif dx < 0:
                self.angle = 360 - 180*math.atan(-dx/dy)/math.pi
            else:
                self.angle = self.angle
        else:
            if dx > 0:
                self.angle = 180 - 180*math.atan(dx/-dy)/math.pi
            elif dx < 0:
                self.angle = 180 + 180*math.atan(-dx/-dy)/math.pi
            else:
                self.angle = self.angle
        self.target.do(MoveTo((target_x,target_y),duration = distance/self.target.speed)| RotateTo(self.angle,0))
        super(P_move, self).step(dt)

class p_layer(cocos.sprite.Sprite):
    def __init__(self):
        super(p_layer, self).__init__("img/car.png")
        self.position = 200, 500
        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)
        self.do(P_move())
    def stop(self):
        global target_x,target_y
        target_x,target_y= self.position

class draw_rec(cocos.layer.util_layers.ColorLayer):
    def __init__(self,w,h):
        super().__init__(255, 0,0,255,width =w,height=h)
        

class life_bar(cocos.sprite.Sprite):
    def __init__(self):
        super(life_bar, self).__init__("img/yellow_bar.png")


class Mover(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.D] - keyboard[key.A])*500
        vel_y = (keyboard[key.W] - keyboard[key.S])*500
        self.target.velocity = (vel_x, vel_y)

class Sprite1(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        #img = pyglet.image.load(r"D:\MyCode\MyPython\BUPT_TowerDefence\img\man.png")
        img = pyglet.image.load(r"D:\CSHE\BUPT_TowerDefence\img\man.png")
        img_grid = pyglet.image.ImageGrid(img,1,4,item_width=100,item_height = 100)     #1row 4col each one is 100*100


        anim = pyglet.image.Animation.from_image_sequence(img_grid[0:],0.2,loop = True) #define the range of the photo and the second parameter is to descibe the period

        spr = cocos.sprite.Sprite(anim)
        spr.position = 200,500
        self.add(spr)


class PeopleLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        #img = pyglet.image.load(r"D:\MyCode\MyPython\BUPT_TowerDefence\img\girl.png")
        img = pyglet.image.load(r"D:\CSHE\BUPT_TowerDefence\img\girl.png")

        img_grid = pyglet.image.ImageGrid(img,4,8,item_width = 120,item_height=150)

        anim = pyglet.image.Animation.from_image_sequence(img_grid,0.1,loop = True)

        spr = cocos.sprite.Sprite(anim)
        spr.position = 640,500
        spr.velocity = (0,0)

        spr.do(Mover())
        self.add(spr)

        
class Moving_man(cocos.layer.Layer):
    def __init__(self):
        super( Moving_man, self ).__init__()

        x,y = director.get_window_size()
        self.skin = skeleton.BitmapSkin(my_sample_skeleton.skeleton, my_sample_skin.skin)
        self.add( self.skin )
        x, y = director.get_window_size()
        self.skin.position = 100, 120
        #fp = open(r"D:/MyCode/MyPython/BUPT_TowerDefence/my_SAMPLE.anim","rb+")
        fp = open(r"D:/CSHE/BUPT_TowerDefence/my_SAMPLE.anim","rb+")
        anim = cPickle.load(fp)
        self.skin.do( cocos.actions.Repeat( skeleton.Animate(anim) ) )
        self.do(Repeat(MoveTo((800,0),5)+MoveTo((100,0),5)))


class Mr_cai(cocos.layer.Layer):
    def __init__(self):
        super( Mr_cai, self ).__init__()

        x,y = director.get_window_size()
        self.skin = skeleton.BitmapSkin(model1_skeleton.skeleton, model1_skin.skin)
        #self.skin = skeleton.BitmapSkin(my_sample_skeleton.skeleton, my_sample_skin.skin)
        self.add( self.skin )
        x, y = director.get_window_size()
        self.skin.position = 300, 150
        #fp = open(r"D:/MyCode/MyPython/BUPT_TowerDefence/Mr_cai.anim","rb+")
        fp = open(r"D:/CSHE/BUPT_TowerDefence/Mr_cai.anim", "rb+")
        #fp = open(r"D:/CSHE/BUPT_TowerDefence/MOOOOVE.anim","rb+")
        anim = cPickle.load(fp)
        self.skin.do( cocos.actions.Repeat( skeleton.Animate(anim) ) )

class Mooooove(cocos.layer.Layer):
    def __init__(self):
        super( Mooooove, self ).__init__()

        x,y = director.get_window_size()
        #self.skin = skeleton.BitmapSkin(model1_skeleton.skeleton, model1_skin.skin)
        self.skin = skeleton.BitmapSkin(my_sample_skeleton.skeleton, my_sample_skin.skin)
        self.add( self.skin )
        x, y = director.get_window_size()
        self.skin.position = 300, 300
        #fp = open(r"D:/MyCode/MyPython/BUPT_TowerDefence/Mr_cai.anim","rb+")
        fp = open(r"D:/CSHE/BUPT_TowerDefence/MOOOOVE.anim","rb+")
        anim = cPickle.load(fp)
        self.skin.do( cocos.actions.Repeat( skeleton.Animate(anim) ) )

class bone(cocos.layer.Layer):
    def __init__(self):
        super(bone,self).__init__()

        x,y = director.get_window_size()

        self.skin = cocos.skeleton.BitmapSkin(root_bone.skeleton,root_skin.skin)

        self.add(self.skin)
        x,y = director.get_window_size()
        self.skin.position = 300,500


if __name__=='__main__':
    #全局变量
    colli= False
    target_x,target_y = (0,0)

    enemy_x,enemy_y = 0,0
    collision_manager = CollisionManager()
    #初始化导演
    director.init(width=1201,height=686,caption="BUPT Tower Defence")
    director.window.pop_handlers()
    #键盘
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    bg_1 = BG(bg_name="img/start_bg.png")           #1.获取背景图片路径
    scene_1=cocos.scene.Scene(bg_1)     #2.把背景图片生成scene
    scene_1_menu = menu_button(pic_1='img/start.png',pic_2='img/setting.png' ,pic_3='img/help.png',poi=[(1100,339),(1100,220),(1100,100)])    #3.生成按钮
    scene_1.add(scene_1_menu)                #4.把按钮加入到scene
    director.run(scene_1)    #5.启动场景