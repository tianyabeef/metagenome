nohup perl /data_center_03/USER/zhongwd/soft/GenePredict/GenePredict.pl -s scaftigs.list -l 100 -d ./ &
path_pwd=`pwd`
check(){
    echo "$path_pwd"
    #process_num=`echo $!`
    #echo "your process is: $!"
    num=`ps xf|grep "$path_pwd" |wc -l`
    if test $num -eq 1; then
        echo "IS NULL"
    else
        echo "IS not NULL,sleep "
        sleep 1m
        echo "sleep end"
        check
    fi
}
sleep 2s
check
echo "start cat gene/*fna run"



#mkdir ../05.gene_catalog
cat gene/*fna > ../05.gene_catalog/redundant.gene_catalog.fna

ls gene/*fna | sed 's/.fna//g' | while read a ; do cds2pep $a.fna $a.faa; gzip -c $a.fna > $a.fna.gz; gzip -c $a.faa > $a.faa.gz; done
ls gene/*fna | perl /data_center_07/Project/RY2015K16A01-1/04.gene_predict/bin/stat.pl > orf.stat.tsv 

mkdir histogram
cut -f 1 scaftigs.list | while read a; do mkdir histogram/$a; lengthfasta gene/$a.gene.fna > histogram/$a/gene.length; cd histogram/$a; Rscript /data_center_03/USER/zhongwd/temp/0106/length/gene.R; cd - ;done
