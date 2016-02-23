#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


import os

class Node(object):
    def __init__(self,name,path,config=None,commads=None):
        self.name = name
        self.path = path
        if config is None:
            self.config = "%s/%s.config" % (path,name)
        else:
            self.config = config
        if commads is not None:
            self.commands = commads
        else:
            self.commands = []
    def run_node(self):
        script_dir = os.path.dirname(__file__)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        print "test"
        os.popen("cp %s/../config/%s.config %s" % (script_dir,self.name, self.config))
