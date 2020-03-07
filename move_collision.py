import cocos
from cocos.layer import *
from pyglet.window import key
import cocos.collision_model as cm
import cocos.euclid  as eu
from cocos.actions import MoveTo, Repeat

barrier_area=([65,1135,167,267],[65,1135,385,485])


class Mover(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT]-keyboard[key.LEFT])*500
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN])*500
        self.target.velocity = (vel_x, vel_y)
        self.target.cshape.center = eu.Vector2(*self.target.position)

class Player(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("img/car.png")
        self.position = 200, 200
        self.velocity = (0,0)

        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)

        self.do(Mover())

class Enemy(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("img/level_1_road.png")
        self.position = 600,400

        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)

        #self.do(Repeat(MoveTo((100,500),2) + MoveTo((1000,500),2)))

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)
class MainLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.enemy = Enemy()

        self.add(self.player,1)
        self.add(self.enemy,0)

        # self.coll_manager = cm.CollisionManagerBruteForce()
        self.coll_manager = cm.CollisionManagerGrid(0,1280,0,720,70,70)
        self.coll_manager.add(self.player)


    def update(self,dt):
        self.enemy.update_()
        self.tag = False
        for barrier in barrier_area:
            if self.coll_manager.objs_into_box(barrier[0],barrier[1],barrier[2],barrier[3]):
                self.tag = True
                break
        if self.tag:
            self.player.color = [255, 0, 0]
        else:
                self.player.color = [255,255,255]
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

if __name__ == '__main__':
    director.init(width=1280,height = 720, resizable =True)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    main_scene = cocos.scene.Scene()
    game_layer = MainLayer()
    
    main_scene.schedule_interval(game_layer.update,1/70)
    main_scene.add(game_layer)
    main_scene.add(MouseDisplay())
    director.run(main_scene)