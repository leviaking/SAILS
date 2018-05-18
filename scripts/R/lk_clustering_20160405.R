###LK: Note that any clusters based on parameter performance (those labeled "PARAMS" and later) are based on our older (pre-3/4/2016) method of scoring experiments where we assign errors a score equal to their rank, and sum those scores for the experiment score. I.e., this version of the parameter scores is NOT normalized or based on distance from the optimal ranking.


###ITEMS_absolutecounts: these item vectors are: gs lem tokens, gs lem types, nnso lem tokens, nnso lem types, nnslm lem tokens, nnslm lem types, gs ldh tokens, gs ldh types, nnso ldh tokens, nnso ldh types, nnslm ldh tokens, nnslm ldh types, gs xdh tokens, gs xdh types, nnso xdh tokens, nnso xdh types, nnslm xdh tokens, nnslm xdh types, gs lxh tokens, gs lxh types, nnso lxh tokens, nnso lxh types, nnslm lxh tokens, nnslm lxh types, gs ldx tokens, gs ldx types, nnso ldx tokens, nnso ldx types, nnslm ldx tokens, nnslm ldx types, gs triple tokens, gs triple types, nnso triple types, nnslm triple types (this is how they are presented in SAILS_variability.xlsx)
i01 = c(98, 15, 262, 31, 262, 32, 98, 29, 262, 62, 262, 67, 98, 29, 262, 61, 262, 66, 98, 22, 262, 42, 262, 46, 98, 18, 262, 38, 262, 40, 14, 5, 13, 14)
i02 = c(95, 19, 272, 45, 272, 40, 95, 34, 272, 109, 272, 99, 95, 34, 272, 108, 272, 97, 95, 23, 272, 75, 272, 72, 95, 20, 272, 59, 272, 53, 13, 6, 21, 17)
i03 = c(125, 30, 273, 44, 273, 34, 125, 56, 273, 99, 273, 84, 125, 54, 273, 98, 273, 81, 125, 43, 273, 66, 273, 57, 125, 36, 273, 52, 273, 44, 12, 5, 24, 19)
i04 = c(107, 20, 281, 33, 281, 31, 107, 37, 281, 73, 281, 58, 107, 37, 281, 73, 281, 58, 107, 27, 281, 50, 281, 39, 107, 24, 281, 42, 281, 35, 11, 3, 13, 11)
i05 = c(111, 28, 312, 55, 313, 54, 111, 46, 312, 136, 313, 133, 111, 45, 312, 131, 313, 129, 111, 33, 312, 89, 313, 88, 111, 34, 312, 71, 313, 68, 11, 4, 32, 30)
i06 = c(126, 22, 289, 46, 290, 40, 126, 45, 289, 113, 290, 105, 126, 44, 289, 110, 290, 102, 126, 32, 289, 71, 290, 65, 126, 26, 289, 64, 290, 61, 15, 8, 25, 25)
i07 = c(114, 31, 271, 45, 271, 41, 114, 47, 271, 87, 271, 79, 114, 47, 271, 86, 271, 77, 114, 34, 271, 53, 271, 49, 114, 35, 271, 53, 271, 49, 12, 7, 25, 23)
i08 = c(102, 21, 277, 45, 280, 44, 102, 45, 277, 102, 280, 97, 102, 43, 277, 95, 280, 90, 102, 31, 277, 70, 280, 64, 102, 28, 277, 61, 280, 59, 12, 6, 27, 25)
i09 = c(127, 38, 289, 45, 289, 49, 127, 67, 289, 139, 289, 147, 127, 64, 289, 132, 289, 143, 127, 49, 289, 95, 289, 104, 127, 44, 289, 65, 289, 65, 10, 5, 36, 36)
i10 = c(115, 32, 272, 45, 272, 43, 115, 48, 272, 107, 272, 104, 115, 48, 272, 102, 272, 97, 115, 33, 272, 72, 272, 68, 115, 38, 272, 58, 272, 58, 12, 5, 23, 21)
ITEMS_absolutecounts_df = data.frame(i01, i02, i03, i04, i05, i06, i07, i08, i09, i10)
ITEMS_absolutecounts = dist(as.matrix(ITEMS_absolutecounts_df))
ITEMS_absolutecounts_hc = hclust(ITEMS_absolutecounts)
#(ITEMS_absolutecounts_dend = as.dendrogram(ITEMS_absolutecounts_hc))
#ITEMS_absolutecounts_labels = c(gs_lem_tokens, gs_lem_types, nnso_lem_tokens, nnso_lem_types, nnslm_lem_tokens, nnslm_lem_types, gs_ldh_tokens, gs_ldh_types, nnso_ldh_tokens, nnso_ldh_types, nnslm_ldh_tokens, nnslm_ldh_types, gs_xdh_tokens, gs_xdh_types, nnso_xdh_tokens, nnso_xdh_types, nnslm_xdh_tokens, nnslm_xdh_types, gs_lxh_tokens, gs_lxh_types, nnso_lxh_tokens, nnso_lxh_types, nnslm_lxh_tokens, nnslm_lxh_types, gs_ldx_tokens, gs_ldx_types, nnso_ldx_tokens, nnso_ldx_types, nnslm_ldx_tokens, nnslm_ldx_types, gs_triple_tokens, gs_triple_types, nnso_triple_types, nnslm_triple_types)
ITEMS_absolutecounts_labels = c('gs_lem_tokens', ' gs_lem_types', ' nnso_lem_tokens', ' nnso_lem_types', ' nnslm_lem_tokens', ' nnslm_lem_types', ' gs_ldh_tokens', ' gs_ldh_types', ' nnso_ldh_tokens', ' nnso_ldh_types', ' nnslm_ldh_tokens', ' nnslm_ldh_types', ' gs_xdh_tokens', ' gs_xdh_types', ' nnso_xdh_tokens', ' nnso_xdh_types', ' nnslm_xdh_tokens', ' nnslm_xdh_types', ' gs_lxh_tokens', ' gs_lxh_types', ' nnso_lxh_tokens', ' nnso_lxh_types', ' nnslm_lxh_tokens', ' nnslm_lxh_types', ' gs_ldx_tokens', ' gs_ldx_types', ' nnso_ldx_tokens', ' nnso_ldx_types', ' nnslm_ldx_tokens', ' nnslm_ldx_types', ' gs_triple_tokens', ' gs_triple_types', ' nnso_triple_types', ' nnslm_triple_types')

