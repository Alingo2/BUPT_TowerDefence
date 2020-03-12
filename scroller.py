import cocos
from cocos.director import director
import pyglet
from pyglet.window import key

class Mover(cocos.actions.BoundedMove):
    def __init__(self):
        super().__init__(2560,1440)
    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT]-keyboard[key.LEFT])*500
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN])*500
        self.target.velocity = (vel_x, vel_y)
        scroller.set_focus(self.target.x,self.target.y)


class PeopleLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        img = pyglet.image.load(r"D:\MyCode\MyPython\BUPT_TowerDefence\img\girl.png")
        # img = pyglet.image.load(r"D:\CSHE\BUPT_TowerDefence\img\girl.png")

        img_grid = pyglet.image.ImageGrid(img,4,8,item_width = 120,item_height=150)

        anim = pyglet.image.Animation.from_image_sequence(img_grid,0.1,loop = True)

        spr = cocos.sprite.Sprite(anim)
        spr.position = 50,50
        spr.velocity = (0,0)

        spr.do(Mover())
        self.add(spr)

class BackgroundLayer(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()

        bg = cocos.sprite.Sprite("img/bg_4.jpg")

        bg.position = bg.width//2,bg.height//2

        self.px_width = bg.width
        self.px_height = bg.height

        self.add(bg)

if __name__ == "__main__":

    director.init(width=1280, height=720)
    director.window.pop_handlers()

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)


    people_layer = PeopleLayer()
    bg_layer = BackgroundLayer()

    scroller = cocos.layer.ScrollingManager()
    scroller.add(bg_layer)
    scroller.add(people_layer)

    main_scene = cocos.scene.Scene()
    main_scene.add(scroller,0)

    director.run(main_scene)