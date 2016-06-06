## calculate abundance
/data_center_03/USER/zhongwd/bin/speciesabundance clean_reads_list
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=15G --maxjob 10 --jobprefix MA --lines 1 --getmem shell_alignment/match.sh &
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=15G --maxjob 10 --jobprefix AB --lines 2 --getmem shell_alignment/abun.sh &

## form species profile
ls alignment/*/*species.abundance | /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/bin/taxnomy.pl -
mkdir profile
ls alignment/*/*species.abundance | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/species.profile
ls alignment/*/*genus.abundance   | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/genus.profile
ls alignment/*/*class.abundance   | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/class.profile
ls alignment/*/*family.abundance  | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/family.profile
ls alignment/*/*order.abundance   | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/order.profile
ls alignment/*/*phylum.abundance  | /data_center_01/pipeline/huangy/metagenome/perlscript/02_profile - > profile/phylum.profile

## use rate
mkdir use_rate
ls alignment/*/*MATCH |while read a; do echo "perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/bin/stat.pl < $a > $a.stat" ;done > use_rate/stat.sh
nohup /data_center_03/USER/zhongwd/bin/qsge --queue all.q --resource vf=1G --maxjob 10 --jobprefix ST --lines 1 --getmem use_rate/stat.sh &
ls alignment/*/*MATCH.stat | perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/bin/stat_tab.pl - ../00.raw_reads/qc_final.stat.tsv > use_rate/stat.tsv

## profile example
#rm -f profile/example.profile.tsv
head -4 profile/phylum.profile  >> profile/example.profile.tsv
head -4 profile/class.profile   >> profile/example.profile.tsv
head -4 profile/order.profile   >> profile/example.profile.tsv
head -4 profile/family.profile  >> profile/example.profile.tsv
head -4 profile/genus.profile   >> profile/example.profile.tsv
head -4 profile/species.profile >> profile/example.profile.tsv
#sed '/^\t/s/^/Taxon name/g' -i profile/example.profile.tsv

## 00.piechart     need finish
mkdir 00.piechart
ls alignment/*/*species.abundance | sed 's/alignment\/\(.*\)\/.*species.abundance/\1/g' | while read a ; do perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/test/pieplot/pie.pl < alignment/$a/$a.species.abundance > 00.piechart/$a.species.pie.svg;done
ls alignment/*/*genus.abundance   | sed 's/alignment\/\(.*\)\/.*genus.abundance/\1/g'   | while read a ; do perl /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/test/pieplot/pie.pl < alignment/$a/$a.genus.abundance   > 00.piechart/$a.genus.pie.svg;done

## 01.barplot      need finish
mkdir 01.barplot
cd 01.barplot; Rscript /data_center_03/USER/zhongwd/temp/0106/barplot/species.barplot.r; cd -
cd 01.barplot; Rscript /data_center_03/USER/zhongwd/temp/0106/barplot/genus.barplot.r;   cd -

## 02.core
mkdir 02.core
perl /data_center_06/Project/pracrice/yehaocheng_20160120/02.taxon_group1/bin/core_sum.pl clean_reads_list profile/species.profile > 02.core/core.profile
cd 02.core; Rscript /data_center_04/Projects/pichongbingdu/pair_reads/02.taxon/core/venn.r core.profile ; cd -
perl /data_center_03/USER/zhongwd/rd/06_R2svg/flower/flower.pl profile/species.profile > 02.core/species.flower.svg
cd 02.core; Rscript /data_center_04/Projects/pichongbingdu/pair_reads/02.taxon/core/venn.r ../profile/species.profile; cd -

## 03.accum
mkdir 03.accum_share
ln -s ../profile/genus.profile 03.accum_share
ln -s ../profile/species.profile 03.accum_share
perl /data_center_03/USER/zhongwd/rd/Finish/07_acumm_share_curve/Accumulated_Shared_Curve.pl -p 03.accum_share/genus.profile -c genus -t 100
perl /data_center_03/USER/zhongwd/rd/Finish/07_acumm_share_curve/Accumulated_Shared_Curve.pl -p 03.accum_share/species.profile -c species -t 100

## 04.rarecurve
mkdir 04.rarecurve
list alignment/*/*MATCH > 04.rarecurve/match.list; sed 's/.*alignment\/\(.*\)\/.*MATCH/\1/g' 04.rarecurve/match.list | paste - 04.rarecurve/match.list > 04.rarecurve/match.list.tmp; mv -f 04.rarecurve/match.list.tmp 04.rarecurve/match.list
nohup perl /data_center_03/USER/zhongwd/rd/05_rarecurve/RareCurve/RareCurve.pl -s clean_reads_list -m 04.rarecurve/match.list -d 04.rarecurve &

## 06.ternaryplot
#mkdir 06.ternaryplot
#Rscript /data_center_04/Projects/pichongbingdu/pair_reads/02.taxon/ternary/ternary.r profile/species.profile sample.list 06.ternaryplot/species.ternary.pdf species
#Rscript /data_center_04/Projects/pichongbingdu/pair_reads/02.taxon/ternary/ternary.r profile/genus.profile   sample.list 06.ternaryplot/genus.ternary.pdf   genus

## 07.treeplot
#mkdir 07.treeplot
#cut -f 1 clean_reads_list | while read a; do mkdir 07.treeplot/$a; perl /data_center_03/USER/zhongwd/temp/0106/tree/a.pl < alignment/$a/$a.species.abundance > 07.treeplot/$a/test.info 2> 07.treeplot/$a/test.tax; done
#cut -f 1 clean_reads_list | while read a; do cd 07.treeplot/$a; perl /data_center_03/USER/zhongwd/temp/0106/tree/zwd_newwick.pl < test.tax > test.tre; ~/anaconda_ete/bin/python /data_center_03/USER/zhongwd/temp/0106/tree/plottre.py; cd -; done

## 08.cluster
#mkdir 08.cluster;
#Rscript /data_center_03/USER/zhongwd/rd/11_taxonomy_V2.0/test/barplot/bartreeplot.r profile/species.profile sample.list 08.cluster/species.clust.pdf

## 09.pca
#mkdir 09.pca
#Rscript /data_center_03/USER/zhongwd/temp/0106/PCA/pca.R profile/species.profile sample.list 09.pca/species.pca.pdf
#Rscript /data_center_03/USER/zhongwd/temp/0106/PCA/pca.R profile/genus.profile   sample.list 09.pca/genus.pca.pdf

## 11.anosim; 13.pcoa; 14.nmds
mkdir 11-14.beta_div; mkdir 11-14.beta_div/species; mkdir 11-14.beta_div/genus
cd 11-14.beta_div/species; perl /data_center_03/USER/zhongwd/bin/Beta_diversity.pl -p ../../profile/species.profile -g ../../sample.list -m bray -r; cd -
cd 11-14.beta_div/genus;   perl /data_center_03/USER/zhongwd/bin/Beta_diversity.pl -p ../../profile/genus.profile   -g ../../sample.list -m bray -r; cd -

