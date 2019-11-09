#!/usr/bin/env python

## 2019/11/08. LK. This script will run over the "master_anno" files in the corpus folder and assemble a set of pairings, which will then be annotated ("A is better", "B is better", "Same"), and these annotation scores will be used to determine the rate at which each annotation feature correlates with the better response. I will apply this as weighting scheme, by which the responses can be ranked, and this will be used as the "GS" ranking -- let's start calling this the "Gold Ranking" instead. The Gold Ranking will be compared against the TC ranking to get Spearman correlations, which will serve as a measure of the quality of my approach overall as well as the relative quality of each Gold Standard set of responses.


import sys, re, csv, datetime, os, random
from shutil import copyfile

sourcedir=('/Users/leviking/Documents/dissertation/SAILS/corpus/')
outfilename=('/Users/leviking/Documents/dissertation/SAILS/weighting/ab_test_pairs.csv')
i_a_name=('/Users/leviking/Documents/dissertation/SAILS/weighting/ab_test_pairs-inter_annotator.csv')


def get_all_source_filenames():
	## Returns list of all 60 item csvs ("master_anno")
	for stuff in os.walk(sourcedir):
		mystuff=stuff[2]  ##[2] is filename
	mystuff = [m for m in mystuff if "TOY" not in m and m.endswith("csv")]
	mystuff.sort()
	return mystuff


def get_csv_lines(myfile):
	## Reads a csv and returns it as list of rows
	myf = open(sourcedir+myfile, 'rU')
	mycsvreader = csv.reader(myf, dialect=csv.excel)
	cheader = next(mycsvreader, None)
	myclines = []
	for row in mycsvreader:
		myclines.append(row)
	myf.close()
	return cheader, myclines
	
	
def get_response_lines(myfile):
	## Returns a list of the csv lines where the response field contains a response (not empty)
	inheader, allrows = get_csv_lines(myfile)
	outheader = inheader+["PairNum", "CAGIV-CAGIV", "Better", "Worse", "Same"]
	resp_lines = []
	for ar in allrows:
		if ar[13] != '0' and ar[14] in ['0', '1']:  ##ar[14] is first annotation column; some profane responses were not annotated
			resp_lines.append(ar)
		else:
			pass
	return outheader, resp_lines


def get_anno_dict(resp_lines):
	anno_dict = {}
	for rl in resp_lines:
		anno_vector = rl[14]+rl[15]+rl[16]+rl[17]+rl[18]
		if anno_vector not in anno_dict:
			anno_dict[anno_vector]=[rl]
		else:
			anno_dict[anno_vector]+=[rl]
	return anno_dict


def get_anno_counts(anno_dict):
	anno_counts = []
	for al in anno_dict:
		anno_counts.append([len(anno_dict[al]), al])  
	anno_counts.sort()  ## e.g., [[1, 10101], [3, 10000], ...]
	return anno_counts


def get_paired_rows(a_dict):
	a_counts = get_anno_counts(a_dict)
	paired_rows = []
	while len(a_counts) >= 2:  # must be 2 for a pair
		l_ct_anno = a_counts.pop(0)
		l_anno = l_ct_anno[1]  # '10001', etc.
		l_vals_list = a_dict[l_anno]  # all the rows with this annotation vector
		current_vals_ct = len(l_vals_list)
		remaining_annos = len(a_counts)
		# # l_val = l_vals_list.pop(0)  ## initialize -- get the first row to be paired
		if remaining_annos <= current_vals_ct:
			for ac in reversed(a_counts):  ## we iterate in descending order
				l_val = l_vals_list.pop(0)
				r_anno = ac[1]
				r_vals_list = a_dict[r_anno]
				r_val = r_vals_list.pop(0)
				paired_rows.append([l_anno+"-"+r_anno, l_val, r_val])				
		elif remaining_annos > current_vals_ct:
			# # for lv in l_vals_list:
			while l_vals_list:
				l_val = l_vals_list.pop(0)
				r_ct_anno = a_counts.pop(-1)  ## we want to iterate through in descending order -- this will ensure we don't 'use up' all the responses with rarer anno vectors and leave behind a big pile of more common ones
				r_anno = r_ct_anno[1]
				r_vals_list = a_dict[r_anno]
				r_val = r_vals_list.pop(0)
				paired_rows.append([l_anno+"-"+r_anno, l_val, r_val])				
		new_dict = {k: v for k, v in a_dict.items() if v}
		# # print("NEW: ", new_dict)
		a_dict = dict(new_dict)
		a_counts = get_anno_counts(a_dict)
	return paired_rows


def prep_output_rows(filenm, ugly_pairs):
	# takes in 2d list, inner lists are: [l_anno+"-"+r_anno, [l_csv_row], [r_csv_row]]
	# extends left and right rows with a unique pairing number and the annotation pairing
	pretty_rows = []
	itemtag = filenm[:4]
	pairct = 0
	anno_ct_dict = {}
	anno_list = []
	max_pairs = 20
	inter_anno_max = 4  # total, so /2 = max pairs for inter anno
	pretty_inter_anno_rows = []
	random.shuffle(ugly_pairs)  ## randomize so we get a fair sample of pairings
	while ugly_pairs and pairct < max_pairs:
		# # for ug in ugly_pairs:
		ug = ugly_pairs.pop(0)
		if "00000" in ug[0]:  # most "00000" is garbage and not informative
			pass
		elif ug[0] in anno_ct_dict:
			pass  ## this ensures we only take unique anno pairs (for each item)
		elif ug[0].split("-")[1]+"-"+ug[0].split("-")[0] in anno_ct_dict:
			pass  ## for anno pair "A-B", screen also for "B-A"
		else:
			pairct += 1
			pairstr = str(pairct).zfill(3)
			pairnum = itemtag+"-"+pairstr
			anno = ug[0]
			if anno not in anno_ct_dict:
				anno_ct_dict[anno] = 1
			else:
				anno_ct_dict[anno] += 1
			lrow = ug[1]+[pairnum+"-a", anno]
			rrow = ug[2]+[pairnum+"-b", anno]
			pretty_rows.append(lrow)
			pretty_rows.append(rrow)
			if pairct <= (inter_anno_max/2) :
				pretty_inter_anno_rows.append(lrow)
				pretty_inter_anno_rows.append(rrow)
	for key in anno_ct_dict:
		anno_list.append([anno_ct_dict[key], key])
	anno_list.sort()
	print "\n\n"+itemtag
	for anno_ct in anno_list:
		print anno_ct
	return pretty_rows, pretty_inter_anno_rows
	pass


def get_item_samples(myfile):
	outheader, resp_lines = get_response_lines(myfile)
	anno_dict = get_anno_dict(resp_lines)
	raw_pairs = get_paired_rows(anno_dict)
	writeable_rows, inter_anno_rows = prep_output_rows(myfile, raw_pairs)
	return outheader, writeable_rows, inter_anno_rows


def write_my_csv(outname, outhead, outrows):
	thisfile=open(outname, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	thiswriter.writerow(outhead)
	for outr in outrows:
		thiswriter.writerow(outr)
	thisfile.close()


def main():
	sourcefilenames = get_all_source_filenames()
	outputrows = []
	i_a_outputrows = []
	for sfn in sourcefilenames:
		outheader, good_rows, i_a_rows = get_item_samples(sfn)
		for gr in good_rows:
			outputrows.append(gr)
		for iar in i_a_rows:
			i_a_outputrows.append(iar)
	write_my_csv(outfilename, outheader, outputrows)
	write_my_csv(i_a_name, outheader, i_a_outputrows)
	

if __name__ == "__main__":
	main()

