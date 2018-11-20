import glob
import requests
import time
import csv
import logging
import urllib.request
import xml.etree.ElementTree as ET

vtapikey = 'XXXXXX'
urlvapikey = 'XXXXXX'
timestr = time.strftime("%Y-%m-%d-%H%M")
namestr = 'C_C_report' + timestr +'.csv'
csv_columns = ["site", "VT detections","URL Void detections", "URL Void engines"]

def getfilename():
  filelist = glob.glob('*')
  validfile = False
  while validfile == False:
    try:
      filename = input('enter filename:')
      if filename not in filelist:
        print ('\nthat file does not exist.   Try again \n')
      elif filename in filelist:
        f = open(filename,'r')
        f = f.readlines()
        #flist = f.split('\n')
        if len(f) > 998:
          print ('\nMax number of lines is 998.\n{} has {} lines\nPlease select another file \n'.format(filename,len(f)))
        elif len(f) <= 998:
          validfile = True
    except Exception as e:
      print('error {}'.format(str(e)))
  results = (f,filename)
  return results

def vt_submit(url):
  try:
    params = {'apikey': vtapikey, 'url':url}
    print('sleeping for 16 seconds')
    time.sleep(16)
    #print('url = {}'.format(url))
    r = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
    print(r.status_code, r.reason) 
    #print(r.text[:300] + '...')
    #json_response = r.json()
    #print(json_response)
  except Exception as e:
    print('error {}'.format(str(e)))

def vt_report(url):
  try:
    headers = {"Accept-Encoding": "gzip, deflate","User-Agent" : "gzip,  My Python requests library example client or username"}
    params = {'apikey': vtapikey, 'resource':url}
    positives = []
    print('sleeping for 16 seconds')
    time.sleep(16)
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
    #print('assessing {}'.format(url))
    print(response.status_code, response.reason)
    json_response_url = response.json()
    if 'Resource does not exist in the dataset' in json_response_url['verbose_msg']:
      print('{} does not exist in VT'.format(url))
      reportdict[url] = 'not found' 
    elif 'positives' in json_response_url.keys():
      positives = json_response_url['positives']
      #reportdict[url] = positives
      #print ("{} sites rate url {} as malicious".format(positives, url))
    #print(json_response_url)
  except Exception as e:
    print('error {}'.format(str(e)))
  return positives

def urlvoid(url):
  urlstring = "http://api.urlvoid.com/api1000/" + urlvapikey + "/host/" + url
  contents = urllib.request.urlopen(urlstring).read()

  et_xml = ET.fromstring(contents)
  root = et_xml

  engines = [ b.text for b in root.iterfind(".//engine")]
  count = [ b.text for b in root.iterfind(".//count")]
  #host = [ b.text for b in root.iterfind(".//host")]
  error = [b.text for b in root.iterfind(".//error")]
  count = ','.join(count)
  host = url.strip('\n')
  if len(engines) == 0:
    engines = 'none'
  if len(count) ==0:
    count = 0
  results = [count,engines]
  if len(error) >0:
    results.append(error)
  return results

def printcsv(results):
  try:
    with open(namestr,'a') as f:
      writer = csv.writer(f)
      writer.writerow(["site", "VT detections","URL Void detections", "URL Void engines"])
      for x in results:
        xlist = []
        for value in x.values():
          xlist.append(value)
        writer.writerow(xlist)
  except Exception as e:
    logging.error('Failed to write to csv: '+ str(e))

def WriteDictToCSV(csv_file,csv_columns,dict_data):
  try:
    with open(csv_file, 'a') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
      writer.writeheader()
      for data in dict_data:
        writer.writerow(data)
  except Exception as e:
    logging.error('Failed to write to csv: '+ str(e))
  return



def aio(f):
  reportlist = []
#take in list of sites, remove spaces/CR 
  f = [x.strip() for x in f]
  f = [x.strip('\n') for x in f]
  f = [x.lstrip() for x in f]
#create dictionary, where each URL is a dict key
  for x in f:
#submit URL to VT, retrieve result
    urldict = {}
    urldict['site'] = x
    vt_submit(x)
    urldict['VT detections'] = vt_report(x) 
#submit URL to URL Void
    urldict['URL Void detections'] = urlvoid(x)[0]
    urldict['URL Void engines'] = urlvoid(x)[1]
    reportlist.append(urldict)
  WriteDictToCSV(namestr,csv_columns,reportlist)

if __name__ == "__main__":
  params = getfilename()
  f = params[0]
  aio(f)