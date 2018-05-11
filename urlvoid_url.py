#This program takes a list of urls and passes them to urlvoid engine for analysis
#only 1000 queries per day are permitted.    enhancement require to ensure we don't go over that limit
#requires input of filename (urls should each be on a separate line) and API key
import logger
import urllib.request
import csv
import xml.etree.ElementTree as ET
import time

timestr = time.strftime("%Y-%m-%d-%H%M")
namestr = 'URLVOID_report' + timestr +'.csv'

key1 = ################
key2 = ################
key3 = ################

apikeylist = [key1,key2,key3]

def remaining_queries(key):
  remaining_url = 'http://api.urlvoid.com/api1000/' + key  + '/stats/remained/'
  contents = urllib.request.urlopen(remaining_url).read()
  
  et_xml = ET.fromstring(contents)
  root = et_xml
  
  remained = [ b.text for b in root.iterfind(".//queriesRemained")]
  remainedint = int(remained[0])
  keyend = key[-4:]
  #print('key ending {} has {} queries remaining today'.format(keyend,(remainedint)))
  return(remainedint)


def checkurl(url,key):
  urlstring = "http://api.urlvoid.com/api1000/" + key + "/host/" + url
  contents = urllib.request.urlopen(urlstring).read()

  et_xml = ET.fromstring(contents)
  root = et_xml

  engines = [ b.text for b in root.iterfind(".//engine")]
  count = [ b.text for b in root.iterfind(".//count")]
  host = [ b.text for b in root.iterfind(".//host")]
  error = [b.text for b in root.iterfind(".//error")]
  engines = ','.join(engines)
  count = ','.join(count)
  host = url.strip('\n')
  if len(engines) == 0:
    engines = 'none'
  if len(count) ==0:
    count = 0
  results = [host,count,engines]
  if len(error) >0:
    results.append(error)
  
  try:
    with open(namestr,'a') as f:
      writer = csv.writer(f)
      writer.writerow(results)
  except Exception as e:
    logger.error('Failed to write to csv: '+ str(e))

def choosekey(keylist):
  for key in keylist:
    counter = remaining_queries(key)
    keyend = key[-4:]
    try:
      if counter == 0:
        print('key ending {} has used all queries for today'.format(keyend))
      elif counter > 978:
        print ('choosekye func selecting key ending {}'.format(keyend))
        return(key)
    except Exception as e:
      logger.error('all keys have been used for today')
      return None
      
def urlvoid(file):
  with open(file,'r') as f:
    #remove blank space
    lines = (line.rstrip() for line in f) 
    lines = list(line for line in lines if line)
    for x in lines:
      key = choosekey(apikeylist)
      keyend = key[-4:]
      print('urlvoid func using key ending {} to submit {}'.format(keyend,x))
      checkurl(x,key)
    
#urlvoid('test.csv')

#for x in apikeylist:
#  print(remaining_queries(x))
# Next add error check for no more useable keys
