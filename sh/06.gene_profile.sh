#cp ../01.clean_reads/clean_reads_list ./
/data_center_01/pipeline/huangy/metagenome/perlscript/06_geneabundance clean_reads_list gene_catalog.list gene_catalog.length
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=10G --maxjob 10 --jobprefix MA --lines 1 --getmem shell_alignment/match.sh &
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=10G --maxjob 10 --jobprefix AB --lines 2 --getmem shell_alignment/abun.sh &
ls alignment/*/*abundance |/data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > gene.profile

/data_center_01/pipeline/huangy/metagenome/perlscript/06_shannon gene.profile gene.alpha.div.tsv

head -4 gene.profile | sed '1s/^/Gene ID/g' > example.gene.profile.tsv

Rscript /data_center_01/pipeline/huangy/metagenome/Rscript/06_geneset.R
