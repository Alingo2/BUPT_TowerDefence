from __future__ import division, print_function, unicode_literals
address = "D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/"
# address = "C:/Users/张帅帅/AppData/Local/Programs/Python/Python37/Lib/site-packages/cocos/resources/"
bodylist=[]

def refresh(name):
    global  skin
    name = name.strip('.png')
    print("角色名:"+name)
    skin = [
    ('brazo izq', (0, 120), name+'_right_hand.png', False, False, 0.5),
    # ('antebrazo izq', (10, 10), weapen, False, False, 0.4),
    ('muslo izq', (-10, 75), name+'_right_leg.png', False, False, 0.5),
    # ('pierna izq', (10, 75), 'gil-bota2.png', False, False, 0.5),
    ('torso', (50, 50), name+'_body.png', True, True, 0.5),
    ('cabeza', (150, 30), name+'_head.png', True, True, 0.5),
    ('brazo der', (80,90), name+'_left_hand.png', False, False, 0.5),
    ('muslo der', (70, 80),name+'_left_leg.png', False, False, 0.5),
  ]
