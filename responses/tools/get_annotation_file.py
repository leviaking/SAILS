#!/usr/bin/env python

##LK: This script takes the "combined_master.csv" file and condenses the sentence tokens into sentence types. This is so that we can do manual annotation on the types, then apply those annotations back to all sentence tokens; i.e., it's for saving labor.

##USAGE:
##python get_annotation_file.py combined_master.csv

##the output file will be called "annotation_file_<date>.csv"

##LK: Note that any CSV files produced in Excel must be saved as WINDOWS csv in Excel in order to work smoothly with this script!

import sys, re, csv, datetime, os

def get_timestamp():
	timestuff = datetime.datetime.now()
	timelist = [str(timestuff.year), str(timestuff.month).zfill(2), str(timestuff.day).zfill(2), str(timestuff.hour).zfill(2), str(timestuff.minute).zfill(2)]
	hourlist = [str(timestuff.hour).zfill(2), str(timestuff.minute).zfill(2)]
	ts = ''.join(timelist)
	hour = ''.join(hourlist)
	return ts, hour

def make_output_directory(timestamp):
	os.mkdir(timestamp)

def get_allrows(csv_in):
	allrows = []
	with open(csv_in, 'r') as masterfile:
		masterreader = csv.reader(masterfile)
		mheader1 = next(masterreader, None)
		mheader2 = next(masterreader, None)
		for mrow in masterreader:
			allrows.append(mrow)
	return allrows

def get_itemnames():
	tnames = []
	unames = []
	for itemn in range(1,31):
	#for itemn in [1,2,3,11]:
		tnames.append('I'+str(itemn).zfill(2)+'T')
		unames.append('I'+str(itemn).zfill(2)+'U')
	return tnames, unames

def get_responsetypes(rows, tnms, unms):
	# alltdicts=[]
	# alludicts=[]
	typedict={}
	tcolumn_add=11 ##column 11 is the first containing targeted responses
	ucolumn_add=71 ##column 71 is the first containing untargeted responses
	tns=list(tnms)
	tns.sort()
	uns=list(unms)
	uns.sort()
	# print tns
	# print uns
	#typecounts=[]
	while tns:
		currt=tns.pop(0)
		currtindex=int(currt[1:3])
		curru=uns.pop(0)
		curruindex=int(curru[1:3])
		currboth=currt[:-1]
		currtresponses = []
		curruresponses = []
		currbothresponses=[]
		tcolumn = (currtindex - 1) * 2 + tcolumn_add
		ucolumn = (curruindex - 1) * 2 + ucolumn_add
		for r in rows:
			tresp1=r[tcolumn]
			tresp1normal=' '.join(tresp1.split())
			tresp1normal=tresp1normal.strip(' .!')
			tresp1normal=tresp1normal.lower()
			tresp2=r[tcolumn+1]
			tresp2normal=' '.join(tresp2.split())
			tresp2normal=tresp2normal.strip(' .!')
			tresp2normal=tresp2normal.lower()
			uresp1=r[ucolumn]
			uresp1normal=' '.join(uresp1.split())
			uresp1normal=uresp1normal.strip(' .!')
			uresp1normal=uresp1normal.lower()
			uresp2=r[ucolumn+1]
			uresp2normal=' '.join(uresp2.split())
			uresp2normal=uresp2normal.strip(' .!')
			uresp2normal=uresp2normal.lower()
			if tresp1!='0':
				if tresp1normal not in currtresponses:
					currtresponses.append(tresp1normal)
				if tresp1normal not in currbothresponses:
					currbothresponses.append(tresp1normal)
			if tresp2!='0':
				if tresp2normal not in currtresponses:
					currtresponses.append(tresp2normal)
				if tresp2normal not in currbothresponses:
					currbothresponses.append(tresp2normal)
			if uresp1!='0':
				if uresp1normal not in curruresponses:
					curruresponses.append(uresp1normal)
				if uresp1normal not in currbothresponses:
					currbothresponses.append(uresp1normal)
			if uresp2!='0':
				if uresp2normal not in curruresponses:
					curruresponses.append(uresp2normal)
				if uresp2normal not in currbothresponses:
					currbothresponses.append(uresp2normal)
		#typecounts.append(len(currtresponses))
		#typecounts.append(len(curruresponses))
		typedict[currt]=currtresponses
		tcolumn+=2
		typedict[curru]=curruresponses
		ucolumn+=2
		typedict[currboth]=currbothresponses
	#typecounts.sort()
	# print typecounts[0], typecounts[-1]
	# print typedict['I15U']
	return typedict

def write_type_csv(orows, prefix, timestamp):
	with open(timestamp+'/annotat_'+prefix+'-'+timestamp+'.csv', 'wb') as cfile:
		cwriter = csv.writer(cfile)
		for o in orows:
			cwriter.writerow(o)

