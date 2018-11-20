## open a file and pull out line numbers that are of a particular length

with open('a','r') as a:
  alist = a.readlines()

counter = 1
for x in alist:
  if len(x) > 10000:
    print(f'match at line {counter}') 
    counter+=1
  else:
    counter+=1