#!/usr/bin/env python

import sys, re, csv, datetime, os
from shutil import copyfile

###this script was created for finding various stats regarding the responses. it operates on the corpus csv files. if you are looking for a particular stat or count from the corpus, this would be a good place to add a function to retrieve whatever you need.

all_file_ids=[]
all_file_ids_dict={} ##{'I01T': [[x], [x]...] ...} #each '[x]' is a list of the first 11 columns (the demographic info) from corpus respondents; it begins with Respondentid
t_v_u_uniques={}
master_demographics=[] ## this will be a flat list of every demographic row contained in any file of the corpus
response_ids=[]
id_response_dict={} ## this is a flat dictionary created from all files; key:value = response_id:response; note that response_id looks like: I29U-gNSC-p041-r2 (item-group-participant-response1or2) ## the dict can be flat because the response id contains all we need.
intrans=['01', '04', '07', '10', '13', '18', '20', '24', '27', '30']
trans=['02', '06', '09', '12', '15', '16', '19', '22', '25', '29']
ditrans=['03', '05', '08', '11', '14', '17', '21', '23', '26', '28']


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
	all_items=[]
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

def transform_response(myresp):
	tresp=' '.join(myresp.split())
	tresp=tresp.strip(' .!')
	tresp=tresp.lower()
	return tresp

def get_ttrs():  ##5/24; break time. I don't think I'm ignoring the NNS responses, as I should be. Also, the T and U counts are all coming out identically. 
	t_intrans_firsts=0
	t_intrans_f_types=0
	t_trans_firsts=0
	t_trans_f_types=0
	t_ditrans_firsts=0
	t_ditrans_f_types=0
	t_intrans_seconds=0
	t_intrans_s_types=0
	t_trans_seconds=0
	t_trans_s_types=0
	t_ditrans_seconds=0
	t_ditrans_s_types=0
	u_intrans_firsts=0
	u_intrans_f_types=0
	u_trans_firsts=0
	u_trans_f_types=0
	u_ditrans_firsts=0
	u_ditrans_f_types=0
	u_intrans_seconds=0
	u_intrans_s_types=0
	u_trans_seconds=0
	u_trans_s_types=0
	u_ditrans_seconds=0
	u_ditrans_s_types=0
	for n in range(1,31):
		for v in ['T', 'U']:
			file_id='I'+str(n).zfill(2)+v
			print file_id
			firsts=[]
			f_types=[]
			seconds=[]
			s_types=[]
			for rid in response_ids:
				#print rid
				ridparts=rid.split('-') ### example: i29U-gNSC-p041-r2 (item-group-participant-response1or2)
				i=ridparts[0]
				#print "i: ", i
				if i==file_id:
					#print "match"
					rnum=ridparts[3]
					if id_response_dict[rid]=='0':
						pass
					elif ridparts[1]=="gNNS":
						pass
					else:
						#print rnum
						raw_resp=id_response_dict[rid]
						resp=transform_response(raw_resp)
						if rnum=='r1':
							#print "first"
							#print "first, resp: ", resp
							firsts.append(resp)
							if resp not in f_types:
								f_types.append(resp)
						elif rnum=='r2':
							#print 'second, resp: ', resp
							#print "second"
							seconds.append(resp)
							if resp not in s_types:
								s_types.append(resp)
						else:
							print "nada"
							pass
				else: pass
			if str(n).zfill(2) in intrans:
				#print "INTRANS"
				if v=='T':
					#print "T intrans"
					t_intrans_firsts+=len(firsts)
					#print "adding", len(firsts)
					t_intrans_f_types+=len(f_types)
					t_intrans_seconds+=len(seconds)
					t_intrans_s_types+=len(s_types)
				elif v=='U':
					#print "U intrans"
					u_intrans_firsts+=len(firsts)
					u_intrans_f_types+=len(f_types)
					u_intrans_seconds+=len(seconds)
					u_intrans_s_types+=len(s_types)
				else: pass
			elif str(n).zfill(2) in trans:
				if v=='T':
					t_trans_firsts+=len(firsts)
					t_trans_f_types+=len(f_types)
					t_trans_seconds+=len(seconds)
					t_trans_s_types+=len(s_types)
				elif v=='U':
					u_trans_firsts+=len(firsts)
					u_trans_f_types+=len(f_types)
					u_trans_seconds+=len(seconds)
					u_trans_s_types+=len(s_types)
				else: pass
			elif str(n).zfill(2) in ditrans:
				if v=='T':
					t_ditrans_firsts+=len(firsts)
					t_ditrans_f_types+=len(f_types)
					t_ditrans_seconds+=len(seconds)
					t_ditrans_s_types+=len(s_types)
				elif v=='U':
					u_ditrans_firsts+=len(firsts)
					u_ditrans_f_types+=len(f_types)
					u_ditrans_seconds+=len(seconds)
					u_ditrans_s_types+=len(s_types)
				else: pass
			else: pass
	print 't_intrans_firsts:', t_intrans_f_types, t_intrans_firsts, float(t_intrans_f_types)/float(t_intrans_firsts)
	print 't_intrans_seconds:', t_intrans_s_types, t_intrans_seconds, float(t_intrans_s_types)/float(t_intrans_seconds)
	print 'u_intrans_firsts:', u_intrans_f_types, u_intrans_firsts, float(u_intrans_f_types)/float(u_intrans_firsts)
	print 'u_intrans_seconds:', u_intrans_s_types, u_intrans_seconds, float(u_intrans_s_types)/float(u_intrans_seconds)
	print 't_trans_firsts:', t_trans_f_types, t_trans_firsts, float(t_trans_f_types)/float(t_trans_firsts)
	print 't_trans_seconds:', t_trans_s_types, t_trans_seconds, float(t_trans_s_types)/float(t_trans_seconds)
	print 'u_trans_firsts:', u_trans_f_types, u_trans_firsts, float(u_trans_f_types)/float(u_trans_firsts)
	print 'u_trans_seconds:', u_trans_s_types, u_trans_seconds, float(u_trans_s_types)/float(u_trans_seconds)
	print 't_ditrans_firsts:', t_ditrans_f_types, t_ditrans_firsts, float(t_ditrans_f_types)/float(t_ditrans_firsts)
	print 't_ditrans_seconds:', t_ditrans_s_types, t_ditrans_seconds, float(t_ditrans_s_types)/float(t_ditrans_seconds)
	print 'u_ditrans_firsts:', u_ditrans_f_types, u_ditrans_firsts, float(u_ditrans_f_types)/float(u_ditrans_firsts)
	print 'u_ditrans_seconds:', u_ditrans_s_types, u_ditrans_seconds, float(u_ditrans_s_types)/float(u_ditrans_seconds)


def main():
	get_id_response_dict()
	#get_response_counts()
	get_ttrs()
	

if __name__ == "__main__":
    main()