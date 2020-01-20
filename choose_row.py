import sys

lists=[ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]
lst=[k for k in lists[int(sys.argv[2])]]
print(lst)
if len(sys.argv) >= 4:
  with open(sys.argv[3],'w') as fp:
    i=0
    while i<len(lst)-1:
      fp.write(lst[i]+'\n')
      i+=1
    fp.write(lst[i])
