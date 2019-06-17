#!/usr/bin/env python

import sys, re, csv, datetime, os

outfilenames = ['I01T_merged_anno.csv', 'I01U_merged_anno.csv', 'I02T_merged_anno.csv', 'I02U_merged_anno.csv', 'I03T_merged_anno.csv', 'I03U_merged_anno.csv', 'I04T_merged_anno.csv', 'I04U_merged_anno.csv', 'I05T_merged_anno.csv', 'I05U_merged_anno.csv', 'I06T_merged_anno.csv', 'I06U_merged_anno.csv', 'I07T_merged_anno.csv', 'I07U_merged_anno.csv', 'I08T_merged_anno.csv', 'I08U_merged_anno.csv', 'I09T_merged_anno.csv', 'I09U_merged_anno.csv', 'I10T_merged_anno.csv', 'I10U_merged_anno.csv', 'I11T_merged_anno.csv', 'I11U_merged_anno.csv', 'I12T_merged_anno.csv', 'I12U_merged_anno.csv', 'I13T_merged_anno.csv', 'I13U_merged_anno.csv', 'I14T_merged_anno.csv', 'I14U_merged_anno.csv', 'I15T_merged_anno.csv', 'I15U_merged_anno.csv', 'I16T_merged_anno.csv', 'I16U_merged_anno.csv', 'I17T_merged_anno.csv', 'I17U_merged_anno.csv', 'I18T_merged_anno.csv', 'I18U_merged_anno.csv', 'I19T_merged_anno.csv', 'I19U_merged_anno.csv', 'I20T_merged_anno.csv', 'I20U_merged_anno.csv', 'I21T_merged_anno.csv', 'I21U_merged_anno.csv', 'I22T_merged_anno.csv', 'I22U_merged_anno.csv', 'I23T_merged_anno.csv', 'I23U_merged_anno.csv', 'I24T_merged_anno.csv', 'I24U_merged_anno.csv', 'I25T_merged_anno.csv', 'I25U_merged_anno.csv', 'I26T_merged_anno.csv', 'I26U_merged_anno.csv', 'I27T_merged_anno.csv', 'I27U_merged_anno.csv', 'I28T_merged_anno.csv', 'I28U_merged_anno.csv', 'I29T_merged_anno.csv', 'I29U_merged_anno.csv', 'I30T_merged_anno.csv', 'I30U_merged_anno.csv']

for ofn in outfilenames:
	
	pass

def get_inputs():
	pass

def main():
	pass
	# timestamp, hour = get_timestamp() ##hour is a 4 digit number (hour + minute); this is included in file names primarily to avoid overwriting existing annotation if this script is run again at a later time.
	# make_output_directory(timestamp)
	# allrows=get_allrows(sys.argv[1])
	# tnames, unames=get_itemnames()
	# rtypesdict=get_responsetypes(allrows,tnames,unames)
	# for tt in tnames:
	#  	create_annotation_sheets(rtypesdict, tt, timestamp, hour)

if __name__ == "__main__":
    main()
