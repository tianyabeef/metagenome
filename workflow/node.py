#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


import os
import sys
import workflow.util.globals as glo

config_file_suffix = glo.const.config_file_suffix
config_default_dir = glo.const.config_default_dir

class Node(object):
    def __init__(self,name,path,config=None,commads=None):
        self.name = "%s.%s" % (name,config_file_suffix)
        self.path = path
        if config is None:
            self.config = "%s/%s" % (path,name)
        else:
            self.config = config
        if commads is not None:
            self.commands = commads
        else:
            self.commands = []
    def run_node(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        config_default_file = "%s/%s" % (config_default_dir,self.name)
        if os.path.exists(config_default_file):
            os.popen("cp %s %s" % (config_default_file, self.config))
        else:
            sys.stderr.write("the %s step no add default config : %s \n" % (os.path.splitext(self.name)[0],config_default_file))