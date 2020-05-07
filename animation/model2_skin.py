from __future__ import division, print_function, unicode_literals
with open(r"D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/data.txt", "r") as f:  # 打开文件
    weapen = f.read()

skin = [
    ('brazo izq', (10, 10), 'gil-mano2.png', False, False, 0.5),
    ('antebrazo izq', (20, 22), weapen, False, False, 0.4),
    ('muslo izq', (10, 70), 'gil-bota2.png', False, False, 0.5),
    #('pierna izq', (10, 75), 'gil-bota2.png', False, False, 0.5),
    ('cabeza', (31, 44), 'gil-peluca.png', True, True, 0.5),
    ('torso', (25, 91), 'gil-cuerpo.png', True, True, 0.5),
    ('cabeza', (16, 18), 'gil-cara.png', True, True, 0.5),
    ('antebrazo der', (33, 5), 'pistal1.png', False, False, 0.4),
    ('brazo der', (8, 50), 'gil-mano1.png', False, False, 0.5),
    ('muslo der', (10, 70), 'gil-bota1.png', False, False, 0.5),
    #('pierna der', (15, 67), 'gil-bota1.png', False, False, 0.5),
  ]


# skin = [
#     ('torso', (45, 70), 'body.png', True, True, 0.5),
#     ('cabeza', (16, -5), 'gil-cara.png', True, True, 0.5),
#   ]
