# takes 4 files as input, checks each file to see if there are duplicate entries, and returns alist of duplicates

with open ('April25','r') as week1:
  week1list = week1.readlines()
  week1list = [x.lower() for x in week1list]
  week1list = [x.strip('\n') for x in week1list]
with open ('May1','r') as week2:
  week2list = week2.readlines()
  week2list = [x.lower() for x in week2list]
  week2list = [x.strip('\n') for x in week2list]
with open ('May9','r') as week3:
  week3list = week3.readlines()
  week3list = [x.lower() for x in week3list]
  week3list = [x.strip('\n') for x in week3list]
with open ('May16','r') as week4:
  week4list = week4.readlines()
  week4list = [x.lower() for x in week4list]
  week4list = [x.strip('\n') for x in week4list]
  

week1dupes = [x for x in week1list if x in (week2list or week3list or week4list)]

week2dupes = [x for x in week2list if x in (week1list or week3list or week4list)]

week3dupes = [x for x in week3list if x in (week1list or week2list or week4list)]

week4dupes = [x for x in week4list if x in (week1list or week2list or week3list)]

dupes = [week1dupes,week2dupes,week3dupes,week4dupes]

print(dupes)
