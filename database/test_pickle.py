#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"



import pickle
import sys

if __name__ == '__main__':
    #_,outdir = sys.argv
    rank={"species":1,"genus":1, "family":1,
          "class":1,"order":1,"phylum":1,"kingdom":1,"superkingdom":1}
    tax2name ={}
    merged = {}
    tax2rank = {}
    gi2tax = {}

    with open("names.dmp","r") as fq:
        for line in fq:
            tabs = line.strip().split("|")
            tax_id = tabs[0].strip()
            desc = tabs[1].strip()
            types = tabs[3].strip()
            if types == "scientific name":
                continue
            tax2name[tax_id]=desc
    with open("nodes.dmp","r") as fq:
        for line in fq:
            tabs = line.strip().split("|")
            tax_id= tabs[0].strip()
            parent_id = tabs[1].strip()
            rank = tabs[2].strip()
            tax2rank[tax_id]=[parent_id,rank];
    with open("merged.dmp","r") as fq:
        for line in fq:
            tabs=line.strip().split("|")
            old = tabs[0].strip()
            new = tabs[1].strip()
            merged[old]=new

    output = open('data.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(tax2name, output)

    # Pickle the list using the highest protocol available.
    pickle.dump(merged, output, 2)

    output.close()