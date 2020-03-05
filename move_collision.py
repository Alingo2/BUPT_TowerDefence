import cocos
from cocos.layer import *
from pyglet.window import key
import cocos.collision_model as cm
import cocos.euclid  as eu
from cocos.actions import MoveTo, Repeat


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
        bar=cocos.Canvas.
        self.position = 200, 200
        self.velocity = (0,0)

        self.cshape = cm.AARectShape(eu.Vector2(*self.position),self.width/2,self.height/2)

        self.do(Mover())

class Enemy(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("img/level_1_road.png")
        self.position = 700,600

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

        self.coll_manager = cm.CollisionManagerBruteForce()

    def update(self,dt):
        self.enemy.update_()
        print(self.coll_manager.they_collide(self.player,self.enemy))
        if self.coll_manager.they_collide(self.player,self.enemy):
            self.player.color = [255,0,0]
        else:
            self.player.color = [255,255,255]
if __name__ == '__main__':
    director.init(width=1280,height = 720, resizable =True)

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)
    bar=p_bar()
    main_scene = cocos.scene.Scene()
    game_layer = MainLayer()
    
    main_scene.schedule_interval(game_layer.update,1/60)
    main_scene.add(game_layer)
    main_scene.add(bar)

    director.run(main_scene)