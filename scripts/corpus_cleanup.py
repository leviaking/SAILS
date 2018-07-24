#!/usr/bin/env python

import sys, re, csv, datetime, os
from shutil import copyfile

all_file_ids=[]
all_file_ids_dict={} ##{'i01T': [[x], [x]...] ...} #each '[x]' is a list of the first 11 columns (the demographic info) from corpus respondents; it begins with Respondentid
t_v_u_uniques={}
master_demographics=[] ## this will be a flat list of every demographic row contained in any file of the corpus


##this constructs all_file_ids and all_file_ids_dict;
def get_file_respondents():
	for n in range(1,31):
		for v in ['T', 'U']:
			file_id='I'+str(n).zfill(2)+v
			all_file_ids.append(file_id)
			file_demographics=[] ##this is the first 11 columns of the file, starting with Respondentid
			myfile=open('../sails/corpus/'+file_id+'_master_anno.csv', 'rU')
			myreader=csv.reader(myfile, dialect=csv.excel)
			skip_header=next(myreader, None)
			for row in myreader:
				if row not in file_demographics:
					file_demographics.append(row[0:11])
				else:
					pass
			all_file_ids_dict[file_id]=file_demographics
			for fd in file_demographics:
				if fd not in master_demographics:
					master_demographics.append(fd)
	#print len(master_demographics)
	

##I need to see if there are any cases where a Respondentid appears in different places with non-identical demographic fields. Here's a function for that.
def check_demographic_consistency():
	total_mismatches=0
	all_demographics=[] ##first, get a set of all unique demographic rows from all files. (we'll check each file's demographic rows against this master list, which includes that current file's own demographic rows, because a respondent could theoretically have two non-identical demograhpic rows within a single file)
	for file_id in all_file_ids:
		all_demographics+=all_file_ids_dict[file_id]
	#print all_demographics, '\n\n\n\n\n\n\n'
	all_respondents=[l[0] for l in all_demographics]
	#print all_respondents
	all_respondents=list(set(all_respondents))
	all_respondents.sort()
	for file_id in all_file_ids:  ##now we iterate through each file
		file_demographics=[]
		temp_file_demographics=all_file_ids_dict[file_id]
		for demo in temp_file_demographics: ##removing duplicates here
			if demo not in file_demographics:
				file_demographics.append(demo)
		file_respondents=[i[0] for i in file_demographics]
		file_respondents=list(set(file_respondents)) ##get a list of *unique* respondents (remove duplicates)
		for td in file_demographics:
			test_id=td[0]
			for sd in all_demographics:
				some_id=sd[0]
				if some_id==test_id:
					if sd==td:
						pass
					else:
						total_mismatches+=1
						print 'Mismatch: '+file_id
						print td
						print sd
						print '\n\n'
	print "TOTAL Mismatches: "+str(total_mismatches)


def check_template_response_ids(): ##i have merged the demographic info into a single template for each file; i.e., the first 11 columns contain identical entries for all files. now I want to make sure that the Responseid column is indeed identical across all files. If so, I plan to replace the long RespondentIDs with a shorter id.
	all_respondents_dict={}
	match_count=1
	for file_id in all_file_ids:
		respondents=[]
		myfile=open('../corpus/'+file_id+'_master_anno.csv', 'rU')
		myreader=csv.reader(myfile, dialect=csv.excel)
		skip_header=next(myreader, None)
		for row in myreader:
			respondents.append(row[0])
		myfile.close()
		all_respondents_dict[file_id]=respondents
	for fi in all_file_ids:
		test_respondent_ids=all_respondents_dict[fi]
		for other_id in all_file_ids:
			if other_id == fi:
				pass
			else:
				other_respondent_ids=all_respondents_dict[other_id]
				if test_respondent_ids != other_respondent_ids:
					print 'Mismatch: '+fi+' '+other_id
				else:
					print 'Match: '+fi+' '+other_id+' '+str(match_count)
					match_count+=1

def renumber_respondents(): ##I have checked and double-checked that all files contain an identical first 11 columns. Now it is safe to blindly renumber the RespondentIDs (column 0) from 001-498.
	for file_id in all_file_ids:
		new_id=1
		step_up=0
		outrows=[]
		myfile=open('../corpus/'+file_id+'_master_anno.csv', 'rU')
		myreader=csv.reader(myfile, dialect=csv.excel)
		skip_header=next(myreader, None)
		for row in myreader:
			outrows.append(row)
		myfile.close()
		outfile=open('../corpus/'+file_id+'_renum.csv', 'w')
		outwriter=csv.writer(outfile, dialect=csv.excel)
		outwriter.writerow(skip_header)
		for outr in outrows:
			new_id_str=str(new_id).zfill(3)
			outr[0]=new_id_str
			outwriter.writerow(outr)
			if step_up==1:
				new_id+=1
				step_up=0
			elif step_up==0:
				step_up+=1
		outfile.close()
		
