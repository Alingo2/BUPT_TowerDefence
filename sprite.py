import cocos
from cocos.sprite import Sprite
from cocos.director import director

class Sprite1(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        spr = cocos.sprite.Sprite("img/car.png")

        spr.position = 400,360

        self.add(spr)

class Sprite2(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("img/player.png")

        self.position = 640,360


class life(cocos.layer.util_layers.ColorLayer):
    def __init__(self,w,h):
        super().__init__(0, 255,0,255,width =w,height=h )
        


if __name__ == "__main__":
    enemy_x,enemy_y = 0,0
    director.init(width=1280, height=720)
    director.window.pop_handlers()

    spr1_layer = Sprite1()
    spr2_layer = Sprite2()

    test_scene = cocos.scene.Scene()

    test_scene.add(spr1_layer,0)
    test_scene.add(spr2_layer,1)
    life_bar = life(200,400)
    test_scene.add(life_bar)

    director.run(test_scene)