#This program takes a list of urls and passes them to urlvoid engine for analysis
#only 1000 queries per day are permitted.    enhancement require to ensure we don't go over that limit
#requires input of filename (urls should each be on a separate line) and API key
import logging
import urllib.request
import csv
import xml.etree.ElementTree as ET
import time

timestr = time.strftime("%Y-%m-%d-%H%M")
namestr = 'URLVOID_report' + timestr +'.csv'
apikey = input('please enter API key: ')

def checkurl(url):
  urlstring = "http://api.urlvoid.com/api1000/" + apikey + "/host/" + url
  contents = urllib.request.urlopen(urlstring).read()

  et_xml = ET.fromstring(contents)
  root = et_xml

  engines = [ b.text for b in root.iterfind(".//engine")]
  count = [ b.text for b in root.iterfind(".//count")]
  host = [ b.text for b in root.iterfind(".//host")]
  error = [b.text for b in root.iterfind(".//error")]
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
    logging.error('Failed to write to csv: '+ str(e))

def urlvoid():
  urlvoid_file = input('please enter file name: ')
  with open (urlvoid_file,'r') as f:
    for x in f:
      try:
        print('submitting {}'.format(x))
        checkurl(x)
      except Exception as e:
        logstr = 'Failed to submit {}: '.format(x) + str(e)
        logging.error(logstr)
        results.append(error)

urlvoid()