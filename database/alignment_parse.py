#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import argparse
import sys
import re

def read_params(args):
    parser = argparse.ArgumentParser(description='alignement parse 20160504 huangy')
    parser.add_argument('-i','--input',dest='input',metavar="SOAP_LIST",type=str,required=True,
                        help="match.list")
    parser.add_argument('-o', '--output', dest='output', metavar='FILE', type=str, required=True,
                        help=".MATCH")
    args = parser.parse_args()
    params = vars(args)
    return params

def read_pe(pe,inf):
    for key in pe:
        with open(key,"r") as fq:
            names = re.split('\.|-',key)
            stringname = names[-2]
            print "running  %s" % stringname
            for line in fq:
                tabs = line.strip().split("\t")
                query = tabs[0]
                refer = tabs[7]
                flag = tabs[4]
                outstring = "%s\tP\t%s\t%s\t%s\t%s"%(refer,stringname,flag,tabs[-2],tabs[9])
                if inf.has_key(query):
                    inf[query] = "%s\n%s" % (outstring,inf[query])
                else:
                    inf[query] = outstring
    return inf

def read_se(se,inf):
    for key,values in se.items():
        with open(key,"r") as fq:
            names = re.split('\.|-',key)

            stringname = names[-2]
            print stringname
            for line in fq:

                tabs = line.strip().split("\t")
                query = tabs[0]
                refer = tabs[7]
                flag = tabs[4]
                outstring = "%s\tS\t%s\t%s\t%s\t%s"%(refer,stringname,flag,tabs[-2],tabs[9])
                if inf.has_key(query):
                    inf[query] = "%s\n%s" % (outstring,inf[query])
                else:
                    inf[query] = outstring
    return inf



if __name__ == '__main__':
    params = read_params(sys.argv)
    inputfile = params["input"]
    outputfile = params["output"]
    pe = []
    se = []
    inf = {}
    with open(inputfile,"r") as fq:
        for line in fq:
            tabs = line.strip().split("\t")
            if tabs[0] == "PE":
                pe.append(tabs[1])
            else:
                se.append(tabs[1])
    inf = read_pe(pe,inf)
    print len(inf)
    inf = read_se(se,inf)
    print len(inf)
    with open(outputfile,"w") as fqout:
        for key,value in inf.items():
            fqout.write(">%s\n%s\n" % (key,value))






