#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import sys
from workflow.util import configparserself
from workflow.src.raw_reads import raw_reads
from workflow.src.clean_reads import clean_reads
from workflow.src.taxon import taxon
from workflow.src.assembly import assembly
from workflow.src.gene_predict import gene_predict
from workflow.src.gene_catalog import gene_catalog
from workflow.src.gene_profile import gene_profile
from workflow.src.kegg import kegg
from workflow.src.eggnog import eggnog
from workflow.src.ardb import ardb

def touch_sh_file(config,sh_default_file,outpath,name):
    commands=""
    if name=="00.raw_reads":
        commands = raw_reads(config,sh_default_file,outpath)
    elif name=="01.clean_reads":
        commands = clean_reads(config,sh_default_file,outpath)
    elif name == "02.taxon":
        commands =taxon(config,sh_default_file,outpath)
    elif name == "03.assembly":
        commands = assembly(config,sh_default_file,outpath)
    elif name == "04.gene_predict":
        commands = gene_predict(config,sh_default_file,outpath)
    elif name == "05.gene_catalog":
        commands = gene_catalog(config,sh_default_file,outpath)
    elif name == "06.gene_profile":
        commands = gene_profile(config,sh_default_file,outpath)
    elif name == "07.kegg":
        commands = kegg(config,sh_default_file,outpath)
    elif name == "08.eggnog":
        commands = eggnog(config,sh_default_file,outpath)
    elif name == "09.ardb":
        commands = ardb(config,sh_default_file,outpath)
    else:
        sys.stderr.write("step name is %s not in src" % name)
        return False
    if commands:
        with open(outpath,"w") as fqout:
            for key in commands:
                fqout.write("%s\n" % key)
        return True
    else:
        return False
