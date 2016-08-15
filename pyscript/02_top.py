#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import argparse
import sys
import workflow.util.globals as glo
from workflow.util.useful import parse_group_file,mkdir,Rparser,get_name,image_trans
from collections import OrderedDict
import pandas as pd

def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--inputfile', dest='inputfile', metavar='inputfile', type=str, required=True,
                        help="set input file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="set out put dir")
    parser.add_argument('-g','--group',dest='group',metavar='group',type=str,required=True,
                        help='set group file')
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    outputdir = params['outputdir']
    inputfile = params['inputfile']
    pdfoutput = outputdir+"top.pdf"
    pngoutput = outputdir+"top.png"
    group = params['group']


    vars = {'group': group,
            'pdfoutput':pdfoutput
            }
    r_job = Rparser()
    r_job.open(glo.Rscript + '02_top.R')
    r_job.format(vars)
    r_job.write(outputdir+ '/top.R')
    r_job.run()
    image_trans(pdfoutput, pngoutput)
