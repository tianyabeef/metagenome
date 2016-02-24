#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys

import argparse
import subprocess
import pandas as pd
import os

def read_params(args):
    parser = argparse.ArgumentParser(description='''Sequencing data path ,it including fq.gz file ''')
    parser.add_argument('-i', '--sample_list', dest='sample_list', metavar='FILE', type=str, required=True,
                        help="list of Sequence data url")
    parser.add_argument('-s','--sample_name',dest="sample_name",metavar="FILE",type=str,required = True,
                        help = "list of sample_name,one sample in line.")
    parser.add_argument('-o', '--out_file', dest='out_file', metavar='FILE', type=str, required=True,
                        help="set the output file")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    sample_list = params['sample_list']
    sample_name_file = params['sample_name']
    out_file = params['out_file']
    with open(sample_list,mode="r") as fq:
        for line in fq:
            tabs = line.rstrip().split("\t")
            command = "ln -s %s %s \n" % (tabs[1],out_file)
            command += "ln -s %s %s \n" % (tabs[2],out_file)
            subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
