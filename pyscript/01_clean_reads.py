#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import  argparse
import sys
import  os
import gzip
import time
from multiprocessing import Process
from multiprocessing import Pool
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

def write_gzip(commands):
    print "subprocess pid:%s" % os.getpid()
    os.popen(commands)

if __name__ == '__main__':
    params = read_params(sys.argv)
    inputdir = params['inputdir']
    outputdir = params['outputdir']
    files,_ = GetFileList(inputdir)
    dirs = defaultdict(list)
    sample_name_list = []
    starttime = time.time()
    p=Pool()
    for value in files:
        if os.path.isdir(value):
            sample_fq,fnlist = GetFileList(value,FlagStr=['fq'])
            dirs[value]=fnlist
            for fn in fnlist:
                sample_name_list.append(fn)
    print "main pid: %s"%os.getpid()
    for value in set(sample_name_list):
        commands = "cat "
        i=0
        for key,file_value in dirs.items():
            if value in file_value:
                i += 1
                commands += "%s/%s " % (key,value)
        if i>1:
            commands += ">%s/%s\n"%(outputdir,value)
            commands += "gzip -c %s/%s > %s/%s.gz\n"%(outputdir,value,outputdir,value)
        else:
            commands = "gzip -c %s > %s/%s.gz\n"%(commands.replace("cat",""),outputdir,value)
        print commands
        p.apply_async(write_gzip,args=(commands,))
    p.close()
    p.join()
    print 'Process end.'
    endtime = time.time()
    print "need time %s second"%(endtime-starttime)







