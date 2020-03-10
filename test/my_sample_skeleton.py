from __future__ import division, print_function, unicode_literals

from cocos.skeleton import Bone, Skeleton
def Point2(*args): return args
root_bone = Bone('torso', 70, -180.0, Point2(0.00, 0.00)).add(
    Bone('brazo der', 40, 152.308491558, Point2(34.00, -67.00))    .add(
        Bone('antebrazo der', 40, 121.203546669, Point2(-4.00, -36.00))
)
)

skeleton = Skeleton( root_bone )
