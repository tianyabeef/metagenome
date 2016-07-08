from collections import OrderedDict
import sys
import argparse
def read_params(args):
    parser = argparse.ArgumentParser(description='group file change')
    parser.add_argument('-i', '--input', dest='input', metavar='input', type=str, required=True,
                        help="input file")
    parser.add_argument('-o', '--outputdir', dest='outputdir', metavar='outputdir', type=str, required=True,
                        help="out put dir")
    args = parser.parse_args()
    params = vars(args)
    return params


if __name__ == '__main__':
    param = read_params(sys.argv)
    inputfile = param["input"]
    outdir = param["outputdir"]
    result = OrderedDict

    with open(inputfile,"r") as fq , \
           open("%s/otu_table_L1.txt"%outdir,"w") as fqout1 ,\
           open("%s/otu_table_L2.txt"%outdir,"w") as fqout2,\
           open("%s/otu_table_L3.txt"%outdir,"w") as fqout3,\
           open("%s/otu_table_L4.txt"%outdir,"w") as fqout4,\
           open("%s/otu_table_L5.txt"%outdir,"w") as fqout5,\
           open("%s/otu_table_L6.txt"%outdir,"w") as fqout6,\
           open("%s/otu_table_L7.txt"%outdir,"w") as fqout7,\
           open("%s/otu_table_L8.txt"%outdir,"w") as fqout8:
        head=fq.next()
        fqout1.write(head)
        fqout2.write(head)
        fqout3.write(head)
        fqout4.write(head)
        fqout5.write(head)
        fqout6.write(head)
        fqout7.write(head)
        fqout8.write(head)




        for line in fq:
            tabs = line.strip().split("\t")[0].split("|")
            if len(tabs)==1:
                fqout1.write(line)
            if len(tabs)==2:
                fqout2.write(line)
            if len(tabs)==3:
                fqout3.write(line)
            if len(tabs)==4:
                fqout4.write(line)
            if len(tabs)==5:
                fqout5.write(line)
            if len(tabs)==6:
                fqout6.write(line)
            if len(tabs)==7:
                fqout7.write(line)
            if len(tabs)==8:
                fqout8.write(line)
