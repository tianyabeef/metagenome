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
import re
import time
import pandas as pd


def read_params(args):
    parser = argparse.ArgumentParser(description='alignement parse 20160504 huangy')
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
    pkl_files = []
    for key in pe:
        inf = {}
        with open(key, "r") as fq:
            names = re.split('\.|-', key)
            stringname = names[-2]
            sys.stdout.write("running  %s\n" % stringname)
            for line in fq:
                tabs = line.strip().split("\t")
                query = tabs[0]
                refer = tabs[7]
                flag = tabs[4]
                outstring = "%s\tP\t%s\t%s\t%s\t%s" % (refer, stringname, flag, tabs[-2], tabs[9])
                if inf.has_key(query):
                    inf[query] = "%s\n%s" % (outstring, inf[query])
                else:
                    inf[query] = outstring
        f1 = file("%s.pkl" % key, 'wb')
        pickle.dump(inf,f1,protocol=2)
        f1.close()
        pkl_files.append(f1)
    return pkl_files


def read_se(se):
    pkl_files = []
    for key in se:
        inf = {}
        with open(key, "r") as fq:
            names = re.split('\.|-', key)
            stringname = names[-2]
            sys.stdout.write("running  %s\n" % stringname)
            for line in fq:
                tabs = line.strip().split("\t")
                query = tabs[0]
                refer = tabs[7]
                flag = tabs[4]
                outstring = "%s\tS\t%s\t%s\t%s\t%s" % (refer, stringname, flag, tabs[-2], tabs[9])
                if inf.has_key(query):
                    inf[query] = "%s\n%s" % (outstring, inf[query])
                else:
                    inf[query] = outstring
        f1 = file("%s.pkl" % key, 'wb')
        pickle.dump(inf,f1,protocol=2)
        f1.close()
        pkl_files.append(f1)
    return pkl_files


if __name__ == '__main__':
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
    pkl_files_pe = []
    pkl_files_se = []
    if len(pe)>0:
        sys.stdout.write("start work PE\n")
        pkl_files_pe = read_pe(pe)
    if len(se)>0:
        sys.stdout.write("start work SE\n")
        pkl_files_se = read_se(se)
    end = time.time()
    sys.stdout.write(" run time: %s\n" % (end-start))

    start = time.time()
    inf = {}
    dfs = []
    for key in [pkl_files_pe,pkl_files_se]:
        if not key:
            names = re.split('\.|-', key)
            stringname = names[-3]
            file_handle = open('key', 'rb')
            d = pickle.load(file_handle)
            file_handle.close()
            df = pd.DataFrame(d,index=[stringname]).T
            dfs.append(df)
    result = pd.concat(dfs, axis=1)
    result.to_csv(outputfile,seq="\t",header=True)
    end = time.time()
    sys.stdout.write(" concat step run time: %s\n" % (end-start))
    # with open(outputfile, "w") as fqout:
    #     for key, value in inf.items():
    #         fqout.write(">%s\n%s\n" % (key, value))
