#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import division
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"



import re
from string import Template
from collections import OrderedDict
import os
import pandas as pd


def cutcol_dataFrame(data,group):
    data = pd.DataFrame.from_csv(data,sep="\t")
    samples = parse_group_file(group).keys()
    data.to_csv()
    return data.loc[:,samples],parse_group_file(group)
def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
def parse_group(group_file):
    sample_set = set()
    group_set = {}
    with open(group_file) as group:
        for line in group:
            sample_name, group_name = line.strip().split('\t')
            if group_name not in group_set:
                group_set[group_name] = set()
            group_set[group_name].add(sample_name)
            sample_set.add(sample_name)
    sample_num_in_groups = map(lambda s: len(s), group_set.itervalues())
    min_sample_num_in_groups = min(sample_num_in_groups)
    sample_num_total = len(sample_set)
    group_num = len(group_set)
    return sample_num_in_groups, min_sample_num_in_groups, sample_num_total, group_num
def get_name(path):
    basename = os.path.basename(path)
    dirname = os.path.split(path)[0]
    filename = os.path.splitext(basename)[0]
    suffix = os.path.splitext(basename)[1]
    return dirname,filename,suffix
def parse_group_file(file):
    if file is None:
        return None
    group = OrderedDict()
    with open(file) as g:
        for line in g:
            tabs = line.strip().split('\t')
            if len(tabs) >= 2:
                group[tabs[0]] = tabs[1]
            else:
                group[tabs[0]] = tabs[0]
    return group




class MyTemplate(Template):
    delimiter = '@#'


class Rparser(object):
    def __init__(self):
        self.template = None
        self.R_script = None
        self.file = None

    def open(self, template):
        fp = open(template)
        template = fp.read()
        fp.close()
        self.template = MyTemplate(template)

    def format(self, var):
        self.R_script = self.template.safe_substitute(var)

    def write(self, outfile):
        fp = open(outfile, 'w')
        fp.write(self.R_script)
        self.file = outfile
        fp.close()

    def run(self):
        os.system('R CMD BATCH --slave %(Rfile)s %(Rfile)sout' % {'Rfile': self.file})

def image_trans(num,input,output):
    os.system('convert -density %s %s %s' % (num,input,output))