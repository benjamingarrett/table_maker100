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
write_csv(rows,field_list,sys.argv[2])
