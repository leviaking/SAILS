#!/usr/bin/env python

##LK: Due to the strict rules around Answerhood, a number of responses can be automatically rejected These are responses that contain the subject but not in the form in which it appears in the sentence. The rejected responses will need to be reviewed, but this is much quicker than annotating. The remaining responses will still need to be annotated manually.

##For example, a response that uses "a boy" or "that boy" instead of the required "the boy" can be automatically rejected.

##usage:
##python answerhood_targeted_response.py <hour>
##"hour" here is the four digit number that occurs as the last four digits of all the files you are checking. It's also the last four digits of the folder containing those files.

import sys, re, csv, datetime, os
from shutil import copyfile


Qs = 		['What is the boy doing?',
			  'What is the boy doing?',
			  'What is the man doing?',
			  'What is the boy doing?',
			  'What is the teacher doing?',
			  'What is the boy doing?',
			  'What is the bird doing?',
			  'What is the waiter doing?',
			  'What is the girl doing?',
			  'What is the baby doing?',
			  'What is the boy doing?',
			  'What is the woman doing?',
			  'What is the man doing?',
			  'What is the man doing?',
			  'What is the man doing?',
			  'What is the frog doing?',
			  'What is the girl doing?',
			  'What is the man doing?',
			  'What is the woman doing?',
			  'What is the girl doing?',
			  'What is the boy doing?',
			  'What is the woman doing?',
			  'What is the doctor doing?',
			  'What is the boy doing?',
			  'What is the dog doing?',
			  'What is the man doing?',
			  'What is the girl doing?',
			  'What is the man doing?',
			  'What is the woman doing?',
			  'What is the woman doing?']

subjects = ['the boy ', #1
			'the boy ',
			'the man ',
			'the boy ',
			'the teacher ',#5
			'the boy ',
			'the bird ',
			'the waiter ',
			'the girl ',
			'the baby ', #10
			'the boy ',
			'the woman ',
			'the man ',
			'the man ',
			'the man ', #15
			'the frog ',
			'the girl ',
			'the man ',
			'the woman ',
			'the girl ', #20
			'the boy ',
			'the woman ',
			'the doctor ',
			'the boy ',
			'the dog ', #25
			'the man ',
			'the girl ',
			'the man ',
			'the woman ',
			'the woman ']

def get_csv_name(itemnum, hour):
	tname = 'I'+str(itemnum).zfill(2)+'T_Answer-'+hour+'.csv'
	#tname = 'I'+str(itemnum).zfill(2)+'T_Answer-'+hour+'-TEMPBACKUP.csv'
	return tname

def get_responses_from_csv(csv_in): ##note that this also copies the file as a backup filename and deletes the original.
	responses = []
	with open(csv_in, 'r') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		mheader1 = next(masterreader, None)
		for mrow in masterreader:
			#print mrow
			resp=mrow[0]
			#print resp
			responses.append(resp)
	responses = filter(None, responses)
	copyfile(csv_in, 'answerhood_backup/BACKUP_'+csv_in)
	os.remove(csv_in)
	return responses, mheader1

def sort_by_subjects(i, hr): ##'i' should be an item number
	#print i
	manualresponses = [] ##these are responses that need to be manually annotated.
	badresponses = [] ##these are responses that can be automatically rejected.
	question = Qs[i-1]
	subj = subjects[i-1]
	subjhead = subj.split(' ')[1]
	inputfile = get_csv_name(i, hr)
	responselist, header = get_responses_from_csv(inputfile)
	for r in responselist: ##the regex and string matching in the lines below are far from ideal, but they are getting me pretty close and I don't want to fiddle with it any longer.
		#if subjhead in r:
		if re.search(' '+subjhead, r) or re.search('^'+subjhead, r):
			if subj in r:
				manualresponses.append(r)
			else:
				badresponses.append(r)
		else: manualresponses.append(r)
	return manualresponses, badresponses, inputfile, header 

def write_files(mr, br, i, h): ##manualresponses, badresponses, item number
							   #####I'm currently working in this area; I'm having trouble writing rows correctly. I get one character per cell, or i end up with some responses across multiple cells because the response contains one or more commas...
	#header = ['I'+str(i).zfill(2)+'T', INFItem+'_'+INFFeat2]
	with open('REJECTED_'+str(i).zfill(2), 'w') as bfile:
		bwriter = csv.writer(bfile, dialect=csv.excel)
		bwriter.writerow(h)
		for b in br:
			#print b
			bwriter.writerow([b])
	with open(i, 'w') as mfile:
		mwriter = csv.writer(mfile, dialect=csv.excel)
		mwriter.writerow(h)
		for m in mr:
			#print m
			mwriter.writerow([m])

def main():
	#hour = sys.argv[1]
	hour = '2039'
	for n in range(1,31):
		#get_stats(n, hour)
		manresp, badresp, infi, headerrow = sort_by_subjects(n, hour)
		write_files(manresp, badresp, infi, headerrow)
	# write_type_csv(targeted_outputrows, 'targeted', timestamp)
	# write_type_csv(untargeted_outputrows, 'untargeted', timestamp)
	
if __name__ == "__main__":
    main()
