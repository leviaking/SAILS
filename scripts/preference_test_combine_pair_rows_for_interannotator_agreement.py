#!/usr/bin/env python

import csv


# # inputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs-interannotator_agreement.csv'
inputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/older/ab_test_pairs-interannotator_agreement.csv'
# # outputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs-interannotator_agreement-scores_only.csv'
outputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs-interannotator_agreement-scores_only-2.csv'


def get_all_input_rows(csv_in):
	allrows = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		for mrow in masterreader:
			allrows.append(mrow)
	return allrows


def combine_pair_rows(raw_rows):
	oldheader = raw_rows.pop(0)
	newheader = ["PairNum", "CAGIV-CAGIV", "A1 A Better", "A1 B Better", "A1 Same", "A2 A Better", "A2 B Better", "A2 Same"]
	combined_rows = [newheader]
	while raw_rows:
		a_row = raw_rows.pop(0)
		b_row = raw_rows.pop(0)  ## we don't need to see or use this row, but we need to pop it away
		pairnum = a_row[2][:-2]
		cagiv = a_row[3]
		a1a_better = a_row[4]
		a1a_worse = a_row[5]
		a1a_same = a_row[6]
		combo_row = [pairnum, cagiv]
		if a1a_same == "1":
			a1_extend = ["0", "0", "1"]
		elif a1a_better == "1":
			a1_extend = ["1", "0", "0"]
		elif a1a_worse == "1":
			a1_extend = ["0", "1", "0"]
		else:
			print "THERE'S A PROBLEM WITH "+pairnum
		a2a_better = a_row[7]
		a2a_worse = a_row[8]
		a2a_same = a_row[9]
		combo_row = [pairnum, cagiv]
		if a2a_same == "1":
			a2_extend = ["0", "0", "1"]
			print combo_row
		elif a2a_better == "1":
			a2_extend = ["1", "0", "0"]
		elif a2a_worse == "1":
			a2_extend = ["0", "1", "0"]
		else:
			print "THERE'S A PROBLEM WITH "+pairnum
		combo_row = combo_row+a1_extend+a2_extend
		combined_rows.append(combo_row)
	return combined_rows


def combine_pair_rows_2(raw_rows):
	oldheader = raw_rows.pop(0)
	newheader = ["PairNum", "CAGIV-CAGIV", "A1", "A2"]
	combined_rows = [newheader]
	while raw_rows:
		a_row = raw_rows.pop(0)
		b_row = raw_rows.pop(0)  ## we don't need to see or use this row, but we need to pop it away
		pairnum = a_row[2][:-2]
		cagiv = a_row[3]
		a1a_better = a_row[4]
		a1a_worse = a_row[5]
		a1a_same = a_row[6]
		combo_row = [pairnum, cagiv]
		if a1a_same == "1":
			a1_extend = ["s"]
		elif a1a_better == "1":
			a1_extend = ["a"]
		elif a1a_worse == "1":
			a1_extend = ["b"]
		else:
			print "THERE'S A PROBLEM WITH "+pairnum
		a2a_better = a_row[7]
		a2a_worse = a_row[8]
		a2a_same = a_row[9]
		combo_row = [pairnum, cagiv]
		if a2a_same == "1":
			a2_extend = ["s"]
			print combo_row
		elif a2a_better == "1":
			a2_extend = ["a"]
		elif a2a_worse == "1":
			a2_extend = ["b"]
		else:
			print "THERE'S A PROBLEM WITH "+pairnum
		combo_row = combo_row+a1_extend+a2_extend
		combined_rows.append(combo_row)
	return combined_rows


def write_out_csv(ks):
	cfile = open(outputfilename, 'w')
	cwriter = csv.writer(cfile, dialect=csv.excel)
	for k in ks:
		cwriter.writerow(k)
	cfile.close()


allrows = get_all_input_rows(inputfilename)
# # combined_pair_rows = combine_pair_rows(allrows)
combined_pair_rows = combine_pair_rows_2(allrows)
write_out_csv(combined_pair_rows)

