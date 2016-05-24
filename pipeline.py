#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


from matplotlib import pylab
#pylab.figure().add_subplot.legend
#pylab.figure().subplots_adjust
import argparse
import os
import sys
from ConfigParser import ConfigParser

from workflow.node import Node
from workflow.configObj import ConfigObj
from workflow.util.globals import const


def read_params(args):
    parsers = argparse.ArgumentParser(description='''The initial run script of metagene ''')
    parsers.add_argument('--config', dest='config_path', metavar='FILE', type=str, required=True,
                        help="config file for metagenome pipeline")
    args = parsers.parse_args()
    return args


if __name__ == '__main__':
    config_default_dir = const.config_default_dir
    step_names_order = const.step_names_order

    args = sys.argv
    params = read_params(args)
    config_path = params.config_path

    config = ConfigParser()
    config.read(config_path)
    work_dir = config.get("param","work_dir")
    sample_name = config.get("param","sample_name")

    step_names = step_names_order.split(",")
    pipeline = []
    for name in step_names:
        step_dir = "%s/%s/" % (work_dir,name)
        step1 = Node(name, path=step_dir)
        step1.cp_config_node(work_dir)
        pipeline.append(step1)
    step0,step1,step2,step3,step4,step5,step6= pipeline
    config_step0 = ConfigParser()
    config_step0.read(step0.config)
    rawlink = config_step0.get("script","01_rawlink")
    step0.command = "python %s -i %s -o %s" % (rawlink,sample_name,step0.path)
    config_step0.write(open(step0.config,"w"))
    step0.create_shell()




