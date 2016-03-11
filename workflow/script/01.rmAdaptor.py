#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
import re
from Bio import SeqIO




mistaken_ratio = 0.2
keep_reads = True


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
    print "%s\t%s\t%s\t%s\n" % (adaptor_read1_pos_1,adaptor_read1_pos_2,adaptor_read2_pos_1,adaptor_read2_pos_2)
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
def rmPE(read1,read2,adaptor1,adaptor2,min_length):
    result = situation_1(read1,read2,adaptor1,adaptor2)
    if result[0]:
        return False,result[1],result[2] #del seq1 and seq2

    result = situation_2(read1,read2,adaptor1,adaptor2)
    if result[0]:
        return True,result[1],result[2]

    res_1 = rmSE(read1,adaptor1,min_length,mistaken_ratio)
    res_2 = rmSE(read2,adaptor2,min_length,mistaken_ratio)
    if res_1 and res_2:
        return True,res_1,res_2
    else:
        return False,read1,read2 #有比较多的错配


def rmSE(read,adaptor,min_length,mistaken_ratio):
    seq = read.seq
    seed_len = 6
    adaptor_len = len(adaptor)

    seq_len = len(seq)
    _b = seq_len
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
                        return False
                pos = find_pos + 1
            else:
                break
    return read[:_b+1]


def rmAdaptor(argv):
    argv.pop(0)
    type = argv.pop(0)
    if type=='PE':
        read1_file,read2_file,adaptor1,adaptor2,out_prefix,min_length = argv
        read2_records = SeqIO.parse(open(read2_file),'fastq')
        read1_out = open( '%s.1.fq'%out_prefix,'w' )
        read2_out = open( '%s.2.fq'%out_prefix,'w' )
        read1_rm_out = open( '%s.1_rm.fq'%out_prefix,'w' )
        read2_rm_out = open( '%s.2_rm.fq'%out_prefix,'w' )
        for read1 in SeqIO.parse(open(read1_file),'fastq'):
            read2 = read2_records.next()
            rmPE_res = rmPE(read1,read2,adaptor1,adaptor2,min_length)
            if rmPE_res[0]:
                read1_out.write(rmPE_res[1].format('fastq'))
                read2_out.write(rmPE_res[2].format('fastq'))
            else:
                read1_rm_out.write(rmPE_res[1].format('fastq'))
                read2_rm_out.write(rmPE_res[2].format('fastq'))
        read1_out.close()
        read2_out.close()
        read1_rm_out.close()
        read2_rm_out.close()
    elif type=='SE':
        reads_file,adaptor1,adaptor2,out_prefix,min_length = argv
        reads_out = open( '%s.single.fq'%out_prefix,'w' )
        for reads in SeqIO.parse(open(reads_file),'fastq'):
            rmSE_res = False
            if re.search('[\s\/](\d)',reads.id).group(1) == '1':
                rmSE_res = rmSE(reads,adaptor1,min_length)
            elif re.search('[\s\/](\d)',reads.id).group(1) == '2':
                rmSE_res = rmSE(reads,adaptor2,min_length)
            if rmSE_res:
                reads_out.write(rmSE_res.format('fastq'))
        reads_out.close()




if __name__ == '__main__':
    sys.argv = ['workflow\\script\\01.rmAdaptor.py', 'PE', 'D:\\Workspaces\\metagenome\\test.read.1.fq', 'D:\\Workspaces\\metagenome\\test.read.2.fq', 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC', 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT', 'D:\\Workspaces\\metagenome\\test', '150']
    rmAdaptor(sys.argv)

