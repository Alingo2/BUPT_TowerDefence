import cocos
from cocos.sprite import Sprite
from cocos.director import director
import pyglet
from cocos.actions import Move
from pyglet.window import key
from cocos import layer

director.init(width=800, height=600, autoscale=False, resizable=True)
keyboard = key.KeyStateHandler()

class P_move(Move):
    def step(self,dt):
        self.target.velocity=((keyboard[key.RIGHT]-keyboard[key.LEFT])*100,(keyboard[key.UP] - keyboard[key.DOWN])*100)
        super(P_move, self).step(dt)

class p_layer(layer.Layer):
    def __init__(self):
        super(p_layer, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite("assets/img/car.png")

        # We set the position (standard stuff)
        self.sprite.position = 200, 500


        # Then we add it
        self.add(self.sprite)

        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        self.sprite.do(P_move())
p= p_layer()
main_pic_scence=cocos.scene.Scene()     #2.把背景图片生成scene
main_pic_scence.add(p)
director.run(main_pic_scence)