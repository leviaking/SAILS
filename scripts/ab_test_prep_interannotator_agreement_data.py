#!/usr/bin/env python

import csv


inputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs-interannotator_agreement-raw.csv'
outputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs-interannotator_agreement.csv'


def get_all_input_rows(csv_in):
	allrows = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		for mrow in masterreader:
			allrows.append(mrow)
	return allrows


def write_only_populated_lines(ks):
	cfile = open(outputfilename, 'w')
	cwriter = csv.writer(cfile, dialect=csv.excel)
	for k in ks:
		if k[7]:
			cwriter.writerow(k)
	cfile.close()


allrows = get_all_input_rows(inputfilename)
write_only_populated_lines(allrows)

