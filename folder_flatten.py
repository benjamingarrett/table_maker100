# Usage: python flatten_folder.py <folder> <output_file>
# Description: assume one row of data and a SORT_BY field in each csv in the folder


import csv, itertools, os, sys


def write_csv(rows, field_list, output_fname):
  with open(output_fname, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_list)
    writer.writeheader()
    for row_dict in rows:
      writer.writerow(row_dict)


def transpose_results(r):
  print(r)
  transposed = []
  for m in r:
    s = []
    for i in range(len(m))


if __name__ == '__main__':
  lists=[[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn]
  transpose_results(lists)
  exit(0)
  rows = []
  warn = 0
  for k in lists:
    print('k->{}<-'.format(k))
    if len(k) < 3:
      warn += 1
      print('no empirical data found')
      exit(1)
    else:
      rows.append({'n': int(k[1][1]), 'size': int(k[2][0]), 'misses': int(k[2][1])})
  d = {k['n']: k['misses'] for k in rows}
  print(d)
  exit(0)
  print('warnings: {}'.format(warn))
  write_csv(sorted(rows,key=lambda k: k['n']), ['n', 'size', 'misses'], sys.argv[2])
