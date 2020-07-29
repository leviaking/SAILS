#!/usr/bin/env python

import csv


inputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs-LKfull-annotated.csv'
outputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs_for_A2.csv'


def get_all_input_rows(csv_in):
	allrows = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		for mrow in masterreader:
			allrows.append(mrow)
	return allrows


def select_sample_rows(allrows):
	header = allrows.pop(0)
	keepers = [header]
	keep_nums = ["004", "008", "012", "016", "020"]
	for row in allrows:
		this_num = row[24].split("-")[1]
		if this_num in keep_nums:
			keepers.append(row)
	return keepers


def write_sample_file(ks):
	cfile = open(outputfilename, 'w')
	cwriter = csv.writer(cfile, dialect=csv.excel)
	for k in ks:
		cwriter.writerow(k)
	cfile.close()


allrows = get_all_input_rows(inputfilename)
keepers = select_sample_rows(allrows)
write_sample_file(keepers)

