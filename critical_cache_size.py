# Usage: python critical_cache_size <folder> <output_fname> [<method>]
# method is optional and defaults to 'normal' -> critical_cache_size          : min such that misses are min with warnings
# other methods are                  'relax'  -> relaxed_critical_cache_size  : min such that misses are min without warnings
#                                    'custom' -> custom_critical_cache_size   : min such that misses <= f(n)

from math import log 
import os,sys


def relaxed_critical_cache_size(lst):
  # For the given list return the cache size for which cache misses are minimal, regardless of whether the first two are not equal
  j = 1
  while j<len(lst):
    if lst[0][1]!=lst[j][1]:
      return (lst[j-1][0],lst[j-1][1],False)
    j+=1
  if len(lst) > 0:
    return (lst[len(lst)-1][0],lst[len(lst)-1][1],False)
  else:
    return (-1,-1,True)


def critical_cache_size(lst):
  # Find cache size such that cache misses are minimized
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
  if len(lst) > 0:
    return (lst[len(lst)-1][0],lst[len(lst)-1][1],bad_data_set)
  else:
    return (-1,-1,True)


def custom_critical_cache_size(lst,threshold=1):
  # Find minimum cache size, such that cache misses <= f(n)
  print('method custom_critical_cache_size is broken, please fix in order to receive threshold properly')
  exit()
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


def process_data_set(lists,j,last_item,method,fp=None):
  lst=[(int(k[0]),int(k[1])) for k in lists[j] if k[0]!='COMMENT' and k[0]!='SORT_BY']
  n=[(k[0],int(k[1])) for k in lists[j] if k[0]=='SORT_BY'][0][1]

  (c_size,misses,warning)=relaxed_critical_cache_size(lst)

  #(c_size,misses,warning)=method(lst)
  #(c_size,misses,warning)=critical_cache_size(lst)
  #(c_size,misses,warning)=custom_critical_cache_size(lst,1.411723841*log(n+2,2)*log(log(n+2,2),2))
  #print('{} {} {}'.format(n,c_size,misses))
  if warning:
    print('warning {} {} {}'.format(n,c_size,misses))
  else:
    if fp:
      if last_item:
        fp.write(str(n)+','+str(c_size)+','+str(misses))
      else:
        fp.write(str(n)+','+str(c_size)+','+str(misses)+'\n')
  return warning


lists=sorted([[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn and fn!='m.csv'],key=lambda k:(int(k[1][1]),k[0][1]))
#print(lists)
#exit()

if len(sys.argv) >= 3:
  fp=open(sys.argv[2],'w')
if len(sys.argv) >= 4:
  print('warning: selecting method is disabled')
  if sys.argv[3].casefold()=='normal'.casefold():
    method = critical_cache_size
  if sys.argv[3].casefold()=='relax'.casefold():
    method = relaxed_critical_cache_size
  if sys.argv[3].casefold()=='custom'.casefold():
    method = custom_critical_cache_size
else:
  method = critical_cache_size
j = 0
warnings=0
while j<len(lists)-1:
  if process_data_set(lists,j,False,method,fp):
    warnings+=1
  j+=1
if process_data_set(lists,j,True,fp):
  warnings+=1
print('Number of warnings: {}'.format(warnings))
if len(sys.argv[2]) >= 3:
  fp.close()
