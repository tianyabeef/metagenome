#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


import os
import sys
import workflow.util.globals as glo
from ConfigParser import ConfigParser


config_file_suffix = glo.const.config_file_suffix
shell_file_suffix = glo.const.shell_file_suffix
config_default_dir = glo.const.config_default_dir


class Node(object):
    def __init__(self,name,path,shell=None,config=None,commads=None):
        self.name = name
        self.configName = "%s.%s" % (name,config_file_suffix)
        self.shellName = "%s.%s" % (name,shell_file_suffix)
        self.path = path
        if config is None:
            self.config = "%s/%s" % (path,self.configName)
        else:
            self.config = config
        if shell is None:
            self.shell = "%s/%s" % (path,self.shellName)
        else:
            self.config = config
        if commads is not None:
            self.commands = commads
        else:
            self.commands = []
    def cp_config_node(self,work_dir):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        config_default_file = "%s/%s" % (config_default_dir,self.configName)
        if os.path.exists(config_default_file):
            os.popen("cp %s %s" % (config_default_file, self.config))
            config = ConfigParser()
            config.read(self.config)
            config.set("param","work_dir",work_dir)
            config.set("param","out_dir",self.path)
            config.write(open(self.config,mode="w"))
        else:
            sys.stderr.write("the %s step no add default config : %s \n" % (self.name,config_default_file))
    def create_shell(self):
        if os.path.exists(self.shell ):
            sys.stderr.write("Covered the file before:%s\n" % self.shell)
        with open(self.shell,"w") as fqout:
            for command in self.commands:
                fqout.write(command)




