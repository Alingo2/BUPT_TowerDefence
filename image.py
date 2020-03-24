from skimage import io,color,measure,morphology
import skimage.morphology as sm
import matplotlib.pyplot as plt
import numpy as np
#灰度
img0=color.rgb2gray(io.imread('img\\15.png'))
img=color.rgb2gray(io.imread('img\\15.png',as_gray='True'))
img2=img
rows=img0.shape[0]
cols=img0.shape[1]

for i in range(rows):
    for j in range(cols):
        if img[i][j]>0.4:
            img[i][j]=0
        else :
            img[i][j]=1

dst=sm.opening(img,sm.disk(1))  #用边长为9的圆形滤波器进行膨胀滤波
#收集点
I=[]
J=[]
for i in range(rows):
    for j in range(cols):
        if dst[i][j]==1:
            I.append(i)
            J.append(j)

#计算重心
center_i=sum(I)/len(I)
max_i=max(I)
min_i=min(I)
judge1=(center_i-min_i)/(max_i-min_i)
print("竖直重心：",center_i)#竖直重心
print(judge1)
center_y=sum(J)/len(J)
print("水平重心",center_y)#水平重心
#长宽比 （判断类型）
judge2=(max(J)-min(J))/(max(I)-min(I))
print("长宽比",judge2)
judge=0.5*judge1+0.5*judge2
print("judge:",judge)
if (judge<1):
    print("人")
else:
    print("动物")

contours = measure.find_contours(dst, 0.5)#获取图像轮廓（所有的  对应图4） 返回很多个数组 每个数组是个闭合的轮廓线

#骨架图必须是实心的
for i in range(rows):
    for j in range(cols):
        img2[i][j] = 0
dots=[]     #有可能 有重复
img_full=np.zeros((rows,cols))
for i in enumerate(contours):
    for j in i[1]:
        img2[int(j[0])][int(j[1])]=1
        dots.append([int(j[0]),int(j[1])])

for i in range(min(I),max(I)):      #判断该点是否在轮廓线内 8个方向是否有点
    for j in range(min(J),max(J)):
        Pro=P1=P2=P3=P4=P5=P6=P7=P8= 0
        for dot in dots[0:8000]:

            if (dot[0] == i  and dot[1] - j > 0):
                P3 = 1
            if (dot[0] == i  and dot[1] - j < 0):
                P4 = 1
            if (dot[1] == j and dot[0] - i > 0):
                P5 = 1
            if (dot[1] == j and dot[0] - i < 0):
                P6 = 1
            if (dot[0] - i == -dot[1] + j and dot[0] - i > 0):
                P7 = 1
            if (dot[0] - i == -dot[1] + j and dot[0]-i<0):
                P8 = 1
            if (dot[0] - i == dot[1] - j and dot[0] - i > 0):
                P1 = 1
            if (dot[0] - i == dot[1] - j and dot[0]-i<0):
                p2 = 1
        Pro=P1+P2+P3+P4+P5+P6+P7+P8
        if(Pro>=6):     #可能有缺损  所有没有取8
            img_full[i][j]=1
        else:
            img_full[i][j]=0
#以上生成了 倒数第二图
plt.figure('morphology',figsize=(12,8))
plt.subplot(2,3,1)
plt.title('origin image')
plt.imshow(img0)
plt.axis('off')

plt.subplot(2,3,2)
plt.title('gray')
plt.imshow(img,plt.cm.gray)
plt.axis('off')

plt.subplot(2,3,3)
plt.title('morphological image')
plt.imshow(dst,plt.cm.gray)
plt.axis('off')

plt.subplot(2,3,4)
plt.title("skelen image")
plt.imshow(img2,plt.cm.gray)
skeleton =morphology.skeletonize(dst)
print("skeleton:",skeleton)
plt.axis('off')

plt.subplot(2,3,5)
plt.title('full')
plt.imshow(img_full,plt.cm.gray)
plt.axis('off')

skeleton =morphology.skeletonize(img_full)
plt.subplot(2,3,6)
plt.title('skeleton')
plt.imshow(skeleton,plt.cm.gray)
plt.axis('off')
plt.show()