def change_ResponseID_to_Participant(): ##I'm simply changing "ResponseID" to "Participant" in the header of each file. This is because I'm going to add a unique ID to each response, and I want to have separate abbreviations to indicate "Participant" and "Response" (vs. "Respondent" and "Response"; see "def insert_response_id()")
	for file_id in all_file_ids:
		myfile=open('../corpus/'+file_id+'_master_anno.csv', 'rU')
		myreader=csv.reader(myfile, dialect=csv.excel)
		header=next(myreader, None)
		header[0]='Participant'
		outfile=open('../corpus/'+file_id+'_participant.csv', 'w')
		outwriter=csv.writer(outfile, dialect=csv.excel)
		outwriter.writerow(header)
		for row in myreader:
			outwriter.writerow(row)
		myfile.close()
		outfile.close()


def insert_response_id(): ##This function will insert a unique response ID to each response (even blank responses). This ID will be: i<item>-g<group>-p<participant>-r<response>, where: item is 01-30 + T or U; group is NNS (non-native speaker) or NSC (native speaker crowdsourced) or NSF (native speaker familiar); participant is the participant number, 001-498; and response is 1 or 2, for first or second response. So a response ID might look like: i03T-gNNS-p355-r1 or i29U-gNSC-p041-r2 etc.
	for file_id in all_file_ids:
		myfile=open('../sails/corpus/'+file_id+'_master_anno.csv', 'rU')
		myreader=csv.reader(myfile, dialect=csv.excel)
		header=next(myreader, None)
		#header.insert(12, 'ResponseID') ##commented this out because I'm running this a second time on some files
		outfile=open('../sails/corpus/'+file_id+'_ResponseID.csv', 'w')
		outwriter=csv.writer(outfile, dialect=csv.excel)
		outwriter.writerow(header)
		for row in myreader:
			dummy=row.pop(12) ##added this because i'm running the script on some files a second time and need to remove the old (faulty) ResponseIDs
			item=file_id
			source=row[2]
			if source=='NNSv1' or source=='NNSv2':
				group='gNNS'
			elif source=='NSv1pt1' or source=='NSv1pt2' or source=='NSv2pt1' or source=='NSv2pt2':
				group='gNSC'
			elif source=='NSv1' or source=='NSv2':
				group='gNSF'
			else: pass
			participant='p'+str(row[0]).zfill(3)
			response='r'+row[11]
			response_id='-'.join([item, group, participant, response])
			row.insert(12, response_id)
			outwriter.writerow(row)
		myfile.close()
		outfile.close()

		

def rewrite_files_using_master_demographics():
	for n in range(1,31):
		for v in ['T', 'U']:
			current_rows=[]
			outrows=[]
			file_id='I'+str(n).zfill(2)+v
			myfile=open('../corpus/'+file_id+'_master_anno.csv', 'rU')
			myreader=csv.reader(myfile, dialect=csv.excel)
			skip_header=next(myreader, None)
			outfile=open('../corpus/'+file_id+'_rev2.csv', 'w')
			outwriter=csv.writer(outfile, dialect=csv.excel)
			outwriter.writerow(skip_header)
			for row in myreader:
				current_rows.append(row)
			myfile.close()
			outrows=list(current_rows)
			for md in master_demographics:
				found=0
				for cr in current_rows:
					if md[:11]==cr[:11]:
						found=1
						break
					else:
						pass
				if found==1: ##the demographic entry in master_demographics already exists in current file, so do nothing
					pass
				elif found==0: ##demographic entry in master_demographics isn't found in the current file, so we need to add it to the current file, with empty fields for the response info; note that we add it twice, for response 1 and response 2
					dummy1=md+['1', '0', '', '', '', '', '', '', '', '', '', '']
					dummy2=md+['2', '0', '', '', '', '', '', '', '', '', '', '']
					outrows.append(dummy1)
					outrows.append(dummy2)
			outrows.sort()
			for row in outrows:
				outwriter.writerow(row)
			outfile.close()


