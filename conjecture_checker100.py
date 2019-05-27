import csv,os,sys

def get_size_bounds():
  min_n = sys.maxsize
  max_n = 0
  for fname in d:
    new_list = [line.rstrip('\n').split(',') for line in open('./results/' + fname)]
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    for item in new_list:
      if item[0] == '0':
        n = int(item[1][0:item[1].find('-')])
        min_n = n if n < min_n else min_n
        max_n = n if n > max_n else max_n
  return (min_n,max_n)

def verify_list(new_list,q,n):
  #print("verify_list {}".format(new_list))
  for item in new_list:
    if item[0] is not '0':
      s = int(item[0])
      c = int(item[1])
      if s == 2 * n:
        x = g(n,q)
        #print("{} {}".format(c,x))
        if c > g(n,q):
          #print('false')
          #print("{} {}".format(c,x))
          return False
  return True

def verify(q):
  for fname in d:
    new_list = [line.rstrip('\n').split(',') for line in open('./results/' + fname)]
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    for item in new_list:
      if item[0] == '0':
        n = int(item[1][0:item[1].find('-')])
    if verify_list(new_list,q,n) == False:
      return False
  return True

def write_plotting_data():
  plotting_data = []
  value_dict = {}
  for fname in d:
    new_list = [line.rstrip('\n').split(',') for line in open('./results/' + fname)]
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    for item in new_list:
      if item[0] == '0':
        n = int(item[1][0:item[1].find('-')])
    if n not in value_dict:
      value_dict[n] = []
    for item in new_list:
      if item[0] is not '0':
        if int(item[0]) == 2 * n:
          value_dict[n].append(int(item[1]))
  #print("value_dict={}".format(value_dict))
  for k,v in value_dict.items():
    plotting_data.append([k,max(v)])
  plotting_data.sort(key = lambda x: x[0])
  print("plotting_data={}".format(plotting_data))
  with open('plotting_data.csv','w') as fp:
    writer = csv.writer(fp)
    writer.writerows(plotting_data)
  fp.close()

d = os.listdir('./results')
f = lambda x: x if len(x) > 0 else '0'
#g = lambda x,y: y**x
g = lambda x,y: x**y
#g = lambda x,y: y*x*x
q = 2.89
best = q
while q > 1:
  result = verify(q)
  print("{} {}".format(q,result))
  if result == True:
    best = q
  else:
    break
  q -= 0.000001
(min_n,max_n) = get_size_bounds()
write_plotting_data()
print("min_n = {}  max_n = {}".format(min_n,max_n))
print("best = {}".format(best))
