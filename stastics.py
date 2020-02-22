import os
import jieba
import pandas as pd
import csv

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
        print("number:" + str(i) + "is OK!")


def process(path, files, location, coefficient):
    f1 = open(path + files, 'r+', encoding='utf-8')  # f1 政策文件的词频文件
    lines = f1.readlines()  # f1的每个词，得到词语和频数
    for line in lines:
        line = line.replace('\n', '').replace('\r', '')
        l0 = list(line.split(','))
        keyword = l0[0]
        percent = float(l0[2])
        # new csv
        f2 = open("new/" + path + location + '.txt', 'r', encoding='utf-8')
        oldLines = []  # 创建了一个空列表，里面没有元素
        for line in f2.readlines():  # 将f2的list复制到oldLines
            # print('9999', line)
            if line == '\n':
                break
            oldLines.append(line)
        f2.close()
        f3 = open("new/" + path + location + '.txt', 'w', encoding='utf-8')
        # newlines = f2.readlines()
        flag = False
        j = 0
        for newline in oldLines:
            if line == '\n':
                # print("7777777777777777777777")
                break
            newline1 = newline.replace('\n', '').replace('\r', '')
            # print(newline1)
            l2 = list(newline1.split(','))
            print(l2)
            keyword2 = l2[0]
            # print("k1；",keyword,",k2:", keyword2)
            percent2 = float(l2[1])
            count = int(l2[2])
            if keyword == keyword2:
                # print(oldLines)
                newpercent = average(percentOringin=percent,
                                     percentNow=percent2, n=count,
                                     coefficient=coefficient)
                count += 1
                # print("6666")
                del oldLines[j]
                oldLines.append(str(keyword+','+str(newpercent)+','+str(int(count))+'\n'))
                # print(oldLines[j])
                flag = True
                break
            j += 1
        if flag is False:
            oldLines.append(str(keyword+','+str(percent)+','+'1'+'\n'))
        for oldLine in oldLines:
            f3.write('%s' % oldLine)
        f1.close()


def average(percentOringin, percentNow, n, coefficient):
    return (percentOringin * n + percentNow*coefficient) / (n + 1)


def process1(path, files, location, coefficient):
    f1 = open(path + files, 'r+')
    lines = f1.readlines()
    dataset = pd.read_csv("new/" + path + location)
    for line in lines:
        l0 = list(line.split(','))
        keyword = l0[0]
        percent = float(l0[2])
        # new csv
        f2 = open("new/" + path + location, "w+")
        newlines = f2.readlines()
        flag = False

        j = 0
        for newline in newlines[1:]:
            l2 = list(newline.split(','))
            keyword2 = l2[0]
            percent2 = float(l2[1])
            count = float(l2[2])
            if keyword == keyword2:
                newpercent = average(percentOringin=percent, percentNow=percent2, n=count)
                count += 1

                flag = True
                break
            j += 1
        if flag is False:
            df = pd.DataFrame(dataset)
            line = {'word': keyword, 'percent': percent, 'count': 1}
            df = df.append(line, ignore_index=True)
            print(df.iloc[0])

        # new_df = pd.DataFrame.from_dict(dict, orient='index')
        df.to_csv("new/" + path + location, mode='a')
        f2.close()
    f1.close()


    print("well done")


if __name__ == '__main__':
    analysis()
