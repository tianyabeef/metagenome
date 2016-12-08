#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
import pandas as pd
import time
from collections import defaultdict
import numpy as np
import os
def read_params(args):
    parser = argparse.ArgumentParser(description='''species abundance profile ''')
    stat_choices = ['avg_g','avg_l','tavg_g','tavg_l','wavg_g','wavg_l','med']
    parser.add_argument('-i', '--match_file', dest='match_file', metavar='FILE', type=str, required=True,
                        help="MATCH file")
    parser.add_argument('-o', '--species_abundance', dest='species_abundance', metavar='FILE', type=str, required=True,
                        help="species_abundance")
    parser.add_argument('-oc', '--species_coverage', dest='species_coverage', metavar='FILE', type=str, required=True,
                        help="species_coverage")
    parser.add_argument('-log', '--log', dest='log', metavar='FILE', type=str, required=True,
                        help="species_abundance.log")
    parser.add_argument('-r',dest='rep',metavar='NUM',type=int,default=2,
                        help=" INT   How  to  report repeat hits,1=random one; 2=all, [2]")
    parser.add_argument( '--stat',dest = "stat", metavar="STR", choices=stat_choices, default="avg_g", type=str, help =
         "EXPERIMENTAL! Statistical approach for converting marker abundances into clade abundances\n"
         "'avg_g'  : clade global (i.e. normalizing all markers together) average\n"
         "'avg_l'  : average of length-normalized marker counts\n"
         "'tavg_g' : truncated clade global average at --stat_q quantile\n"
         "'tavg_l' : trunated average of length-normalized marker counts (at --stat_q)\n"
         "'wavg_g' : winsorized clade global average (at --stat_q)\n"
         "'wavg_l' : winsorized average of length-normalized marker counts (at --stat_q)\n"
         "'med'    : median of length-normalized marker counts\n"
         "[default avg_g]"   )
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
    parser.add_argument('--strain_abundance',dest='strain_abundance', action = 'store_true',default=False,
         help="add put out strain abundance")
    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    #sys.argv = ["test.py", "-i", "test.out", "-o", "test.out2", "-log", "test.log"]
    # sys.argv=["species_py", "-i","tt","-o","test.out","-log","test.log"]
    params = read_params(sys.argv)
    match_file = params["match_file"] #解析出来的match文件
    species_abundance = params["species_abundance"] #输出结果
    species_coverage = params["species_coverage"]
    logout = params["log"] #出来log文件
    rep = params["rep"] #随机，或所有
    stat = params["stat"] #丰度统计方式
    quantile = params["stat_q"]
    min_alignment_len = params["min_alignment_len"]
    strain = {}
    B_strain = {}
    A_strain = {}
    F_strain = {}
    V_strain = {}
    species = {}
    strain_gi=defaultdict(set)
    gi_len = {}
    strain_len = {}
    TAXLIST=["/data_center_06/Database/NCBI_Bacteria/20160825/accession/GENOME.TAX","/data_center_06/Database/NCBI_Archaea/20160525/accession/GENOME.TAX","/data_center_06/Database/NCBI_Fungi/20160601/accession/GENOME.TAX","/data_center_06/Database/NCBI_Virus/20160615/accession/GENOME.TAX"]
    SIZELIST=["/data_center_06/Database/NCBI_Bacteria/20160825/accession/GENOME.SIZE","/data_center_06/Database/NCBI_Archaea/20160525/accession/GENOME.SIZE","/data_center_06/Database/NCBI_Fungi/20160601/accession/GENOME.SIZE","/data_center_06/Database/NCBI_Virus/20160615/accession/GENOME.SIZE"]
    for ttax in TAXLIST:
       with open(ttax,"r") as fq:
           if ttax.find("Bacteria")>0:
               for line in fq:
                   tabs = line.strip().split("\t")
                   B_strain[tabs[0]] = tabs[9]
                   strain[tabs[0]] = tabs[9] #登入号对应物种
                   species[tabs[9]] = tabs[7]
                   strain_gi[tabs[9]].add(tabs[0])
           if ttax.find("Archaea")>0:
               for line in fq:
                   tabs = line.strip().split("\t")
                   A_strain[tabs[0]] = tabs[9]
                   strain[tabs[0]] = tabs[9] #登入号对应物种
                   species[tabs[9]] = tabs[7]
                   strain_gi[tabs[9]].add(tabs[0])
           if ttax.find("Fungi")>0:
               for line in fq:
                   tabs = line.strip().split("\t")
                   F_strain[tabs[0]] = tabs[9]
                   strain[tabs[0]] = tabs[9] #登入号对应物种
                   species[tabs[9]] = tabs[7]
                   strain_gi[tabs[9]].add(tabs[0])
           if ttax.find("Virus")>0:
               for line in fq:
                   tabs = line.strip().split("\t")
                   V_strain[tabs[0]] = tabs[9]
                   strain[tabs[0]] = tabs[9] #登入号对应物种
                   species[tabs[9]] = tabs[7]
                   strain_gi[tabs[9]].add(tabs[0])
    for tsize in SIZELIST:
        with open(tsize,"r") as fq:
            for line in fq:
                tabs = line.strip().split("\t")
                gi_len[tabs[0]] = float(tabs[1]) #gi的长度
                strain_len[tabs[0]] = float(tabs[2]) #strain的长度

    starttime = time.time()
    B_match_nums = 0
    A_match_nums = 0
    F_match_nums = 0
    V_match_nums = 0
    with open(match_file,"r") as infq , open(species_abundance,"w") as outfq ,open(species_coverage,"w") as outfqcoverage, open(logout,"w") as logfq:
        reads_gi = defaultdict(set)
        gi_counter = {}
        gi_bases = defaultdict(set)
        abund_str = {}
        cover_str = {}#converages of strain
        cover_g_str = {}#coverages breadth  of strain
        strain_statistical_len ={} #statistical len of strain
        strain_statistical_reads = {} #statistical the num of reads in strain
        abund_sp = {}
        cover_sp_temp = defaultdict(list)
        cover_g_sp_temp = defaultdict(list)
        sp_statistical_len =defaultdict(list)
        sp_statistical_reads = defaultdict(list)
        sp_statistical_reads_single = defaultdict(list)
        strain_reads = {}
        strain_reads_single ={}
        cover_sp = {} # converages of species
        cover_g_sp ={} #coverages breadth  of species
        for line in infq:
            if line.startswith(","):
                headline = line.strip().split(",")
                continue
            tabs = line.strip().split(",")
            if len(tabs)!=len(headline):
                raise TypeError("err tabs num in %s file"%match_file)
            query = tabs.pop(0)#reads编号
            hits=[]
            for key in tabs:
                if not key:
                    continue
                subtabs = key.strip().strip("\"").split(";:")
                for subkey in  subtabs:
                    subchot = subkey.strip().split("\t")
                    subchot[1]=int(subchot[1].strip('M'))
                    if min_alignment_len==None or min_alignment_len<subchot[1]:
                        #0:IDxxx  1:150M  2:mismatchsum 3:stata 4:startb ,5:blen
                        hits.append((subchot[0],subchot[1],subchot[2],subchot[3],subchot[4]))
                    else:
                        sys.stderr.write("align match length is %s < %s "%(subchot[1],min_alignment_len))
                        continue
            hits = sorted(hits,key=lambda x: (-x[1], x[2]))
            max_M = hits[0][1]
            min_s = hits[0][2]
            besthit_num = 0
            besthits = []
            if rep==2:
                for n,M,s,astart,bstart in hits:
                    if M<max_M or s>min_s:
                        continue
                    elif M==max_M and s==min_s:
                        besthit_num += 1
                        besthits.append((n,astart,bstart,M))
                    else:
                        sys.stderr.write("min_s max statistical error")
            elif rep==1:
                besthits = besthits[0]
            for tempn in besthits:
                n,astart,bstart,alen = tempn
                if B_strain.has_key(n):
                    B_match_nums += 1/float(besthit_num)
                if A_strain.has_key(n):
                    A_match_nums += 1/float(besthit_num)
                if F_strain.has_key(n):
                    F_match_nums += 1/float(besthit_num)
                if V_strain.has_key(n):
                    V_match_nums += 1/float(besthit_num)
                reads_gi[strain[n]].add(n)
                gi_counter[n] = float(gi_counter[n])+1/float(besthit_num) if n in gi_counter else 1/float(besthit_num)
                for v in range(int(astart),int(int(alen)+int(astart))):
                    gi_bases[n].add(v)
                for v in range(int(bstart),int(int(alen)+int(bstart))):
                    gi_bases[n].add(v)
                strain_reads[strain[n]]= strain_reads[strain[n]]+1 if strain[n] in strain_reads else 1
                if besthit_num==1:
                    strain_reads_single[strain[n]] = strain_reads_single[strain[n]]+1 if strain[n] in strain_reads_single else 1
                else:
                    strain_reads_single[strain[n]] = 0
        for key,value in reads_gi.items():
            quant = int(quantile*len(reads_gi[key]))
            ql,qr,qn = (quant,-quant,quant) if quant else (None,None,0)
            rat_nreads = []
            for gi in value:
                le = float(gi_len[gi])
                co = float(gi_counter[gi])
                coverage = len(gi_bases[gi])
                coverage_g = max(gi_bases[gi])-min(gi_bases[gi])+1
                rat_nreads.append((le,co,coverage,coverage_g))
            for gi in strain_gi[key]:
                if gi not in value:
                    le = float(gi_len[gi])
                    rat_nreads.append((le,0,0,0))
            rat_nreads = sorted(rat_nreads, key = lambda x: x[1])
            rat_v,nreads_v,coverage_v,coverage_g_v = zip(*rat_nreads) if rat_nreads else sys.stderr.write("rat_nreads statical err")
            try:
                rat, nrawreads,coverages,coverages_g= float(sum(rat_v)),float(sum(nreads_v)),float(sum(coverage_v)),float(sum(coverage_g_v))
            except TypeError:
                print(rat_nreads)
            if stat == 'avg_g' or (not qn and stat in ['wavg_g','tavg_g']):
                loc_ab = nrawreads / rat if rat >= 0 else 0.0
                loc_cov = coverages/ rat if rat >= 0 else 0.0
                loc_cov_g = coverages_g/ rat if rat >= 0 else 0.0
            elif stat == 'avg_l' or (not qn and stat in ['wavg_l','tavg_l']):
                loc_ab = np.mean([float(n)/r for r,n in rat_nreads])
            # elif stat == 'tavg_g':
            #     wnreads = sorted([(float(n)/r,r,n) for r,n in rat_nreads], key=lambda x:x[0])
            #     den,num = zip(*[v[1:] for v in wnreads[ql:qr]])
            #     loc_ab = float(sum(num))/float(sum(den)) if any(den) else 0.0
            elif stat == 'tavg_l':
                loc_ab = np.mean(sorted([float(n)/r for r,n in rat_nreads])[ql:qr])
            # elif stat == 'wavg_g':
            #     vmin, vmax = nreads_v[ql], nreads_v[qr]
            #     wnreads = [vmin]*qn+list(nreads_v[ql:qr])+[vmax]*qn
            #     loc_ab = float(sum(wnreads)) / rat
            elif stat == 'wavg_l':
                wnreads = sorted([float(n)/r for r,n in rat_nreads])
                vmin, vmax = wnreads[ql], wnreads[qr]
                wnreads = [vmin]*qn+list(wnreads[ql:qr])+[vmax]*qn
                loc_ab = np.mean(wnreads)
            elif stat == 'med':
                loc_ab = np.median(sorted([float(n)/r for r,n in rat_nreads])[ql:qr])
            abund_str[key] = loc_ab
            cover_str[key] = loc_cov
            cover_g_str[key] = loc_cov_g
            strain_statistical_len[key] = int(rat)
            strain_statistical_reads[key] = int(strain_reads[key])
        for key,value in abund_str.items():
	    if key=="GCA_000774955.1" or key=="GCA_000774945.1" or key=="GCA_000774975.1" or key=="GCA_000770565.1" or key=="GCA_000827875.1" or key=="GCA_000757255.1" or key=="GCA_000763555.1" or key=="GCA_001563765.1" or key=="GCA_001461825.1" or key=="GCA_001461835.1" or key=="GCA_001461845.1" or key=="GCA_001521815.1" :
                continue
            abund_sp[species[key]] = abund_sp[species[key]]+value if species[key] in abund_sp else value
        for key,value in cover_str.items():
            cover_sp_temp[species[key]].append(value)
            sp_statistical_len[species[key]].append(strain_statistical_len[key])
            sp_statistical_reads[species[key]].append(strain_statistical_reads[key])
            sp_statistical_reads_single[species[key]].append(strain_reads_single[key])
        for key,value in cover_g_str.items():
            cover_g_sp_temp[species[key]].append(value)
        for key,value in cover_sp_temp.items():
            cover_sp[key] = float(sum(value))/len(value)
        for key,value in cover_g_sp_temp.items():
            cover_g_sp[key] = float(sum(value))/len(value)
        df = pd.DataFrame(abund_sp,index=["a"])
        total_abundance = float(df.sum(axis=1))
        abund_sp = sorted(abund_sp.items(),key = lambda d: d[1])
        for key,value in abund_sp:
            if value!=0:
                outfq.write("%s\t%s\n"%(key,value/total_abundance))
                outfqcoverage.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(key,";".join([str(sing) for sing in sp_statistical_reads_single[key]]) ,";".join([str(rea) for rea in sp_statistical_reads[key]]),';'.join([str(vs) for vs in sp_statistical_len[key]]),cover_sp[key],cover_g_sp[key]))
            else:
                logfq.write("%s\t%s\tabundance is zero\n"%(key,value))
        #for key,value in cover_sp.items():
        #    if value!=0:
                
        endtime = time.time()
        logfq.write("matchs\tBacteria\tArchaea\tFungi\tVirus\n%s\t%s\t%s\t%s\nuse time is %s second\n" % (B_match_nums,A_match_nums,F_match_nums,V_match_nums,(endtime-starttime)))
        logfq.write("total_abundance:%s"%total_abundance)
        if params['strain_abundance']:
            try:
                sname = os.path.basename(species_abundance).split("\.")[0]
            except Exception,e:
                print "%s file name need XXX.species.abundance"%species_abundance
            strain_abundance = "%s/%s.strain.abundance"%(os.path.dirname(species_abundance),sname)
            with open(strain_abundance,"w") as outfq:
                for key,value in abund_str.items():
                    outfq.write("%s\t%s\n"%(key,value/total_abundance))
