from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -185.13746808221953, Point2(37.00, -7.00))


skeleton = Skeleton( root_bone )