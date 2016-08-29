#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
import pandas as pd
import time
from collections import defaultdict
import numpy as np
def read_params(args):
    parser = argparse.ArgumentParser(description='''species abundance profile ''')
    stat_choices = ['avg_g','avg_l','tavg_g','tavg_l','wavg_g','wavg_l','med']
    parser.add_argument('-i', '--match_file', dest='match_file', metavar='FILE', type=str, required=True,
                        help="MATCH file")
    parser.add_argument('-o', '--species_abundance', dest='species_abundance', metavar='FILE', type=str, required=True,
                        help="species_abundance")
    parser.add_argument('-log', '--log', dest='log', metavar='FILE', type=str, required=True,
                        help="species_abundance.log")
    parser.add_argument('-r',dest='rep',metavar='NUM',type=int,default=2,
                        help=" INT   How  to  report repeat hits,1=random one; 2=all, [2]")
    parser.add_argument( '--stat',dest = "stat", metavar="STR", choices=stat_choices, default="tavg_g", type=str, help =
         "EXPERIMENTAL! Statistical approach for converting marker abundances into clade abundances\n"
         "'avg_g'  : clade global (i.e. normalizing all markers together) average\n"
         "'avg_l'  : average of length-normalized marker counts\n"
         "'tavg_g' : truncated clade global average at --stat_q quantile\n"
         "'tavg_l' : trunated average of length-normalized marker counts (at --stat_q)\n"
         "'wavg_g' : winsorized clade global average (at --stat_q)\n"
         "'wavg_l' : winsorized average of length-normalized marker counts (at --stat_q)\n"
         "'med'    : median of length-normalized marker counts\n"
         "[default tavg_g]"   )
    parser.add_argument('--stat_q', dest = "stat_q",metavar="STR", type = float, default=0.1, help =
         "Quantile value for the robust average\n"
         "[default 0.1]"   )
    parser.add_argument( '--min_cu_len', dest="min_cu_len",metavar="", default="2000", type=int, help =
         "minimum total nucleotide length for the markers in a clade for\n"
         "estimating the abundance without considering sub-clade abundances\n"
         "[default not to do]\n"   )
    parser.add_argument( '--min_alignment_len',dest="min_alignment_len", metavar="", default=None, type=int, help =
         "The sam records for aligned reads with the longest subalignment\n"
         "length smaller than this threshold will be discarded.\n"
         "[default None]\n"   )

    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    sys.argv = ["test.py", "-i", "test.out", "-o", "test.out2", "-log", "test.log"]
    #sys.argv=["species_py", "-i","test2","-o","test.out","-log","test.log"]
    params = read_params(sys.argv)
    match_file = params["match_file"] #解析出来的match文件
    species_abundance = params["species_abundance"] #输出结果
    logout = params["log"] #出来log文件
    rep = params["rep"] #随机，或所有
    stat = params["stat"] #丰度统计方式
    quantile = params["stat_q"]
    min_alignment_len = params["min_alignment_len"]
    strain = {}
    gi_len = {}
    species = {}
    # TAXLIST=["/data_center_06/Database/NCBI_Bacteria/20160825/accession/GENOME.TAX","/data_center_06/Database/NCBI_Archaea/20160525/accession/GENOME.TAX","/data_center_06/Database/NCBI_Fungi/20160601/accession/GENOME.TAX","/data_center_06/Database/NCBI_Virus/20160615/accession/GENOME.TAX"]
    # SIZELIST=["/data_center_06/Database/NCBI_Bacteria/20160825/accession/GENOME.SIZE","/data_center_06/Database/NCBI_Archaea/20160525/accession/GENOME.SIZE","/data_center_06/Database/NCBI_Fungi/20160601/accession/GENOME.SIZE","/data_center_06/Database/NCBI_Virus/20160615/accession/GENOME.SIZE"]
    # for ttax in TAXLIST:
    #    with open(ttax,"r") as fq:
    #        for line in fq:
    #            tabs = line.strip().split("\t")
    #            strain[tabs[0]] = tabs[9] #登入号对应物种
    #            species[tabs[9]] = tabs[7]
    # for tsize in SIZELIST:
    #     with open(tsize,"r") as fq:
    #         for line in fq:
    #             tabs = line.strip().split("\t")
    #             gi_len[tabs[0]] = float(tabs[1]) #gi的长度

    starttime = time.time()
    species_value_unique = {}
    reads_unique_num = 0
    reads_multip_unispecies_num = 0
    reads_multip_mulspecies_num = 0
    match_nums = 0
    with open(match_file,"r") as infq , open(species_abundance,"w") as outfq , open(logout,"w") as logfq:
        reads_gi = defaultdict(set)
        gi_counter = {}
        abund_str = {}
        abund_sp = {}
        for line in infq:
            if line.startswith(","):
                headline = line.strip().split(",")
                continue
            match_nums += 1
            tabs = line.strip().split(",")
            if len(tabs)!=len(headline):
                raise TypeError("err tabs num in %s file"%match_file)
            query = tabs.pop(0)#reads编号
            hits=[]
            for key in tabs:
                if not key:
                    continue
                #if key.find("\""):
                subtabs = key.strip().strip("\"").split(";:")
                for subkey in  subtabs:
                    subchot = subkey.strip().split("\t")
                    subchot[1]=int(subchot[1].strip('M'))
                    if min_alignment_len==None or min_alignment_len<subchot[1]:
                        hits.append((subchot[0],subchot[1],subchot[2],subchot[3]))
                    else:
                        sys.stderr.write("align match length is %s < %s "%(subchot[1],min_alignment_len))
                        continue
                #else:
                #    raise TypeError("no have \" file!")
                    #chot = key.strip().split("\t")
                    #chot[1]=int(chot[1].strip('M'))
                    #if min_alignment_len==None or min_alignment_len<chot[1]:
                        #hit[chot[3]].append(chot[3])
                        #hit[chot[3]].append(chot[1])
                        #hit[chot[3]].append(chot[2])
                        #hits.append(hit[chot[3]])
                    #else:
                        #sys.stderr.write("align match length is %s < %s "%(chot[1],min_alignment_len))
                        #continue
            hits = sorted(hits,key=lambda x: (-x[1], x[2]))
            max_M = hits[0][1]
            min_s = hits[0][2]
            besthit_a_num =0
            besthit_b_num = 0
            besthits = []
            if rep==2:
                for n,M,s,tread in hits:
                    if M<max_M or s>min_s:
                        continue
                    elif M==max_M and s==min_s:
                        if tread == "a":
                            besthit_a_num += 1
                            besthits.append((n,tread))
                        else:
                            besthit_b_num += 1
                            besthits.append((n,tread))
                    else:
                        sys.stderr.write("min_s max statistical error")
            elif rep==1:
                besthits = besthits[0]
            if besthit_b_num >= besthit_a_num:
                for n,tread in besthits:
                    if tread=="b":
                        reads_gi[strain[n]].add(n)
                        gi_counter[n] = float(gi_counter[n])+float(1/besthit_b_num) if n in gi_counter else float(1/besthit_b_num)
            else:
                for n,tread in besthits:
                    if tread=="a":
                        reads_gi[strain[n]].add(n)
                        gi_counter[n] = float(gi_counter[n])+float(1/besthit_a_num) if n in gi_counter else float(1/besthit_a_num)
        for key,value in reads_gi.items():
            quant = int(quantile*len(reads_gi[key]))
            ql,qr,qn = (quant,-quant,quant) if quant else (None,None,0)
            rat_nreads = []
            for gi in value:
                le = gi_len[gi]
                co = gi_counter[gi]
                rat_nreads.append((le,co))
            rat_nreads = sorted(rat_nreads, key = lambda x: x[1])
            rat_v,nreads_v = zip(*rat_nreads) if rat_nreads else sys.stderr.write("rat_nreads statical err")
            try:
                rat, nrawreads= float(sum(rat_v)),float(sum(nreads_v))
            except TypeError:
                print(rat_nreads)
            if stat == 'avg_g' or (not qn and stat in ['wavg_g','tavg_g']):
                loc_ab = nrawreads / rat if rat >= 0 else 0.0
            elif stat == 'avg_l' or (not qn and stat in ['wavg_l','tavg_l']):
                loc_ab = np.mean([float(n)/r for r,n in rat_nreads])
            elif stat == 'tavg_g':
                wnreads = sorted([(float(n)/r,r,n) for r,n in rat_nreads], key=lambda x:x[0])
                den,num = zip(*[v[1:] for v in wnreads[ql:qr]])
                loc_ab = float(sum(num))/float(sum(den)) if any(den) else 0.0
            elif stat == 'tavg_l':
                loc_ab = np.mean(sorted([float(n)/r for r,n in rat_nreads])[ql:qr])
            elif stat == 'wavg_g':
                vmin, vmax = nreads_v[ql], nreads_v[qr]
                wnreads = [vmin]*qn+list(nreads_v[ql:qr])+[vmax]*qn
                loc_ab = float(sum(wnreads)) / rat
            elif stat == 'wavg_l':
                wnreads = sorted([float(n)/r for r,n in rat_nreads])
                vmin, vmax = wnreads[ql], wnreads[qr]
                wnreads = [vmin]*qn+list(wnreads[ql:qr])+[vmax]*qn
                loc_ab = np.mean(wnreads)
            elif stat == 'med':
                loc_ab = np.median(sorted([float(n)/r for r,n in rat_nreads])[ql:qr])
            abund_str[key] = loc_ab
        for key,value in abund_str.items():
            abund_sp[species[key]] = abund_sp[species[key]]+value if species[key] in abund_sp else value
        df = pd.DataFrame(abund_sp,index=["a"])
        total_abundance = float(df.sum(axis=1))
        abund_sp = sorted(abund_sp.items(),key = lambda d: d[1])
        for key,value in abund_sp:
            outfq.write("%s\t%s\n"%(key,value/total_abundance))
        endtime = time.time()
        logfq.write("sum match is %s\nuse time is %s second" % (match_nums,(endtime-starttime)))
