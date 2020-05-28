from skimage import io,color,measure,morphology
import skimage.morphology as sm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as pg
# address=('D:\\CSHE\BUPT_TowerDefence\image\\my_man2.png')
address=('D:\\MyCode\\MyPython\\BUPT_TowerDefence\\image\\demo1.png')
#img0=io.imread('C:\\Users\MA\Desktop\image\\15.png')

#img=color.rgb2gray(io.imread('C:\\Users\MA\Desktop\image\\15.png',as_gray='True'))
#img_four=pg.imread('C:\\Users\MA\Desktop\image\\15.png')
img0=io.imread(address)

img=color.rgb2gray(io.imread(address,as_gray='True'))
img_four=pg.imread(address)
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



skeleton =morphology.skeletonize(img_full)
guanjies=[]
img_skeleton=np.zeros((rows,cols))
row=img_full.shape[0]
col=img_full.shape[1]
for i in range(0,row):
    for j in range(0,col):
        if skeleton[i][j]!=0 :
            guanjies.append([i,j])
            img_skeleton[i][j]=1

img_judge=np.zeros((row,col))
guanjie_judge=[]
k=0
guanjie_x=[]
guanjie_y=[]
for guanjie in guanjies:
    temp=0
    for i in range(guanjie[0]-1,guanjie[0]+2):
        for j in range(guanjie[1]-1,guanjie[1]+2):
            temp=temp+img_skeleton[i][j]
    if temp>3:
        img_judge[guanjie[0],guanjie[1]]=1
        k=k+1
        guanjie_judge.append([guanjie[0],guanjie[1]])
        guanjie_x.append(guanjie[0])
        guanjie_y.append(guanjie[1])
guanjie_max_x=max(guanjie_x)
guanjie_min_x=min(guanjie_x)
guanjie_max_y=max(guanjie_y)
guanjie_min_y=min(guanjie_y)
print(k)
middle_y=sum(guanjie_y)/len(guanjie_y)
head_finish=guanjie_min_x
head123=[0,0,0,0,0,0,0,0,0,0]
for head in range(guanjie_min_x,guanjie_max_x):
    head_counter = 0
    for x in guanjie_x:
        if x<head:
            head_counter=head_counter+1
    if k / 2.0 >= head_counter :
        head123[0] = head
    if k / 2.25 >= head_counter :
        head123[1] = head
    if k / 2.5 >= head_counter :
        head123[2] = head
    if k / 2.75 >= head_counter :
        head123[3] = head
    if k / 3 >= head_counter :
        head123[4] = head
    if k / 3.25 >= head_counter :
        head123[5] = head
    if k / 3.5 >= head_counter :
        head123[6] = head
    if k / 3.75 >= head_counter :
        head123[7] = head
    if k / 4 >= head_counter :
        head123[8] = head
    if k / 4 >= head_counter :
        head123[9] = head

judge_head=[0,0,0,0,0,0,0,0,0,0]
j=-1
for head in head123:
    j=j+1
    for i in range(0,cols):
        if img_full[head][i]==1:
            judge_head[j]=judge_head[j]+1
print("judge_head",judge_head)
j=judge_head.index(min(judge_head))
head_finish=head123[j]
print("j:",j)
print("head123:",head123)


leg_finish=guanjie_min_x
leg123=[0,0,0,0,0,0,0,0,0,0]
for leg in range(guanjie_min_x,guanjie_max_x):
    leg_counter = 0
    for x in guanjie_x:
        if x<leg:
            leg_counter=leg_counter+1
    if k / 2.0 >= leg_counter :
        leg123[0] = leg
    if k / 1.9 >= leg_counter :
        leg123[1] = leg
    if k / 1.8 >= leg_counter :
        leg123[2] = leg
    if k / 1.7 >= leg_counter :
        leg123[3] = leg
    if k / 1.6 >= leg_counter :
        leg123[4] = leg
    if k / 1.5 >= leg_counter:
        leg123[5] = leg
    if k / 1.4 >= leg_counter :
        leg123[6] = leg
    if k / 1.3 >= leg_counter :
        leg123[7] = leg
    if k / 1.3 >= leg_counter:
        leg123[8] = leg
    if k / 1.3 >= leg_counter:
        leg123[9] = leg

judge_leg=[0,0,0,0,0,0,0,0,0,0]
j=-1
for leg in leg123:
    j=j+1
    for i in range(0,cols):
        if img_full[leg][i]==1:
            judge_leg[j]=judge_leg[j]+1
print("judge_leg",judge_leg)
j=judge_leg.index(max(judge_leg))
leg_finish=leg123[j]
change=40
leg_finish=leg_finish+change
print("j:",j)
print("leg123:",leg123)


temp_hand=np.zeros(2)
judge=1
for i in range(0,cols):
    if img_full[leg_finish][i]==1 and judge==1:
        temp_hand[0]=i
        judge=0
    if img_full[leg_finish][i]==0 and judge==0:
        temp_hand[1]=i
        judge=1
print("temp_hand:",temp_hand)
for i in range(img_full.shape[0]):
    for j in range(img_full.shape[1]):
        if img_full[i][j]==0:
            img_four[i][j][3]=0
img_head=img_four[0:head_finish,:,:]
img_body=img_four[head_finish:leg_finish,int(temp_hand[0]):int(temp_hand[1]),:]
img_left_leg=img_four[leg_finish:max(I),min(J):int(middle_y),:]
img_right_leg=img_four[leg_finish:max(I),int(middle_y):max(J),:]
img_left_hand=img_four[head_finish:leg_finish,0:int(temp_hand[0]),:]
img_right_hand=img_four[head_finish:leg_finish,int(temp_hand[1]):cols,:]
plt.figure('morphology',figsize=(12,8))

plt.subplot(3,4,1)
plt.title('origin image')
plt.imshow(img0)
plt.axis('off')

plt.subplot(3,4,2)
plt.title('gray')
plt.imshow(img,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,3)
plt.title('morphological image')
plt.imshow(dst,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,4)
plt.title("skelen image")
plt.imshow(img2,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,5)
plt.title('full')
plt.imshow(img_full,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,6)
plt.title('skeleton')
plt.imshow(skeleton,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,7)
plt.title('img_left_leg')
plt.imshow(img_left_leg,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,8)
plt.title('img_head')
plt.imshow(img_head,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,9)
plt.title('img_body')
plt.imshow(img_body,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,10)
plt.title('img_right_leg')
plt.imshow(img_right_leg,plt.cm.gray)
plt.axis('off')


plt.subplot(3,4,11)
plt.title('img_left_hand')
plt.imshow(img_left_hand,plt.cm.gray)
plt.axis('off')

plt.subplot(3,4,12)
plt.title('img_right_hand')
plt.imshow(img_right_hand,plt.cm.gray)
plt.axis('off')

pg.imsave('D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/img_right_leg.png',img_right_leg)
pg.imsave('D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/img_right_leg',img_left_leg)
pg.imsave('D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos/resources/img_right_leg',img_left_hand)
pg.imsave('D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos//resources/img_right_hand.png',img_right_hand)
pg.imsave('D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos//resources/img_head.png',img_head)
pg.imsave('D:/代码编辑器/SoulOfPython/Lib/site-packages/cocos//resources/img_body.png',img_body)

plt.show()
