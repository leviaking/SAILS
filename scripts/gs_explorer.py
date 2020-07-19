#!/usr/bin/env python

##LK 2018... This script generates a csv that shows how many responses there are various GS files, listed for all 60 items.

import sys, re, csv, datetime, os
from shutil import copyfile

# all_file_ids=[] ## e.g., 'I01T', 'I29U'
# superdict={} ##{'I01T': [[x], [x]...] ...} #each '[x]' is a list of seven values (row[12:19])

gs_names=['all_ns', 'all_fns', 'all_cns', 'firsts', 'seconds', 'perfects', 'almosts', 'coreyes']
header=list(gs_names)
header.insert(0, 'item-gs')
outfile=open('../stats/gs_response_counts.csv', 'w')
outwriter=csv.writer(outfile, dialect=csv.excel)
outwriter.writerow(header)

def get_response_counts():
	for n in range(1,31):
		for v in ['T', 'U']:
			itemrow=[]
			for gsn in gs_names:
				linecounter=0
				file_id='I'+str(n).zfill(2)+v
				myfilename='../gold_standards/'+file_id+'_'+gsn+'.csv'
				myfile=open(myfilename, 'r')
				myreader=csv.reader(myfile, dialect=csv.excel)
				skip_header=next(myreader, None)
				for row in myreader:
					linecounter+=1
				#print myfilename[18:], '\t', linecounter
				itemrow.append(linecounter)
			itemrow.insert(0, file_id)
			outwriter.writerow(itemrow)
	outfile.close()

def main():
	get_response_counts()


if __name__ == "__main__":
    main()