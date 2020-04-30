import cocos
from cocos.director import director
from cocos.audio.pygame import mixer, music

director.init()
scene = cocos.scene.Scene()

mixer.init()
music.load(r'D:/MyCode/MyPython/BUPT_TowerDefence/sound/bullet.ogg'.encode())
music.play()
music.set_volume(1)

sprite = cocos.sprite.Sprite("img/bullet.png")
sprite.position = (100,100)

scene.add(sprite)
director.run(scene)