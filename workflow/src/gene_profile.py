#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

import os
import re
from  ConfigParser import ConfigParser
from workflow.util.useful import mkdir
def gene_profile(config,sh_default_file,outpath,name):
    commands = []
    work_dir = os.path.dirname(config)
    commands.append("/data_center_01/pipeline/huangy/metagenome/perlscript/06_geneabundance clean_reads_list gene_catalog.list gene_catalog.length")
    commands.append("nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=10G --maxjob 10 --jobprefix MA --lines 1 --getmem shell_alignment/match.sh &")
    commands.append("nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=10G --maxjob 10 --jobprefix AB --lines 2 --getmem shell_alignment/abun.sh &")
    commands.append("ls alignment/*/*abundance |/data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > gene.profile")
    commands.append("/data_center_01/pipeline/huangy/metagenome/perlscript/06_shannon gene.profile gene.alpha.div.tsv")
    commands.append("head -4 gene.profile | sed '1s/^/Gene ID/g' > example.gene.profile.tsv")
    commands.append("Rscript /data_center_01/pipeline/huangy/metagenome/Rscript/06_geneset.R")
    commands.append("#差异分析")
    config_gene = ConfigParser()
    config_gene.read(config)
    group = re.split("\s+|\t",config_gene.get("param","group"))
    mkdir("%s/group/" % work_dir)
    for subgroup in group:
        subgroup = os.path.basename(subgroup)
        subgroup_split =os.path.splitext(subgroup)[0]
        mkdir("%s/group/%s/"%(work_dir,subgroup_split))
        commands.append("python /data_center_01/pipeline/huangy/metagenome/pyscript/convert_abundance_group.py gene.profile ../group/%s group/%s/gene.profile genus" % (subgroup,subgroup_split))
        commands.append("/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/03_otu_pca.py -i group/%s/gene.profile -g ../group/%s -o group/%s/09.pca --with_boxplot" % (subgroup_split,subgroup,subgroup_split))
        mkdir("%s/group/%s/11-14.beta_div/"%(work_dir,subgroup_split))
        mkdir("%s/group/%s/11-14.beta_div/gene/"%(work_dir,subgroup_split))
        commands.append("cd group/%s/11-14.beta_div/gene; perl /data_center_01/pipeline/huangy/metagenome/perlscript/02_Beta_diversity.pl -p ../../../../group/%s/gene.profile -g ../../../../../group/%s -m bray -r; cd -" %(subgroup_split,subgroup_split,subgroup))
        mkdir("%s/group/%s/15.LEfSe/" % (work_dir,subgroup_split))
        commands.append("/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/05_tax_diff.py -i group/%s/gene.profile -o group/%s/gene_diff/ -g ../group/%s -c 0.05"%(subgroup_split,subgroup_split,subgroup))
        commands.append("/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/05_diff_pca.py -i group/%s/gene_diff/profile.for_plot.txt -o group/%s/gene_diff/pca -g ../group/%s" %(subgroup_split,subgroup_split,subgroup))
        commands.append("/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/03_tax_heatmap.py -f group/%s/gene_diff/profile.for_plot.txt -o group/%s/gene_diff/heatmap -g ../group/%s -t 30" % (subgroup_split,subgroup_split,subgroup))
        commands.append(" /data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/05_diff_boxplot.py -i group/%s/gene_diff/profile.for_plot.txt -o group/%s/gene_diff/boxplot -g ../group/%s -t 20"%(subgroup_split,subgroup_split,subgroup))
        #commands.append("/data_center_01/pipeline/16S_ITS_pipeline_v3.0/script/05_LEfSe.py -i group/%s/gene.profile -l /data_center_03/USER/huangy/soft/LEfSe_lzb -g ../group/%s -o group/%s/15.LEfSe/ --LDA 2" %(subgroup_split,subgroup,subgroup_split))
    return commands
