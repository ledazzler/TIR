import pprint
import json
import glob
import csv
import time


if __name__ == "__main__":

	list_of_files = glob.glob('*.txt')
	routerdict = {}

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
		#routerdict = {}
		fileinfo = fileinfo.readlines()
		lines = fileinfo
		hn = ''
		iplist = []
		hostname_exclude = ['logging' ,'prompt','exceed','chap']
		#print 'trying {}'.format(file)
		for i in lines:
			try:
				i = i.strip()
				i = i.lstrip()
				if 'hostname' in i.lower() and i.split(' ')[0].lower() == 'hostname':
					hn = i.split('hostname')[1]
					hn = hn.strip()
					hn = hn.lstrip()
					print 'working on file {}, hostname = {}'.format(file,hn)
				elif 'ip address' in i.lower():
					ipad = i.split('ip address')[1]
					ipad = ipad.strip()
					ipad = ipad.lstrip()
					ipad = ipad.split(' ')[0]
					if check_ip(ipad) == True:
						iplist.append(ipad)
					else:
						continue
			except Exception as e:
				print 'error {} at filename {}'.format(e,file)
				
		if hn not in routerdict.keys():
			routerdict[hn] = iplist
			#print 'adding {} \n'.format(hn)
			#print '{} - adding {}'.format(hn, str(iplist))
			#print'\n'
		elif hn in routerdict.keys():
			#print 'NOT adding {} \n'.format(hn)
			for x in iplist:
				if x not in routerdict[hn]:
					routerdict[hn].append(x)
					#print '{} already exists , appending {} to ip list \n'.format(hn,x)
			
			
	for i in list_of_files:
		gethn(i)
	
	#output
	
	w = csv.writer(open("output_ips_customer_partner.csv", "a"))
	for key, val in routerdict.items():
		w.writerow([key, val])
