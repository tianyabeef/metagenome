#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import os
import re
import sys
#import tarfile
#from Bio import SeqIO
import pandas   as pd
if __name__ == '__main__':
    args = sys.argv
    _,profile,group,outfile,type=args
    group = pd.read_table(group,sep="\t",header=None).to_dict()[0]
    data = pd.DataFrame.from_csv(profile,sep="\t")
    data2 = data[group.values()]
    data3 = data2[data2.sum(axis=1)>0]
    if type=="species":
        data3.index = "s__"+data3.index
    if type=="genus":
        data3.index = "g__"+data3.index
    data3.index.name="Name"
    data3.to_csv(outfile,sep="\t")
