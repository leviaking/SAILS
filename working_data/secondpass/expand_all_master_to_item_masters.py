#!/usr/bin/env python

import sys, csv, itertools, os
from shutil import copyfile

##This is probably the ugliest script I've ever written, but I only need it once, so fast and dirty it is!

ufilename='SAILS_untargeted_master.csv'
tfilename='SAILS_targeted_master.csv'
ufile=open(ufilename, 'r')
tfile=open(tfilename, 'r')
ureader=csv.reader(ufile, dialect=csv.excel)
treader=csv.reader(tfile, dialect=csv.excel)
olduheader=next(ureader, None)
print olduheader
oldtheader=next(treader, None)
uheader=olduheader[0:11]+['1stOr2ndResponse', 'What is happening?']
theaderpartial=oldtheader[0:11]+['1stOr2ndResponse']
theaditems=[oldtheader[11], oldtheader[13], oldtheader[15], oldtheader[17], oldtheader[19], oldtheader[21], oldtheader[23], oldtheader[25], oldtheader[27], oldtheader[29], oldtheader[31], oldtheader[33], oldtheader[35], oldtheader[37], oldtheader[39], oldtheader[41], oldtheader[43], oldtheader[45], oldtheader[47], oldtheader[49], oldtheader[51], oldtheader[53], oldtheader[55], oldtheader[57], oldtheader[59], oldtheader[61], oldtheader[63], oldtheader[65], oldtheader[67], oldtheader[69]]

urows=[]
trows=[]
for ur in ureader:
	urows.append(ur)
for tr in treader:
	trows.append(tr)
ufile.close()
tfile.close()

i01t=[]
i02t=[]
i03t=[]
i04t=[]
i05t=[]
i06t=[]
i07t=[]
i08t=[]
i09t=[]
i10t=[]
i11t=[]
i12t=[]
i13t=[]
i14t=[]
i15t=[]
i16t=[]
i17t=[]
i18t=[]
i19t=[]
i20t=[]
i21t=[]
i22t=[]
i23t=[]
i24t=[]
i25t=[]
i26t=[]
i27t=[]
i28t=[]
i29t=[]
i30t=[]

i01u=[]
i02u=[]
i03u=[]
i04u=[]
i05u=[]
i06u=[]
i07u=[]
i08u=[]
i09u=[]
i10u=[]
i11u=[]
i12u=[]
i13u=[]
i14u=[]
i15u=[]
i16u=[]
i17u=[]
i18u=[]
i19u=[]
i20u=[]
i21u=[]
i22u=[]
i23u=[]
i24u=[]
i25u=[]
i26u=[]
i27u=[]
i28u=[]
i29u=[]
i30u=[]

