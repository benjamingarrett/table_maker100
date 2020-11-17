# Argument: <parent_folder>
# Description: Given a folder containing folders, each of which contains csv files having
# one row, create a single csv file for each folder by taking the first result from each
# csv file in the given folder. The csv files have the form
# COMMENT,<some info>
# SORT BY,<problem size>
# <cache size>,<cache misses>
# <possibly other rows, that get ignored>
#
# This script assumes:
# 1) in each result only the first row matters


import os, sys
import merge_on_sort_by_field


folders = os.listdir(sys.argv[1])
for f in folders:
  if os.path.isdir(f):
    merge_on_sort_by_field.do_merge(f, 'results_'+f)
