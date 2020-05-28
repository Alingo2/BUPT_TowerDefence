from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('torso', 70, -180.0, Point2(-21.00, -30.00)).add(
    Bone('brazo der', 40, 166.50418844655482, Point2(11.00, -84.00))    .add(
        Bone('antebrazo der', 40, 188.9676098848677, Point2(20.00, -7.00))
)
).add(
    Bone('brazo izq', 80, 162.7435372950183, Point2(89.00, -96.00))    .add(
        Bone('antebrazo izq', 40, 123.24018672001495, Point2(-67.00, -72.00))
)
).add(
    Bone('muslo izq', 40, 185.82860308971078, Point2(-1.00, 5.00))    .add(
        Bone('pierna izq', 40, -69.95371317060682, Point2(0.00, -104.00))
)
).add(
    Bone('muslo der', 40, 190.96525124743613, Point2(-10.00, 20.00))    .add(
        Bone('pierna der', 40, -55.637708424863625, Point2(-11.00, -56.00))
)
).add(
    Bone('cabeza', 20, -9.90592089762, Point2(-2.00, -15.00))
)


skeleton = Skeleton( root_bone )