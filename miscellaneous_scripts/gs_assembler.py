#!/usr/bin/env python

##LK 2018/06/21: This script is used to assemble the various gold standard sets that will be used in the experiments. For example, one GS will consist of all NS responses; another will be all 5/5 annotated responses; another will contain only 1st responses from NSs; etc. The resulting files will have a header file, then each row will have: ResponseID, Response, Core, Answerhood, Grammaticality, Interpretability, Verifiability (feature annotations).

import sys, re, csv, datetime, os
from shutil import copyfile

all_file_ids=[] ## e.g., 'I01T', 'I29U'
superdict={} ##{'I01T': [[x], [x]...] ...} #each '[x]' is a list of seven values (row[12:19])


##this constructs all_file_ids and superdict;
def get_all_content():
	#rcount=0
	for n in range(1,31):
		for v in ['T', 'U']:
			file_id='I'+str(n).zfill(2)+v
			all_file_ids.append(file_id)
			meat=[] ##for lack of better term; this is row[12:19] (ResponseID, Response, 5 feature annotations)
			#file_demographics=[] ##this is the first 11 columns of the file, starting with Respondentid
			myfile=open('../sails/corpus/'+file_id+'_master_anno.csv', 'rU')
			myreader=csv.reader(myfile, dialect=csv.excel)
			skip_header=next(myreader, None)
			for row in myreader:
				if str(row[13])!='0':
					#rcount+=1
					#print row[12:19]
					meat.append(row[12:19])
				else:
					pass
			myfile.close()
			superdict[file_id]=meat
	#print rcount

def create_gs_files():
	header=['ResponseID', 'Response', 'Core', 'Answer', 'Gramm', 'Interp', 'Verif']
	for file_id in all_file_ids:
		all_nns=[]
		all_fns=[]
		all_cns=[]
		firsts=[]
		seconds=[]
		perfects=[]
		almosts=[]
		for m in superdict[file_id]:
			rid=m[0]
			rid=rid.split('-')
			group=rid[1]
			fs=rid[3] ##fs for "first-second"
			if 'gNS' in group:
				all_nns.append(m)
				if group=='gNSF':
					all_fns.append(m)
				elif group=='gNSC':
					all_cns.append(m)
				else: pass
				if fs=='r1':
					firsts.append(m)
				elif fs=='r2':
					seconds.append(m)
				else: pass
				if str(m[2])=='1': ##this is Core Event
					if sum([int(q) for q in m[2:]])==4 or sum([int(q) for q in m[2:]])==5:
						almosts.append(m)
					else: pass
					if sum([int(q) for q in m[2:]])==5:
						perfects.append(m)
					else: pass
				else: pass
			else: pass
		gs_names=['all_nns', 'all_fns', 'all_cns', 'firsts', 'seconds', 'perfects', 'almosts']
		gs_dict={'all_nns':all_nns, 'all_fns':all_fns, 'all_cns':all_cns, 'firsts':firsts, 'seconds':seconds, 'perfects':perfects, 'almosts':almosts}
		for gn in gs_names:
			outfile=open('../gold_standards/'+file_id+'_'+gn+'.csv', 'w')
			outwriter=csv.writer(outfile, dialect=csv.excel)
			outwriter.writerow(header)
			current_pile=gs_dict[gn]
			for cprow in current_pile:
				outwriter.writerow(cprow)
			outfile.close()


def main():
	get_all_content()
	create_gs_files()
	

if __name__ == "__main__":
    main()