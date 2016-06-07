#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import os
import re
import sys
import tarfile
from Bio import SeqIO
if __name__ == '__main__':
    args = sys.argv
    args.pop(0)
    fna_list_path,outpathori = args
    i=0
    j=0
    with open("%s/statistical.txt" % outpathori,"w") as haveout:
        with open(fna_list_path,"r") as fq1:
            for line in fq1:
                j = j+1
                print "%s fna file" % j
                fnafile_path = line.strip()
                seq_sum = 0
                for recond in SeqIO.parse(fnafile_path,"fasta"):
                    tabs = recond.id.split(" ")
                    if len(tabs)>0:
                        seq_sum = seq_sum+len(recond.seq)
                        haveout.write(tabs[0])
                        haveout.write(":")
                        haveout.write("%s;" % (len(recond.seq)))
                    else:
                        print recond.id
                        sys.stderr.write("%s can not split ,infor:%s\n" % (fnafile_path,recond.id))
                haveout.write("\t%s\t%s\n" % (fnafile_path,seq_sum))
