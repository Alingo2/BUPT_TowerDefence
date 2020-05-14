from __future__ import division, print_function, unicode_literals
from cocos.skeleton import Bone, Skeleton

#torso:躯干 brazo der:右臂  antebrazo der：前臂
#brazo izq:左臂  muslo izq：左大腿    pierna izq：左腿
#muslo der：右大腿 pierna der：右腿
#cabeza:头
def Point2(*args): return args
# root_bone = Bone('torso', 70, -180.0, Point2(0.00, 0.00)).add(
#     Bone('cabeza', 20, -9.90592089762, Point2(2.00, -94.00))
#  )
root_bone = Bone('point', 70, 180, Point2(6.00, -46.00)).add(
    Bone('torso', 3, 0.0, Point2(0,0)).add(Bone('armor', 1, 180.0, Point2(65,-15)))).add(
    Bone('brazo der', 25, 152.308491558, Point2(34.00, -67.00)).
        add(Bone('antebrazo der', 40, 152.308491558, Point2(-4.00, -36.00)))
).add(
    Bone('muslo izq', 20, 179.587915727, Point2(-5.00, -60.00))
).add(
    Bone('muslo der', 20, 179.587915727, Point2(24.00, -60.00))
).add(
    Bone('point1', 3, -9.90592089762, Point2(0,0)).add(Bone('point1', 15, -9.90592089762, Point2(0,0)).add(Bone('cabeza', 20, -9.90592089762, Point2(-4.00, -94.00)).add(
Bone('helmet',1,180, Point2(117,46))
    )
)
))


skeleton = Skeleton( root_bone )
