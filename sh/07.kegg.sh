#cp /data_center_01/home/NEOLINE/zwd/project/LiuLin-ascites-stool/07.kegg/db.list ./
#blatprot db.list sq.list
#nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=5G --maxjob 10 --jobprefix KE --lines 1 --getmem shell_blat/blat.sh & 

cat blat/* > blat/all.m8
pick_blast_m8 blat/all.m8 > kegg.m8
perl /data_center_02/Database/KEGG/bin/05_blast2ko.pl -blastout kegg.m8 -output geneset.ko
perl /data_center_02/Database/KEGG/bin/06_pathfind.pl -fg geneset.ko -output geneset.path
perl /data_center_02/Database/KEGG/bin/07_keggMap_nodiff.pl -ko geneset.ko -outdir geneset.map
perl /data_center_02/Database/KEGG/bin/10_KEGG_class.pl geneset.path geneset.path

perl /data_center_01/Projects/Chongcao/metagenomics/09_KEGG/04_get_profiling_ko.pl geneset.ko ../06.gene_profile/gene.profile ko.profile
head -4 ko.profile > example.ko.profile.tsv

perl /data_center_07/Project/RY2015K16A01-1/07.kegg/bin/prokaryote.annotation.pl < kegg.m8 > kegg.anno.tsv
head -4 kegg.anno.tsv > example.kegg.anno.tsv
