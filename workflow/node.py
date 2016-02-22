#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


import os

class Node(object):
    def __init__(self,name,path,config,commads=None):
        self.name = name
        self.path = path
        self.config = config
        if commads is not None:
            self.commands = commads
        else:
            self.commands = []
    def run_node(self):
        script_path = os.path.realpath(__file__)
        os.mkdir(self.path)
        print "test"
        os.popen("cp %s/%s.config %s" % (script_path,self.name, self.config))
