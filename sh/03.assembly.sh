perl /data_center_03/USER/zhongwd/rd/12_soap_denovo/soapdenovo_shell_maker.pl -l clean_reads_list -i ../ins.list -minkmer 51 -maxkmer 63 -b 4
nohup /data_center_03/USER/zhongwd/bin/qsge --queue big.q,all.q,neo.q --resource vf=60G:5G:20G:3G --maxjob 4 --lines 4 --jobprefix AS -getmem shell/assembly.sh &
#cp /data_center_01/pipeline/huangy/metagenome/sh/check.sh ./

## best contigs
#mkdir ../04.gene_predict
ls assembly/*/*/*scafSeq |while read a ; do  perl /data_center_06/Project/LiuLin-ascites-stool/03.assembly/bin/N_spliter.pl $a $a.cut 500; done
ls assembly/*/*/*scafSeq.cut | while read a ; do perl /data_center_06/Project/LiuLin-ascites-stool/03.assembly/bin/N50_counter.pl < $a > $a.sort 2> $a.stat; done
list assembly/*/* | perl /data_center_06/Project/LiuLin-ascites-stool/03.assembly/bin/best_contig_selecter.pl > ../04.gene_predict/scaftigs.list
list best_scaftigs/*stat | perl /data_center_07/Project/RY2015K16A01-1/03.assembly/bin/stat.pl > scaftigs.best.stat.tsv

ls best_scaftigs/*fna | sed 's/.fna//g' | while read a ; do gzip -c $a.fna > $a.fna.gz; done

mkdir histogram
cut -f 1 clean_reads_list | while read a; do mkdir histogram/$a; lengthfasta best_scaftigs/$a.*.scaftigs.fna > histogram/$a/contig.length; cd histogram/$a; Rscript /data_center_03/USER/zhongwd/temp/0106/length/contig.R; cd - ;done
