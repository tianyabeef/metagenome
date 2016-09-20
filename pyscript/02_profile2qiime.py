#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import argparse
import sys
def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--input', dest='input', metavar='input', type=str, required=True,
                        help="set all.profile input file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="out put dir")
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    inputfile = params["input"]
    outputdir = params["outputdir"]
    with open(inputfile,"r") as fq,open("%s/otu_table_L1.txt"%outputdir,"w") as fq1,\
    open("%s/otu_table_L2.txt"%outputdir,"w") as fq2,open("%s/otu_table_L3.txt"%outputdir,"w") as fq3,\
    open("%s/otu_table_L4.txt"%outputdir,"w") as fq4,open("%s/otu_table_L5.txt"%outputdir,"w") as fq5,\
    open("%s/otu_table_L6.txt"%outputdir,"w") as fq6,open("%s/otu_table_L7.txt"%outputdir,"w") as fq7:
        head = fq.next()
        fq1.write("# Constructed from biom file\n#OTU ID%s"%head)
        fq2.write("# Constructed from biom file\n#OTU ID%s"%head)
        fq3.write("# Constructed from biom file\n#OTU ID%s"%head)
        fq4.write("# Constructed from biom file\n#OTU ID%s"%head)
        fq5.write("# Constructed from biom file\n#OTU ID%s"%head)
        fq6.write("# Constructed from biom file\n#OTU ID%s"%head)
        fq7.write("# Constructed from biom file\n#OTU ID%s"%head)
        for line in fq:
            tabs=line.strip().split("\t")[0].split("|")
            line = line.replace("|",";")
            if len(tabs)==1:
                fq1.write(line)
            if len(tabs)==2:
                fq2.write(line)
            if len(tabs)==3:
                fq3.write(line)
            if len(tabs)==4:
                fq4.write(line)
            if len(tabs)==5:
                fq5.write(line)
            if len(tabs)==6:
                fq6.write(line)
            if len(tabs)==7:
                fq7.write(line)
