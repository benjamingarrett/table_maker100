import csv,itertools,os,sys

def write_lists(merged,fields,output_fname):
  with open(output_fname, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for entry in merged:
      writer.writerow(entry)

def merge_lists(current_list, fields, new_list, new_field, descending=True):
  fields.append(new_field)
  while len(new_list) > 0:
    entry = new_list.pop(0)
    merged = False
    for x in current_list:
      if x['_'] == entry['_']:
        x.update(entry)
        merged = True
        break
    if merged == False:
      current_list.append(entry)
  if descending == True:
    return (sorted(current_list, key = lambda i: int(i['_']), reverse=True), fields)
  else:
    return (sorted(current_list, key = lambda i: int(i['_'])), fields)

def fill_table(table):
  filled = []
  entry = table.pop(0)
  prev = int(entry['_'])
  filled.append(entry)
  while len(table) > 0:
    entry = table.pop(0)
    current = int(entry['_'])
    while current < prev - 1:
      prev -= 1
      filled.append({'_': prev})
    filled.append(entry)
    prev = current
  return filled

#input_path = './lcs_results'
input_path = sys.argv[1]
output_fname = sys.argv[2]
d = os.listdir(input_path)
merged = []
fields = ['_']
f = lambda x: x if len(x) > 0 else '0'
lists = []
for new_field in d:
  new_list = [line.rstrip('\n').split(',') for line in open(input_path+'/'+new_field)]
  new_list = [[f(x[0]),f(x[1])] for x in new_list]
  for item in new_list:
    if item[0] == '0':
      fname = item[1][0:item[1].find('.')]
      item[1] = item[1][0:item[1].find('-')]
  lists.append([fname, new_list])
lists.sort(key=lambda x: int(x[1][0][1]))
for item in lists:
  new_list = [{'_': x[0], item[0]: x[1]} for x in item[1]]
  (merged, fields) = merge_lists(merged, fields, new_list, item[0])
write_lists(fill_table(merged),fields,output_fname)

