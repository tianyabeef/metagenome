#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import os
import re
import sys
import tarfile
from Bio import SeqIO
if __name__ == '__main__':
    args = sys.argv
    args.pop(0)
    path,outpathori,gitxt = args
    fna_list_path = "/data_center_04/Projects/test_Q30/NCBI_Bacteria/Bacteria_file_fna_list.txt"
    gi_ori={}
    i=0
    j=0
    with open(gitxt,"r") as fqgi:
                        for line in fqgi:
                            tabs = line.strip().split("\t")
                            gi_ori[tabs[0]]=tabs[1]
    print "read gitxt end!"
    with open(path,"r") as fq , open("%s/statistical.txt" % outpathori,"w") as haveout , open("%s/nohave.txt" % outpathori,"w") as nohaveout , open("%s/cat.txt" % outpathori,"w") as catout:
        with open(fna_list_path,"r") as fq1:
            for line in fq1:
                j = j+1
                print "%s fna file" % j
                fnafile_path = line.strip().split("\t")[1]
                catout.write("%s\n" % fnafile_path)
                for recond in SeqIO.parse(fnafile_path,"fasta"):
                    m = re.match("^gi\|(\d*)\|gb\|([A-Za-z0-9\.]+)\| ([\s\S]*),\.*",recond.description)
                    if m:
                        gi_num,gb_num,name=m.groups()
                    else:
                        gi_num=re.match("^gi\|(\d*)\|\.*",recond.id).group(1)
                        gb_num = recond.id
                        name = recond.description.split(",")[0]
                        sys.stderr.write("%s can not split ,infor:%s\n" % (fnafile_path,recond.id))
                    species = os.path.dirname(fnafile_path).split("/")[-1].split("_")
                    del species[-1]
                    species_name = " ".join(species)
                    if gi_ori.has_key(gi_num):
                        haveout.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (species_name,gi_num,gi_ori[gi_num],gb_num,name,len(recond.seq)))
                    else:
                        nohaveout.write("%s\n" % gi_num)

        tarlist = [line.strip().split("\t")[1] for line in fq if re.match(".*contig\.fna.*",line.strip().split("\t")[1])]
        for file in tarlist:
            i = i+1
            print "%s\t%s" % (i,file)
            filename = os.path.dirname(file).split("/")[-1]
            outpath = "%s/%s/" % (outpathori,filename)
            if not os.path.exists(outpath):
                os.popen("mkdir %s" % outpath)
            t = tarfile.open(file,"r")
            fnas = t.getnames()
            t.extractall(path=outpath)
            t.close()
            for fnafile in fnas:
                fnafile_path = "%s/%s" % (outpath,fnafile)
                catout.write("%s\n" % fnafile_path)
                for recond in SeqIO.parse(fnafile_path,"fasta"):
                    m = re.match("^gi\|(\d*)\|gb\|([A-Za-z0-9\.]+)\| ([\s\S]*),\.*",recond.description)
                    if m:
                        gi_num,gb_num,name=m.groups()
                    else:
                        gi_num=re.match("^gi\|(\d*)\|\.*",recond.id).group(1)
                        gb_num = recond.id
                        name = recond.description.split(",")[0]
                        sys.stderr.write("%s can not split ,infor:%s\n" % (fnafile_path,recond.id))
                    species = os.path.dirname(fnafile_path).split("/")[-1].split("_")
                    del species[-1]
                    species_name = " ".join(species)
                    if gi_ori.has_key(gi_num):
                        haveout.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (species_name,gi_num,gi_ori[gi_num],gb_num,name,len(recond.seq)))
                    else:
                        nohaveout.write("%s\n" % gi_num)



