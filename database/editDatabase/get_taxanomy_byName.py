import csv
from ete3 import NCBITaxa

ncbi = NCBITaxa()

def get_desired_ranks(taxname, desired_ranks):
    taxid = ncbi.get_descendant_taxa(taxname)
    print "%s  id is : %s" %(taxname,taxid)
    lineage = ncbi.get_lineage(taxid[0])
    lineage2ranks = ncbi.get_rank(lineage)
    ranks2lineage = dict((rank, taxid) for (taxid, rank) in lineage2ranks.items())
    tmp = {}
    name_def="viral"
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
def main(taxnames, desired_ranks, path):
    with open(path, 'w') as csvfile:
        fieldnames = ['{}_name'.format(rank) for rank in header]
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for taxname in taxnames:
            writer.writerow(get_desired_ranks(taxname, desired_ranks))

if __name__ == '__main__':
    taxnames = []
    with open("tax_info/tax_species_name.sort.list","r") as fq:
        for line in fq:
            taxnames.append(line.strip())
    #taxids = [1204725, 2162,  1300163, 420247]
    header = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species','speciesTaxId']
    desired_ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    path = 'tax_info/taxids.csv'
    main(taxnames, desired_ranks, path)
