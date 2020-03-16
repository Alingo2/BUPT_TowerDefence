import cocos
import pyglet
from cocos.director import director
from pyglet.window import mouse

address = "D:\MyCode\MyPython\BUPT_TowerDefence\img"

class Sprite1(cocos.layer.Layer):

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


if __name__=='__main__':
    #全局变量
    #初始化导演
    director.init(width=1201,height=686,caption="BUPT Tower Defence")
    director.window.pop_handlers()
    #键盘

    spr1_layer = Sprite1()
    scene_1=cocos.scene.Scene()     #2.把背景图片生成scene
    scene_1.add(spr1_layer)                #4.把按钮加入到scene
    director.run(scene_1)    #5.启动场景