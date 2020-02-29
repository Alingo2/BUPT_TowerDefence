
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


class main_pic_menu(cocos.menu.Menu):
    def __init__(self):
        super(main_pic_menu, self).__init__()
 
        # 也可以改变图片项的大小
        # 改变字体
        self.font_item['font_size'] = 66
        # 选中时
        self.font_item_selected['font_size'] = 66
        #改变颜色 rgba
        self.font_item['color'] = (255,255,255,25)
        # 选中时
        self.font_item_selected['color'] = (25,255,255,255)
 
        menu_start=cocos.menu.ImageMenuItem('img/start.png',self.menu_start_callback)
        menu_setting= cocos.menu.ImageMenuItem('img/setting.png', self.menu_setting_callback)
        help_setting = cocos.menu.ImageMenuItem('img/help.png', self.menu_help_callback)
        #创建菜单（添加项的列表，自定义布局位置）
        self.create_menu([menu_start,menu_setting,help_setting],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout([(900,339),(900,220),(900,100)]),   #三个按钮的位置
                         selected_effect=cocos.menu.zoom_in(),
                         unselected_effect=cocos.menu.zoom_out())
 
 
    def menu_start_callback(self):
        print("start")
        # mainmenu=main_menu()
        # main_scence=cocos.scene.Scene(mainmenu)
        # cocos.director.director.run(main_scence)
        game_map=BG(bg_name="img/game_map.png")
        cocos.director.director.run(game_map)
    def menu_help_callback(self):
        print("help")
    def menu_setting_callback(self):
        print("setting")

if __name__=='__main__':
    #初始化导演
    cocos.director.director.init(width=1011,height=598,caption="BUPT Tower Defence")
    #创建层   的实例
    layer=hello()
    #创建场景   添加层进来
    # main_scence=cocos.scene.Scene(layer)

    start_bg=BG(bg_name="img/start.jpeg")
    main_pic_scence=cocos.scene.Scene(start_bg)
    mainpicmenu=main_pic_menu()
    main_pic_scence.add(mainpicmenu)

    # mainmenu=main_menu()
    # main_scence=cocos.scene.Scene(mainmenu)
    #启动场景
    cocos.director.director.run(main_pic_scence)