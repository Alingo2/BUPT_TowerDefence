import cocos
import math
from cocos.actions import *
from cocos.sprite import Sprite
import cocos.collision_model as cm
from cocos.actions import Driver
from cocos.director import director
import pyglet
from cocos.actions import Move
from pyglet.window import key
from cocos import layer
from pyglet.window import mouse
from cocos.collision_model import *
from cocos.skeleton import Bone, Skeleton
from cocos import skeleton
import root_bone
import root_skin
import my_sample_skeleton
import my_sample_skin
import _pickle as cPickle

colli= False
target_x,target_y = (0,0)
enemy_x,enemy_y = 0,0
collision_manager = CollisionManager()

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
                self.life_bar.position = (enemy_x,enemy_y+30)
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


class Enemy(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("img/player.png")
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
        self.target.cshape.center = eu.Vector2(*self.target.position)
        super(P_move, self).step(dt)


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
        

class draw_rec(cocos.layer.util_layers.ColorLayer):
    def __init__(self,w,h):
        super().__init__(255, 0,0,255,width =w,height=h)
        

class life_bar(cocos.sprite.Sprite):
    def __init__(self):
        super(life_bar, self).__init__("img/yellow_bar.png")
        self.position = 700,610


class p_layer(cocos.sprite.Sprite):
    def __init__(self):
        super(p_layer, self).__init__("img/car.png")
        self.position = 200, 500
        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)
        self.do(P_move())
    def stop(self):
        global target_x,target_y
        target_x,target_y= self.position


class Mover(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT]-keyboard[key.LEFT])*500
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN])*500
        self.target.velocity = (vel_x, vel_y)


class Sprite1(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(r"D:\MyCode\MyPython\BUPT_TowerDefence\img\man.png")
        # img = pyglet.image.load(r"D:\CSHE\BUPT_TowerDefence\img\man.png")
        img_grid = pyglet.image.ImageGrid(img,1,4,item_width=100,item_height = 100)     #1row 4col each one is 100*100


        anim = pyglet.image.Animation.from_image_sequence(img_grid[0:],0.2,loop = True) #define the range of the photo and the second parameter is to descibe the period

        spr = cocos.sprite.Sprite(anim)
        spr.position = 200,500
        self.add(spr)


class PeopleLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(r"D:\MyCode\MyPython\BUPT_TowerDefence\img\girl.png")
        # img = pyglet.image.load(r"D:\CSHE\BUPT_TowerDefence\img\girl.png")

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
        self.skin.position = x/2, y/2
        fp = open(r"D:/MyCode/MyPython/BUPT_TowerDefence/my_SAMPLE.anim","rb+")
        # fp = open(r"D:/CSHE/BUPT_TowerDefence/my_SAMPLE.anim","rb+")
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



if __name__ == "__main__":
    director.init(width=1280, height=720)
    director.window.pop_handlers()

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)


    spr1_layer = Sprite1()
    people_layer = PeopleLayer()
    bones = bone()
    moving_man = Moving_man()

    m_layer= MainLayer()
    main_scene = cocos.scene.Scene()
    main_scene.schedule_interval(m_layer.update, 1 / 70)
    main_scene.add(m_layer)

    main_scene.add(people_layer,1)
    main_scene.add(spr1_layer,0)
    main_scene.add(bones,2)
    main_scene.add(moving_man,3)
    main_scene.add(MouseDisplay())

    director.run(main_scene)