from skimage import io,color,measure,morphology
import skimage.morphology as sm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as pg
img0=io.imread('D:\\MyCode\\MyPython\\BUPT_TowerDefence\\image\\17.png')

img=color.rgb2gray(io.imread('D:\\MyCode\\MyPython\\BUPT_TowerDefence\\image\\17.png',as_gray='True'))
img_four=pg.imread('D:\\MyCode\\MyPython\\BUPT_TowerDefence\\image\\17.png')
img2=img
rows=img0.shape[0]
cols=img0.shape[1]
I=[]
J=[]
for i in range(rows):
    for j in range(cols):
        if img[i][j]>0.4:
            img[i][j]=0
        else :
            img[i][j]=1

dst=sm.opening(img,sm.disk(1))  #用边长为9的圆形滤波器进行膨胀滤波
for i in range(rows):
    for j in range(cols):
        if dst[i][j]==1:
            I.append(i)
            J.append(j)
print("I:",min(I),max(I))
print("J:",min(J),max(J))
center_i=sum(I)/len(I)
max_i=max(I)
min_i=min(I)
judge1=(center_i-min_i)/(max_i-min_i)
print("竖直重心：",center_i)#竖直重心
print(judge1)
center_y=sum(J)/len(J)
print("水平重心",center_y)#水平重心
judge2=(max(J)-min(J))/(max(I)-min(I))
print("长宽比",judge2)
judge=0.5*judge1+0.5*judge2
print("judge:",judge)
if (judge<1):
    print("人")
else:
    print("动物")

contours = measure.find_contours(dst, 0.5)

for i in range(rows):
    for j in range(cols):
        img2[i][j] = 0
dots=[]
img_full=np.zeros((rows,cols))
for i in enumerate(contours):
    for j in i[1]:
        img2[int(j[0])][int(j[1])]=1
        dots.append([int(j[0]),int(j[1])])
print("len(dots):",len(dots))
dots_different=[]
for dot in dots:
    if(dot not in dots_different):
        dots_different.append(dot)
dots = dots_different
dots_zip=[]
for i in range(0,len(dots),2):
    dots_zip.append(dots[i])
dots=dots_zip
print("len(dots):",len(dots))
print("len(dots_different):",len(dots_different))
for i in range(min(I),max(I),3):
    for j in range(min(J),max(J),3):
        Pro=P1=P2=P3=P4=P5=P6=P7=P8= 0
        for dot in dots:
            if (abs(dot[0] - i )<=2  and dot[1] - j > 0):
                P3 = 1
            if (abs(dot[0] - i )<=2  and dot[1] - j < 0):
                P4 = 1
            if (abs(dot[1] - j )<=2 and dot[0] - i > 0):
                P5 = 1
            if (abs(dot[1] - j )<=2 and dot[0] - i < 0):
                P6 = 1
            if (abs(dot[0] - i -( -dot[1] + j))<= 2 and dot[0] - i > 0):
                P7 = 1
            if (abs(dot[0] - i -( -dot[1] + j ))<=2and dot[0]-i<0):
                P8 = 1
            if (abs(dot[0] - i -( dot[1] - j))<=2 and dot[0] - i > 0):
                P1 = 1
            if (abs(dot[0] - i -( dot[1] - j))<=2 and dot[0]-i<0):
                p2 = 1
        Pro=P1+P2+P3+P4+P5+P6+P7+P8
        if(Pro>=7):
            img_full[i][j]=1
        else:
            img_full[i][j]=0
for i in range(min(I),max(I),3):
    for j in range(min(J),max(J),3):
        if img_full[i][j]==1:
            img_full[i-1][j-1]=img_full[i-1][j]=img_full[i-1][j+1]=img_full[i][j-1]=img_full[i][j+1]=img_full[i+1][j-1]=img_full[i+1][j]=img_full[i+1][j+1]=1
for i in range(img_full.shape[0]):
    for j in range(img_full.shape[1]):
        if img_full[i][j]==0:
            img_four[i][j][3]=0
pg.imsave('D:\\MyCode\\MyPython\\BUPT_TowerDefence\\img\\hi.png',img_four)
print("1")