#cp ../01.clean_reads/sample.list ./
#geneabundance sample.list gene_catalog.list gene_catalog.length
#nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=10G --maxjob 10 --jobprefix MA --lines 1 --getmem shell_alignment/match.sh &
#nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=10G --maxjob 10 --jobprefix AB --lines 2 --getmem shell_alignment/abun.sh &
ls alignment/*/*abundance |profile - > gene.profile

shannon gene.profile gene.alpha.div.tsv

head -4 gene.profile | sed '1s/^/Gene ID/g' > example.gene.profile.tsv

Rscript /data_center_03/USER/zhongwd/temp/0106/length/geneset.R
