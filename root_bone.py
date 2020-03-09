from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -186.88284572663372, Point2(2.00, 23.00))


skeleton = Skeleton( root_bone )