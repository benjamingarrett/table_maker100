# Usage: python flatten_folder.py <folder> <output_file>
# Description: assume one row of data and a SORT_BY field in each csv in the folder

import csv, itertools, os, sys


def write_csv(rows, field_list, output_fname):
  with open(output_fname, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_list)
    writer.writeheader()
    for row_dict in rows:
      writer.writerow(row_dict)


#for fn in os.listdir(sys.argv[1]):
#  if 'csv' in fn:
#    print(fn)
#    lst = []
#    cnt = 0
#    for ln in open(sys.argv[1]+'/'+fn):
#      cnt += 1
#      if cnt > 4:
#        break
#      lst.append(ln.rstrip('\n').split(','))
#    print(lst)
#exit(1)


lists=[[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn]
rows = []
warn = 0
for k in lists:
  # find the characteristic cache size for this instance, assuming possibly several trials have to be searched
  print('k->{}<-'.format(k))
  j = 2 # this is the first trial
  s = int(k[j][0])
  m = int(k[j][1])
  while j < len(k):
    if int(k[j][1]) == m:
      s = int(k[j][0])
    else:
      break
    j += 1
  rows.append({'n': int(k[1][1]), 'size': s, 'misses': m})
print('warnings: {}'.format(warn))
write_csv(sorted(rows,key=lambda k: k['n']), ['n', 'size', 'misses'], sys.argv[2])