def write_targeted_csvs(t, orows, timestamp, hr):
	with open(timestamp+'/'+t+'_Interp-'+hr+'.csv', 'wb') as tfile:
		twriter = csv.writer(tfile)
		twriter.writerow([t, t+' Interp'])
		for o in orows:
			#print o
			twriter.writerow(o)	
	with open(timestamp+'/'+t+'_Core-'+hr+'.csv', 'wb') as tfile:
		twriter = csv.writer(tfile)
		twriter.writerow([t, t+' Core'])
		for o in orows:
			#print o
			twriter.writerow(o)
	with open(timestamp+'/'+t+'_Verif-'+hr+'.csv', 'wb') as tfile:
		twriter = csv.writer(tfile)
		twriter.writerow([t, t+' Verif'])
		for o in orows:
			#print o
			twriter.writerow(o)
	with open(timestamp+'/'+t+'_Answer-'+hr+'.csv', 'wb') as tfile:
		twriter = csv.writer(tfile)
		twriter.writerow([t, t+' Answer'])
		for o in orows:
			#print o
			twriter.writerow(o)

def write_untargeted_csvs(u, orows, timestamp, hr):
	with open(timestamp+'/'+u+'_Interp-'+hr+'.csv', 'wb') as ufile:
		uwriter = csv.writer(ufile)
		uwriter.writerow([u, u+' Interp'])
		for o in orows:
			#print o
			uwriter.writerow(o)
	with open(timestamp+'/'+u+'_Core-'+hr+'.csv', 'wb') as ufile:
		uwriter = csv.writer(ufile)
		uwriter.writerow([u, u+' Core'])
		for o in orows:
			#print o
			uwriter.writerow(o)
	with open(timestamp+'/'+u+'_Verif-'+hr+'.csv', 'wb') as ufile:
		uwriter = csv.writer(ufile)
		uwriter.writerow([u, u+' Verif'])
		for o in orows:
			#print o
			uwriter.writerow(o)
	with open(timestamp+'/'+u+'_Answer-'+hr+'.csv', 'wb') as ufile:
		uwriter = csv.writer(ufile)
		uwriter.writerow([u, u+' Answer'])
		for o in orows:
			#print o
			uwriter.writerow(o)
			
def write_combined_csvs(c, orows, timestamp, hr):
	with open(timestamp+'/'+c+'TU_Gramm-'+hr+'.csv', 'wb') as cfile:
		cwriter = csv.writer(cfile)
		cwriter.writerow([c, c+' Gramm'])
		for o in orows:
			cwriter.writerow(o)
	with open(timestamp+'/'+c+'TU_Nativ-'+hr+'.csv', 'wb') as cfile:
		cwriter = csv.writer(cfile)
		cwriter.writerow([c, c+' Nativ'])
		for o in orows:
			cwriter.writerow(o)

def create_annotation_sheets(rd, t, tst, hr):
	c = t[:-1]
	u = t[:-1]+'U'
	crows = construct_combined_rows(rd, c)
	write_combined_csvs(c, crows, tst, hr)
	trows = construct_targeted_rows(rd, t)
	#print trows
	write_targeted_csvs(t, trows, tst, hr)
	urows = construct_untargeted_rows(rd, u)
	write_untargeted_csvs(u, urows, tst, hr)

def construct_combined_rows(rd, c):
	csheet=[]
	rdc = list(rd[c])
	while rdc:
		currentrow=[]
		l=rdc.pop(0)
		currentrow.append(l)
		currentrow.append('')
		csheet.append(currentrow)
	return csheet
			
def construct_targeted_rows(fd, t):
	tsheet=[]
	fdt = list(fd[t])
	while fdt:
		currentrow=[]
		m=fdt.pop(0)
		currentrow.append(m)
		currentrow.append('')
		tsheet.append(currentrow)
	return tsheet

def construct_untargeted_rows(fd, u):
	usheet = []
	fdu = list(fd[u])
	while fdu:
		currentrow=[]
		p=fdu.pop(0)
		currentrow.append(p)
		currentrow.append('')
		usheet.append(currentrow)
	return usheet


def main():
	timestamp, hour = get_timestamp() ##hour is a 4 digit number (hour + minute); this is included in file names primarily to avoid overwriting existing annotation if this script is run again at a later time.
	make_output_directory(timestamp)
	allrows=get_allrows(sys.argv[1])
	tnames, unames=get_itemnames()
	rtypesdict=get_responsetypes(allrows,tnames,unames)
	for tt in tnames:
	 	create_annotation_sheets(rtypesdict, tt, timestamp, hour)

if __name__ == "__main__":
    main()
