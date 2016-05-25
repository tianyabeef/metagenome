#nohup cdhit redundant.gene_catalog.fna gene_catalog.fna 8 &

#mkdir ../06.gene_profile
#lengthfasta gene_catalog.fna > ../06.gene_profile/gene_catalog.length
#(echo -e "gene_catalog\t\c"; list gene_catalog.fna) > ../06.gene_profile/gene_catalog.list
2bwt-builder gene_catalog.fna

#cds2pep gene_catalog.fna gene_catalog.faa
#cutfasta gene_catalog.faa 10 > gene_catalog.list
#mkdir ../07.kegg
#cut -f 2 gene_catalog.list > ../07.kegg/sq.list
#mkdir ../08.eggnog
#cut -f 2 gene_catalog.list > ../08.eggnog/sq.list
#mkdir ../09.ardb
#cut -f 2 gene_catalog.list > ../09.ardb/sq.list

#gzip -c redundant.gene_catalog.fna > redundant.gene_catalog.fna.gz
#gzip -c gene_catalog.fna > gene_catalog.fna.gz
#gzip -c gene_catalog.faa > gene_catalog.faa.gz

#perl /data_center_06/Project/LiuLin-ascites-stool/03.assembly/bin/stat.pl < gene_catalog.fna > gene_catalog.stat.tsv

