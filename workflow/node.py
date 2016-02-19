#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"


import os
class Node(object):
    def __init__(self,name,config,path,commads=None):
        self.name = name
        self.config = config
        self.path = path
        if commads is not None:
            self.commands = commads
        else:
            self.commands = []
def run_node(node):
    os.mkdir(node.path)
    os.popen("cp %s %s/%s" % (node.config.path , node.path , node.config.name))
