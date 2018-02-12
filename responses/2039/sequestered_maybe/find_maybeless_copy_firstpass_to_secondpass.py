#!/usr/bin/env python

from shutil import copyfile


inlist='''Answer/secondpassanno_I01T_Answer-2039.csv	Answer/secondpassanno_I14T_Answer-2039.csv
Answer/secondpassanno_I01U_Answer-2039.csv	Answer/secondpassanno_I14U_Answer-2039.csv
Answer/secondpassanno_I02T_Answer-2039.csv	Answer/secondpassanno_I15U_Answer-2039.csv
Answer/secondpassanno_I02U_Answer-2039.csv	Answer/secondpassanno_I16U_Answer-2039.csv
Answer/secondpassanno_I03T_Answer-2039.csv	Answer/secondpassanno_I18U_Answer-2039.csv
Answer/secondpassanno_I03U_Answer-2039.csv	Answer/secondpassanno_I19T_Answer-2039.csv
Answer/secondpassanno_I04T_Answer-2039.csv	Answer/secondpassanno_I19U_Answer-2039.csv
Answer/secondpassanno_I04U_Answer-2039.csv	Answer/secondpassanno_I20U_Answer-2039.csv
Answer/secondpassanno_I05T_Answer-2039.csv	Answer/secondpassanno_I21T_Answer-2039.csv
Answer/secondpassanno_I05U_Answer-2039.csv	Answer/secondpassanno_I21U_Answer-2039.csv
Answer/secondpassanno_I06T_Answer-2039.csv	Answer/secondpassanno_I22T_Answer-2039.csv
Answer/secondpassanno_I06U_Answer-2039.csv	Answer/secondpassanno_I23T_Answer-2039.csv
Answer/secondpassanno_I07T_Answer-2039.csv	Answer/secondpassanno_I23U_Answer-2039.csv
Answer/secondpassanno_I07U_Answer-2039.csv	Answer/secondpassanno_I24T_Answer-2039.csv
Answer/secondpassanno_I08T_Answer-2039.csv	Answer/secondpassanno_I24U_Answer-2039.csv
Answer/secondpassanno_I08U_Answer-2039.csv	Answer/secondpassanno_I27T_Answer-2039.csv
Answer/secondpassanno_I09T_Answer-2039.csv	Answer/secondpassanno_I28T_Answer-2039.csv
Answer/secondpassanno_I09U_Answer-2039.csv	Answer/secondpassanno_I29T_Answer-2039.csv'''
inlist=inlist.split('\n')
items=[]
for il in inlist:
	items+=il.split()
#print items

itemnums=[]
for item in items:
	itemnums.append(item[23:26])

missing=[]
for n in range(1,31):
	tn=str(n).zfill(2)+'T'
	un=str(n).zfill(2)+'U'
	if tn not in itemnums:
		missing.append(tn)
	if un not in itemnums:
		missing.append(un)

#print missing

for m in missing:
	sourcename='Answer/firstpassanno_I'+m+'_Answer-2039.csv'
	destname='Answer/secondpassanno_I'+m+'_Answer-2039.csv'
	copyfile(sourcename, destname)


# >>> fns=[]
# >>> for n in range(1,31):
# ...     tn=str(n).zfill(2)+'T'
# ...     un=str(n).zfill(2)+'U'
# ...     if not tn in fns: fns.append(tn)
# ...     if not un in fns: fns.append(un)
# ... 
# >>> fns.sort()
# >>> fns=list(set(fns))
# >>> fns
