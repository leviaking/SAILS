#!/usr/bin/env python

import sys, re, csv, datetime, os
from shutil import copyfile

###this script was created for finding various stats regarding the responses. it operates on the corpus csv files. if you are looking for a particular stat or count from the corpus, this would be a good place to add a function to retrieve whatever you need.

all_file_ids=[]
all_file_ids_dict={} ##{'i01T': [[x], [x]...] ...} #each '[x]' is a list of the first 11 columns (the demographic info) from corpus respondents; it begins with Respondentid
t_v_u_uniques={}
master_demographics=[] ## this will be a flat list of every demographic row contained in any file of the corpus
response_ids=[]
id_response_dict={} ## this is a flat dictionary created from all files; key:value = response_id:response; note that response_id looks like: i29U-gNSC-p041-r2 (item-group-participant-response1or2) ## the dict can be flat because the response id contains all we need.

##this constructs all_file_ids and id_response_dict;
def get_id_response_dict():
	for n in range(1,31):
		for v in ['T', 'U']:
			file_id='I'+str(n).zfill(2)+v
			all_file_ids.append(file_id)
			myfile=open('../sails/corpus/'+file_id+'_master_anno.csv', 'rU')
			myreader=csv.reader(myfile, dialect=csv.excel)
			skip_header=next(myreader, None)
			for row in myreader:
				response_id=row[12]
				response=row[13]
				response_ids.append(response_id)
				id_response_dict[response_id]=response
			myfile.close()
			
def get_response_counts():
	responses=0
	empties=0
	nns_responses=0
	ns_responses=0
	nsc_responses=0
	nsf_responses=0
	first_responses=0
	second_responses=0
	nsc_firsts=0
	nsc_seconds=0
	nsf_firsts=0
	nsf_seconds=0
	for rid in response_ids:
		if id_response_dict[rid]=='0':
			empties+=1
		else:
			responses+=1
			ridparts=rid.split('-') ### example: i29U-gNSC-p041-r2 (item-group-participant-response1or2)
			g=ridparts[1]
			r=ridparts[3]
			##count group
			if g=='gNNS':
				nns_responses+=1
			elif g=='gNSC':
				ns_responses+=1
				nsc_responses+=1
				if r=='r1':
					first_responses+=1
					nsc_firsts+=1
				elif r=='r2':
					second_responses+=1
					nsc_seconds+=1
				else: pass
			elif g=='gNSF':
				ns_responses+=1
				nsf_responses+=1
				if r=='r1':
					first_responses+=1
					nsf_firsts+=1
				elif r=='r2':
					second_responses+=1
					nsf_seconds+=1
				else: pass
			else: pass
	print 'empties: ', empties
	print 'responses: ', responses
	print 'NNS responses: ', nns_responses
	print 'NS responses: ', ns_responses
	print 'NSC responses: ', nsc_responses
	print 'NSF responses: ', nsf_responses
	print 'first responses: ', first_responses
	print 'second responses: ', second_responses
	print 'NSC firsts: ', nsc_firsts
	print 'NSC seconds: ', nsc_seconds
	print 'NSF firsts: ', nsf_firsts
	print 'NSF seconds: ', nsf_seconds




def main():
	get_id_response_dict()
	get_response_counts()

if __name__ == "__main__":
    main()