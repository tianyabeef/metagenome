#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
import re
from Bio import SeqIO
import os

def read_params(args):
    parser = argparse.ArgumentParser(description='plot alpha rare | v1.0 at 2015/09/28 by liangzb')
    parser.add_argument('--out_prefix',dest='out_prefix',metavar="DIR",type=str,required=True,
                        help="out file prefix")
    parser.add_argument('-r1', '--read1', dest='read1', metavar='DIR', type=str, required=True,
                        help="read1.fastq")
    parser.add_argument('-r2', '--read2', dest='read2', metavar='DIR', type=str, required=True,
                        help="read2.fastq")
    parser.add_argument('-a1', '--read1Adaptor', dest='read1Adaptor', metavar='string', type=str, required=True,
                        help="AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC")
    parser.add_argument('-a2', '--read2Adaptor', dest='read2Adaptor', metavar='string', type=str, required=True,
                        help="AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT")
    parser.add_argument('--type',dest="type",metavar='string',type=str,required=True,
                        help="PE or SE")
    parser.add_argument('--mistaken_ratio',dest="mistaken_ratio",metavar="int",type=float,default=0.2,
                        help="mistaken_ratio defult[0.2]")
    parser.add_argument('--out_type',dest="out_type",metavar="STRING",type=int,default=4,
                        help="2 : two file out ;  4 : four file out.")
    args = parser.parse_args()
    params = vars(args)
    return params





def match_adaptor(seq,seed):
#seed_first
    index=-1
    indexs = []
    while True:
        index = seq.find(seed,index+1)#从index+1位置开始找，如果找到返回索引，没找到则返回-1
        if index==-1:#没找到 跳出
            break
        indexs.append(index)
    return indexs
def situation_1(read1,read2,adaptor1,adaptor2):#adaptor1 30个碱基匹配到read1，adaptor2 20个碱基匹配到read2
    seq1 =read1.seq
    seq2 =read2.seq
    if len(adaptor1)>30:
        pos = seq1.find(adaptor1[0:30]) #截取30个碱基的adaptor1
    else:
        pos = seq1.find(adaptor1)
    if pos > 0:
        return True,read1[:pos],read2[:pos] # del seq1\seq2
    if len(adaptor2) > 30:
        pos2 = seq2.find(adaptor2[0:30])
    else:
        pos2 = seq2.find(adaptor2)
    if pos2 > 0:
        return True,read1[:pos2],read2[:pos2]
    return False,[],[]
def situation_2(read1,read2,adaptor1,adaptor2): #四次匹配中只有0、1、2次匹配上的
    seq1 = read1.seq
    seq2 = read2.seq
    true_num = 0
    adaptor_read1_pos_1 = match_adaptor(seq1,adaptor1[0:7])
    adaptor_read1_pos_2 = match_adaptor(seq1,adaptor1[7:13])
    adaptor_read2_pos_1 = match_adaptor(seq2,adaptor2[0:7])
    adaptor_read2_pos_2 = match_adaptor(seq2,adaptor2[7:13])
    if adaptor_read1_pos_1:
        true_num += 1
    if adaptor_read1_pos_2:
        true_num += 1
    if adaptor_read2_pos_1:
        true_num += 1
    if adaptor_read2_pos_2:
        true_num += 1
    if true_num == 0 or true_num==1 :
        return True,read1,read2 #clean reads
    else:
        return False,[],[]
def rmPE(read1,read2,adaptor1,adaptor2,mistaken_ratio):
    result = situation_1(read1,read2,adaptor1,adaptor2)
    if result[0]:
        return False,result[1],result[2] #del seq1 and seq2

    result = situation_2(read1,read2,adaptor1,adaptor2)
    if result[0]:
        return True,result[1],result[2]  #clean seq1 and seq2

    res_1 = rmSE(read1,adaptor1,mistaken_ratio)
    res_2 = rmSE(read2,adaptor2,mistaken_ratio)
    if res_1[0] and res_2[0]:
        return True,res_1[1],res_2[1]
    else:
        return False,res_1[1],res_2[1]


