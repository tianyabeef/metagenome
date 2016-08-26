#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import argparse
import sys

def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    pa = parser.add_argument(type=str,required=True)
    pa('-n','--name',dest='name',metavar='name',
       help='set updata name bacteria Archaea Fungi Virus')
    pa('--org_dir',dest='org_dir',metavar='ORGDIR',
       help='set origin dir example /data_center_06/Database/NCBI_Bacteria/20160326/Bacteria/')
    pa('--up_dir',dest='up_dir',metavar='UPDIR',
       help='set up dir example /data_center_06/Database/NCBI_Bacteria/20160825/Bacteria')
    args = parser.parse_args()
    params = vars(args)
    return params
if __name__ == '__main__':
    params = read_params(sys.argv)
    name = params["name"]
    org_dir = params["org_dir"]
    up_dir = params["up_dir"]
