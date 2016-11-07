#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import time
import argparse
import sys

from workflow.util import configparserself
from workflow.util import error
print("import error :%s s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
from workflow.node import Node
print("import Node :%s s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
from workflow.util.globals import const

def read_params(args):
    parsers = argparse.ArgumentParser(description='''The initial run script of metagene ''')
    parsers.add_argument('--config', dest='config_path', metavar='FILE', type=str, required=True,
                        help="config file for metagenome pipeline")
    args = parsers.parse_args()
    return args


if __name__ == '__main__':
    print("start :%s s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    config_default_dir = const.config_default_dir
    step_names_order = const.step_names_order
    params = read_params(sys.argv)
    config_path = params.config_path
    config = configparserself.ConfigParserSelf()
    config.read(config_path)
    option_value = config.read_config()
    work_dir = option_value['work_dir']
    step_names = option_value['step_names_order'].split(",")
    #group = option_value['group'].split("\s+")
    step_names_all = step_names_order.split(",")
    steps = []
    for i,name in enumerate(step_names):
        if name in step_names_all:
            print("end mkdir :%s s"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            step_dir = "%s/%s/" % (work_dir,name)
            step1 = Node(name, path=step_dir)
            step1.mkdir()

            opts = []
            if i>0:
                opts = step1.getconfig(work_dir,step_names[i-1])
            step1.setconfig(opts,{"group":option_value["group"]})
            complete = step1.setshell()
            if not complete:
                step1.cp_sh_node()
#            step1.cp_config_node()
#            step1.cp_sh_node()
            steps.append(step1)
        else:
            raise error.NoStepError("no have %s step" % name,name)
#    step0,step1,step2,step3,step4,step5,step6= steps
#    config_step0 = ConfigParser()
#    config_step0.read(step0.config)
#    rawlink = config_step0.get("script","01_rawlink")
 #   step0.command = "python %s -i %s -o %s" % (rawlink,sample_name,step0.path)
#    config_step0.write(open(step0.config,"w"))
 #   step0.create_shell()




