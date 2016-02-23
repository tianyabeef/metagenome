#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

from ConfigParser import ConfigParser
import sys
import node
import argparse
import os
def read_params(args):
    parsers = argparse.ArgumentParser(description='''The initial run script of metagene ''')
    parsers.add_argument('--config', dest='config_path', metavar='FILE', type=str, required=True,
                        help="config file for metagenome pipeline")
    args = parsers.parse_args()
    return args


if __name__ == '__main__':
    args = sys.argv
    params = read_params(args)
    config_path = params.config_path
    config = ConfigParser()
    config.read(config_path)
    work_dir = config.get("param","work_dir")
    sample_name = config.get("param","sample_name")
    script_dir = os.path.dirname(__file__)
    config_step = ConfigParser()
    config_step.read("%s/%s" % (script_dir,"../config/step.config"))
    step_names = config_step.get("steps","name").rstrip().split(",")
    for name in step_names:
        step1 = node.Node("00_rawData",path =work_dir, config="work_dir/%s" % "00_raw_data.config")
        step1.run_node()