for tmrow in trows:
	demog=[]
	for x in range(0,11):
		demog.append(tmrow[x])
	i01t.append(demog+['1', tmrow[11]])
	i01t.append(demog+['2', tmrow[12]])
	i02t.append(demog+['1', tmrow[13]])
	i02t.append(demog+['2', tmrow[14]])
	i03t.append(demog+['1', tmrow[15]])
	i03t.append(demog+['2', tmrow[16]])
	i04t.append(demog+['1', tmrow[17]])
	i04t.append(demog+['2', tmrow[18]])
	i05t.append(demog+['1', tmrow[19]])
	i05t.append(demog+['2', tmrow[20]])
	i06t.append(demog+['1', tmrow[21]])
	i06t.append(demog+['2', tmrow[22]])
	i07t.append(demog+['1', tmrow[23]])
	i07t.append(demog+['2', tmrow[24]])
	i08t.append(demog+['1', tmrow[25]])
	i08t.append(demog+['2', tmrow[26]])
	i09t.append(demog+['1', tmrow[27]])
	i09t.append(demog+['2', tmrow[28]])
	i10t.append(demog+['1', tmrow[29]])
	i10t.append(demog+['2', tmrow[30]])
	i11t.append(demog+['1', tmrow[31]])
	i11t.append(demog+['2', tmrow[32]])
	i12t.append(demog+['1', tmrow[33]])
	i12t.append(demog+['2', tmrow[34]])
	i13t.append(demog+['1', tmrow[35]])
	i13t.append(demog+['2', tmrow[36]])
	i14t.append(demog+['1', tmrow[37]])
	i14t.append(demog+['2', tmrow[38]])
	i15t.append(demog+['1', tmrow[39]])
	i15t.append(demog+['2', tmrow[40]])
	i16t.append(demog+['1', tmrow[41]])
	i16t.append(demog+['2', tmrow[42]])
	i17t.append(demog+['1', tmrow[43]])
	i17t.append(demog+['2', tmrow[44]])
	i18t.append(demog+['1', tmrow[45]])
	i18t.append(demog+['2', tmrow[46]])
	i19t.append(demog+['1', tmrow[47]])
	i19t.append(demog+['2', tmrow[48]])
	i20t.append(demog+['1', tmrow[49]])
	i20t.append(demog+['2', tmrow[50]])
	i21t.append(demog+['1', tmrow[51]])
	i21t.append(demog+['2', tmrow[52]])
	i22t.append(demog+['1', tmrow[53]])
	i22t.append(demog+['2', tmrow[54]])
	i23t.append(demog+['1', tmrow[55]])
	i23t.append(demog+['2', tmrow[56]])
	i24t.append(demog+['1', tmrow[57]])
	i24t.append(demog+['2', tmrow[58]])
	i25t.append(demog+['1', tmrow[59]])
	i25t.append(demog+['2', tmrow[60]])
	i26t.append(demog+['1', tmrow[61]])
	i26t.append(demog+['2', tmrow[62]])
	i27t.append(demog+['1', tmrow[63]])
	i27t.append(demog+['2', tmrow[64]])
	i28t.append(demog+['1', tmrow[65]])
	i28t.append(demog+['2', tmrow[66]])
	i29t.append(demog+['1', tmrow[67]])
	i29t.append(demog+['2', tmrow[68]])
	i30t.append(demog+['1', tmrow[69]])
	i30t.append(demog+['2', tmrow[70]])

for umrow in urows:
	demog=[]
	for x in range(0,11):
		demog.append(umrow[x])
	i01u.append(demog+['1', umrow[11]])
	i01u.append(demog+['2', umrow[12]])
	i02u.append(demog+['1', umrow[13]])
	i02u.append(demog+['2', umrow[14]])
	i03u.append(demog+['1', umrow[15]])
	i03u.append(demog+['2', umrow[16]])
	i04u.append(demog+['1', umrow[17]])
	i04u.append(demog+['2', umrow[18]])
	i05u.append(demog+['1', umrow[19]])
	i05u.append(demog+['2', umrow[20]])
	i06u.append(demog+['1', umrow[21]])
	i06u.append(demog+['2', umrow[22]])
	i07u.append(demog+['1', umrow[23]])
	i07u.append(demog+['2', umrow[24]])
	i08u.append(demog+['1', umrow[25]])
	i08u.append(demog+['2', umrow[26]])
	i09u.append(demog+['1', umrow[27]])
	i09u.append(demog+['2', umrow[28]])
	i10u.append(demog+['1', umrow[29]])
	i10u.append(demog+['2', umrow[30]])
	i11u.append(demog+['1', umrow[31]])
	i11u.append(demog+['2', umrow[32]])
	i12u.append(demog+['1', umrow[33]])
	i12u.append(demog+['2', umrow[34]])
	i13u.append(demog+['1', umrow[35]])
	i13u.append(demog+['2', umrow[36]])
	i14u.append(demog+['1', umrow[37]])
	i14u.append(demog+['2', umrow[38]])
	i15u.append(demog+['1', umrow[39]])
	i15u.append(demog+['2', umrow[40]])
	i16u.append(demog+['1', umrow[41]])
	i16u.append(demog+['2', umrow[42]])
	i17u.append(demog+['1', umrow[43]])
	i17u.append(demog+['2', umrow[44]])
	i18u.append(demog+['1', umrow[45]])
	i18u.append(demog+['2', umrow[46]])
	i19u.append(demog+['1', umrow[47]])
	i19u.append(demog+['2', umrow[48]])
	i20u.append(demog+['1', umrow[49]])
	i20u.append(demog+['2', umrow[50]])
	i21u.append(demog+['1', umrow[51]])
	i21u.append(demog+['2', umrow[52]])
	i22u.append(demog+['1', umrow[53]])
	i22u.append(demog+['2', umrow[54]])
	i23u.append(demog+['1', umrow[55]])
	i23u.append(demog+['2', umrow[56]])
	i24u.append(demog+['1', umrow[57]])
	i24u.append(demog+['2', umrow[58]])
	i25u.append(demog+['1', umrow[59]])
	i25u.append(demog+['2', umrow[60]])
	i26u.append(demog+['1', umrow[61]])
	i26u.append(demog+['2', umrow[62]])
	i27u.append(demog+['1', umrow[63]])
	i27u.append(demog+['2', umrow[64]])
	i28u.append(demog+['1', umrow[65]])
	i28u.append(demog+['2', umrow[66]])
	i29u.append(demog+['1', umrow[67]])
	i29u.append(demog+['2', umrow[68]])
	i30u.append(demog+['1', umrow[69]])
	i30u.append(demog+['2', umrow[70]])



