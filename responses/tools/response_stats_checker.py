#!/usr/bin/env python

##LK: This is for troubleshooting the output of "get_annotation_file.py". Copy this script into the folder of the output files and run it there.

##usage:
##python response_stats_checker.py <hour>
##"hour" here is the four digit number that occurs as the last four digits of all the files you are checking. It's also the last four digits of the folder containing those files.

import sys, re, csv, datetime, os

def get_csv_names(itemnum, hour):
	tname = 'I'+str(itemnum).zfill(2)+'T_Verif-'+hour+'.csv'
	uname = 'I'+str(itemnum).zfill(2)+'U_Interp-'+hour+'.csv'
	cname = 'I'+str(itemnum).zfill(2)+'TU_Gramm-'+hour+'.csv'
	return tname, uname, cname

def get_responses_from_csv(csv_in):
	responses = []
	with open(csv_in, 'r') as masterfile:
		masterreader = csv.reader(masterfile)
		mheader1 = next(masterreader, None)
		for mrow in masterreader:
			resp=mrow[0]
			responses.append(resp)
	responses = filter(None, responses)
	return responses

def get_stats(n, hour):
	tn, un, cn = get_csv_names(n, hour)
	trs = get_responses_from_csv(tn)
	urs = get_responses_from_csv(un)
	crs = get_responses_from_csv(cn)
	tdups = check_duplicates(list(trs))
	udups = check_duplicates(list(urs))
	cdups = check_duplicates(list(crs))
	missing =[] ##these responses are in T or U, but not in C for some reason (this shouldn't happen)
	tmiss = []
	umiss = []
	intersection = []
	for t in trs:
		if t not in crs:
			tmiss.append(t)
			missing.append(t)
		if t in urs:
			intersection.append(t)
	for u in urs:
		if u not in crs:
			umiss.append(u)
			missing.append(u)
		if u in trs:
			if u not in intersection:
				intersection.append(u)
	exs = [] ##exclusives
	tex = [] 
	uex = [] 
	for t in trs:
		if t not in urs:
			tex.append(t)
			exs.append(t)
	for u in urs:
		if u not in trs:
			uex.append(u)
			exs.append(u)
	print n 
	tt = len(trs)
	print 'Targeted types: ', tt
	ut = len(urs)
	print 'Untarget types: ', ut
	tut = len(crs)
	print 'Targ+Unt types: ', tut
	ix = len(intersection)
	print 'Intersection: ', ix
	texl = len(tex)
	print 'Targ Exclusives: ', texl
	uexl = len(uex)
	print 'Untarg Exclusives: ', uexl
	ex = len(exs)
	print 'Total exclusives: ', ex
	if tdups:
		print 't duplicates: ', tdups
	if udups:
		print 'u duplicates: ', udups
	if cdups:
		print 'c duplicates: ', cdups
	if missing:
		print 'Missing resps: ', len(missing)
	if tmiss:
		print 'Missing targeted responses: ', tmiss
	if umiss:
		print 'Missing untargeted responses: ', umiss
	print '\n\n'

def check_duplicates(mylist):
	duplicates = []
	while mylist:
		m = mylist.pop()
		if m in mylist:
			duplicates.append(m)
	return duplicates ##these are responses (types) that appear more than once in the response set for a given item.
	
	
def main():
	hour = sys.argv[1]
	for n in range(1,31):
		get_stats(n, hour)
	# write_type_csv(targeted_outputrows, 'targeted', timestamp)
	# write_type_csv(untargeted_outputrows, 'untargeted', timestamp)
	
if __name__ == "__main__":
    main()
