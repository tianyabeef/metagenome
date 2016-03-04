#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys
import re
from Bio import SeqIO


def match_adaptor(read,seed):
    seq = read.seq

#seed_first
    index=-1
    indexs = []
    while True:
        index = seq.find(seed,index+1)#从index+1位置开始找，如果找到返回索引，没找到则返回-1
        if index==-1:#没找到 跳出
            break
        indexs.append(index)
    return indexs

def rmPE(read1,read2,adaptor1,adaptor2,min_length):
    seq1 = read1.seq
    if len(adaptor1)>30:
        pos = seq1.find(adaptor1[0:30])
    seq2 = read2.seq
    if pos > 0:
        if  seq2.find(adaptor2[0:20]) == pos:
            pass
            #TODO del fastq
            # pos2 = seq2.find(adaptor2)
            # if pos2<0:
            #     print "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT"
            #     end = seq2[pos:(len(seq2)-1)]
            #     print end
            #     print adaptor2.find(end)

    adaptor_read1_pos_1 = match_adaptor(read1,adaptor1[0:7])
    adaptor_read1_pos_2 = match_adaptor(read1,adaptor1[7:13])
    adaptor_read2_pos_1 = match_adaptor(read2,adaptor2[0:7])
    adaptor_read2_pos_2 = match_adaptor(read2,adaptor2[7:13])
    if not (adaptor_read1_pos_1 + adaptor_read1_pos_2 + adaptor_read2_pos_1 + adaptor_read2_pos_2):
        pass
        #TODO clean reads
        print "%s\t%s\t%s\t%s" % (adaptor_read1_pos_1,adaptor_read1_pos_2,adaptor_read2_pos_1,adaptor_read2_pos_2)
    elif(not ((adaptor_read1_pos_1 and adaptor_read1_pos_2) and (adaptor_read2_pos_1 and adaptor_read2_pos_2))):
        #TODO clean reads
        print "%s\t%s\t%s\t%s" % (adaptor_read1_pos_1,adaptor_read1_pos_2,adaptor_read2_pos_1,adaptor_read2_pos_2)
    else:
        res_1 = rmSE(read1,adaptor1,min_length)
        res_2 = rmSE(read2,adaptor2,min_length)
        if res_1 and res_2:
            return res_1,res_2
        else:
            return False





def rmSE(read,adaptor,min_length):
    pass

    # def rmSE(read,adaptor,min_length):
    # seq = read.seq
    # seed_len = 6
    # adaptor_len = len(adaptor)
    # seq_len = len(seq)
    # for i in range(adaptor_len - seed_len):
    #     seed = adaptor[i:i+seed_len]
    #     pos = 0
    #     while(pos < seq_len):
    #         find_pos = seq.find(seed,pos)
    #         if find_pos > 0:
    #             mistaken_count = 0
    #             _b = find_pos
    #             _e = find_pos + seed_len
    #             while(_b >= 0 and i >= find_pos - _b):
    #                 if adaptor[i - find_pos + _b] != seq[_b]:
    #                     mistaken_count += 1
    #                 if mistaken_count > 3:
    #                     break
    #                 _b -= 1
    #             else :
    #                 while(_e < seq_len and i - find_pos + _e < adaptor_len):
    #                     if adaptor[ i - find_pos + _e ] != seq[_e]:
    #                         mistaken_count += 1
    #                     if mistaken_count > 3:
    #                         break
    #                     _e += 1
    #                 else:
    #                     return False
    #             pos = find_pos + 1
    #         else:
    #             break
    # return reads

def rmAdaptor(argv):
    argv.pop(0)
    type = argv.pop(0)
    if type=='PE':
        read1_file,read2_file,adaptor1,adaptor2,out_prefix,min_length = argv
        read2_records = SeqIO.parse(open(read2_file),'fastq')
        read1_out = open( '%s.1.fq'%out_prefix,'w' )
        read2_out = open( '%s.2.fq'%out_prefix,'w' )
        for read1 in SeqIO.parse(open(read1_file),'fastq'):
            read2 = read2_records.next()
            rmPE_res = rmPE(read1,read2,adaptor1,adaptor2,min_length)
            if rmPE_res:
                read1_out.write(rmPE_res[0].format('fastq'))
                read2_out.write(rmPE_res[1].format('fastq'))
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





if __name__ == '__main__':
    sys.argv = ['workflow\\script\\01.rmAdaptor.py', 'PE', 'D:\\Workspaces\\metagenome\\read1.fq', 'D:\\Workspaces\\metagenome\\read2.fq', 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC', 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT', 'D:\\Workspaces\\metagenome\\test', '150']
    rmAdaptor(sys.argv)