i01tfile=open('I01T_master.csv', 'w')
i01twriter=csv.writer(i01tfile, dialect=csv.excel)
i01twriter.writerow(theaderpartial+[theaditems[0]])
for row in i01t:
	i01twriter.writerow(row)
i01tfile.close()
i02tfile=open('I02T_master.csv', 'w')
i02twriter=csv.writer(i02tfile, dialect=csv.excel)
i02twriter.writerow(theaderpartial+[theaditems[1]])
for row in i02t:
	i02twriter.writerow(row)
i02tfile.close()
i03tfile=open('I03T_master.csv', 'w')
i03twriter=csv.writer(i03tfile, dialect=csv.excel)
i03twriter.writerow(theaderpartial+[theaditems[2]])
for row in i03t:
	i03twriter.writerow(row)
i03tfile.close()
i04tfile=open('I04T_master.csv', 'w')
i04twriter=csv.writer(i04tfile, dialect=csv.excel)
i04twriter.writerow(theaderpartial+[theaditems[3]])
for row in i04t:
	i04twriter.writerow(row)
i04tfile.close()
i05tfile=open('I05T_master.csv', 'w')
i05twriter=csv.writer(i05tfile, dialect=csv.excel)
i05twriter.writerow(theaderpartial+[theaditems[4]])
for row in i05t:
	i05twriter.writerow(row)
i05tfile.close()
i06tfile=open('I06T_master.csv', 'w')
i06twriter=csv.writer(i06tfile, dialect=csv.excel)
i06twriter.writerow(theaderpartial+[theaditems[5]])
for row in i06t:
	i06twriter.writerow(row)
i06tfile.close()
i07tfile=open('I07T_master.csv', 'w')
i07twriter=csv.writer(i07tfile, dialect=csv.excel)
i07twriter.writerow(theaderpartial+[theaditems[6]])
for row in i07t:
	i07twriter.writerow(row)
i07tfile.close()
i08tfile=open('I08T_master.csv', 'w')
i08twriter=csv.writer(i08tfile, dialect=csv.excel)
i08twriter.writerow(theaderpartial+[theaditems[7]])
for row in i08t:
	i08twriter.writerow(row)
i08tfile.close()
i09tfile=open('I09T_master.csv', 'w')
i09twriter=csv.writer(i09tfile, dialect=csv.excel)
i09twriter.writerow(theaderpartial+[theaditems[8]])
for row in i09t:
	i09twriter.writerow(row)
i09tfile.close()
i10tfile=open('I10T_master.csv', 'w')
i10twriter=csv.writer(i10tfile, dialect=csv.excel)
i10twriter.writerow(theaderpartial+[theaditems[9]])
for row in i10t:
	i10twriter.writerow(row)
i10tfile.close()
i11tfile=open('I11T_master.csv', 'w')
i11twriter=csv.writer(i11tfile, dialect=csv.excel)
i11twriter.writerow(theaderpartial+[theaditems[10]])
for row in i11t:
	i11twriter.writerow(row)
i11tfile.close()
i12tfile=open('I12T_master.csv', 'w')
i12twriter=csv.writer(i12tfile, dialect=csv.excel)
i12twriter.writerow(theaderpartial+[theaditems[11]])
for row in i12t:
	i12twriter.writerow(row)
