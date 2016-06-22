#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

from . import const
const.pipeline_dir = "/data_center_01/pipeline/huangy/metagenome/"
const.config_default_dir = "%s/config/" % const.pipeline_dir
const.sh_default_dir = "%s/sh/" % const.pipeline_dir
const.config_file_suffix = "config"
const.shell_file_suffix = "sh"
const.step_names_order = "00.raw_reads,01.clean_reads,02.taxon,03.assembly,04.gene_predict,05.gene_catalog,06.gene_profile,07.kegg,08.eggnog,09.ardb"