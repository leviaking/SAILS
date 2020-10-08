#!/usr/bin/env python

## July 2020; This script needs to construct training sets based on parameter combinations

import sys, csv
from os import walk


intrans=['01', '04', '07', '10', '13', '18', '20', '24', '27', '30']
trans=['02', '06', '09', '12', '15', '16', '19', '22', '25', '29']
ditrans=['03', '05', '08', '11', '14', '17', '21', '23', '26', '28']


items=[str(x).zfill(2) for x in range(1,31)]
targeting=["T", "U"]
deps=['ldh', 'xdh', 'xdx']
sources=['gNSF', 'gNSC']
first_second=['r1', 'r2']


def get_sets_dict():
	all_sets = {}
	for  item in items:
		if item in intrans:
			tran = "In"
		elif item in trans:
			tran = "Tr"
		elif item in ditrans:
			tran = "Di"
		else:
			pass
		for source in sources:
			for fs in first_second:
				for trg in targeting:
					all_sets["-".join(["I"+item+trg, source, fs, tran])]=[]
	return all_sets


def get_infile_names(somedir): 
	docnames = []
	for (dirpath, dirnames, filenames) in walk(somedir+"pool/"):
		docnames.extend(filenames)
		break
	docnames = [dn for dn in docnames if "training_pool" in dn]
	docnames.sort()
	return docnames


def get_source_rows(tdf): ## tdf ~= test doc file; returns csv lines as lists
# input header:
# ResponseID	Response	Core	Answer	Gramm	Interp	Verif	parse	ldh	xdh	xdx	ldh TC weighted	xdh TC weighted	xdx TC weighted	ldh TC unweighted	xdh TC unweighted	xdx TC unweighted
# scores are row[11] thru row[16]
	everything=[]
	tdoc=open(tdf, 'rU')
	tdocreader=csv.reader(tdoc, dialect=csv.excel)
	skipheader=next(tdocreader, None)
	for row in tdocreader:
		everything.append(row)
	tdoc.close()
	return skipheader, everything


def get_sets(pool, sets_dict):
	for row in pool:
		rid = row[0]
		rid = rid.split("-")
		myitem = rid[0]
		mysource = rid[1]
		my_first_second = rid[3]
		rlabels = [myitem, mysource, my_first_second]
		rlab = "-".join(rlabels)
		for st in sets_dict:
			if rlab == st[:-3]:
				sets_dict[st]+=[row]
	return sets_dict


def write_output(hd, rs, nm):
	thisfile=open(nm, 'w')
	thiswriter=csv.writer(thisfile, dialect=csv.excel)
	thiswriter.writerow(hd)
	for r in rs:
		thiswriter.writerow(r)
	thisfile.close()


def write_sets(hd, srcdir, srd):
	for k in srd:
		knm = srcdir+"sets/"+k+"-training_pool.csv"
		write_output(hd, srd[k], knm)
		if "gNSC" in k:
			if "r1" in k:
				r1sample = srd[k][:50]
				r2r1sample = srd[k][:25]
				r2k = k.replace("r1", "r2")
				r2r2sample = srd[r2k][:25]
				r2sample = r2r1sample+r2r2sample
				r1nm = srcdir+'N50/'+k+'-N50.csv'
				r2nm = srcdir+'N50/'+r2k+'-N50.csv'
				write_output(hd, r1sample, r1nm)
				write_output(hd, r2sample, r2nm)
			else:
				pass


def report_counts(srd):
	tally = []
	for k in srd:
		tally.append([len(srd[k]), k])
	tally.sort()
	print("responses per set: ")
	for ta in tally:
		print(ta[0], ta[1])


def main():
	mysets_dict = get_sets_dict()
	print("total number of sets: "+str(len(mysets_dict)))
	sourcedir=('/Users/leviking/Documents/dissertation/SAILS/training_data/')
	input_files = get_infile_names(sourcedir)
	resp_rows = []
	for inp in input_files:
		header, new_source_rows = get_source_rows(sourcedir+"pool/"+inp)
		resp_rows += new_source_rows
	set_row_dict=get_sets(resp_rows, mysets_dict)
	report_counts(set_row_dict)
	write_sets(header, sourcedir, set_row_dict)


if __name__ == "__main__":
    main()
