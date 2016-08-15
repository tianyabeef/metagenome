#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import  os
import re
from  ConfigParser import ConfigParser
from workflow.util.useful import mkdir,parse_group,get_name
from workflow.util.globals import const

def taxon(config,sh_default_file,outpath,name):
    commands = []
    work_dir = os.path.dirname(config)
    pyscript_dir = const.PYscript
    commands.append("## calculate abundance")
    commands.append("/data_center_01/pipeline/huangy/metagenome/perlscript/02_speciesabundance clean_reads_list bacteria,fungi,archaea,virus")
    commands.append("nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=15G --maxjob 10 --jobprefix MA --lines 1 --getmem shell_alignment/match.sh &")
    commands.append("nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=15G --maxjob 10 --jobprefix AB --lines 2 --getmem shell_alignment/abun.sh &")
    commands.append("## form species profile")
    commands.append("ls alignment/*/*species.abundance >list")
    commands.append("python /data_center_01/pipeline/huangy/metagenome/pyscript/02_taxnomy.py -i list")
    commands.append("rm list")
    mkdir("%s/profile/" % work_dir)
    commands.append("ls alignment/*/*species.abundance | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/species.profile")
    commands.append("ls alignment/*/*genus.abundance   | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/genus.profile")
    commands.append("ls alignment/*/*class.abundance   | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/class.profile")
    commands.append("ls alignment/*/*family.abundance  | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/family.profile")
    commands.append("ls alignment/*/*order.abundance   | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/order.profile")
    commands.append("ls alignment/*/*phylum.abundance  | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/phylum.profile")
    commands.append("## use rate")
    commands.append("#mkdir use_rate")
    commands.append("#ls alignment/*/*MATCH |while read a; do echo \"perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/bin/stat.pl < $a > $a.stat\" ;done > use_rate/stat.sh")
    commands.append("#nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=1G --maxjob 10 --jobprefix ST --lines 1 --getmem use_rate/stat.sh &")
    commands.append("#ls alignment/*/*MATCH.stat | perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/bin/stat_tab.pl - ../00.raw_reads/qc_final.stat.tsv > use_rate/stat.tsv")
    config_gene = ConfigParser()
    config_gene.read(config)
    group = re.split("\s+|\t",config_gene.get("param","group"))
    mkdir("%s/group/" % work_dir)
    commands.append("## 00.piechart     need finish")
    mkdir("%s/group/00.piechart"%(work_dir))
    commands.append("ls alignment/*/*species.abundance | sed 's/alignment\/\(.*\)\/.*species.abundance/\\1/g' | while read a ; do perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/test/pieplot/pie.pl < alignment/$a/$a.species.abundance > 00.piechart/$a.species.pie.svg;done")
    commands.append("ls alignment/*/*genus.abundance   | sed 's/alignment\/\(.*\)\/.*genus.abundance/\\1/g'   | while read a ; do perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/test/pieplot/pie.pl < alignment/$a/$a.genus.abundance   > 00.piechart/$a.genus.pie.svg;done")

    commands.append("## 03.accum")
    mkdir("%s/group/%s/03.accum_share"%(work_dir))
    commands.append("ln -s ../profile/genus.profile 03.accum_share")
    commands.append("ln -s ../profile/species.profile 03.accum_share")
    commands.append("perl /data_center_03/USER/zhongwd/rd/Finish/07_acumm_share_curve/Accumulated_Shared_Curve.pl -p 03.accum_share/genus.profile -c genus -t 100")
    commands.append("perl /data_center_03/USER/zhongwd/rd/Finish/07_acumm_share_curve/Accumulated_Shared_Curve.pl -p 03.accum_share/species.profile -c species -t 100")
    commands.append("## 04.rarecurve")
    mkdir("%s/04.rarecurve"%(work_dir))
    commands.append("list alignment/*/*MATCH > 04.rarecurve/match.list; sed 's/.*alignment\/\(.*\)\/.*MATCH/\\1/g' 04.rarecurve/match.list | paste - 04.rarecurve/match.list > 04.rarecurve/match.list.tmp; mv -f 04.rarecurve/match.list.tmp 04.rarecurve/match.list")
    commands.append("nohup perl /data_center_03/USER/zhongwd/rd/05_rarecurve/RareCurve/RareCurve.pl -s clean_reads_list -m 04.rarecurve/match.list -d 04.rarecurve &")

    commands.append("## 06.ternaryplot")
    mkdir("%s/06.ternaryplot"%(work_dir))
    commands.append("#Rscript /data_center_04/Projects/pichongbingdu/pair_reads/02.taxon/ternary/ternary.r profile/species.profile sample.list 06.ternaryplot/species.ternary.pdf species")
    commands.append("#Rscript /data_center_04/Projects/pichongbingdu/pair_reads/02.taxon/ternary/ternary.r profile/genus.profile   sample.list 06.ternaryplot/genus.ternary.pdf   genus")
    commands.append("## 07.treeplot")
    mkdir("%s/07.treeplot"%(work_dir))
    commands.append("#cut -f 1 clean_reads_list | while read a; do mkdir 07.treeplot/$a; perl /data_center_03/USER/zhongwd/temp/0106/tree/a.pl < alignment/$a/$a.species.abundance > 07.treeplot/$a/test.info 2> 07.treeplot/$a/test.tax; done")
    commands.append("#cut -f 1 clean_reads_list | while read a; do cd 07.treeplot/$a; perl /data_center_03/USER/zhongwd/temp/0106/tree/zwd_newwick.pl < test.tax > test.tre; ~/anaconda_ete/bin/python /data_center_03/USER/zhongwd/temp/0106/tree/plottre.py; cd -; done")

    commands.append("## 08.cluster")
    mkdir("%s/08.cluster"%(work_dir))
    commands.append("#Rscript /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/test/barplot/bartreeplot.r profile/species.profile sample.list 08.cluster/species.clust.pdf")

    for subgroup in group:
        dirname,subgroup_name,_ = get_name(subgroup)
        _,min_sample_num_in_groups,sample_num_total,group_num=parse_group(subgroup)
        mkdir("%s/group/%s"%(work_dir,subgroup_name))
        commands.append("## 01.barplot      need finish")
        mkdir("%s/group/%s/01.barplot"%(work_dir,subgroup_name))
        commands.append("%s/02_bar_plot.py -i %s/profile/species.profile -o %s/%s/01.barplot/species.pdf \
        -g %s -t %s"%(pyscript_dir,work_dir,work_dir,subgroup_name,subgroup,"species"))
        commands.append("%s/02_bar_plot.py -i %s/profile/genus.profile -o %s/%s/01.barplot/genus.pdf \
        -g %s -t %s"%(pyscript_dir,work_dir,work_dir,subgroup_name,subgroup,"genus"))
        commands.append("## 02.core")
        mkdir("%s/group/%s/02.core"%(work_dir,subgroup_name))
        commands.append("%s"%(pyscript_dir))
        commands.append("%s/02_venn.py -i %s/profile/species.profile -o %s/group/%s/02.core/%s/ -g %s "%(pyscript_dir,work_dir,work_dir,subgroup,"species"))
        commands.append("%s/02_venn.py -i %s/profile/species.profile -o %s/group/%s/02.core/%s/ -g %s "%(pyscript_dir,work_dir,work_dir,subgroup,"genus"))
        commands.append("## 05.top_boxplot")
        mkdir("%s/group/%s/05.top_boxplot"%(work_dir,subgroup_name))
        commands.append("cut -f 1 profile/genus.profile   | perl /data_center_03/USER/zhongwd/temp/0106/top/a.pl > 05.top_boxplot/genus.phylum")
        commands.append("cut -f 1 profile/species.profile | perl /data_center_03/USER/zhongwd/temp/0106/top/a.pl > 05.top_boxplot/species.phylum")
        commands.append("%s/02_top.py -i test -g %s -o %s/group/%s/05.top_boxplot/"%(pyscript_dir,subgroup,work_dir,subgroup_name))
        commands.append("## 09.pca")
        mkdir("%s/group/%s/09.pca"%(work_dir,subgroup_name))
        commands.append("%s/02_otu_pca.py -i %s/profile/species.profile -g %s -o %s/group/%s/09.pca --with_boxplot"%\
                        (pyscript_dir,work_dir,subgroup,work_dir,subgroup_name))
        commands.append("%s/02_otu_pca.py -i %s/profile/genus.profile -g %s -o %s/group/%s/09.pca --with_boxplot"%\
                        (pyscript_dir,work_dir,subgroup,work_dir,subgroup_name))
        commands.append("## 11.anosim; 13.pcoa; 14.nmds")
        mkdir("%s/group/%s/11-14.beta_div"%(work_dir,subgroup_name))
        mkdir("%s/group/%s/11-14.beta_div/species"%(work_dir,subgroup_name))
        mkdir("%s/group/%s/11-14.beta_div/genus"%(work_dir,subgroup_name))
        commands.append("cd group/%s/11-14.beta_div/species; perl /data_center_01/pipeline/huangy/metagenome/perlscript/02_Beta_diversity.pl -p ../../../../profile/species.profile -g %s -m bray -r; cd -"%(subgroup_name,subgroup))
        commands.append("cd group/%s/11-14.beta_div/genus; perl /data_center_01/pipeline/huangy/metagenome/perlscript/02_Beta_diversity.pl -p ../../../../profile/genus.profile -g %s -m bray -r; cd -"%(subgroup_name,subgroup))
        mkdir("%s/group/%s/15.LEfSe"%(work_dir,subgroup_name))
        commands.append("/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/05_LEfSe.py -i profile/species.profile -l /data_center_03/USER/huangy/soft/LEfSe_lzb -g %s -o group/%s/15.LEfSe/ --LDA 2"%(subgroup,subgroup_name))
    return commands
