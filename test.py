# -*- coding: utf-8 -*-
import sys
import importlib

importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os
import pandas as pd

'''
 解析txt文件中
'''

def stopWordsList():
    stopwords = []
    for word in open('chineseStopWords.txt', encoding="utf-8"):
        stopwords.append(word.strip())
    return stopwords

def solve():
    path = "C:/Users/63505/Desktop/文本数据/文本数据/2016/"
    year = "2016/"
    dirs = os.listdir(path)
    import jieba

    for files in dirs:
        excludes = {"\n","\t"}  # {"将军","却说","丞相"}
        # txt = open(r"C:\Users\63505\Desktop\文本数据\文本数据\2020\A山西省人大.txt", "r").read()
        path_join = os.path.join(path, files)
        print(path_join)
        txt = open(path_join, 'r', encoding="utf-8").read()
        jieba.load_userdict('userdict.txt')
        words = jieba.lcut(txt)
        countAllWord = 0  # type: int
        counts = {}
        stopwords = stopWordsList()
        for word in words:
            if len(word) == 1:  # 排除单个字符的分词结果
                continue
            elif word in stopwords:
                continue
            elif word == "/t":
                continue
            else:
                counts[word] = counts.get(word, 0) + 1
                countAllWord += 1

        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        items = items[:20]
        word = ['a', 'b']
        count = [0, 0]
        for i in range(2):
            word[i], count[i] = items[i]
        # filename = os.path.splitext(files)[0]
        (filename, extension) = os.path.splitext(files)
        path_join1 = os.path.join(year, filename + "_" + word[0]+"_"+word[1]+".txt ")
        fo = open(path_join1, "w+", encoding='utf-8')
        # fo = open(rpath1
        #           + word[0] + "_" + word[1] + files, "wb")
        # print(items[:10])
        for item in items:
            # print(type(item))
            ls = list(item)
            percent = ls[1]/countAllWord
            # print(type(ls))
            # temp = [ls[0], ls[1], int(ls[1])/countAllWord]
            # print(temp)
            # fo.write(",".join(temp) + "\n")
            fo.write(ls[0] +"," + str(ls[1]) +"," +
                     str(percent)+'\n')
        fo.close()
        print("well done")


if __name__ == '__main__':
    # parse()
    solve()
    # plot()
