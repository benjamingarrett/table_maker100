# Usage: python merge_tables.py <folder with csv files> <output filename>
# Description: Given a collection of N 2-column csv files, this script merges them all into one (N+1)-column table, with the firstmost column being the left column
#   from all input tables, adding empty rows if necessary in order for data to be given as continuous rows. The COMMENT field explains what the given column means.
#   The SORT_BY field is used to order the columns from left to right.

import csv,itertools,os,sys

def write_csv(rows,field_list,output_fname):
  with open(output_fname, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_list)
    writer.writeheader()
    for row_dict in rows:
      writer.writerow(row_dict)


def init(first_column,first_field):
  return ([{first_field:x} for x in first_column],[first_field])


def merge(rows,field_list,first_field,new_column,new_field):
  field_list.append(new_field)
  while len(new_column)>0:
    row=new_column.pop(0)
    if 'COMMENT' not in row[0] and 'SORT_BY' not in row[0]:
      for current in rows:
        if current[first_field]==int(row[0]):
          current.update({new_field:row[1]})
  return (rows,field_list)


lists=sorted([[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn],key=lambda k:(int(k[1][1]),k[0][1]))
max_row_key=max(list(itertools.chain(*[[int(x[0]) for x in y if 'COMMENT' not in x[0] and 'SORT_BY' not in x[0]] for y in lists])))
min_row_key=min(list(itertools.chain(*[[int(x[0]) for x in y if 'COMMENT' not in x[0] and 'SORT_BY' not in x[0]] for y in lists])))
a=list(range(min_row_key,max_row_key+1))
a.reverse()
(rows,field_list)=init(a,'cache size')
for item in lists:
  (rows,field_list)=merge(rows,field_list,'cache size',item,[x for x in item if 'COMMENT' in x[0]][0][1])


chosen_fields = input('Enter the fields to display in the desired order: ').split(',')
chosen_fields.insert(0,'cache size')
aliases = {k.split('=')[0]: k.split('=')[1] for k in chosen_fields if k.find('=') != -1}
for field in chosen_fields:
  if field not in aliases and field.find('=') == -1:
    aliases[field] = field
print('aliases: {}'.format(aliases))
custom_rows = [{aliases[k]:v for k,v in row.items() if k in aliases.keys()} for row in rows]
aliased_fields = [aliases[k] for k in chosen_fields]
print('custom rows: {}'.format(custom_rows))

write_csv(custom_rows, aliased_fields, sys.argv[2])
