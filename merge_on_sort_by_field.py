# Arguments: <folder_with_csv_files> <output_filename>
# Description: Given a folder with csv files having the form
# COMMENT,<some info>
# SORT_BY,<problem size>
# <cache size>,<cache misses>
# <possibly other rows>
#
# This script assumes:
# 1) only the first row matters
# 2) The cache size is constant
#
# problem_size,cache_misses
# <problem size>,<cache misses>
#
# Warnings are given if not all data files indicate the same cache size on the first row
# All other rows after the first row of data are ignored

import csv, itertools, os, sys


def write_csv(rows, field_list, output_fname):
  with open(output_fname, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_list)
    #writer.writeheader()  taking this out for the compatibility with plot scripts
    for row_dict in rows:
      writer.writerow(row_dict)


def do_merge(folder, out_fname, comment, sort_by):
  print('do_merge {}, {}'.format(folder, out_fname))
  lists = sorted([[ln.rstrip('\n').split(',') for ln in open(folder+'/'+fn)] for fn in os.listdir(folder) if 'csv' in fn], key=lambda k: (int(k[1][1]), k[0][1]))
  if len(lists) == 0:
    print('No data found in folder {}'.format(folder))
    exit(1)
  rows, fields = [], ['column_1', 'column_2']
  for lst in lists:
    print('do_merge, processing list {}'.format(lst))
    if len([k[1] for k in lst if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0]]) > 0:
      prob_size = int([k[1] for k in lst if k[0]=='SORT_BY'][0])
      misses = int([k[1] for k in lst if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0]][0])
      rows.append({'column_1': prob_size, 'column_2': misses})
  rows = sorted(rows, key=lambda k: k['column_1'])
  rows.insert(0, {'column_1': 'SORT_BY', 'column_2': sort_by})
  rows.insert(0, {'column_1': 'COMMENT', 'column_2': comment}) 
  write_csv(rows, fields, out_fname)


if __name__ == "__main__":
  print('beginning sort_on_merge_by_field')
  do_merge(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
