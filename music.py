import cocos
import pygame
from cocos.audio import effect
from cocos.director import director
from cocos.audio.pygame import mixer, music

director.init()
scene = cocos.scene.Scene()

# mixer.init()
# music.load(r'D:/MyCode/MyPython/BUPT_TowerDefence/sound/bullet.ogg'.encode())
# music.play()
# music.set_volume(1)

# sprite = cocos.sprite.Sprite("img/bullet.png")
# sprite.position = (100,100)

# scene.add(sprite)




pygame.mixer.init()
pygame.mixer.music.load('D:/MyCode/MyPython/BUPT_TowerDefence/sound/bgm.mp3',)

s= pygame.mixer.Sound('D:/MyCode/MyPython/BUPT_TowerDefence/sound/bullet.wav')
s.play()

q= pygame.mixer.Sound('D:/MyCode/MyPython/BUPT_TowerDefence/sound/beheat.wav')
q.play()

pygame.mixer.music.play()


director.run(scene)