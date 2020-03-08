from cocos.skeleton import Bone, Skeleton

def Point2(*args): return args

root_bone = Bone('body', 70, -180.0, Point2(0, 0)).add(
    Bone('upper_arm', 30, 120, (0, -70)).add(
        Bone('lower_arm', 30, 30, (0, -30))
    )
)

skeleton = Skeleton(root_bone)

skin = [
    ('body', (25, 91), 'gil-cuerpo.png', True, True, 0.5),
    ('lower_arm', (0, 0), 'gil-mano2.png', False, False, 0.5),
    ('upper_arm', (0, 0), 'gil-brazo1.png', False, False, 0.5),
  ]