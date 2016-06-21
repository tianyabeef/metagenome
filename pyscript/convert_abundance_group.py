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
    _,profile,group,outfile=args
    group = pd.read_table(group,sep="\t",header=None).to_dict()[1]
    data = pd.DataFrame.from_csv(profile,sep="\t")
    data2 = data[group.keys()]
    data3 = data2[data2.sum(axis=1)>0]
    data3.to_csv(outfile,sep="\t")
