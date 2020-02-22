#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 将doc或docx 转成pdf"""
__author__ = 'Lanyixing'

# python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout=1000 pypiwin32

import os
import sys
import fnmatch
import win32com.client

# PATH = os.path.abspath(os.path.dirname('C:\Users\63505\Desktop\文本数据\文本数据')
PATH_DATA = os.path.abspath(r'C:\Users\63505\Desktop\文本数据\文本数据\2017')
str = '*.docx'
# str = '*.doc'
if str == '*.docx':
    length = 4
else:
    length = 3
# 主要执行函数
def main():
    wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")
    try:
        for root, dirs, files in os.walk(PATH_DATA):
            for _dir in dirs:
                pass
            for _file in files:
                if not fnmatch.fnmatch(_file, str):
                    continue
                word_file = os.path.join(root, _file)
                wordapp.Documents.Open(word_file)
                docastxt = word_file[:-length] + 'txt'
                wordapp.ActiveDocument.SaveAs(docastxt,
                                              FileFormat=win32com.client.constants.wdFormatText,
                                              Encoding=65001)
                wordapp.ActiveDocument.Close()
    finally:
        wordapp.Quit()
    print('well done!')


if __name__ == '__main__':
    main()
