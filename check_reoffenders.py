#Take a list of 4 files, and compare each list for duplicates
#Print any usernames or hostnames that occur in two or more weeks
#imput should have one username or hostname per line, and no special characters etc



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



#print(w1d)
#print('***')
#print(w2d)
#print('***')
#print(w3d)
#print('***')
#print(w4d)
#print('***')

nodupes = [(set().union(w1d,w2d,w3d,w4d))]
for x in nodupes:
  for a in x:
    print(a)