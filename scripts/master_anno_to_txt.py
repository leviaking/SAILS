#!/usr/bin/env python

## 2018/07/05. LK. 

import sys, re, csv, datetime, os
from shutil import copyfile

def write_responses_to_txt_files():
	for n in range(1,31):
		for v in ['T', 'U']:
			file_id='I'+str(n).zfill(2)+v
			myfile=open('../sails/corpus/'+file_id+'_master_anno.csv', 'rU')
			myreader=csv.reader(myfile, dialect=csv.excel)
			skip_header=next(myreader, None)
			mytxt=open('../sails/corpus/txt/'+file_id+'_responses_only.txt', 'w')
			for row in myreader:
				respy=str(row[13])
				if respy!='0':
					mytxt.write(respy.strip()+'\n')
				else:
					pass
			myfile.close()
			mytxt.close()

write_responses_to_txt_files()
