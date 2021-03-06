#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import division
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


import sys
import os
sys.path.append('/data_center_01/pipeline/huangy/metagenome/')
import argparse
from workflow.util.globals import const
from workflow.util.useful import parse_group_file,mkdir,Rparser,get_name,image_trans
import pandas as pd


def read_params(args):
    parser = argparse.ArgumentParser(description='tax bar plot | v1.0 at 2015/11/06 by liangzb')
    parser.add_argument('-i', '--inputfile', dest='inputfile', metavar='FILE', type=str, required=True,
                        help="input micbiom abundance file")
    parser.add_argument('-g', '--group', dest='group', metavar='FILE', type=str, default=None,
                        help="set the group_file")
    parser.add_argument('-o', '--outputfile', dest='outputfile', metavar='FILE', type=str, required=True,
                        help="set the output file")
    parser.add_argument('-t','--title',dest='title',metavar='STRING',type=str,required=True,
                        help="set title of plot")
    parser.add_argument('--with_group', dest='with_group', action='store_true',
                        help="plot group bar plot, if group is not set, this param will not be used")
    parser.add_argument('--without_group', dest="with_group", action='store_false',
                        help="plot sample bar plot, if this params is set, group file will only for order")
    parser.add_argument('--contains_other', dest="contains_other", action='store_true',
                        help="totel abundance contains other abundance ; totel aundance is 1")
    parser.add_argument('--top', dest="top",metavar="INT",type=int,default=20,
                        help='set the top num, [default is 20]')
    parser.set_defaults(with_group=False)
    args = parser.parse_args()
    params = vars(args)
    params['group'] = parse_group_file(params['group'])
    return params


if __name__ == '__main__':
    params = read_params(sys.argv)
    outputfile = params['outputfile']
    dirname,filename,suffix =get_name(outputfile)
    inputfile = params['inputfile']
    top = params['top']
    title = params['title']
    data = pd.DataFrame.from_csv(file=inputfile,sep="\t")
    data["sum"] = data.sum(axis=1)
    data = data.sort_values(by="sum",ascending=False)
    del data["sum"]
    data = data.ix[:top]
    data.to_csv("%s/for_plot.csv"%dirname,sep="\t")
    mkdir(os.path.split(outputfile)[0])
    RscriptDir = const.Rscript
    r_job = Rparser()
    r_job.open("%s/02_barplot.R"%RscriptDir)
    vars = {"top":top,
            "infile": "%s/for_plot.csv"%dirname,
            "pdf_file": outputfile,
            "title": title}
    r_job.format(vars)
    r_job.write("%s/bar_plot.R"%dirname)
    r_job.run()
    image_trans(300,"%s/%s.pdf"%(dirname,filename),"%s/%s.png"%(dirname,filename))
