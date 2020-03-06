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

director.init(width=800, height=600, autoscale=False, resizable=True)
keyboard = key.KeyStateHandler()
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
m_layer= MainLayer()
main_scene = cocos.scene.Scene()

main_scene.schedule_interval(m_layer.update, 1 / 70)
main_scene.add(m_layer)
main_scene.add(MouseDisplay())
# director.window.push_handlers(keyboard)
director.run(main_scene)