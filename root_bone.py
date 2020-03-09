from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -123.54528007752278, Point2(29.00, -6.00))


skeleton = Skeleton( root_bone )