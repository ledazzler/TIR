with open('week1','r') as week1:
  w1list = week1.readlines()
  w1list = [x.strip('\n') for x in w1list]
  w1list = [x.lower() for x in w1list]
  w1list = [x.strip() for x in w1list]

with open('week2','r') as week2:
  w2list = week2.readlines()
  w2list = [x.strip('\n') for x in w2list]
  w2list = [x.lower() for x in w2list]
  w2list = [x.strip() for x in w2list]

with open('week3','r') as week3:
  w3list = week3.readlines()
  w3list = [x.strip('\n') for x in w3list]
  w3list = [x.lower() for x in w3list]
  w3list = [x.strip() for x in w3list]

with open('week4','r') as week4:
  w4list = week4.readlines()
  w4list = [x.strip('\n') for x in w4list]
  w4list = [x.lower() for x in w4list]
  w4list = [x.strip() for x in w4list]

w1d = [x for x in w1list if x in w2list or x in w3list or x in w4list]
w2d = [x for x in w2list if x in w1list or x in w3list or x in w4list]
w3d = [x for x in w3list if x in w1list or x in w2list or x in w4list]
w4d = [x for x in w4list if x in w1list or x in w2list or x in w3list]

nodupes = [(set().union(w1d,w2d,w3d,w4d))]

w12list = []
w13list = []
w14list = []
w23list = []
w24list = []
w34list = []
w124list = []
w134list = []
w234list = []
w1234list = []

overlaplists = [w12list,w13list,w14list,w23list,w24list,w34list,w124list,w134list,w234list,w1234list]
counter = 0
for a in nodupes[0]:
  alist = []

  if a in w1list:
    alist.append('1')
  if a in w2list:
    alist.append(',2') 
  if a in w3list:
    alist.append(',3')
  if a in w4list:
    alist.append(',4')
  
  aliststr = ''.join(alist)
  if aliststr[0] == ',':
    aliststr = aliststr[1:]
  if aliststr == '1,2':
    w12list.append(a)
  elif aliststr == '1,3':
    w13list.append(a)
  elif aliststr == '1,4':
    w14list.append(a)
  elif aliststr == '2,3':
    w23list.append(a)    
  elif aliststr == '2,4':
    w24list.append(a)
  elif aliststr == '3,4':
    w34list.append(a)
  elif aliststr == '3,4':
    w34list.append(a)

  #print('{} detected in weeks {}'.format(a,aliststr))

#print (len(w12list)+ len(w14list) + len(w24list))
#print(len(nodupes[0]))

print ('w12: \n')
for x in w12list:
  print(x)
print ('\nw14: \n')
for x in w14list:
  print(x)
print ('\nw24: \n')
for x in w24list:
  print(x)