i12tfile.close()
i13tfile=open('I13T_master.csv', 'w')
i13twriter=csv.writer(i13tfile, dialect=csv.excel)
i13twriter.writerow(theaderpartial+[theaditems[12]])
for row in i13t:
	i13twriter.writerow(row)
i13tfile.close()
i14tfile=open('I14T_master.csv', 'w')
i14twriter=csv.writer(i14tfile, dialect=csv.excel)
i14twriter.writerow(theaderpartial+[theaditems[13]])
for row in i14t:
	i14twriter.writerow(row)
i14tfile.close()
i15tfile=open('I15T_master.csv', 'w')
i15twriter=csv.writer(i15tfile, dialect=csv.excel)
i15twriter.writerow(theaderpartial+[theaditems[14]])
for row in i15t:
	i15twriter.writerow(row)
i15tfile.close()
i16tfile=open('I16T_master.csv', 'w')
i16twriter=csv.writer(i16tfile, dialect=csv.excel)
i16twriter.writerow(theaderpartial+[theaditems[15]])
for row in i16t:
	i16twriter.writerow(row)
i16tfile.close()
i17tfile=open('I17T_master.csv', 'w')
i17twriter=csv.writer(i17tfile, dialect=csv.excel)
i17twriter.writerow(theaderpartial+[theaditems[16]])
for row in i17t:
	i17twriter.writerow(row)
i17tfile.close()
i18tfile=open('I18T_master.csv', 'w')
i18twriter=csv.writer(i18tfile, dialect=csv.excel)
i18twriter.writerow(theaderpartial+[theaditems[17]])
for row in i18t:
	i18twriter.writerow(row)
i18tfile.close()
i19tfile=open('I19T_master.csv', 'w')
i19twriter=csv.writer(i19tfile, dialect=csv.excel)
i19twriter.writerow(theaderpartial+[theaditems[18]])
for row in i19t:
	i19twriter.writerow(row)
i19tfile.close()
i20tfile=open('I20T_master.csv', 'w')
i20twriter=csv.writer(i20tfile, dialect=csv.excel)
i20twriter.writerow(theaderpartial+[theaditems[19]])
for row in i20t:
	i20twriter.writerow(row)
i20tfile.close()
i21tfile=open('I21T_master.csv', 'w')
i21twriter=csv.writer(i21tfile, dialect=csv.excel)
i21twriter.writerow(theaderpartial+[theaditems[20]])
for row in i21t:
	i21twriter.writerow(row)
i21tfile.close()
i22tfile=open('I22T_master.csv', 'w')
i22twriter=csv.writer(i22tfile, dialect=csv.excel)
i22twriter.writerow(theaderpartial+[theaditems[21]])
for row in i22t:
	i22twriter.writerow(row)
i22tfile.close()
i23tfile=open('I23T_master.csv', 'w')
i23twriter=csv.writer(i23tfile, dialect=csv.excel)
i23twriter.writerow(theaderpartial+[theaditems[22]])
for row in i23t:
	i23twriter.writerow(row)
i23tfile.close()
i24tfile=open('I24T_master.csv', 'w')
i24twriter=csv.writer(i24tfile, dialect=csv.excel)
i24twriter.writerow(theaderpartial+[theaditems[23]])
for row in i24t:
	i24twriter.writerow(row)
i24tfile.close()
i25tfile=open('I25T_master.csv', 'w')
i25twriter=csv.writer(i25tfile, dialect=csv.excel)
i25twriter.writerow(theaderpartial+[theaditems[24]])
for row in i25t:
	i25twriter.writerow(row)
i25tfile.close()
i26tfile=open('I26T_master.csv', 'w')
i26twriter=csv.writer(i26tfile, dialect=csv.excel)
i26twriter.writerow(theaderpartial+[theaditems[25]])
for row in i26t:
	i26twriter.writerow(row)
i26tfile.close()
i27tfile=open('I27T_master.csv', 'w')
i27twriter=csv.writer(i27tfile, dialect=csv.excel)
i27twriter.writerow(theaderpartial+[theaditems[26]])
for row in i27t:
	i27twriter.writerow(row)
