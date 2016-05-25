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
from workflow.util import configparserself
from workflow.util import error
from workflow.node import Node
#from workflow.configObj import ConfigObj
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
    params = read_params(sys.argv)
    config_path = params.config_path
    config = configparserself.ConfigParserSelf()
    config.read(config_path)
    option_value = config.read_config()
    work_dir = option_value['work_dir']
    step_names = option_value['step_names_order'].split(",")
    step_names_all = step_names_order.split(",")
    steps = []
    for name in step_names:
        if name in step_names_all:
            step_dir = "%s/%s/" % (work_dir,name)
            step1 = Node(name, path=step_dir)
            step1.cp_config_node(work_dir)
            step1.cp_sh_node(work_dir)
            steps.append(step1)
        else:
            print name
            raise error.NoStepError("no have %s step" % name,name)
#    step0,step1,step2,step3,step4,step5,step6= steps
#    config_step0 = ConfigParser()
#    config_step0.read(step0.config)
#    rawlink = config_step0.get("script","01_rawlink")
 #   step0.command = "python %s -i %s -o %s" % (rawlink,sample_name,step0.path)
#    config_step0.write(open(step0.config,"w"))
 #   step0.create_shell()




