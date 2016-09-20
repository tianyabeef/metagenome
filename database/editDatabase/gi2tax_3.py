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
    fna_list_path,outpathori,assembly_summary,taxids_info_file= args
    j=0
    taxids_info={}
    with open(taxids_info_file,"r") as fq:
        fq.next()
        for line in fq:
            tabs = line.strip().split("\t")
            taxids_info[tabs[8]] = line.strip()
    strain_species_taxid={}
    with open(assembly_summary,"r") as fq:
        for line in fq:
            if not line.strip().startswith("#"):
                tabs = line.strip().split("\t")
                try:
                    ftp_split = tabs[19].split("/")
                    strain_species_taxid[ftp_split[-1]] =tabs[0]
                except Exception,e:
                    sys.stderr.write(Exception,":",e)
    with open("%s/statistical.txt" % outpathori,"w") as haveout:
        with open(fna_list_path,"r") as fq1:
            for line in fq1:
                j = j+1
                sys.stdout.write("%s fna file" % j)
                fnafile_path = line.strip()
                seq_sum = 0
                for recond in SeqIO.parse(fnafile_path,"fasta"):
                    tabs = recond.id.split(" ")
                    if len(tabs)>0:
                        seq_sum = seq_sum+len(recond.seq)
                        haveout.write(tabs[0])
                        haveout.write(":")
                        haveout.write("%s;" % (len(recond.seq)))
                    else:
                        print recond.id
                        sys.stderr.write("%s can not split ,infor:%s\n" % (fnafile_path,recond.id))
                haveout.write("\t%s\t%s\n" % (fnafile_path,seq_sum))
    with open("%s/statistical.txt" % outpathori,"r") as fqsta ,\
            open("%s/GENOME.TAX" % outpathori,"w") as fqtax , open("%s/GENOME.SIZE" % outpathori,"w") as genomesize:
        for line in fqsta:
            tabs = line.strip().split("\t")
            gi_nums = [tmp.split(':') for tmp in tabs[0].split(';')[:-1]]
            fnafile_path = tabs[1]
            specise_read_len = tabs[2]
            try:
                if strain_species_taxid.has_key(fnafile_path.split("/")[-2]):
                    tax_inf=taxids_info[strain_species_taxid[fnafile_path.split("/")[-2]]]
                else:
                    sys.stdout("strain no have %s" % fnafile_path.split("/")[-2])
            except Exception,e:
                sys.stderr.write(Exception,":",e)
            for gi_and_len in gi_nums:
                gi_num = gi_and_len[0]
                gi_read_len = gi_and_len[1]
                fqtax.write("%s\t%s\n" % (gi_num,tax_inf))
                genomesize.write("%s\t%s\t%s\n" % (gi_num,gi_read_len,specise_read_len))