i27tfile.close()
i28tfile=open('I28T_master.csv', 'w')
i28twriter=csv.writer(i28tfile, dialect=csv.excel)
i28twriter.writerow(theaderpartial+[theaditems[27]])
for row in i28t:
	i28twriter.writerow(row)
i28tfile.close()
i29tfile=open('I29T_master.csv', 'w')
i29twriter=csv.writer(i29tfile, dialect=csv.excel)
i29twriter.writerow(theaderpartial+[theaditems[28]])
for row in i29t:
	i29twriter.writerow(row)
i29tfile.close()
i30tfile=open('I30T_master.csv', 'w')
i30twriter=csv.writer(i30tfile, dialect=csv.excel)
i30twriter.writerow(theaderpartial+[theaditems[29]])
for row in i30t:
	i30twriter.writerow(row)
i30tfile.close()


i01ufile=open('I01U_master.csv', 'w')
i01uwriter=csv.writer(i01ufile, dialect=csv.excel)
i01uwriter.writerow(uheader)
for row in i01u:
	i01uwriter.writerow(row)
i01ufile.close()
i02ufile=open('I02U_master.csv', 'w')
i02uwriter=csv.writer(i02ufile, dialect=csv.excel)
i02uwriter.writerow(uheader)
for row in i02u:
	i02uwriter.writerow(row)
i02ufile.close()
i03ufile=open('I03U_master.csv', 'w')
i03uwriter=csv.writer(i03ufile, dialect=csv.excel)
i03uwriter.writerow(uheader)
for row in i03u:
	i03uwriter.writerow(row)
i03ufile.close()
i04ufile=open('I04U_master.csv', 'w')
i04uwriter=csv.writer(i04ufile, dialect=csv.excel)
i04uwriter.writerow(uheader)
for row in i04u:
	i04uwriter.writerow(row)
i04ufile.close()
i05ufile=open('I05U_master.csv', 'w')
i05uwriter=csv.writer(i05ufile, dialect=csv.excel)
i05uwriter.writerow(uheader)
for row in i05u:
	i05uwriter.writerow(row)
i05ufile.close()
i06ufile=open('I06U_master.csv', 'w')
i06uwriter=csv.writer(i06ufile, dialect=csv.excel)
i06uwriter.writerow(uheader)
for row in i06u:
	i06uwriter.writerow(row)
i06ufile.close()
i07ufile=open('I07U_master.csv', 'w')
i07uwriter=csv.writer(i07ufile, dialect=csv.excel)
i07uwriter.writerow(uheader)
for row in i07u:
	i07uwriter.writerow(row)
i07ufile.close()
i08ufile=open('I08U_master.csv', 'w')
i08uwriter=csv.writer(i08ufile, dialect=csv.excel)
i08uwriter.writerow(uheader)
for row in i08u:
	i08uwriter.writerow(row)
i08ufile.close()
i09ufile=open('I09U_master.csv', 'w')
i09uwriter=csv.writer(i09ufile, dialect=csv.excel)
i09uwriter.writerow(uheader)
for row in i09u:
	i09uwriter.writerow(row)
i09ufile.close()
i10ufile=open('I10U_master.csv', 'w')
i10uwriter=csv.writer(i10ufile, dialect=csv.excel)
i10uwriter.writerow(uheader)
for row in i10u:
	i10uwriter.writerow(row)
i10ufile.close()
i11ufile=open('I11U_master.csv', 'w')
i11uwriter=csv.writer(i11ufile, dialect=csv.excel)
i11uwriter.writerow(uheader)
for row in i11u:
	i11uwriter.writerow(row)
i11ufile.close()
i12ufile=open('I12U_master.csv', 'w')
i12uwriter=csv.writer(i12ufile, dialect=csv.excel)
i12uwriter.writerow(uheader)
for row in i12u:
	i12uwriter.writerow(row)
i12ufile.close()
i13ufile=open('I13U_master.csv', 'w')
i13uwriter=csv.writer(i13ufile, dialect=csv.excel)
i13uwriter.writerow(uheader)
for row in i13u:
	i13uwriter.writerow(row)
