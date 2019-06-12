import cv2
import os
import fnmatch
import numpy as np
import queue
from PIL import Image
import pytesseract


def two_value(filedir, imgName):  # 图像二值化,参数是图像的路径
    filename = imgName[0] + '-result1.png'  # 二值化结果的路径
    imgName = filedir + '/' + imgName
    im = cv2.imread(imgName)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # 图像灰度处理,
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    cv2.imwrite(filename, th1)
    return th1


def cleanTheBorder(img, imgName):
    filename = imgName[0] + '-result2.png'  # 清除边框结果的路径

    h, w = img.shape  # 高和宽
    for y in range(0, w):
        for x in range(0, h):
            if y < 10 or y > w - 10:  # 左边和右边
                img[x, y] = 255
            if x < 6 or x > h - 6:  # 上边和下边
                img[x, y] = 255

    cv2.imwrite(filename, img)
    return img


def cleanTheLine(img, imgName):  # 8邻域降噪，
    filename = './output/' + imgName[0] + '-result3.png'

    h, w = img.shape
    # ！！！opencv矩阵点是反的
    # img[1,2] 1:图片的高度，2：图片的宽度
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if img[x + 1, y + 1] > 245:
                count = count + 1
            if img[x + 1, y - 1] > 245:
                count = count + 1
            if img[x - 1, y + 1] > 245:
                count = count + 1
            if img[x - 1, y - 1] > 245:
                count = count + 1
            if count > 4:
                img[x, y] = 255
    cv2.imwrite(filename, img)
    return img


def floodFillDeNoise(img, imgName, area):
    filename = imgName[0] + '-result4.png'
    h, w = img.shape
    color = 1
    colorCount = [0] * 255
    mask = np.zeros([h + 2, w + 2], np.uint8)
    for y in range(0, w - 1):  # 每找到一个灰度值为0的点，即黑点，就将该点的灰度值改为color
        for x in range(0, h - 1):
            if img[x, y] == 0:
                cv2.floodFill(img, mask, (y, x), (color), (20), (20), 4 | (
                        252 << 8) | cv2.FLOODFILL_FIXED_RANGE)  # 第三个参数是开始染色的点，第四个参数是要染的颜色，第五、第六个参数表示如果 点的灰度值在起始点-20到起始点+20之间，就进行染色
                color = color + 1
    for y in range(0, w - 1):
        for x in range(0, h - 1):
            if img[x, y] != 255:  # 如果不是白点
                colorCount[img[x, y] - 1] += 1  # 记录对应灰度值的点的个数

    for y in range(0, w - 1):
        for x in range(0, h - 1):
            if colorCount[img[x, y] - 1] < area:  # 如果某个连通域的面积小于area阈值，就将其判断为干扰线或干扰点，就将这个区域修改为白色
                img[x, y] = 255

    for y in range(0, w - 1):
        for x in range(0, h - 1):
            if img[x, y] < 255:
                img[x, y] = 0

    cv2.imwrite(filename, img)
    return img


def cfs(img, x, y):
    xaxis = []
    yaxis = []
    visited = set()
    q = queue.Queue()  # 先进先出队列
    q.put((x, y))  # 坐标加入队列
    visited.add((x, y))  # 坐标加入集合
    offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 四邻域

    while not q.empty():  # 从第一个黑色点开始，向周围扩展，找到该黑色点所能连通到的最大范围，然后返回左右上下边界的坐标
        x1, y1 = q.get()  # 获取并弹出队首元素

        for xoffset, yoffset in offsets:  # 判断队首元素坐标的上下左右是否访问过
            x_neighbor, y_neighbor = x1 + xoffset, y1 + yoffset

            if (x_neighbor, y_neighbor) in (visited):  # 访问了就跳过
                continue  # 已经访问过了

            visited.add((x_neighbor, y_neighbor))

            try:
                if img[x_neighbor, y_neighbor] == 0:  # 如果该点的邻居是黑点，把邻居的坐标加入到队列中
                    xaxis.append(x_neighbor)
                    yaxis.append(y_neighbor)
                    q.put((x_neighbor, y_neighbor))

            except IndexError:
                pass
            # print(xaxis)

    if (len(xaxis) == 0 | len(yaxis) == 0):
        xmax = x + 1
        xmin = x
        ymax = y + 1
        ymin = y

    else:
        xmax = max(xaxis)
        xmin = min(xaxis)
        ymax = max(yaxis)
        ymin = min(yaxis)
        # ymin,ymax=sort(yaxis)

    return ymax, ymin, xmax, xmin  # 上下左右边界的坐标


def detectFgPix(img, xmax):  # 找黑点作为起点,xmax是为了防止重复找到相同的字符
    h, w = img.shape[:2]
    for y in range(xmax + 1, w):
        for x in range(h):
            if img[x, y] == 0:
                return x, y


def CFS(img):
    zoneL = []
    zoneWB = []  # 各个区块的横轴[起始点，终点]坐标
    zoneHB = []  # 各个区块的纵轴[起始点，终点]坐标
    xmax = 0  # 记录上一个区块的横轴终点
    for i in range(10):
        try:
            x, y = detectFgPix(img, xmax)
            xmax, xmin, ymax, ymin = cfs(img, x, y)
            L = xmax - xmin
            H = ymax - ymin
            zoneL.append(L)
            zoneWB.append([xmin, xmax])
            zoneHB.append([ymin, ymax])
        except:
            return zoneL, zoneWB, zoneHB
    return zoneL, zoneWB, zoneHB


def cutting_img(im, im_position, img, xoffset=2, yoffset=2):
    filename = '' + imgName[0]
    # 识别出的字符个数
    im_number = len(im_position[1])  # zoneWB的元素个数，也就是字符个数
    # 切割字符
    for i in range(im_number):
        im_start_X = im_position[1][i][0] - xoffset
        im_end_X = im_position[1][i][1] + xoffset
        im_start_Y = im_position[2][i][0] - yoffset
        im_end_Y = im_position[2][i][1] + yoffset
        cropped = im[im_start_Y:im_end_Y, im_start_X:im_end_X]
        cv2.imwrite(filename + '-cutting-' + str(i) + '.png', cropped)


filedir = 'D:\\python\\20190611'
for file in os.listdir(filedir):  # 对于pic文件夹中的每张jpg图
    if fnmatch.fnmatch(file, '*.png'):
        imgName = file
    print(imgName)
    im = two_value(filedir, imgName)  # 二值化灰度化
    im = cleanTheBorder(im, imgName)  # 清除边框
    im = cleanTheLine(im, imgName)  # 8邻域降噪
    im = floodFillDeNoise(im, imgName, 230)  # 将连通区域小于300的都判断为干扰线，修改为白色
    imPosition = CFS(im)
    maxL = max(imPosition[0])  # imPosition[0]是zoneL列表
    minL = min(imPosition[0])
    cutting_img(im, imPosition, imgName, 1, 1)  # 切割出每个字符

    cuttingImgNum = 0

    for file1 in os.listdir(''):  # 计算切割后的单个字符有几个
        str_img = ''
        if fnmatch.fnmatch(file1, '%s-cutting-*.png' % imgName[0]):
            cuttingImgNum += 1

    for i in range(cuttingImgNum):  # 对于每个字符
        try:
            file2 = './output/%s-cutting-%s.png' % (imgName[0], i)
            str_img = str_img + pytesseract.image_to_string(Image.open(file2), lang='eng',
                                                            config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')  # 单个字符是10，一行文本是7
        except Exception as err:
            pass
    print('识别为：%s' % str_img)
