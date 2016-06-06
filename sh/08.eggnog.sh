cp /data_center_05/Project/Health_in_ZJTCM/08.eggnog/db.list ./
/data_center_01/pipeline/huangy/metagenome/perlscript/07_blatprot db.list sq.list
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=5G --maxjob 10 --jobprefix EG --lines 1 --getmem shell_blat/blat.sh &

check(){
    num=`ps xf|grep "jobprefix EG" |wc -l`
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
    num=`qstat -r|grep "EG_" |wc -l`
    if test $num -gt 0;then
        echo "IS not NULL,start sleep"
        sleep 1m
        echo "sleep end"
    fi
}
sleep 2s
check
check_sge


cat blat/* > all.m8
/data_center_01/pipeline/huangy/metagenome/perlscript/07_pick_blast_m8 all.m8 > eggnog.m8
perl /data_center_02/Database/eggNOGv4.0/03_get_annot_info.pl eggnog.m8 /data_center_02/Database/eggNOGv4.0/all.members.txt /data_center_02/Database/eggNOGv4.0/all.description.txt /data_center_02/Database/eggNOGv4.0/all.funccat.txt eggnog.m8.tab
perl /data_center_02/Database/eggNOGv4.0/04_get_count.pl eggnog.m8.tab /data_center_02/Database/eggNOGv4.0/eggnogv4.funccats.txt eggnog.tab
perl /data_center_07/Project/RY2015K16A01-1/08.eggnog/bin/eggnog.annotation.pl < eggnog.m8.tab > eggnog.anno.tsv
egrep "^\s" -v eggnog.anno.tsv | head -4 > example.eggnog.anno.tsv

mkdir samples
cut -f 1 ../01.clean_reads/sample.list | while read a ; do cut -f 1 ../06.gene_profile/alignment/$a/$a.gene.abundance > samples/$a.gene.list; done
ls samples/*gene.list | sed 's/.gene.list//g'|while read a; do perl /data_center_02/Database/eggNOGv4.0/04_get_countlist.pl eggnog.m8.tab /data_center_02/Database/eggNOGv4.0/eggnogv4.funccats.txt $a.gene.list $a.eggnog.tab;done
ls samples/*.eggnog.tab | sed 's/.eggnog.tab//g' | while read a;do cut -f 3,4 $a.eggnog.tab > $a.eggnog.count.tab; done
ls samples/*.eggnog.count.tab | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > eggnog.count.tab
Rscript /data_center_04/Projects/pichongbingdu/pair_reads/05.eggnog/NOG.R eggnog.count.tab
