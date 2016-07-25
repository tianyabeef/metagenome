#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
'''统计fastq或fasta的reads长度'''
import argparse
from Bio import SeqIO
import sys
import os
def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--input', dest='input', metavar='input', type=str, required=True,
                        help="input fastq list file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="out put dir")
    parser.add_argument('-t','--type',dest='type',metavar='type',type=str,required=True,
                        hel="fastq or fasta")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    inputlist = params['input']
    outputdir = params['outputdir']
    ftype = params['type']
    with open(inputlist,'r') as fq:
        for line in fq:
            alllen = {}
            for record in SeqIO.parse(line.strip(),ftype):
                if alllen.has_key(len(record.seq)):
                    alllen[len(record.seq)] += 1
                else:
                    alllen[len(record.seq)] = 1
            with open("%s/%s_reads_len.txt"%(os.path.basename(line.strip()),outputdir)) as fqout:
                for key in sorted(alllen.keys()):
                    fqout.write("%s\t%s\n"%(key,alllen[key]))

