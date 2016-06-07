import csv
from ete3 import NCBITaxa

ncbi = NCBITaxa()

def get_desired_ranks(taxid, desired_ranks):
    lineage = ncbi.get_lineage(taxid)
    lineage2ranks = ncbi.get_rank(lineage)
    ranks2lineage = dict((rank, taxid) for (taxid, rank) in lineage2ranks.items())
    tmp = {}
    name_def="Bacteria"
    for rank in desired_ranks:
        if ranks2lineage.get(rank, 'notRank')=="notRank":
            tmp["%s_name" % rank] = ("%s--" % name_def)
        else:
            tax_name = ncbi.translate_to_names([ranks2lineage.get(rank, 'notrank')])[0].encode("utf-8")
            tmp["%s_name" % rank] = tax_name
            name_def = tax_name
    tmp["speciesTaxId_name"]=taxid
    return tmp
#    return {'{}_name'.format(rank): ncbi.translate_to_names([ranks2lineage.get(rank, 'notrank')])[0].encode("utf-8") for rank in desired_ranks}
#    return {'{}_name'.format(rank): ncbi.translate_to_names([ranks2lineage.get(rank, '<not present>')]) for rank in desired_ranks}
def main(taxids, desired_ranks, path):
    with open(path, 'w') as csvfile:
        fieldnames = ['{}_name'.format(rank) for rank in header]
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for taxid in taxids:
            writer.writerow(get_desired_ranks(taxid, desired_ranks))

if __name__ == '__main__':
    taxids = []
    with open("tax_info/tax_species_id.sort.list","r") as fq:
        for line in fq:
            taxids.append(line.strip())
    #taxids = [1204725, 2162,  1300163, 420247]
    header = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species','speciesTaxId']
    desired_ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    path = 'tax_info/taxids.csv'
    main(taxids, desired_ranks, path)
