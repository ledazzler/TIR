import pprint
import json
import glob
import csv
import time

#to run:
#from get_device_ip_csv import *
#for i in list_of_files:
  #gethn(i)


timestr = time.strftime("%Y-%m-%d-%H%M")

list_of_files = glob.glob('*.config')

def check_ip(str):
#Check that text after string 'ip-address' is formatted like an ip address
  str = str.strip()
  str = str.lstrip()
  chunks = str.split('.')
  if len(chunks) ==4:
    return True
  else:
    return False

def gethn(file):
  fileinfo = open(file,'rb')
  routerdict = {}
  fileinfo = fileinfo.readlines()
  lines = fileinfo
  hn = ''
  iplist = []
  for i in lines:
    i = i.strip()
    i = i.lstrip()
    if 'hostname' in i.lower() and 'logging' not in i.lower():
      hn = i.split('hostname')[1]
      hn = hn.strip()
      hn = hn.lstrip()
    elif 'ip address' in i.lower():
      ipad = i.split('ip address')[1]
      ipad = ipad.strip()
      ipad = ipad.lstrip()
      ipad = ipad.split(' ')[0]
      if check_ip(ipad) == True:
        iplist.append(ipad)
    else:
      continue
  		
  if hn not in routerdict.keys():
    routerdict[hn] = iplist
  
  #output
  
  w = csv.writer(open("output_ips.csv", "a"))
  for key, val in routerdict.items():
    w.writerow([key, val])