def rmSE(read,adaptor,mistaken_ratio):
    seq = read.seq
    seed_len = 6
    adaptor_len = len(adaptor)

    seq_len = len(seq)
    for i in [0,6,12]:
        seed = adaptor[i:i+seed_len]
        pos = 0
        while(pos < seq_len):
            find_pos = seq.find(seed,pos)
            if seq_len-find_pos>adaptor_len:
                mistaken_count_max = adaptor_len*mistaken_ratio
            else:
                mistaken_count_max = (seq_len-find_pos)*mistaken_ratio
            if find_pos > 0:
                mistaken_count = 0
                _b = find_pos
                _e = find_pos + seed_len
                while(_b >= 0 and i >= find_pos - _b):
                    if adaptor[i - find_pos + _b] != seq[_b]:
                        mistaken_count += 1
                    if mistaken_count > mistaken_count_max:
                        break
                    _b -= 1
                else :
                    while(_e < seq_len and i - find_pos + _e < adaptor_len):
                        if adaptor[ i - find_pos + _e ] != seq[_e]:
                            mistaken_count += 1
                        if mistaken_count > mistaken_count_max:
                            break
                        _e += 1
                    else:
                        return False,read[:_b+1]
                pos = find_pos + 1
            else:
                break
    return True,read


def rmAdaptor(type,read1_file,read2_file,adaptor1,adaptor2,out_prefix,out_type,mistaken_ratio):
    total_read_num = 0
    clean_read_num = 0
    adaptor_read_num = 0
    if type=='PE':
        read2_records = SeqIO.parse(open(read2_file),'fastq')
        read1_out = open( '%s.1.fq'%out_prefix,'w' )
        read2_out = open( '%s.2.fq'%out_prefix,'w' )
        if out_type==4:
            read1_rm_out = open( '%s.1_rm.fq'%out_prefix,'w' )
            read2_rm_out = open( '%s.2_rm.fq'%out_prefix,'w' )
            for read1 in SeqIO.parse(open(read1_file),'fastq'):
                total_read_num += 2
                read2 = read2_records.next()
                rmPE_res = rmPE(read1,read2,adaptor1,adaptor2,mistaken_ratio)
                if rmPE_res[0]:
                    clean_read_num += 2
                    read1_out.write(rmPE_res[1].format('fastq'))#clean read
                    read2_out.write(rmPE_res[2].format('fastq'))#clean read
                else:
                    adaptor_read_num += 2
                    read1_rm_out.write(rmPE_res[1].format('fastq'))#adaptor read
                    read2_rm_out.write(rmPE_res[2].format('fastq'))#adaptor read
            read1_rm_out.close()
            read2_rm_out.close()
        else:
            for read1 in SeqIO.parse(open(read1_file),'fastq'):
                total_read_num += 2
                read2 = read2_records.next()
                rmPE_res = rmPE(read1,read2,adaptor1,adaptor2,mistaken_ratio)
                if rmPE_res[0]:
                    clean_read_num += 2
                    read1_out.write(rmPE_res[1].format('fastq'))#clean read
                    read2_out.write(rmPE_res[2].format('fastq'))#clean read
                else:
                    adaptor_read_num += 2
                    read1_out.write(rmPE_res[1].format('fastq'))#adaptor read
                    read2_out.write(rmPE_res[2].format('fastq'))#adaptor read
        read1_out.close()
        read2_out.close()
        return total_read_num,clean_read_num,adaptor_read_num







if __name__ == '__main__':
    params = read_params(sys.argv)
    read1_file = params["read1"]
    read2_file = params["read2"]
    adaptor1 = params["read1Adaptor"]
    adaptor2 = params["read2Adaptor"]
    type = params["type"]
    out_prefix = params["out_prefix"]
    mistaken_ratio = params["mistaken_ratio"]
    out_type = params["out_type"]
    # type ="PE"
    # read1_file="D:\\Workspaces\\metagenome\\test.1.fq"
    # read2_file="D:\\Workspaces\\metagenome\\test.2.fq"
    # adaptor1="AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC"
    # adaptor2="AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT"
    # out_prefix = "D:\\Workspaces\\metagenome\\test2_"
    # out_type = 2
    # mistaken_ratio= 0.2

    total_read_num,clean_read_num,adaptor_read_num = rmAdaptor(type,read1_file,read2_file,adaptor1,adaptor2,out_prefix,out_type,mistaken_ratio)
    with open("%s_adaptor_statistical.tsv" % out_prefix,mode="w") as fqout:
        fqout.write("sampleName\ttotal_reads\tremain_reads\tadaptor_reads\n")
        fqout.write("%s\t%s\t%s\t%s\n" % (os.path.basename(out_prefix),total_read_num,clean_read_num,adaptor_read_num))