i13ufile.close()
i14ufile=open('I14U_master.csv', 'w')
i14uwriter=csv.writer(i14ufile, dialect=csv.excel)
i14uwriter.writerow(uheader)
for row in i14u:
	i14uwriter.writerow(row)
i14ufile.close()
i15ufile=open('I15U_master.csv', 'w')
i15uwriter=csv.writer(i15ufile, dialect=csv.excel)
i15uwriter.writerow(uheader)
for row in i15u:
	i15uwriter.writerow(row)
i15ufile.close()
i16ufile=open('I16U_master.csv', 'w')
i16uwriter=csv.writer(i16ufile, dialect=csv.excel)
i16uwriter.writerow(uheader)
for row in i16u:
	i16uwriter.writerow(row)
i16ufile.close()
i17ufile=open('I17U_master.csv', 'w')
i17uwriter=csv.writer(i17ufile, dialect=csv.excel)
i17uwriter.writerow(uheader)
for row in i17u:
	i17uwriter.writerow(row)
i17ufile.close()
i18ufile=open('I18U_master.csv', 'w')
i18uwriter=csv.writer(i18ufile, dialect=csv.excel)
i18uwriter.writerow(uheader)
for row in i18u:
	i18uwriter.writerow(row)
i18ufile.close()
i19ufile=open('I19U_master.csv', 'w')
i19uwriter=csv.writer(i19ufile, dialect=csv.excel)
i19uwriter.writerow(uheader)
for row in i19u:
	i19uwriter.writerow(row)
i19ufile.close()
i20ufile=open('I20U_master.csv', 'w')
i20uwriter=csv.writer(i20ufile, dialect=csv.excel)
i20uwriter.writerow(uheader)
for row in i20u:
	i20uwriter.writerow(row)
i20ufile.close()
i21ufile=open('I21U_master.csv', 'w')
i21uwriter=csv.writer(i21ufile, dialect=csv.excel)
i21uwriter.writerow(uheader)
for row in i21u:
	i21uwriter.writerow(row)
i21ufile.close()
i22ufile=open('I22U_master.csv', 'w')
i22uwriter=csv.writer(i22ufile, dialect=csv.excel)
i22uwriter.writerow(uheader)
for row in i22u:
	i22uwriter.writerow(row)
i22ufile.close()
i23ufile=open('I23U_master.csv', 'w')
i23uwriter=csv.writer(i23ufile, dialect=csv.excel)
i23uwriter.writerow(uheader)
for row in i23u:
	i23uwriter.writerow(row)
i23ufile.close()
i24ufile=open('I24U_master.csv', 'w')
i24uwriter=csv.writer(i24ufile, dialect=csv.excel)
i24uwriter.writerow(uheader)
for row in i24u:
	i24uwriter.writerow(row)
i24ufile.close()
i25ufile=open('I25U_master.csv', 'w')
i25uwriter=csv.writer(i25ufile, dialect=csv.excel)
i25uwriter.writerow(uheader)
for row in i25u:
	i25uwriter.writerow(row)
i25ufile.close()
i26ufile=open('I26U_master.csv', 'w')
i26uwriter=csv.writer(i26ufile, dialect=csv.excel)
i26uwriter.writerow(uheader)
for row in i26u:
	i26uwriter.writerow(row)
i26ufile.close()
i27ufile=open('I27U_master.csv', 'w')
i27uwriter=csv.writer(i27ufile, dialect=csv.excel)
i27uwriter.writerow(uheader)
for row in i27u:
	i27uwriter.writerow(row)
i27ufile.close()
i28ufile=open('I28U_master.csv', 'w')
i28uwriter=csv.writer(i28ufile, dialect=csv.excel)
i28uwriter.writerow(uheader)
for row in i28u:
	i28uwriter.writerow(row)
i28ufile.close()
i29ufile=open('I29U_master.csv', 'w')
i29uwriter=csv.writer(i29ufile, dialect=csv.excel)
i29uwriter.writerow(uheader)
for row in i29u:
	i29uwriter.writerow(row)
i29ufile.close()
i30ufile=open('I30U_master.csv', 'w')
i30uwriter=csv.writer(i30ufile, dialect=csv.excel)
i30uwriter.writerow(uheader)
for row in i30u:
	i30uwriter.writerow(row)
i30ufile.close()
