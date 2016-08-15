#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import division
import sys
import re
import argparse
import workflow.util.globals as glo
from workflow.util.useful import parse_group_file,mkdir,Rparser,get_name,image_trans
from collections import OrderedDict

def read_params(args):
    parser = argparse.ArgumentParser(description='''otu pca analysis | v1.0 at 2015/10/13 by liangzb ''')
    parser.add_argument('-i', '--otu_profile', dest='otu_table', metavar='FILE', type=str, required=True,
                        help="set the otu table file")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('--with_boxplot', dest='with_boxplot', action='store_true',
                        help="plot boxplot")
    parser.add_argument('--without_boxplot', dest='with_boxplot', action='store_false',
                        help="unplot boxplot")
    parser.add_argument('--two_legend', dest='two_legend', action = 'store_true',default=False,
                        help="two_legend")
    parser.set_defaults(with_boxplot=True)
    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    pdf_file = params['out_dir'] + '/otu_pca.pdf'
    png_file = params['out_dir'] + '/otu_pca.png'
    vars = {'otu_profile': params['otu_table'],
            'group_file': params['group'],
            'pdf_file': pdf_file}

    r_job = Rparser()
    if params['two_legend']:
        if params['with_boxplot']:
            r_job.open(glo.Rscript + '/03_tax_pca_two.Rtp')
        else:
            r_job.open(glo.Rscript + '/03_tax_pca_two.Rtp')
    else:
        if params['with_boxplot']:
            r_job.open(glo.Rscript + '/03_tax_pca_with_boxplot.Rtp')
        else:
            r_job.open(glo.Rscript + '/03_tax_pca.Rtp')
    r_job.format(vars)
    r_job.write(params['out_dir'] + '/tax_pca.R')
    r_job.run()
    image_trans(pdf_file, png_file)
