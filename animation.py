import cocos
from cocos.director import director
import pyglet
from pyglet.window import key
from cocos.skeleton import Bone, Skeleton
from cocos import skeleton
import root_bone
import root_skin


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
        img_grid = pyglet.image.ImageGrid(img,1,4,item_width=100,item_height = 100)     #1row 4col each one is 100*100


        anim = pyglet.image.Animation.from_image_sequence(img_grid[0:],0.2,loop = True) #define the range of the photo and the second parameter is to descibe the period

        spr = cocos.sprite.Sprite(anim)
        spr.position = 200,500
        self.add(spr)


class PeopleLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(r"D:\MyCode\MyPython\BUPT_TowerDefence\img\girl.png")
        img_grid = pyglet.image.ImageGrid(img,4,8,item_width = 120,item_height=150)

        anim = pyglet.image.Animation.from_image_sequence(img_grid,0.1,loop = True)

        spr = cocos.sprite.Sprite(anim)
        spr.position = 640,500
        spr.velocity = (0,0)

        spr.do(Mover())
        self.add(spr)

class bone(cocos.layer.Layer):
    def __init__(self):
        super(bone,self).__init__()

        x,y = director.get_window_size()

        self.skin = cocos.skeleton.BitmapSkin(root_bone.skeleton,root_skin.skin)

        self.add(self.skin)
        x,y = director.get_window_size()
        self.skin.position = x/2,y/2

if __name__ == "__main__":
    director.init(width=1280, height=720)
    director.window.pop_handlers()

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)


    spr1_layer = Sprite1()
    people_layer = PeopleLayer()
    bones = bone()

    test_scene = cocos.scene.Scene()

    test_scene.add(spr1_layer,0)
    test_scene.add(people_layer,1)
    test_scene.add(bones,2)

    director.run(test_scene)