#str(ITEMS_absolutecounts_dend)
pdf("./lk_2016_02_26_clusters.pdf")
#for (i in 1:23){
i = 0
for (i in i){
plot(ITEMS_absolutecounts_hc, labels=ITEMS_absolutecounts_labels)
#plot(ITEMS_absolutecounts_dend, labels=FALSE)
#plot(ITEMS_absolutecounts_hc)
#plot(ITEMS_abolute_hc, labs=ITEMS_abolute_labels)

###ITEMS_absolutecounts_notriple: these item vectors are: gs lem tokens, gs lem types, nnso lem tokens, nnso lem types, nnslm lem tokens, nnslm lem types, gs ldh tokens, gs ldh types, nnso ldh tokens, nnso ldh types, nnslm ldh tokens, nnslm ldh types, gs xdh tokens, gs xdh types, nnso xdh tokens, nnso xdh types, nnslm xdh tokens, nnslm xdh types, gs lxh tokens, gs lxh types, nnso lxh tokens, nnso lxh types, nnslm lxh tokens, nnslm lxh types, gs ldx tokens, gs ldx types, nnso ldx tokens, nnso ldx types, nnslm ldx tokens, nnslm ldx types (this is how they are presented in SAILS_variability.xlsx)
i01 = c(98, 15, 262, 31, 262, 32, 98, 29, 262, 62, 262, 67, 98, 29, 262, 61, 262, 66, 98, 22, 262, 42, 262, 46, 98, 18, 262, 38, 262, 40)
i02 = c(95, 19, 272, 45, 272, 40, 95, 34, 272, 109, 272, 99, 95, 34, 272, 108, 272, 97, 95, 23, 272, 75, 272, 72, 95, 20, 272, 59, 272, 53)
i03 = c(125, 30, 273, 44, 273, 34, 125, 56, 273, 99, 273, 84, 125, 54, 273, 98, 273, 81, 125, 43, 273, 66, 273, 57, 125, 36, 273, 52, 273, 44)
i04 = c(107, 20, 281, 33, 281, 31, 107, 37, 281, 73, 281, 58, 107, 37, 281, 73, 281, 58, 107, 27, 281, 50, 281, 39, 107, 24, 281, 42, 281, 35)
i05 = c(111, 28, 312, 55, 313, 54, 111, 46, 312, 136, 313, 133, 111, 45, 312, 131, 313, 129, 111, 33, 312, 89, 313, 88, 111, 34, 312, 71, 313, 68)
i06 = c(126, 22, 289, 46, 290, 40, 126, 45, 289, 113, 290, 105, 126, 44, 289, 110, 290, 102, 126, 32, 289, 71, 290, 65, 126, 26, 289, 64, 290, 61)
i07 = c(114, 31, 271, 45, 271, 41, 114, 47, 271, 87, 271, 79, 114, 47, 271, 86, 271, 77, 114, 34, 271, 53, 271, 49, 114, 35, 271, 53, 271, 49)
i08 = c(102, 21, 277, 45, 280, 44, 102, 45, 277, 102, 280, 97, 102, 43, 277, 95, 280, 90, 102, 31, 277, 70, 280, 64, 102, 28, 277, 61, 280, 59)
i09 = c(127, 38, 289, 45, 289, 49, 127, 67, 289, 139, 289, 147, 127, 64, 289, 132, 289, 143, 127, 49, 289, 95, 289, 104, 127, 44, 289, 65, 289, 65)
i10 = c(115, 32, 272, 45, 272, 43, 115, 48, 272, 107, 272, 104, 115, 48, 272, 102, 272, 97, 115, 33, 272, 72, 272, 68, 115, 38, 272, 58, 272, 58)
ITEMS_absolutecounts_notriple_df = data.frame(i01, i02, i03, i04, i05, i06, i07, i08, i09, i10)
ITEMS_absolutecounts_notriple = dist(as.matrix(ITEMS_absolutecounts_notriple_df))
ITEMS_absolutecounts_notriple_hc = hclust(ITEMS_absolutecounts_notriple)
#plot(ITEMS_absolutecounts_notriple_hc)



###COUNTS: ns and nns response token and type counts
gslemtok = c(98, 95, 125, 107, 111, 126, 114, 102, 127, 115)
gslemtyp = c(15, 19, 30, 20, 28, 22, 31, 21, 38, 32)
nnsolemtok = c(262, 272, 273, 281, 312, 289, 271, 277, 289, 272)
nnsolemtyp = c(31, 45, 44, 33, 55, 46, 45, 45, 45, 45)
nnslmlemtok = c(262, 272, 273, 281, 313, 290, 271, 280, 289, 272)
nnslmlemtyp = c(32, 40, 34, 31, 54, 40, 41, 44, 49, 43)
gsldhtok = c(98, 95, 125, 107, 111, 126, 114, 102, 127, 115)
gsldhtyp = c(29, 34, 56, 37, 46, 45, 47, 45, 67, 48)
nnsoldhtok = c(262, 272, 273, 281, 312, 289, 271, 277, 289, 272)
nnsoldhtyp = c(62, 109, 99, 73, 136, 113, 87, 102, 139, 107)
nnslmldhtok = c(262, 272, 273, 281, 313, 290, 271, 280, 289, 272)
nnslmldhtyp = c(67, 99, 84, 58, 133, 105, 79, 97, 147, 104)
gsxdhtok = c(98, 95, 125, 107, 111, 126, 114, 102, 127, 115)
gsxdhtyp = c(29, 34, 54, 37, 45, 44, 47, 43, 64, 48)
nnsoxdhtok = c(262, 272, 273, 281, 312, 289, 271, 277, 289, 272)
nnsoxdhtyp = c(61, 108, 98, 73, 131, 110, 86, 95, 132, 102)
nnslmxdhtok = c(262, 272, 273, 281, 313, 290, 271, 280, 289, 272)
nnslmxdhtyp = c(66, 97, 81, 58, 129, 102, 77, 90, 143, 97)
gslxhtok = c(98, 95, 125, 107, 111, 126, 114, 102, 127, 115)
gslxhtyp = c(22, 23, 43, 27, 33, 32, 34, 31, 49, 33)
nnsolxhtok = c(262, 272, 273, 281, 312, 289, 271, 277, 289, 272)
nnsolxhtyp = c(42, 75, 66, 50, 89, 71, 53, 70, 95, 72)
nnslmlxhtok = c(262, 272, 273, 281, 313, 290, 271, 280, 289, 272)
nnslmlxhtyp = c(46, 72, 57, 39, 88, 65, 49, 64, 104, 68)
gsldxtok = c(98, 95, 125, 107, 111, 126, 114, 102, 127, 115)
gsldxtyp = c(18, 20, 36, 24, 34, 26, 35, 28, 44, 38)
nnsoldxtok = c(262, 272, 273, 281, 312, 289, 271, 277, 289, 272)
nnsoldxtyp = c(38, 59, 52, 42, 71, 64, 53, 61, 65, 58)
nnslmldxtok = c(262, 272, 273, 281, 313, 290, 271, 280, 289, 272)
nnslmldxtyp = c(40, 53, 44, 35, 68, 61, 49, 59, 65, 58)
gstriptok = c(14, 13, 12, 11, 11, 15, 12, 12, 10, 12)
gstriptyp = c(5, 6, 5, 3, 4, 8, 7, 6, 5, 5)
nnsotriptyp = c(13, 21, 24, 13, 32, 25, 25, 27, 36, 23)
nnslmtriptyp = c(14, 17, 19, 11, 30, 25, 23, 25, 36, 21)

###this section includes all vectors listed under "COUNTS" above; i.e., data from the NS (GS) and NNS responses themselves, which are type and token counts for triples, lemmas, and the various depstrings.

COUNTSdf = data.frame(gstriptok, gstriptyp, nnsotriptyp, nnslmtriptyp, gslemtok, gslemtyp, nnsolemtok, nnsolemtyp, nnslmlemtok, nnslmlemtyp, gsldhtok, gsldhtyp, nnsoldhtok, nnsoldhtyp, nnslmldhtok, nnslmldhtyp, gsxdhtok, gsxdhtyp, nnsoxdhtok, nnsoxdhtyp, nnslmxdhtok, nnslmxdhtyp, gslxhtok, gslxhtyp, nnsolxhtok, nnsolxhtyp, nnslmlxhtok, nnslmlxhtyp, gsldxtok, gsldxtyp, nnsoldxtok, nnsoldxtyp, nnslmldxtok, nnslmldxtyp)
COUNTS = dist(as.matrix(COUNTSdf))
COUNTShc = hclust(COUNTS)
# plot(COUNTShc)

gsdf = data.frame(gstriptok, gstriptyp, gslemtok, gslemtyp, gsldhtok, gsldhtyp, gsxdhtok, gsxdhtyp, gslxhtok, gslxhtyp, gsldxtok, gsldxtyp)
gs_COUNTS = dist(as.matrix(gsdf))
gshc = hclust(gs_COUNTS)
#plot(gshc)

nnsodf = data.frame(nnsotriptyp, nnsolemtok, nnsolemtyp, nnsoldhtok, nnsoldhtyp, nnsoxdhtok, nnsoxdhtyp, nnsolxhtok, nnsolxhtyp, nnsoldxtok, nnsoldxtyp)
nnso_COUNTS = dist(as.matrix(nnsodf))
nnsohc = hclust(nnso_COUNTS)
#plot(nnsohc)

nnslmdf = data.frame(nnslmtriptyp, nnslmlemtok, nnslmlemtyp, nnslmldhtok, nnslmldhtyp, nnslmxdhtok, nnslmxdhtyp, nnslmlxhtok, nnslmlxhtyp, nnslmldxtok, nnslmldxtyp)
nnslm_COUNTS = dist(as.matrix(nnslmdf))
nnslmhc = hclust(nnslm_COUNTS)
#plot(nnslmhc)

nnsbothdf = data.frame(nnsotriptyp, nnslmtriptyp, nnsolemtok, nnsolemtyp, nnslmlemtok, nnslmlemtyp, nnsoldhtok, nnsoldhtyp, nnslmldhtok, nnslmldhtyp, nnsoxdhtok, nnsoxdhtyp, nnslmxdhtok, nnslmxdhtyp, nnsolxhtok, nnsolxhtyp, nnslmlxhtok, nnslmlxhtyp, nnsoldxtok, nnsoldxtyp, nnslmldxtok, nnslmldxtyp)
nnsboth_COUNTS = dist(as.matrix(nnsbothdf))
nnsbothhc = hclust(nnsboth_COUNTS)
#plot(nnsbothhc)

###COUNTS_normalized_notriple: Similar to "COUNTS_notriple" above, but in this case, instead of using type & token counts, I'm using only type/token ratios, so the vectors are half as long. I'm trying to see if this results in the same clustering as COUNTS_notriple.
gs_lem_ttr = c(0.153061224, 0.2, 0.24, 0.186915888, 0.252252252, 0.174603175, 0.271929825, 0.205882353, 0.299212598, 0.27826087)
nnso_lem_ttr = c(0.118320611, 0.165441176, 0.161172161, 0.117437722, 0.176282051, 0.15916955, 0.166051661, 0.162454874, 0.155709343, 0.165441176)
nnslm_lem_ttr = c(0.122137405, 0.147058824, 0.124542125, 0.110320285, 0.172523962, 0.137931034, 0.151291513, 0.157142857, 0.169550173, 0.158088235)
gs_ldh_ttr = c(0.295918367, 0.357894737, 0.448, 0.345794393, 0.414414414, 0.357142857, 0.412280702, 0.441176471, 0.527559055, 0.417391304)
nnso_ldh_ttr = c(0.236641221, 0.400735294, 0.362637363, 0.259786477, 0.435897436, 0.39100346, 0.32103321, 0.368231047, 0.480968858, 0.393382353)
nnslm_ldh_ttr = c(0.255725191, 0.363970588, 0.307692308, 0.206405694, 0.424920128, 0.362068966, 0.291512915, 0.346428571, 0.508650519, 0.382352941)
gs_xdh_ttr = c(0.295918367, 0.357894737, 0.432, 0.345794393, 0.405405405, 0.349206349, 0.412280702, 0.421568627, 0.503937008, 0.417391304)
nnso_xdh_ttr = c(0.232824427, 0.397058824, 0.358974359, 0.259786477, 0.419871795, 0.380622837, 0.317343173, 0.342960289, 0.456747405, 0.375)
nnslm_xdh_ttr = c(0.251908397, 0.356617647, 0.296703297, 0.206405694, 0.412140575, 0.351724138, 0.284132841, 0.321428571, 0.494809689, 0.356617647)
gs_lxh_ttr = c(0.224489796, 0.242105263, 0.344, 0.252336449, 0.297297297, 0.253968254, 0.298245614, 0.303921569, 0.385826772, 0.286956522)
nnso_lxh_ttr = c(0.160305344, 0.275735294, 0.241758242, 0.177935943, 0.28525641, 0.24567474, 0.195571956, 0.252707581, 0.328719723, 0.264705882)
nnslm_lxh_ttr = c(0.175572519, 0.264705882, 0.208791209, 0.138790036, 0.28115016, 0.224137931, 0.180811808, 0.228571429, 0.359861592, 0.25)
gs_ldx_ttr = c(0.183673469, 0.210526316, 0.288, 0.224299065, 0.306306306, 0.206349206, 0.307017544, 0.274509804, 0.346456693, 0.330434783)
nnso_ldx_ttr = c(0.145038168, 0.216911765, 0.19047619, 0.149466192, 0.227564103, 0.221453287, 0.195571956, 0.220216606, 0.224913495, 0.213235294)
nnslm_ldx_ttr = c(0.152671756, 0.194852941, 0.161172161, 0.12455516, 0.217252396, 0.210344828, 0.180811808, 0.210714286, 0.224913495, 0.213235294)

###COUNTS_notriple: same as "COUNTS" but does NOT include triple counts.

COUNTS_notripledf = data.frame(gslemtok, gslemtyp, nnsolemtok, nnsolemtyp, nnslmlemtok, nnslmlemtyp, gsldhtok, gsldhtyp, nnsoldhtok, nnsoldhtyp, nnslmldhtok, nnslmldhtyp, gsxdhtok, gsxdhtyp, nnsoxdhtok, nnsoxdhtyp, nnslmxdhtok, nnslmxdhtyp, gslxhtok, gslxhtyp, nnsolxhtok, nnsolxhtyp, nnslmlxhtok, nnslmlxhtyp, gsldxtok, gsldxtyp, nnsoldxtok, nnsoldxtyp, nnslmldxtok, nnslmldxtyp)
COUNTS_notriple = dist(as.matrix(COUNTS_notripledf))
COUNTS_notriplehc = hclust(COUNTS_notriple)
plot(COUNTS_notriplehc)

COUNTS_normalized_notripledf = data.frame(gs_lem_ttr, nnso_lem_ttr, nnslm_lem_ttr, gs_ldh_ttr, nnso_ldh_ttr, nnslm_ldh_ttr, gs_xdh_ttr, nnso_xdh_ttr, nnslm_xdh_ttr, gs_lxh_ttr, nnso_lxh_ttr, nnslm_lxh_ttr, gs_ldx_ttr, nnso_ldx_ttr, nnslm_ldx_ttr)
COUNTS_normalized_notriple = dist(as.matrix(COUNTS_normalized_notripledf))
COUNTS_normalized_notriplehc = hclust(COUNTS_normalized_notriple)
plot(COUNTS_normalized_notriplehc)

gs_notripledf = data.frame(gslemtok, gslemtyp, gsldhtok, gsldhtyp, gsxdhtok, gsxdhtyp, gslxhtok, gslxhtyp, gsldxtok, gsldxtyp)
gs_COUNTS_notriple = dist(as.matrix(gs_notripledf))
gs_notriplehc = hclust(gs_COUNTS_notriple)
#plot(gs_notriplehc)

nnso_counts_normalized_notripledf = data.frame(nnso_lem_ttr, nnso_ldh_ttr, nnso_xdh_ttr, nnso_lxh_ttr, nnso_ldx_ttr)
nnso_counts_normalized_notriple = dist(as.matrix(nnso_counts_normalized_notripledf))
nnso_counts_normalized_notriplehc = hclust(nnso_counts_normalized_notriple)
plot(nnso_counts_normalized_notriplehc)

nnslm_counts_normalized_notripledf = data.frame(nnslm_lem_ttr, nnslm_ldh_ttr, nnslm_xdh_ttr, nnslm_lxh_ttr, nnslm_ldx_ttr)
nnslm_counts_normalized_notriple = dist(as.matrix(nnslm_counts_normalized_notripledf))
nnslm_counts_normalized_notriplehc = hclust(nnslm_counts_normalized_notriple)
plot(nnslm_counts_normalized_notriplehc)

nnsboth_counts_normalized_notripledf = data.frame(nnso_lem_ttr, nnslm_lem_ttr, nnso_ldh_ttr, nnslm_ldh_ttr, nnso_xdh_ttr, nnslm_xdh_ttr, nnso_lxh_ttr, nnslm_lxh_ttr, nnso_ldx_ttr, nnslm_ldx_ttr)
nnsboth_counts_normalized_notriple = dist(as.matrix(nnsboth_counts_normalized_notripledf))
nnsboth_counts_normalized_notriplehc = hclust(nnsboth_counts_normalized_notriple)
plot(nnsboth_counts_normalized_notriplehc)

gs_counts_normalized_notripledf = data.frame(gs_lem_ttr, gs_ldh_ttr, gs_xdh_ttr, gs_lxh_ttr, gs_ldx_ttr)
gs_counts_normalized_notriple = dist(as.matrix(gs_counts_normalized_notripledf))
gs_counts_normalized_notriplehc = hclust(gs_counts_normalized_notriple)
plot(gs_counts_normalized_notriplehc)


nnso_notripledf = data.frame(nnsolemtok, nnsolemtyp, nnsoldhtok, nnsoldhtyp, nnsoxdhtok, nnsoxdhtyp, nnsolxhtok, nnsolxhtyp, nnsoldxtok, nnsoldxtyp)
nnso_COUNTS_notriple = dist(as.matrix(nnso_notripledf))
nnso_notriplehc = hclust(nnso_COUNTS_notriple)
#plot(nnso_notriplehc)

nnslm_notripledf = data.frame(nnslmlemtok, nnslmlemtyp, nnslmldhtok, nnslmldhtyp, nnslmxdhtok, nnslmxdhtyp, nnslmlxhtok, nnslmlxhtyp, nnslmldxtok, nnslmldxtyp)
nnslm_COUNTS_notriple = dist(as.matrix(nnslm_notripledf))
nnslm_notriplehc = hclust(nnslm_COUNTS_notriple)
#plot(nnslm_notriplehc)

nnsboth_notripledf = data.frame(nnsolemtok, nnsolemtyp, nnslmlemtok, nnslmlemtyp, nnsoldhtok, nnsoldhtyp, nnslmldhtok, nnslmldhtyp, nnsoxdhtok, nnsoxdhtyp, nnslmxdhtok, nnslmxdhtyp, nnsolxhtok, nnsolxhtyp, nnslmlxhtok, nnslmlxhtyp, nnsoldxtok, nnsoldxtyp, nnslmldxtok, nnslmldxtyp)
nnsboth_COUNTS_notriple = dist(as.matrix(nnsboth_notripledf))
nnsboth_notriplehc = hclust(nnsboth_COUNTS_notriple)
#plot(nnsboth_notriplehc)

###PARAMETERS: average error scores (per item) for all experiments with a given parameter setting
###LK: 4/6/2016: I'm pretty sure this data is based on bad analysis and isn't valid...
# # # app_TA_err = c(33.125, 186.25, 197.313, 42.875, 419.688, 96, 70, 162.875, 363.563, 175.75)
# # app_TA_err =   c(34.7, 185.0, 206.85, 41.8, 423.55, 102.8, 88.4, 153.35, 354.05, 176.45)
# # app_FA_err = c(23.8, 133.7, 178, 41.4, 393.1, 92.2, 63.5, 141.5, 357.4, 179.2) ###Did not change
# # app_FC_err = c(26.3, 142.7, 170.8, 51.2, 397.1, 91.4, 66.1, 147.4, 370.5, 174.9) ###did not change
# # # app_TC_err = c(33.125, 186.25, 197.313, 42.875, 419.688, 96, 70, 162.875, 363.563, 175.75)
# # app_TC_err = c(35.25, 172.85, 197.45, 41.5, 415.75, 99.75, 73.05, 164.5, 350.9, 174.95)
# # #### form_lem_err = c(28.25, 132.5, 192.75, 60.25, 383.75, 119, 68.75, 120, 363.75, 189)
# # #### we're currenly not using lemmas, but xdx instead.
# # form_xdx_err = c(39.416, 179.75, 209.75, 48.167, 412.5, 122.167, 84.0, 149.0, 356.0, 179.417)
# # # form_ldh_err = c(30.916, 153.833, 183.916, 41.25, 415.5, 88.5, 64.75, 158.833, 356.25, 167.917)
# # form_ldh_err = c(27.833, 148.25, 183.167, 38.583, 417.75, 86.167, 63.583, 156.75, 355.333, 166.0)
# # # form_xdh_err = c(32, 156.666, 184.916, 40.75, 411.333, 89.5, 65.167, 153.083, 355.5, 169.333)
# # form_xdh_err = c(27.333, 150.75, 181.167, 39.25, 411.667, 87.083, 63.333, 149.5, 355.75, 165.333)
# # # form_lxh_err = c(28.333, 175.666, 187.833, 38.75, 407.417, 84.333, 77, 173.25, 354.583, 171.75)
# # form_lxh_err = c(29.833, 158.833, 189.0, 38.5, 407.667, 86.5, 87.75, 155.0, 350.167, 172.0)
# # # form_ldx_err = c(29.416, 196.666, 195.916, 50.666, 415.5, 107, 64.83, 149.917, 388.5, 191.75)
# # form_ldx_err = c(33.917, 189.167, 197.25, 51.5, 407.75, 108.75, 78.417, 160.5, 364.25, 198.0)
# # # src_nnso_err = c(14.192, 205.231, 258.038, 50.615, 423.769, 84.038, 60.654, 123.962, 344.846, 172.731)
# # src_nnso_err = c(16.167, 202.367, 262.533, 49.733, 431.467, 83.333, 63.433, 124.4, 338.3, 171.2)
# # # src_nnslm_err = c(45.846, 130.308, 118.962, 37.769, 396.692, 104.731, 75.346, 187.615, 382.58, 179.769)
# # src_nnslm_err = c(47.167, 128.333, 262.533, 36.666, 391.467, 112.933, 87.4, 183.9, 374.3, 181.1)
# # # ref_B_err = c(32.125, 180.5, 206.25, 40.875, 414.875, 96.25, 70.125, 158.375, 362.25, 170.75)
# # ref_B_err = c(33.0, 177.3, 193.4, 41.1, 415.9, 98.95, 81.5, 159.15, 350.75, 175.9)
# # # ref_W_err = c(34.125, 192, 188.375, 44.875, 424.5, 95.75, 69.875, 167.375, 364.875, 180.75)
# # ref_W_err = c(36.95, 180.55, 210.9, 42.2, 423.4, 103.7, 79.95, 158.7, 354.2, 175.5)



###PARAMETERS: this section includes all vectors listed under "PARAMETERS" above: average error scores (per item) for all experiments with a given parameter setting
PARAMSdf = data.frame(app_TA_err, app_FA_err, app_FC_err, app_TC_err, form_xdx_err, form_ldh_err, form_xdh_err, form_lxh_err, form_ldx_err, src_nnso_err, src_nnslm_err, ref_B_err, ref_W_err)
PARAMS = dist(as.matrix(PARAMSdf))
PARAMShc = hclust(PARAMS)
plot(PARAMShc)

####Parameters by Average Precision
FA_ap = c(0.196902257, 0.582719189, 0.534117901, 0.32738071, 0.664092202, 0.420125192, 0.381536702, 0.524512628, 0.709264496, 0.605745648)
FC_ap = c(0.193365844, 0.586073647, 0.591133813, 0.329760786, 0.666487754, 0.441868166, 0.38932383, 0.529375368, 0.705969966, 0.644662797)
TA_ap = c(0.183018057, 0.522682157, 0.554098221, 0.365690964, 0.661374733, 0.425898693, 0.351140118, 0.561437174, 0.773844032, 0.676280472)
TC_ap = c(0.181017635, 0.549407082, 0.562749864, 0.3685556, 0.670313227, 0.436083998, 0.370530204, 0.549172014, 0.788309104, 0.681585191)
ldh_ap = c(0.196503154, 0.595259084, 0.575946728, 0.364532363, 0.627145252, 0.444853095, 0.407197675, 0.553853831, 0.729714198, 0.67264911)
ldx_ap = c(0.185415399, 0.49187246, 0.543017019, 0.338800247, 0.694208786, 0.420733694, 0.354707314, 0.500392708, 0.773001369, 0.633012539)
lxh_ap = c(0.180588619, 0.574421001, 0.5697701, 0.354775901, 0.672144141, 0.462640975, 0.357940962, 0.544073784, 0.754614023, 0.664043081)
xdh_ap = c(0.198387623, 0.591469087, 0.572675165, 0.363084087, 0.633819314, 0.452279337, 0.405567714, 0.562763101, 0.728059484, 0.672917563)
xdx_ap = c(0.171054776, 0.507787796, 0.537714226, 0.350169588, 0.700979069, 0.374458518, 0.319753981, 0.568171887, 0.797561537, 0.662494176)
nnslm_ap = c(0.280822403, 0.466204284, 0.545099453, 0.324731523, 0.727045586, 0.399111538, 0.372142967, 0.547777739, 0.818915346, 0.711822719)
nnso_ap = c(0.091957426, 0.638119487, 0.574549842, 0.383813351, 0.60427304, 0.462874709, 0.365924092, 0.543924385, 0.694264898, 0.610223871)
Brown_ap = c(0.188337327, 0.542387666, 0.571308643, 0.369799064, 0.674284079, 0.438566517, 0.353024655, 0.554474769, 0.784336994, 0.676851621)
WSJ_ap = c(0.175698364, 0.529701572, 0.545539443, 0.3644475, 0.657403881, 0.423416175, 0.368645667, 0.556134419, 0.777816142, 0.681014042)

params_ap_df = data.frame(FA_ap, FC_ap, TA_ap, TC_ap, ldh_ap, ldx_ap, lxh_ap, xdh_ap, xdx_ap, nnslm_ap, nnso_ap, Brown_ap, WSJ_ap)
params_ap = dist(as.matrix(params_ap_df))
params_ap_hc = hclust(params_ap)
plot(params_ap_hc)


###ITEMS_relativeparams:
# irp01 = c(b,c,a,lem,lxh,ldx,ldh,xdh,nnso,B)
# irp02 = c(b,c,a,lem,ldh,xdh,lxh,ldx,nnslm,B)
# irp03 = c(c,b,a,ldh,xdh,lxh,lem,ldx,nnslm,W)
# irp04 = c(b,a,c,lxh,xdh,ldh,ldx,lem,nnslm,B)
# irp05 = c(b,c,a,lem,lxh,xdh,ldh,ldx,nnslm,B)
# irp06 = c(c,b,a,lxh,ldh,xdh,ldx,lem,nnso,W)
# irp07 = c(b,c,a,ldh,ldx,xdh,lem,lxh,nnso,W)
# irp08 = c(b,c,a,lem,ldx,xdh,ldh,lxh,nnso,B)
# irp09 = c(b,a,c,lxh,xdh,ldh,lem,ldx,nnso,B)
# irp10 = c(c,a,b,ldh,xdh,lxh,lem,ldx,nnso,B)
### try this as binary info: so for a,b,c, for example, use three positions for each: (a in first place, a in second place, a in third place, b in first place, etc.)

### here i'm simply assigning numerical values to the parameters listed above, e.g., a,b,c is 1,2,3. So I'm reordering these numbers to represent the ranked parameters. The cluster doesn't look meaningful to me, however. I just don't think this is mathematically sound; I don't think this reordering is compatible with the clustering algorithm; I think it's concerned with the values in each position, not the position of each value. In other words, this approach is clustering the positions in the vectors, not the items.
# irp01 = c(2,3,1,1,4,5,2,3,1,1)
# irp02 = c(2,3,1,1,2,3,4,5,2,1)
# irp03 = c(3,2,1,2,3,4,1,5,2,2)
# irp04 = c(2,1,3,4,3,2,5,1,2,1)
# irp05 = c(2,3,1,1,4,3,2,5,2,1)
# irp06 = c(3,2,1,4,2,3,5,1,1,2)
# irp07 = c(2,3,1,2,5,3,1,4,1,2)
# irp08 = c(2,3,1,1,5,3,2,4,1,1)
# irp09 = c(2,1,3,4,3,2,1,5,1,1)
# irp10 = c(3,1,2,2,3,4,1,5,1,1)

## here i'm assigning each parameter a position, then using that parameter's rank as the value of the position. So a,b,c, is 1,2,3, but b,c,a is 3,1,2...
### WRONG: these vectors have 12 values, so there are 12 leaves in the cluster tree; this doesn't correspond to the ITEMS.
# irp01 = c(3,1,2,1,4,5,2,3,1,2,1,2)
# irp02 = c(3,1,2,1,2,3,4,5,2,1,1,2)
# irp03 = c(3,2,1,2,3,4,1,5,2,1,2,1)
# irp04 = c(2,1,3,4,3,2,5,1,2,1,1,2)
# irp05 = c(3,1,2,1,4,3,2,5,2,1,1,2)
# irp06 = c(3,2,1,4,2,3,1,5,1,2,2,1)
# irp07 = c(3,1,2,2,5,3,1,4,1,2,2,1)
# irp08 = c(3,1,2,1,5,3,2,4,1,2,1,2)
# irp09 = c(2,1,3,4,3,2,1,5,1,2,1,2)
# irp10 = c(2,3,1,2,3,4,1,5,1,2,1,2)

# # ITEMS_relativeparams_df = data.frame(irp01, irp02, irp03, irp04, irp05, irp06, irp07, irp08, irp09, irp10)
# ITEMS_relativeparams = dist(as.matrix(ITEMS_relativeparams_df))
# ITEMS_relativeparams_hc = hclust(ITEMS_relativeparams)
# plot(ITEMS_relativeparams_hc)

approach_df = data.frame(app_TA_err, app_FA_err, app_FC_err, app_TC_err)
approach = dist(as.matrix(approach_df))
approach_hc = hclust(approach)
plot(approach_hc)

form_df = data.frame(form_xdx_err, form_ldh_err, form_xdh_err, form_lxh_err, form_ldx_err)
form = dist(as.matrix(form_df))
form_hc = hclust(form)
plot(form_hc)

source_df = data.frame(src_nnso_err, src_nnslm_err)
source = dist(as.matrix(source_df))
source_hc = hclust(source)
plot(source_hc)

reference_corpus_df = data.frame(ref_B_err, ref_W_err)
reference_corpus = dist(as.matrix(reference_corpus_df))
reference_corpus_hc = hclust(reference_corpus)
plot(reference_corpus_hc)
}
dev.off()