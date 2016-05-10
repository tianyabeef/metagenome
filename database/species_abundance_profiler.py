#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import argparse
import sys

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

    super_tmp = {}
    #tax = {}
    species = {}
    species_len = {}
    species_average_length = {}
    with open("/data_center_06/Database/NCBI_Bacteria/20160422/accession/GENOME.TAX","r") as fq:
        for line in fq:
            tabs = line.strip().split("\t")
            #tax[tabs[0]] = tabs[-2] #登入号对应种
            species[tabs[0]] = tabs[-1] #登入号对应菌株
            super_tmp[tabs[0]] = tabs[1] #登入号对应界
    with open("/data_center_06/Database/NCBI_Bacteria/20160422/accession/GENOME.SIZE","r") as fq:
       for line in fq:
           tabs = line.strip().split("\t")
           species_len[tabs[0]] = tabs[2] #菌株的长度
    species_name = {} #物种的名称
    species_value_unique = {}
    species_value_multiple = {}
    reads_unique_num = 0
    reads_multip_unispecies_num = 0
    reads_multip_mulspecies_num = 0
    reads_belong_multiple_species = {}
    with open(match_file,"r") as infq:
        for line in infq:
            if line.startswith(">"):
                tabs = line.strip().split(",")
                query = tabs.pop(0)
                if query:
                    species_tem = {}
                    strains_tem = {}
                    reads_gi = {}
                    for key in tabs:
                        chot = key.strip().strip("\"").split("\t")
                        if ( ( (chot[1] == "P") and (chot[3] == "a") ) or (chot[1] == "S")):
                            pass
                        else:
                            species_tem = species[chot[0]]
                            #strains_tem = strains[chot[0]]
                            if not species_tem.has_key(chot[0]):
                                continue
                            species_tem[species_tem] = 1
                            #strains_tem[strains_tem] = 1
                            reads_gi["G"] = "%s%s\t" % (reads_gi["G"],chot[0])
                            species_name[species_tem] = 1
                    if len(species_tem.keys()) == 1:
                        if len(strains_tem.keys()) ==1:
                            reads_unique_num +=1
                        else:
                            reads_multip_unispecies_num += 1
                        gi_pool = reads_gi["G"].split("\t")
                        le = 0
                        total_length = 0
                        for gi in gi_pool:
                            ss = tax[gi]
                            le = 3.5e6
                            if strains_len.has_key(gi):
                                le = strains_len[gi]
                                total_length += le
                                if len(strains_tem.keys())==1:
                                    if len(strains_tem.keys())>1:
                                        uv = total_length/len(strains_tem.keys())
                                        strains_average_length[ss] = uv
                                        species_value_unique[ss] +=1/uv
                    elif len(species_tem.keys())>1:
                        reads_multip_mulspecies_num += 1
                        pool = species_tem.keys()
                        reads_belong_multiple_species[query] = "\t".join(pool)

    with open(logout,"w") as log:
        log.write("%s\t%s\t%s\n" % (reads_unique_num,reads_multip_unispecies_num,reads_multip_mulspecies_num))
        for key in reads_belong_multiple_species:
            species = reads_belong_multiple_species[key].split("\t")
            sum = 0
            for ss in species:
                if species_value_unique.has_key(ss):
        sum += species_value_unique{ss}
        if sum > 0:
            for q in species:
                coefficient = 0
        if species_value_unique.has_key(q):
            coefficient = species_value_unique[q]
            if coefficient>0:
                multiple_value = coefficient / sum / strains_average_length[q]
            if coefficient > 0:
                species_value_multiple[q] += multiple_value
        for s_name in species_name.keys():
            unique_value = 0
            multiple_value = 0
        if species_value_unique.has_key(s_name):
            unique_value = species_value_unique[s_name]
        if species_value_multiple.has_key(s_name):
            multiple_value = species_value_multiple[s_name]
    ssum[s_name] = unique_value + multiple_value
    sum += ssum[s_name]
    with open(species_abundance,"w") as out:
        for s_name in species_name.keys():
            ssum[s_name]=ssum[s_name]/sum
            if ssum[s_name]>0:
            out.write("%s\t%s\n") % (s_name,ssum[s_name])















foreach my $q (keys %READS_belong_Multiple_Species){

my @SPECIES = split /\t/,$READS_belong_Multiple_Species{$q};
my $sum = 0;
    foreach my $SS (@SPECIES){
    $sum += $Species_value_Unique{$SS} if exists $Species_value_Unique{$SS};
    }

    if ($sum > 0){
        foreach my $Q (@SPECIES){
        my $coefficient = 0;
           $coefficient = $Species_value_Unique{$Q} if (exists $Species_value_Unique{$Q});
        my $multiple_value = $coefficient / $sum / $av_LENGTH{$Q} if ($coefficient > 0);
           $Species_value_Multiple{$Q} += $multiple_value if ($coefficient > 0);
        }
    }
}
my %SSUM;
my $sum;
foreach my $S_name (keys %species_name){
    my $Unique_value = 0;
    my $Multiple_value = 0;
       $Unique_value = $Species_value_Unique{$S_name} if exists $Species_value_Unique{$S_name};
       $Multiple_value = $Species_value_Multiple{$S_name} if exists $Species_value_Multiple{$S_name};
    $SSUM{$S_name} = $Unique_value + $Multiple_value;
    $sum += $SSUM{$S_name};
}
foreach my $S_name (keys %species_name){
    $SSUM{$S_name} /= $sum;
    print OT "$S_name\t$SSUM{$S_name}\n" if $SSUM{$S_name} > 0;
}

