#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

from . import const
const.pipeline_dir = "/data_center_01/pipeline/huangy/metagenome/"
const.config_default_dir = "%s/config/" % const.pipeline_dir
const.config_file_suffix = "config"
shell_file_suffix = "sh"
const.step_names_order = "00_row_data,01_GeneSet,02_GeneAbundance,03_SpeciesAbundance,04_AlphaRare,05_KEGGAnnotation,06_eggNog"
