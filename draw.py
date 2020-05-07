# -*- coding: utf-8 -*-
import cv2
import numpy as np
def nothing(x):
    pass
#赋值命令
drawing = False
mode = False
ix,iy = -1,-1

# 创建回调函数
def draw_circle(event,x,y,flags,param):
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    color = (b,g,r)
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy=x,y

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing:
            if mode:
                cv2.rectangle(img,(ix,iy),(x,y),color,-1)
            else:
                cv2.circle(img,(x,y),3,color,-1)
                # r=int(np.sqrt((x-ix)**2+(y-iy)**2))
                # cv2.circle(img,(x,y),r,(0,0,255),-1)

    elif event==cv2.EVENT_LBUTTONUP:
        drawing==False
        # if mode==True:
        # cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        # else:
        # cv2.circle(img,(x,y),5,(0,0,255),-1)
img = np.zeros((512,512,3),np.uint8)

def Draw():
    cv2.namedWindow('image')
    cv2.createTrackbar('R', 'image', 0, 255, nothing)
    cv2.createTrackbar('G', 'image', 0, 255, nothing)
    cv2.createTrackbar('B', 'image', 0, 255, nothing)
    cv2.setMouseCallback('image', draw_circle)
    global ix,iy,drawing,mode
    while(1):
        cv2.imshow('image',img)
        k=cv2.waitKey(1)&0xFF
        if k==ord('m'):
            mode = not mode
        elif k==ord('s'):
            pic_name = input("Enter your input: ")
            print("Received input is : ", pic_name)
            cv2.imwrite(r"D:/MyCode/MyPython/BUPT_TowerDefence/img/"+ pic_name + ".png", img)
            cv2.imencode('.png', img)[1].tofile(r"D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/"+ pic_name + ".png")
            file = open("D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/data.txt",'w')
            file.write(pic_name + ".png")

            print("successfully saved")
            return(pic_name)
        elif k==27:
            break