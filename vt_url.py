import requests
import time
import csv

reportdict = {}
outlist = []
timestr = time.strftime("%Y-%m-%d-%H%M")
namestr = 'VT_report' + timestr +'.csv'
vt_file = input('please enter file name: ')
apikey = input('please enter API key: ')

def submit_url(url):
        try:
          params = {'apikey': apikey, 'url':url}
          print('sleeping for 16 seconds')
          time.sleep(16)
          #print('url = {}'.format(url))
          r = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
          print(r.status_code, r.reason) 
          #print(r.text[:300] + '...')
          #json_response = r.json()
          #print(json_response)
        except:
          print('there was an error')
  

def url_report(url):
  try:
    headers = {"Accept-Encoding": "gzip, deflate","User-Agent" : "gzip,  My Python requests library example client or username"}
    params = {'apikey': '55c44c1aab59c367d6059c9edcdb535c9d5f7c43dd987026e467fe5d79a50d40', 'resource':url}
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
      reportdict[url] = positives
      #print ("{} sites rate url {} as malicious".format(positives, url))
    #print(json_response_url)
  except:
    print('there was an error')

def to_csv(urldict):
  try:
    with open(namestr, 'w') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(["site", "detections",])
      print('writing headers')
      for key, value in urldict.items():
        writer.writerow([key, value])
  except:
    print('there was an error')

def vt(txtfile):
  try:
    with open(txtfile) as f:
      for line in f:
        line = line.strip()
        outlist.append(line)
    #print(outlist)
    for x in outlist:
      #x = x.strip()
      print('submitting {}'.format(x))
      submit_url(x)
    for x in outlist:
      #x = x.strip()
      print('retreiving {}'.format(x))
      url_report(x)
  
    print('generating CSV')
    to_csv(reportdict)
  except:
    print('there was an error')

vt(vt_file)