#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import  argparse
import sys
import re
GENOME_TXT = "/data_center_06/Database/NCBI_Bacteria/20160422/accession/GENOME.TAX"

def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--input', dest='input', metavar='input', type=str, required=True,
                        help="abundance of list file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str,
                        help="out put dir")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    list_file = params["input"]
    genus_pro={}
    family_pro={}
    order_pro={}
    class_pro={}
    phylum_pro={}
    with open(GENOME_TXT,"r") as fq:
        for line in fq:
            tax = line.strip().split("\t")
            species = tax[-1]
            genus_pro[species] = tax[-2]
            family_pro[species] = tax[-3]
            order_pro[species] = tax[-4]
            class_pro[species] = tax[-5]
            phylum_pro[species] = tax[-6]



    with open(list_file,"r") as fq:
        for line in fq:
            strinfo = re.compile(".species.abundance$")
            name = strinfo.sub("",line.strip())
            genus_abun = {}
            family_abun = {}
            order_abun = {}
            class_abun = {}
            phylum_abun = {}
            with open(line.strip(),"r") as fq2:
                for line_abu in fq2:
                    species,abun = line_abu.strip().split("\t")
                    abun = float(abun)
                    genus_abun[genus_pro[species]] = genus_abun[genus_pro[species]] + abun if genus_abun.has_key(genus_pro[species]) else abun
                    family_abun[family_pro[species]] = abun + family_abun[family_pro[species]]  if family_abun.has_key(family_pro[species]) else abun
                    order_abun[order_pro[species]] = abun + order_abun[order_pro[species]] if order_abun.has_key(order_pro[species]) else abun
                    class_abun[class_pro[species]] = abun + class_abun[class_pro[species]] if class_abun.has_key(class_pro[species]) else abun
                    phylum_abun[phylum_pro[species]] = abun + phylum_abun[phylum_pro[species]] if phylum_abun.has_key(phylum_pro[species]) else abun


            with open("%s.genus.abundance" % name,"w") as fqw:
                for key,value in genus_abun.items():
                    fqw.write("%s\t%s\n" % (key,value))
            with open("%s.family.abundance" % name,"w") as fqw:
                for key,value in family_abun.items():
                    fqw.write("%s\t%s\n" % (key,value))
            with open("%s.order.abundance" % name,"w") as fqw:
                for key,value in order_abun.items():
                    fqw.write("%s\t%s\n" % (key,value))
            with open("%s.class.abundance" % name,"w") as fqw:
                for key,value in class_abun.items():
                    fqw.write("%s\t%s\n" % (key,value))
            with open("%s.phylum.abundance" % name,"w") as fqw:
                for key,value in phylum_abun.items():
                    fqw.write("%s\t%s\n" % (key,value))

