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
from collections import defaultdict


def read_params(args):
    parser = argparse.ArgumentParser(description='alignement parse 20160914 huangy')
    parser.add_argument('-i', '--input', dest='input', metavar="SOAP_LIST", type=str, required=True,
                        help="match.list")
    parser.add_argument('-o', '--output', dest='output', metavar='FILE', type=str, required=True,
                        help=".MATCH")
    parser.add_argument('-t','--type',dest='type',metavar="TYPE",type=str,default="PE",
                        help="PE or SE or all")
    args = parser.parse_args()
    params = vars(args)
    return params

def megermismatch(tabs):
    rtabs=[]
    n = len(tabs)/2
    for i in range(n):
        mismatchall = "%s\t%s" % (tabs[i+0],int(tabs[i+0].split("\t")[2])+int(tabs[i+n].split("\t")[2]))
        rtabs.append(mismatchall)
    return rtabs
def read_pe(pe):
    pkl_list = []
    for key in  pe:
        inf = {}
        start = time.time()
        with open(key, "r") as fq:
            stringname = os.path.basename(os.path.splitext(key)[0])
            sys.stdout.write("running  %s\n" % stringname)
            for line in fq:
                tabs = line.strip().split("\t")
                query = tabs[0]
                try:
                    refer = tabs[7]
                except IndexError:
                    sys.stderr.write("%s no have tabs[7]%s split %s\n" % (key,line,tabs))
                    continue
                # flag = tabs[4]
                outstring = "%s\t%s\t%s" % (refer,tabs[-2],tabs[9])
                if query in inf:
                    inf[query] = "%s;:%s" % (outstring, inf[query])
                else:
                    inf[query] = outstring

        if inf:
            for k,value in inf.items():
                tabs = value.split(";:")
                tabs = megermismatch(tabs)
                hits = []   #所有的hits [(id a X X),(),()]
                suboutstring = defaultdict(set)#Id XX XX mismatchall XX XX mismatchall 一个登入号对应两端的情况

                for v in  tabs:
                    subchot = v.split("\t")
                    subchot[1]=int(subchot[1].strip('M'))
                    hits.append((subchot[0],subchot[1],subchot[3]))
                    suboutstring[subchot[0]].add((subchot[1],subchot[3]))
                hits = sorted(hits, key=lambda x: (-x[1], x[2]))
                max_M = hits[0][1]
                min_s = hits[0][2]
                besthits = []
                for n, M, s in hits:
                    if M < max_M or s > min_s:
                        continue
                    elif M == max_M and s == min_s:
                        besthits.append((n, M, s))
                    else:
                        sys.stderr.write("min_s max statistical error")
                outstring=[]
                for n,M,s in besthits:
                    outstring.append("%s\t%s\t%s"%(n,M,s))
                inf[k] = ";:".join(outstring)

            df = pd.DataFrame(inf,index=[stringname]).T
            df.to_csv("%s.pkl" % key,sep=",",header=True)
            pkl_list.append("%s.pkl" % key)
        else:
            sys.stdout.write("%s file is none\n" % key)
        end = time.time()
        sys.stdout.write("load %s data run time: %s\n" % (stringname,end-start))

    return pkl_list

if __name__ == '__main__':
    # sys.argv=["fesfe.py","-i","test1","-o","tt","-t","PE"]
    params = read_params(sys.argv)
    inputfile = params["input"]
    outputfile = params["output"]
    analysis_type = params["type"]
    pe = []
    se = []
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
    pkl_list = []
    if len(pe)>0:
        sys.stdout.write("start work PE\n")
        pkl_list = read_pe(pe)
    # if len(se)>0:
    #     sys.stdout.write("start work SE\n")
    #     pkl_list = read_se(se,pkl_list)
    end = time.time()
    sys.stdout.write("load all file time: %s\n" % (end-start))


    start = time.time()
    df_list = []
    for key in pkl_list:
        df = pd.DataFrame.from_csv(key,header=0,sep=",",index_col=0)
        df_list.append(df)
    df_final = pd.concat(df_list, axis=1)
    df_final.index = range(len(df_final.index))
    df_final.to_csv(outputfile,sep=",",header=True)

    end = time.time()
    sys.stdout.write("concat step run time: %s\n" % (end-start))

