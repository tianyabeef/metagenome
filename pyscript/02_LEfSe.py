#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
import os
sys.path.append('/data_center_01/pipeline/huangy/metagenome/')
import argparse
from workflow.util.globals import const
from workflow.util.useful import parse_group_file,mkdir,Rparser,get_name,image_trans,cutcol_dataFrame



def read_params(args):
    parser = argparse.ArgumentParser(description='a wrapper for LEfSe | v1.0 at 2015/10/19 by liangzb')
    parser.add_argument('-i', '--summarize_all', dest='infile', metavar='FILE', type=str, required=True,
                        help="set hte otu_table_all.txt produced by 02_summarize_trans.py")
    parser.add_argument('-l', '--LEfSe_path', dest='LEfSe_path', metavar='DIR', type=str, default=None,
                        help="set the LEfSe path, default find in env")
    parser.add_argument('-g', '--group_file', dest='group', metavar='FILE', type=str, required=True,
                        help="set the group file")
    parser.add_argument('-o', '--out_dir', dest='out_dir', metavar='DIR', type=str, required=True,
                        help="set the output dir")
    parser.add_argument('--LDA', dest='LDA', metavar='FLOAT', type=float, default=2,
                        help="set the LDA cutoff, [default is 2]")
    parser.add_argument('--class_row', dest='c', metavar='INT', type=int, default=1,
                        help="set the class row, [default is 1]")
    parser.add_argument('--subject_row', dest='u', metavar='INT', type=int, default=2,
                        help="set the subject row, [default is 2]")
    args = parser.parse_args()
    params = vars(args)
    params['groupDir'] = params['group']
    params['group'] = parse_group_file(params['group'])
    if params['LEfSe_path'] is None:
        params['LEfSe_path'] = ''
    else:
        params['LEfSe_path'] += '/'
    return params


def do_format(infile, outfile, groupDir):
    data,group = cutcol_dataFrame(infile,groupDir)
    groups=group.values()
    samples = group.keys()
    data.index=data.index().replace(';','|')
    for temp in data.index:
        if temp.endswith('Other'):
            data.drop(temp)
        if temp.endswith('norank'):
            data.drop(temp)
        if temp.endswith('unclassfied'):
            data.drop(temp)
    with open(outfile, 'w') as out_fp:
        out_fp.write('class\t%s\n' % '\t'.join(groups))
        out_fp.write('Taxon\t%s\n' % '\t'.join(samples))
        data.to_csv(out_fp,header=False,sep="\t")


def get_commands(infile, LEfSe_path, out_dir, LDA, c, u):
    commands = []
    command = '%sformat_input.py %s %s/LDA.in -c %s -u %s -o 1000000' % (LEfSe_path, infile, out_dir, c, u)
    commands.append(command)
    command = '%srun_lefse.py %s/LDA.in %s/LDA.res -l %s' % (LEfSe_path, out_dir, out_dir, LDA)
    commands.append(command)
    command = '%splot_res.py %s/LDA.res %s/LDA.pdf --format pdf --dpi 150' % (LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command = '%splot_res.py %s/LDA.res %s/LDA.png --format png --dpi 150' % (LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command = '%splot_cladogram.py %s/LDA.res %s/LDA.cladogram.pdf --format pdf --dpi 150' % (
        LEfSe_path, out_dir, out_dir)
    commands.append(command)
    command = '%splot_cladogram.py %s/LDA.res %s/LDA.cladogram.png --format png --dpi 150' % (
        LEfSe_path, out_dir, out_dir)
    commands.append(command)
    if not os.path.isdir('%s/biomarkers_raw_images' % out_dir):
        os.mkdir('%s/biomarkers_raw_images' % out_dir)
    command = '%(LEfSe_path)splot_features.py %(out_dir)s/LDA.in %(out_dir)s/LDA.res %(out_dir)s/biomarkers_raw_images/ --format pdf --dpi 200' % {
        'LEfSe_path': LEfSe_path, 'out_dir': out_dir}
    commands.append(command)
    return commands


if __name__ == '__main__':
    params = read_params(sys.argv)
    mkdir(params['out_dir'])
    for_analysis = '%s/otu_table_for_lefse.txt' % params['out_dir']
    do_format(params['infile'], for_analysis, params['groupDir'])
    commands = get_commands(for_analysis, params['LEfSe_path'], params['out_dir'],
                            params['LDA'], params['c'], params['u'])
    with open(params['out_dir'] + '/commands.sh', 'w') as fp:
        fp.write('\n'.join(commands))
    for command in commands:
        os.system(command)
