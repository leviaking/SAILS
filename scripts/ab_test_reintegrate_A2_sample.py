#!/usr/bin/env python

import csv


inputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs_for_A2-TEMP-A2.csv'
outputfilename = '/Users/leviking/Documents/dissertation/SAILS/weighting_features/ab_test_pairs_for_A2_spaced.csv'


def get_all_input_rows(csv_in):
	allrows = []
	with open(csv_in, 'rU') as masterfile:
		masterreader = csv.reader(masterfile, dialect=csv.excel)
		for mrow in masterreader:
			allrows.append(mrow)
	return allrows


def write_spaced_file(ks):
	cfile = open(outputfilename, 'w')
	cwriter = csv.writer(cfile, dialect=csv.excel)
	header = ks.pop(0)
	cwriter.writerow(header)
	dummy = ["dummy", "", "", ""]
	while ks:
		ra = ks.pop(0)
		rb = ks.pop(0)
		cwriter.writerow(ra)
		cwriter.writerow(rb)
		cwriter.writerow(dummy)
		cwriter.writerow(dummy)
		cwriter.writerow(dummy)
		cwriter.writerow(dummy)
		cwriter.writerow(dummy)
		cwriter.writerow(dummy)
	cfile.close()


allrows = get_all_input_rows(inputfilename)
write_spaced_file(allrows)

