#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys

import argparse
import subprocess
import pandas as pd

def read_params(args):
    parser = argparse.ArgumentParser(description='''Sequencing data path ,it including fq.gz file ''')
    parser.add_argument('-i', '--dir_list', dest='dir_list', metavar='FILE', type=str, required=True,
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
    dir_list = params['dir_list']
    sample_name_file = params['sample_name']
    out_file = params['out_file']
    df = pd.DataFrame.from_csv(sample_name_file,sep="\t",header=None,index_col=None)
    sample_name = df[0].tolist()
    with open(dir_list,mode="rt") as fq:
        for line in fq:
            rowData_url = line.rstrip()
            command = 'ls %s | grep "%s" | while read line; do echo "ln -s %s/$line %s/$line";done  >> %s/command_02' % (rowData_url,
                            "\|".join(sample_name),rowData_url,out_file,out_file)
            out_bytes = subprocess.check_output(command,shell=True)
