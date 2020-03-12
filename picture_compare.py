from PIL import Image
import numpy as np
"""
dhash算法：
1。缩小图片：收缩到9*8的大小，以便它有72的像素点
2.转化为灰度图：把缩放后的图片转化为256阶的灰度图。（具体算法见平均哈希算法步骤）
3.计算差异值：dHash算法工作在相邻像素之间，这样每行9个像素之间产生了8个不同的差异，一共8行，则产生了64个差异值
4.获得指纹：如果左边的像素比右边的更亮，则记录为1，否则为0.
5.最后比对两张图片的指纹，获得汉明距离即可。
"""
im1 = Image.open(r'D:/MyCode/MyPython/BUPT_TowerDefence/img/help.png')
im2 = Image.open(r'D:/MyCode/MyPython/BUPT_TowerDefence/img/setting.png')


def cut_image(image, hash_size=8):
    # 将图像缩小成9*8并转化成灰度图
    image1 = image.resize((hash_size+1,hash_size),Image.ANTIALIAS).convert('L')
    pixel = list(image1.getdata())
    return pixel

print(cut_image(im1))
imag1 = cut_image(im1)
imag2 = cut_image(im2)


def trans_hash(lists):
    '''
    比较列表中相邻元素大小
    '''
    j = len(lists)-1
    hash_list = []
    m, n = 0,1
    for i in range(j):
        if lists[m]>lists[n]:
            hash_list.append(1)
        else:
            hash_list.append(0)
        m +=1
        n +=1
    return hash_list


def difference_value(image_lists):
    '''
    获得图像差异值并获得指纹
    :param image:
    :return:
    '''
    assert len(image_lists) == 72, "size error"
    m, n = 0, 9
    hash_list = []
    for i in range(0,8):
        slc = slice(m,n)
        image_slc = image_lists[slc]
        hash_list.append(trans_hash(image_slc))
        m +=9
        n +=9
    return hash_list


ha_lists1 = difference_value(imag1)
ha_lists2 = difference_value(imag2)
print(ha_lists1)
print(ha_lists2)
print(abs(np.array(ha_lists2)-np.array(ha_lists1)))


def calc_distance(image1, image2):
    image1_lists = cut_image(image1)
    image2_lists = cut_image(image2)
    hash_lists1 = difference_value(image1_lists)
    hash_lists2 = difference_value(image2_lists)
    calc = abs(np.array(hash_lists2)-np.array(hash_lists1))
    return calc