cp /data_center_06/Project/pracrice/yehaocheng_20160120/07.kegg/db.list ./
/data_center_01/pipeline/huangy/metagenome/perlscript/07_blatprot db.list sq.list
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=5G --maxjob 10 --jobprefix KE --lines 1 --getmem shell_blat/blat.sh & 

check(){
    num=`ps xf|grep "jobprefix KE" |wc -l`
    if test $num -eq 1; then
        echo "IS NULL"
    else
        echo "IS not NULL,start sleep"
        sleep 5m
        echo "sleep end"
        check
    fi
}
check_sge(){
    num=`qstat -r|grep "KE_" |wc -l`
    if test $num -gt 0;then
        echo "IS not NULL,start sleep"
        sleep 1m
        echo "sleep end"
    fi
}
sleep 2s
check
check_sge




cat blat/* > blat/all.m8
/data_center_01/pipeline/huangy/metagenome/perlscript/07_pick_blast_m8 blat/all.m8 > kegg.m8
perl /data_center_02/Database/KEGG/bin/05_blast2ko.pl -blastout kegg.m8 -output geneset.ko
perl /data_center_02/Database/KEGG/bin/06_pathfind.pl -fg geneset.ko -output geneset.path
perl /data_center_02/Database/KEGG/bin/07_keggMap_nodiff.pl -ko geneset.ko -outdir geneset.map
perl /data_center_02/Database/KEGG/bin/10_KEGG_class.pl geneset.path geneset.path

perl /data_center_01/Projects/Chongcao/metagenomics/09_KEGG/04_get_profiling_ko.pl geneset.ko ../06.gene_profile/gene.profile ko.profile
head -4 ko.profile > example.ko.profile.tsv

perl /data_center_07/Project/RY2015K16A01-1/07.kegg/bin/prokaryote.annotation.pl < kegg.m8 > kegg.anno.tsv
head -4 kegg.anno.tsv > example.kegg.anno.tsv
