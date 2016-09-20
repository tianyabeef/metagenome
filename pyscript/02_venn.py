#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import division
import sys
sys.path.append('/data_center_01/pipeline/huangy/metagenome/')
import re
import argparse
from workflow.util.globals import const
from workflow.util.useful import parse_group_file,mkdir,Rparser,get_name,image_trans
from collections import OrderedDict


def read_params(args):
    parser = argparse.ArgumentParser(description='''otu venn analysis | v1.0 at 2015/10/13 by liangzb ''')
    parser.add_argument('-i', '--microbial_profile', dest='microbial_profile', metavar='FILE', type=str, required=True,
                        help="set the otu table file")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='DIR', type=str, required=True,
                        help="set the output DIR")
    args = parser.parse_args()
    params = vars(args)
    params['group_dir'] = params['group']
    params['group'] = parse_group_file(params['group'])
    return params


def read(otu_table_file, sample_in_group, vars):
    otu_in_group = OrderedDict()
    group_names = set(sample_in_group.itervalues())
    otu_num_dict = {}
    otu_count = 1
    for ind, group in enumerate(list(group_names)):
        vars['group_name%s' % (ind+1,)] = group
        otu_in_group[group] = set()
    with open(otu_table_file) as otu_table:
        head = otu_table.next()
        if head.startswith('# Constructed from'):
            head = otu_table.next()
        samples = head.strip().split('\t')[1:]
        for line in otu_table:
            tabs = line.strip().split('\t')
            otu_name = tabs.pop(0)
            try:
                otu_num = re.search('(\d+)$', otu_name).group(1)
            except AttributeError:
                if otu_name not in otu_num_dict:
                    otu_num_dict[otu_name] = str(otu_count)
                    otu_count += 1
                otu_num = otu_num_dict[otu_name]
            for ind, tab in enumerate(tabs):
                if float(tab) > 0:
                    if samples[ind-1] in sample_in_group:
                        group = sample_in_group[samples[ind-1]]
                        otu_in_group[group].add(otu_num)
                    else:
                        print "sample %s no in group" % samples[ind-1]
    return otu_in_group



def write(otu_in_group, outfile):
    with open(outfile, 'w') as fp:
        for group, otus in otu_in_group.iteritems():
            otus = sorted(list(otus), cmp=lambda a, b: cmp(int(a), int(b)))
            fp.write('%s\t%s\n' % (group, ' '.join(otus)))


if __name__ == '__main__':
    params = read_params(sys.argv)
    dirname=params['outputdir']
    mkdir(dirname)
    for_plot = dirname + '/for_plot.txt'
    tiff_file = dirname + '/venn.tiff'
    png_file = dirname + '/venn.png'
    vars = {'for_plot': for_plot,
            'tiff_file': tiff_file,
            'group_file': params['group_dir']}

    otu_in_group = read(params['microbial_profile'], params['group'], vars)
    write(otu_in_group, for_plot)

    r_job = Rparser()
    r_job.open(const.Rscript + '02_venn.R')
    r_job.format(vars)
    r_job.write(dirname+ '/otu_venn.R')
    r_job.run()
    image_trans(300,tiff_file, png_file)
