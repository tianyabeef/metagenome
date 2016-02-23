#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import argparse
import os
import sys
from ConfigParser import ConfigParser

from workflow.node import Node
from workflow.util.globals import const


def read_params(args):
    parsers = argparse.ArgumentParser(description='''The initial run script of metagene ''')
    parsers.add_argument('--config', dest='config_path', metavar='FILE', type=str, required=True,
                        help="config file for metagenome pipeline")
    args = parsers.parse_args()
    return args


if __name__ == '__main__':
    config_default_dir = const.config_default_dir

    args = sys.argv
    params = read_params(args)
    config_path = params.config_path
    config = ConfigParser()
    config.read(config_path)
    work_dir = config.get("param","work_dir")
    sample_name = config.get("param","sample_name")
    config_step = ConfigParser()

    config_step.read("%s/%s" % (config_default_dir,"step.config"))
    step_names = config_step.get("steps","name").rstrip().split(",")
    for name in step_names:
        step_dir = "%s/%s/" % (work_dir,name)
        step1 = Node(name, path=step_dir)
        step1.run_node()


