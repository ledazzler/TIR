import logger
import urllib.request
import csv
import xml.etree.ElementTree as ET
import time
from urllib.request import Request

token = '4ac52be1-819d-4151-b251-935e795d3081'


headers = {
  'Authorization': 'Bearer ' + token
}
request = urllib.request.Request('https://investigate.api.opendns.com/domains/categorization/amazon.com', headers=headers)

response_body = urllib.request.urlopen(request).read()
print (response_body)




