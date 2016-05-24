#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import  sys

if __name__ == '__main__':
    _,gi2tax_txt,out_txt = sys.argv
    j=0
    with open(gi2tax_txt,"rb") as fq , open(out_txt,"wb") as fqout:
        for line in fq:
            j=j+1
            tabs = line.strip().split("\t")
            if tabs[9] == "-":
                print tabs[0]
            else:
                tabs[9] = "sk__%s" % tabs[9]
            if tabs[8] == "-":
                tabs[8] = "k__%s" % tabs[9].split("__")[1]
            else:
                tabs[8] = "k__%s" % tabs[8]
            if tabs[7] == "-":
                tabs[7] = "p__%s" % tabs[8].split("__")[1]
            else:
                tabs[7] = "p__%s" % tabs[7]
            if tabs[6] == "-":
                tabs[6] = "c__%s" % tabs[7].split("__")[1]
            else:
                tabs[6] = "c__%s" % tabs[6]
            if tabs[5] == "-":
                tabs[5] = "o__%s" % tabs[6].split("__")[1]
            else:
                tabs[5] = "o__%s" % tabs[5]
            if tabs[4] == "-":
                tabs[4] = "f__%s" % tabs[5].split("__")[1]
            else:
                tabs[4] = "f__%s" % tabs[4]
            if tabs[3] == "-":
                tabs[3] = "g__%s" % tabs[4].split("__")[1]
            else:
                tabs[3] = "g__%s" % tabs[3]
            if tabs[2] == "-":
                tabs[2] = "s__%s" % tabs[3].split("__")[1]
            else:
                tabs[2] = "s__%s" % tabs[2]
            fqout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (tabs[0],tabs[1],tabs[9],tabs[8],tabs[7],tabs[6],tabs[5],tabs[4],tabs[3],tabs[2]))
    print j