def csv_reviser(): ##This function is used to find and replace particular inconsistencies in the demographic info of the corpus.
	for n in range(1,31):
		for v in ['T', 'U']:
			file_id='I'+str(n).zfill(2)+v
			myfile=open('../corpus/'+file_id+'_master_anno.csv', 'rU')
			myreader=csv.reader(myfile, dialect=csv.excel)
			skip_header=next(myreader, None)
			outfile=open('../corpus/'+file_id+'_rev1.csv', 'w')
			outwriter=csv.writer(outfile, dialect=csv.excel)
			outwriter.writerow(skip_header)
			for row in myreader:
				# if row[6]=='Beijing': ##give the index of the column you wish to replace, and the content you want to replace with something else
				# 	row[6]='China' ##give the same index and the new content you wish to replace the old content with
				# else:
				# 	pass
				element=row[10] ##element is the content of the column in question; we want to check element for some substring, and replace that substring if found; give the index of the column you wish to check
				if 'mouths' in element:  ##give the substring you are looking to replace
					newelement=element.replace('mouths', 'months') ##give the old substring and the new substring
					row[10]=newelement ##put the element back where it belongs in the list, but now with the correct substring
				else:
					pass
				outwriter.writerow(row)
			myfile.close()
			outfile.close()
	

def sort_unique_respondents(): ##for each file, this checks that file's respondents against every other file's respondents to find any respondents that only appear in the given file
	for file_id in all_file_ids:
		unique_respondents=[]
		respondents=[item[0] for item in all_file_ids_dict[file_id]]
		all_other_respondents=[]
		#for r_id in respondents:
		for other_file_id in all_file_ids:
			if other_file_id == file_id:
				pass
			else:
				#all_other_respondents+=all_file_ids_dict[other_file_id]
				all_other_respondents+=[i[0] for i in all_file_ids_dict[other_file_id]]
		for r in respondents:
			if r not in all_other_respondents:
				unique_respondents.append(r)
			else: pass
		print file_id
		for ur in unique_respondents:
			print ur
		
def sort_T_vs_U_respondents(): ##for each file, this checks that file's respondents against its targeted or untarged counterpart file's respondents to find any respondents that appear in the given file but not in the counterpart file
	for file_id in all_file_ids:
		unique_respondents=[]
		respondents=[item[0] for item in all_file_ids_dict[file_id]]
		all_other_respondents=[]
		#for r_id in respondents:
		this_V=file_id[-1]
		if this_V=='T':
			other_file_id=file_id[:-1]+'U'
		elif this_V=='U':
			other_file_id=file_id[:-1]+'T'
		else: pass
		other_respondents=[i[0] for i in all_file_ids_dict[other_file_id]]
		
		for r in respondents:
			if r not in other_respondents:
				unique_respondents.append(r)
			else: pass
		t_v_u_uniques[file_id]=unique_respondents
		# print '\n\n'+file_id
		# for ur in unique_respondents:
		# 	print ur

def print_T_vs_U_stuff(): ##for each file, this takes the list of respondent ids present in the given file but not in its T or U counterpart; it compares that list against all the other files of the same version (a T file is compared against all other T files, a U file is compared against all other U files) to find respondent ids that only occur in the given file; at this point, there are none. So that means that all T files have identical respondents, and all U files have identical respondents, but there are some respondents that appear in all T files and no U files, and vice versa.
	for file_id in all_file_ids:
		current_unique_ids=[]
		all_other_respondents=[]
		this_V=file_id[-1]
		if this_V=='T':
			for other_file_id in all_file_ids:
				if other_file_id != file_id and other_file_id[-1]=='T':
					all_other_respondents+=[item[0] for item in all_file_ids_dict[other_file_id]]
		elif this_V=='U':
			for other_file_id in all_file_ids:
				if other_file_id != file_id and other_file_id[-1]=='U':
					all_other_respondents+=[k[0] for k in all_file_ids_dict[other_file_id]]
		else: pass
		for r_id in all_file_ids_dict[file_id]:
			if r_id[0] not in all_other_respondents:
				#print file_id, r_id
				current_unique_ids.append(r_id[0])
			else: pass
		current_unique_ids.sort()
		print current_unique_ids
	

def main():
	get_file_respondents()
	insert_response_id()
	#change_ResponseID_to_Participant()
	#renumber_respondents()
	#check_template_response_ids()
	#rewrite_files_using_master_demographics()
	#check_demographic_consistency()


if __name__ == "__main__":
    main()