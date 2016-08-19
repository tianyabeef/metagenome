#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

try:
    import cPickle as pickle
except ImportError:
    import pickle
import argparse
import sys
import os
import re
import time
import pandas as pd


def read_params(args):
    parser = argparse.ArgumentParser(description='alignement parse 20160819 huangy')
    parser.add_argument('-i', '--input', dest='input', metavar="SOAP_LIST", type=str, required=True,
                        help="match.list")
    parser.add_argument('-o', '--output', dest='output', metavar='FILE', type=str, required=True,
                        help=".MATCH")
    parser.add_argument('-t','--type',dest='type',metavar="TYPE",type=str,default="PE",
                        help="PE or SE or all")
    args = parser.parse_args()
    params = vars(args)
    return params


def read_pe(pe):
    for index,key in  enumerate(pe):
        inf = {}
        start = time.time()
        with open(key, "r") as fq:
            names = re.split('\.|-', key)
            stringname = names[-2]
            sys.stdout.write("running  %s\n" % stringname)
            for line in fq:
                tabs = line.strip().split("\t")
                query = tabs[0]
                refer = tabs[7]
                flag = tabs[4]
                if flag == "a":
                    outstring = "%s\tP\t%s\t%s\t%s\t%s" % (refer, stringname, flag, tabs[-2], tabs[9])
                    if inf.has_key(query):
                        inf[query] = "%s,%s" % (outstring, inf[query])
                    else:
                        inf[query] = outstring
        if index==0:
            df_first = pd.DataFrame(inf,index=[stringname]).T
        else:
            df = pd.DataFrame(inf,index=[stringname]).T
            df_first = pd.concat([df_first,df], axis=1)
        end = time.time()
        sys.stdout.write("load %s data run time: %s\n" % (stringname,end-start))

    return df_first

def read_se(se,df_first):
    pkl_files = []
    for key in se:
        inf = {}
        start = time.time()
        with open(key, "r") as fq:
            names = re.split('\.|-', key)
            stringname = names[-2]
            sys.stdout.write("running  %s\n" % stringname)
            for line in fq:
                tabs = line.strip().split("\t")
                query = tabs[0]
                refer = tabs[7]
                flag = tabs[4]
                if flag=="a":
                    outstring = "%s\tS\t%s\t%s\t%s\t%s" % (refer, stringname, flag, tabs[-2], tabs[9])
                    if inf.has_key(query):
                        inf[query] = "%s,%s" % (outstring, inf[query])
                    else:
                        inf[query] = outstring
        df = pd.DataFrame(inf,index=[stringname]).T
        df_first = pd.concat([df_first,df], axis=1)
        end = time.time()
        sys.stdout.write("load %s data run time: %s\n" % (stringname,end-start))
    return df_first
#        f1 = file("%s.pkl" % key, 'wb')
#        pickle.dump(inf,f1,protocol=2)
#        f1.close()



if __name__ == '__main__':
    params = read_params(sys.argv)
    inputfile = params["input"]
    outputfile = params["output"]
    analysis_type = params["type"]
    pe = []
    se = []
#    inf = {}
    with open(inputfile, "r") as fq:
        for line in fq:
            tabs = line.strip().split("\t")
            if analysis_type == "PE":
                if tabs[0] == "PE":
                    pe.append(tabs[1])
            elif analysis_type == "SE":
                if tabs[0] == "SE":
                    se.append(tabs[1])
            elif analysis_type == "all":
                if tabs[0] == "PE":
                    pe.append(tabs[1])
                else:
                    se.append(tabs[1])
    start = time.time()

    if len(pe)>0:
        sys.stdout.write("start work PE\n")
        df_first = read_pe(pe)
    if len(se)>0:
        sys.stdout.write("start work SE\n")
        df_first = read_se(se,df_first)
    end = time.time()
    sys.stdout.write("load all file time: %s\n" % (end-start))


    start = time.time()
    df_first.to_csv(outputfile,sep=",",header=True)
    end = time.time()
    sys.stdout.write("concat step run time: %s\n" % (end-start))

