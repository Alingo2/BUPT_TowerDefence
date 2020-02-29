
import cocos
 
class hello(cocos.layer.Layer):         #继承了一个hello类
    def __init__(self):
        super (hello, self).__init__()          #super() 函数是用于调用父类函数的一个方法
        # 创建标签！！！！！！！
        label = cocos.text.Label('BUPT_TowerDefence',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        # 获得导演窗口的宽度和高度，是一个二元组
        width, height = cocos.director.director.get_window_size()
        # 设置标签的位置
        label.position = width // 2, height // 2  #    //整数除法 去掉小数部分
        # 添加标签到HelloWorld层
        self.add(label)
 
 
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
        cocos.director.director.run(main_scence)
    def item2_callback(self,value):
        print('item2')

class BG(cocos.layer.Layer):
    def __init__(self,bg_name):
        super(BG,self).__init__()
        d_width, d_height = cocos.director.director.get_window_size()
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
        mapbutton=map_button(pic_1='img/level_1.jpg',pic_2='img/level_2.jpg',poi=[(800,339),(800,220)])
        game_map_scence.add(mapbutton)
        cocos.director.director.run(game_map_scence)
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
    def pic_2_callback(self):
        print("第二关")

        
if __name__=='__main__':
    #初始化导演
    cocos.director.director.init(width=1011,height=598,caption="BUPT Tower Defence")
    #创建层   的实例
    layer=hello()
    #创建场景   添加层进来
    # main_scence=cocos.scene.Scene(layer)

    start_bg=BG(bg_name="img/start.jpeg")           #1.获取背景图片路径
    main_pic_scence=cocos.scene.Scene(start_bg)     #2.把背景图片生成scene
    mainpicmenu=menu_button(pic_1='img/start.png',pic_2='img/setting.png' ,pic_3='img/help.png',poi=[(900,339),(900,220),(900,100)])    #3.生成按钮
    main_pic_scence.add(mainpicmenu)                #4.把按钮加入到scene
    #启动场景
    cocos.director.director.run(main_pic_scence)    #5.启动场景