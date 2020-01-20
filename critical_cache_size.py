from math import log 
import os,sys


def critical_cache_size(lst):
  if lst[0][1]!=lst[1][1]:
    print("Warning: in computing critical cache size, the first two values found not to be equal")
    bad_data_set=True
  else:
    bad_data_set=False
  j = 1
  while j<len(lst):
    if lst[0][1]!=lst[j][1]:
      return (lst[j-1][0],lst[j-1][1],bad_data_set)
    j+=1
  return (lst[len(lst)-1][0],lst[len(lst)-1][1],bad_data_set)


def custom_critical_cache_size(lst,threshold):
  # Find minimum cache size, such that cache misses <= f(n)
  if lst[0][1] > threshold:
    print("Warning: in computing custom critical cache size, the first value violates given condition")
    bad_data_set=True
  else:
    bad_data_set=False
  j = 1
  while j<len(lst):
    if lst[j][1] > threshold:
      return (lst[j-1][0],lst[j-1][1],bad_data_set)
    j+=1
  return (lst[len(lst)-1][0],lst[len(lst)-1][1],bad_data_set)


def process_data_set(lists,j,last_item,fp=None):
  lst=[(int(k[0]),int(k[1])) for k in lists[j] if k[0]!='COMMENT' and k[0]!='SORT_BY']
  n=[(k[0],int(k[1])) for k in lists[j] if k[0]=='SORT_BY'][0][1]
  (c_size,misses,warning)=critical_cache_size(lst)
  #(c_size,misses,warning)=custom_critical_cache_size(lst,1.411723841*log(n+2,2)*log(log(n+2,2),2))
  #print('{} {} {}'.format(n,c_size,misses))
  if warning:
    print('warning {} {} {}'.format(n,c_size,misses))
  if fp:
    if last_item:
      fp.write(str(n)+','+str(c_size)+','+str(misses))
    else:
      fp.write(str(n)+','+str(c_size)+','+str(misses)+'\n')
  return warning


lists=sorted([[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn and fn!='m.csv'],key=lambda k:(int(k[1][1]),k[0][1]))
#print(lists[0])
if len(sys.argv) >= 3:
  fp=open(sys.argv[2],'w')
j = 0
warnings=0
while j<len(lists)-1:
  if process_data_set(lists,j,False,fp):
    warnings+=1
  j+=1
if process_data_set(lists,j,True,fp):
  warnings+=1
print('Number of warnings: {}'.format(warnings))
