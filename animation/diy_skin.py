from __future__ import division, print_function, unicode_literals
address = "D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/"
# address = "C:/Users/张帅帅/AppData/Local/Programs/Python/Python37/Lib/site-packages/cocos/resources/"
bodylist=[]
with open(address+"data.txt", "r") as f:  # 打开文件
    for line in f.readlines():
        line = line.strip('\n')
        bodylist.append(line)
# skin = [
#     ('brazo izq', (130, 160), 'd_larm.png', False, False, 0.5),
#     # ('antebrazo izq', (10, 10), weapen, False, False, 0.4),
#     ('muslo izq', (120, 180), 'd_lleg.png', False, False, 0.5),
#     # ('pierna izq', (10, 75), 'gil-bota2.png', False, False, 0.5),
#     ('torso', (145, 150), 'd_body.png', True, True, 0.5),
#     ('cabeza', (130, 170), 'd_head.png', True, True, 0.5),
#     ('brazo der', (120,180), 'd_rarm.png', False, False, 0.5),
#     ('muslo der', (120, 170), 'd_rleg.png', False, False, 0.5),
#   ]
    skin = [
    ('brazo izq', (130, 160), 'img_left_hand.png', False, False, 0.5),
    # ('antebrazo izq', (10, 10), weapen, False, False, 0.4),
    ('muslo izq', (120, 180), 'img_left_leg.png', False, False, 0.5),
    # ('pierna izq', (10, 75), 'gil-bota2.png', False, False, 0.5),
    ('torso', (30, 100), 'img_body.png', True, True, 0.5),
    ('cabeza', (130, 170), 'img_head.png', True, True, 0.5),
    ('brazo der', (-100,220), 'img_right_hand.png', False, False, 0.5),
    ('muslo der', (120, 200), 'img_right_leg.png', False, False, 0.5),
  ]

def refresh():
    with open(address+"data.txt", "r") as f:  # 打开文件
        weapen = f.read()
        print(weapen)
        global  skin
        skin = [
        ('brazo izq', (130, 160), 'img_left_hand.png', False, False, 0.5),
        # ('antebrazo izq', (10, 10), weapen, False, False, 0.4),
        ('muslo izq', (120, 180), 'img_left_leg.png', False, False, 0.5),
        # ('pierna izq', (10, 75), 'gil-bota2.png', False, False, 0.5),
        ('torso', (145, 150), 'img_body.png', True, True, 0.5),
        ('cabeza', (130, 170), 'img_head.png', True, True, 0.5),
        ('brazo der', (120,180), 'img_right_hand.png', False, False, 0.5),
        ('muslo der', (120, 170), 'img_right_leg.png', False, False, 0.5),
        ]

# skin = [
#     ('torso', (45, 70), 'body.png', True, True, 0.5),
#     ('cabeza', (16, -5), 'gil-cara.png', True, True, 0.5),
#   ]
