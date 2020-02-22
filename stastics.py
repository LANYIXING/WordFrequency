#!/usr/bin/env Python
# coding=utf-8

import os
import jieba
import pandas as pd
import codecs

provinces = ['北京', '天津', '河北', '上海', '江苏', '浙江', '福建',
             '山东', '广东', '海南', '四川', '重庆', '贵州', '云南', '西藏', '陕西', '甘肃',
             '青海', '宁夏', '新疆', '广西', '内蒙古', '山西', '安徽', '江西', '河南', '湖北',
             '湖南', '黑龙江', '辽宁', '吉林']


def get_location(province):
    east = ['北京', '天津', '河北', '上海', '江苏', '浙江', '福建',
            '山东', '广东', '海南']
    west = ['四川', '重庆', '贵州', '云南', '西藏', '陕西', '甘肃',
            '青海', '宁夏', '新疆', '广西', '内蒙古']
    middle = ['山西', '安徽', '江西', '河南', '湖北', '湖南']
    northeast = ['黑龙江', '辽宁', '吉林']
    if province in east:
        return "east"
    elif province in west:
        return "west"
    elif province in northeast:
        return "northeast"
    elif province in middle:
        return "middle"


def getCoefficient(obj="A"):
    if obj == "A":
        return 1
    elif obj == "B":
        return 1
    elif obj == "C":
        return 1
    elif obj == "D":
        return 1
    elif obj == "E":
        return 1


def analysis():
    path = "1517/"
    dirs = os.listdir(path)
    i = 0
    for files in dirs: # 对每个政策文件进行循环，分析它的地区和权重
        if files.find("省") != -1:  # 包含'省'
            sep = '省'
            file = files.split(sep, 1)[0]
        else:  # 包含'省'
            sep = '市'
            file = files.split(sep, 1)[0]
        obj = files[0]
        # print(obj)
        coefficient = float(getCoefficient(obj))
        # get province
        jieba.load_userdict('province.txt')
        words = jieba.lcut(file, cut_all=True)
        flag = False
        for word in words:
            for province in provinces:
                if word == province:
                    location = get_location(word)
                    flag = True
                    break
            if flag is True:
                break
        process(path=path, files=files, location=location, coefficient=coefficient)
        i += 1
        print(files)
        print("number:" + str(i) + "is OK!")


def process(path, files, location, coefficient):
    f1 = open(path + files, 'r+', encoding='utf-8')  # f1 政策文件的词频文件
    lines = f1.readlines()  # f1的每个词，得到词语和频数
    for line in lines:
        line = line.replace('\n', '').replace('\r', '')
        l0 = list(line.split(','))
        keyword = l0[0]
        percent = float(l0[2])
        # 打开f2记录已近保存
        ##  不要用r
        f2 = open("new/" + path + location + '.txt', 'r+', encoding='utf-8')
        oldLines = []  # 创建了一个空列表，里面没有元素
        lines2 = f2.readlines()
        for line2 in lines2:  #lines2 将f2的list复制到oldLines
            # print('9999', line)
            if line2 == '\n':
                break
            oldLines.append(line2)
        f2.close()
        #  重开一个保存新的
        f3 = open("new/" + path + location + '.txt', 'w+', encoding='utf-8')
        newlines = oldLines # 复制一个用于改变
        flag = False
        j = 0
        for newline in oldLines:
            if newline == '\n':
                break
            newline1 = newline.replace('\n', '').replace('\r', '')
            l2 = list(newline1.split(','))
            keyword2 = l2[0]
            # print("k1；",keyword,",k2:", keyword2)
            percent2 = float(l2[1])
            count = int(l2[2])
            if keyword == keyword2:
                print("6666666666666666666666666666666666666")
                newPercent = average(percentOringin=percent,
                                     percentNow=percent2, n=count,
                                     coefficient=coefficient)
                count += 1
                del newlines[j]
                newlines.append(str(keyword+','+str(newPercent)+','+str(int(count))+'\n'))
                flag = True
                break
            j += 1
        if flag is False:
            oldLines.append(str(keyword+','+str(percent)+','+'1'+'\n'))
        for oldLine in oldLines:
            # f3.write('%s' % oldLine)
            f3.write(oldLine)
        f3.close()


def average(percentOringin, percentNow, n, coefficient):
    return (percentOringin * n + percentNow*coefficient) / (n + 1)


if __name__ == '__main__':
    analysis()
