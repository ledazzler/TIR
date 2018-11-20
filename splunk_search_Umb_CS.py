### This program takes a file as input, and generates splunk search query to check those usernames in Umbrella and Crowdstrike index
### First search string returns data in a table, sorted by username
### Second search string returns stats  - count by user

#import glob

def getfilename():
  filelist = glob.glob('*')
  validfile = False
  while validfile == False:
    try:
      filename = input('enter filename:')
      if filename not in filelist:
        print ('\nthat file does not exist.   Try again \n')
      elif filename in filelist:
        validfile = True
    except Exception as e:
      print('error {}'.format(str(e)))
  return(filename)

def searchstrings(infile):
  with open(infile,'r') as umbrella:
    umbrella = umbrella.readlines()
    umbrella = [x.strip() for x in umbrella]
    umbrella = [x.strip('\n') for x in umbrella]
    umbrella = ['"' + x + '"' for x in umbrella]
    umbrella = ['OR identities = ' + x for x in umbrella]
    umbstr = ' '.join(umbrella)
    umbstr = umbstr[3:]
    umbstr = '(index="umbrella" AND action = blocked AND ' + umbstr + ')'
    #print(umbstr)
  with open(infile,'r') as cs:
    cs = cs.readlines()
    cs = [x.strip() for x in cs]
    cs = [x.strip('\n') for x in cs]
    cs = ['"' + x + '"' for x in cs]
    cs = ['OR user = ' + x for x in cs]
    csstr = ' '.join(cs)
    csstr = csstr[3:]
    csstr = '(index="crowdstrike" AND ' + csstr + ')'
    #print(csstr)
  tablesuffix = """| rename event.SeverityName as "CS Severity"  category as "Umbrella category"| eval ID = coalesce(identities,user) | table index, ID, "CS Severity" , "Umbrella category", _time | eval ID = lower(ID) | sort +str(ID)"""

  statssuffix = """| rename event.SeverityName as "CS Severity"  category as "Umbrella category"| eval ID = coalesce(identities,user) | stats count by ID | sort -count"""

  tablestr =  umbstr + ' OR ' + csstr + tablesuffix
  statsstr = umbstr + ' OR ' + csstr + statssuffix
  print('the string to generate a table of users and detctions is: \n')
  print(tablestr)
  print('\n'*3)
  print('the string to generate a count of user detctions is: \n')
  print(statsstr)

if __name__ == "__main__":
  import glob
  a = getfilename()
  searchstrings(a)