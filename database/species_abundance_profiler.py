#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
import pandas as pd
import time
def read_params(args):
    parser = argparse.ArgumentParser(description='''species abundance profile ''')
    parser.add_argument('-i', '--match_file', dest='match_file', metavar='FILE', type=str, required=True,
                        help="MATCH file")
    parser.add_argument('-o', '--species_abundance', dest='species_abundance', metavar='FILE', type=str, required=True,
                        help="species_abundance")
    parser.add_argument('-log', '--log', dest='log', metavar='FILE', type=str, required=True,
                        help="species_abundance.log")
    args = parser.parse_args()
    params = vars(args)
    return params

if __name__ == '__main__':
    params = read_params(sys.argv)
    match_file = params["match_file"] #解析出来的match文件
    species_abundance = params["species_abundance"] #输出结果
    logout = params["log"] #出来log文件
    species = {}
    strains_len = {}
    with open("/data_center_06/Database/NCBI_Bacteria/20160422/accession/GENOME.TAX","r") as fq:
        for line in fq:
            tabs = line.strip().split("\t")
            species[tabs[0]] = tabs[-1] #登入号对应物种
    with open("/data_center_06/Database/NCBI_Bacteria/20160422/accession/GENOME.SIZE","r") as fq:
       for line in fq:
           tabs = line.strip().split("\t")
           strains_len[tabs[0]] = tabs[2] #菌株的长度

    starttime = time.time()
    species_value_unique = {}
    reads_unique_num = 0
    reads_multip_unispecies_num = 0
    reads_multip_mulspecies_num = 0
    with open(match_file,"r") as infq:
        for line in infq:
                if line.startswith(","):
                    continue
                tabs = line.strip().split(",")
                query = tabs.pop(0)#reads编号
                species_tem = {}#物种库
                reads_gi = {}
                for key in tabs:
                    if not key:
                        continue
                    chot = key.strip().strip("\"").split("\t")
                    if ( ( (chot[1] == "P") and (chot[3] == "b") ) or (chot[1] == "S")):
                        sys.stdout.write("warning hava s or pa\n")
                    else:
                        speciesName = species[chot[0]]
                        if reads_gi.has_key(speciesName):
                            reads_gi[speciesName].append(chot[0])
                        else:
                            reads_gi[speciesName] = []
                            reads_gi[speciesName].append(chot[0])
                for key,value in reads_gi.items():
                    le = 0
                    total_length = 0
                    for gi in value:
                        le = strains_len[gi]
                        total_length += float(le)
                    if len(reads_gi.keys()) == 1 :
                        if (float(total_length)/float(len(value)))==float(le):
                            reads_unique_num +=1
                        else:
                            reads_multip_unispecies_num += 1
                        if species_value_unique.has_key(key):
                            species_value_unique[key] += 1/(float(total_length)/float(len(value)))
                        else:
                            species_value_unique[key] = 1/(float(total_length)/float(len(value)))
                    elif len(reads_gi.keys()) > 1 :
                        if species_value_unique.has_key(key):
                            species_value_unique[key] += 1/float(len(reads_gi))/(float(total_length)/float(len(value)))
                        else:
                            species_value_unique[key] = 1/float(len(reads_gi))/(float(total_length)/float(len(value)))
                        reads_multip_mulspecies_num += 1/float(len(reads_gi))
    endtime = time.time()
    sys.stdout.write("static abundance time :%s second\n" % (endtime-starttime))
    with open(logout,"w") as log:
        log.write("%s\t%s\t%s\n" % (reads_unique_num,reads_multip_unispecies_num,reads_multip_mulspecies_num))

    with open(species_abundance,"w") as out:
        df = pd.DataFrame(species_value_unique,index=["a"])
        total_abundance = float(df.sum(axis=1))
        for key,value in species_value_unique.items():
            out.write("%s\t%s\n" % (key,(float(value)/float(total_abundance))))
