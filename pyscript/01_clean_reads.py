#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import  argparse
import sys
import  os
import gzip
from collections import defaultdict

    # def IsSubString(SubStrList,Str)
    # def GetFileList(FindPath,FlagStr=[]):
    # 功能:读取指定目录下特定类型的文件名列表
def IsSubString(SubStrList,Str):
    '''
    #判断字符串Str是否包含序列SubStrList中的每一个子字符串
    #>>>SubStrList=['F','EMS','txt']
    #>>>Str='F06925EMS91.txt'
    #>>>IsSubString(SubStrList,Str)#return True (or False)
    '''
    flag=True
    for substr in SubStrList:
        if not(substr in Str):
            flag=False

    return flag
def GetFileList(FindPath,FlagStr=[]):
    '''
    #获取目录中指定的文件名
    #>>>FlagStr=['F','EMS','txt'] #要求文件名称中包含这些字符
    #>>>FileList=GetFileList(FindPath,FlagStr) #
    '''
    import os
    FileList=[]
    FileNameList = []
    FileNames=os.listdir(FindPath)
    if (len(FileNames)>0):
       for fn in FileNames:
           if (len(FlagStr)>0):
               #返回指定类型的文件名
               if (IsSubString(FlagStr,fn)):
                   fullfilename=os.path.join(FindPath,fn)
                   FileList.append(fullfilename)
                   FileNameList.append(fn)
           else:
               #默认直接返回所有文件名
               fullfilename=os.path.join(FindPath,fn)
               FileList.append(fullfilename)
               FileNameList.append(fn)

    #对文件名排序
    if (len(FileList)>0):
        FileList.sort()

    return (FileList,FileNameList)


def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--inputdir', dest='inputdir', metavar='inputdir', type=str, required=True,
                        help="input file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="out put dir")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    inputdir = params['inputdir']
    outputdir = params['outputdir']
    files,_ = GetFileList(inputdir)
    dirs = defaultdict(list)
    for value in files:
        if os.path.isdir(value):
            sample_fq,fnlist = GetFileList(value,FlagStr=['fq'])
            dirs[value]=fnlist
    for value in set(dirs.values()):
        with gzip.open("%s/%s.qz"%(outputdir,value),"wb") as fqout:
            for key,file_value in dirs:
                if value in file_value:
                    with open("%s/%s" % (key,value),"r") as fq:
                        fqout.write(fq)








