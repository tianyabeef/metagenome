#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import os
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
    dirname = os.path.split(path)
    filename = os.path.splitext(basename)[0]
    suffix = os.path.splitext(basename)[1]
    return dirname,filename,suffix
