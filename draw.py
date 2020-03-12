# -*- coding: utf-8 -*-
"""
Created on Sat May 19 17:34:54 2018

@author: xxx
"""

import cv2 as cv
import numpy as np


def nothing(x):
    pass

# 当鼠标按下时变为 True
drawing = False
# 如果 mode 为 True 绘制矩形。按下 'm' 变成绘制曲线
mode = True
ix, iy = -1, -1

#创建回调函数
def draw_circle(event, x, y, flags, param):
    r = cv.getTrackbarPos('R', 'image')
    g = cv.getTrackbarPos('G', 'image')
    b = cv.getTrackbarPos('B', 'image')
    color = (b, g, r)

    global ix, iy, drawing, mode
    # 当按下左键是返回起始位置坐标
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
#        当鼠标左键按下并移动是绘制图形。event 可以查看移动, flag 查看是否按下
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
        if drawing == True:
            if mode == True:
                cv.rectangle(img, (ix, iy), (x, y), color, -1)
            else:
                # 绘制圆圈，小圆点连在一起就成了线，3代表画笔的粗细
                cv.circle(img, (ix, iy), 3, color, -1)
                # 下面注释的代码是起始点为圆心，起点到终点为半径
#               r = int(np.sqrt((x - ix)**2 + (y - iy)**2))
#               cv.circle(img, (x, y), r, (0, 0, 255), -1)
#        当鼠标松开停止绘画
    elif event == cv.EVENT_LBUTTONUP:
            drawing == False
#            if mode == True:
#                cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
#            else:
#            cv.circle(img, (x, y), 5, (0, 0, 255), -1)

#创建一幅黑色图形
img = np.zeros((512, 512, 3), np.uint8)
cv.namedWindow('image')

cv.createTrackbar('R', 'image', 0, 255, nothing)
cv.createTrackbar('G', 'image', 0, 255, nothing)
cv.createTrackbar('B', 'image', 0, 255, nothing)
cv.setMouseCallback('image', draw_circle)

while(1):
    cv.imshow('image', img)
    k = cv.waitKey(1)&0xFF
    if k == ord('m'):
        mode = not mode
    elif k==27:
        break


cv.destroyAllWindow()