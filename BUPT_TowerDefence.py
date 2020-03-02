import cocos
from cocos.director import director
import pyglet


class KeyDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(KeyDisplay,self).__init__()

        self.text = cocos.text.Label('Keys: ', font_size=18, x=100, y=280)
        self.add(self.text)

        self.keys_pressed = set()

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        self.text.element.text = 'Keys: ' + ','.join(key_names)

    def on_key_press(self, key, modifiers):
        #按下按键自动触发本方法
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        #松开按键自动触发本方法
        self.keys_pressed.remove(key)
        self.update_text()


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
        print(director.get_virtual_coordinates(x, y))

 
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

class BG(cocos.layer.Layer):
    def __init__(self,bg_name,):
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
        game_map=BG(bg_name="img/game_map.png")
        game_map_scence=cocos.scene.Scene(game_map)
        mapbutton=map_button(pic_1='img/level_1_icon.jpg',pic_2='img/level_2_icon.jpg',poi=[(800,339),(800,220)])
        game_map_scence.add(mapbutton)
        director.replace(game_map_scence)
    def pic_3_callback(self):
        print("help")
    def pic_2_callback(self):
        print("setting")


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
        level_1 = BG(bg_name="img/level_1.jpg")
        main_scene = cocos.scene.Scene( KeyDisplay(), MouseDisplay(),level_1)
        director.replace(main_scene)
    def pic_2_callback(self):
        print("第二关")

class Player(cocos.sprite.Sprite):
    def __init__(self, ):
        super(player, self).__init__('img/player.png')
        self.x = 200
        self.y = 200
        self.add(background)
        self.a = 0
        self.v = 1
#人物转身
    def rotate(self, x0, y0):
        tann = abs(y0-self.y)/(x0-self.x)
        radian = math.atan(tann)
        angle = radian*180/math.pi   #角度制的角
        if x0 < self.x and y0 < self.y:
            angle = angle+180
        if x0 < self.x and y0 > self.y:
            angle = 180-angle
        if x0 > self.x and y0 < self.y:
            angle = -angle
        duration = abs(angle)/200.0
        action = RotateTo(angle,duration)
        self.do(action)
#人物移动
    def move(self, x0, y0):
        duration = sqrt((x0 - self.x)^2 + (y0 - self.y)^2)/self.v
        action = MoveTo((x0, y0), duration)
        sprite.do(action)
        self.x = x0
        self.y = y0

if __name__=='__main__':
    #初始化导演
    director.init(width=1011,height=598,caption="BUPT Tower Defence")
    start_bg=BG(bg_name="img/start.jpeg")           #1.获取背景图片路径
    main_pic_scence=cocos.scene.Scene(start_bg)     #2.把背景图片生成scene
    mainpicmenu=menu_button(pic_1='img/start.png',pic_2='img/setting.png' ,pic_3='img/help.png',poi=[(900,339),(900,220),(900,100)])    #3.生成按钮
    main_pic_scence.add(mainpicmenu)                #4.把按钮加入到scene
    director.run(main_pic_scence)    #5.启动场景