pool/
Contains one file per item; each file contains all NS responses for that item.

sets/
Contains 240 files; one file contains all the NS responses for a given model setting.
For example, I01T-gNSF-r1-In-training_pool.csv contains all NS responses for item 1, Targeted, gNSF (group Native Speakers Familiar), first responses;
The "In", "Tr", "Di" stand for intransitive, transitive, ditransitive, but this just for reference because each item number is only In, Tr, or Di. In other words, there is no I01...-Tr or I01...-Di because I01 is strictly -In.

To clarify, this is:
Item: 1-30 (30)
Targeting: T (targeted) or U (untargeted) (2)
Group: gNSF or gNSC (crowd sourced) (2)
FirstOrSecondResponse: r1 or r2 (2)

30*2*2*2=240 sets

These sets are training pools of varying sizes. The gNSF pools are quite small -- roughly 30 or fewer per pool.

N50/
Contains 120 files; each file is a training set of exactly 50 responses drawn randomly from the pool. These follow the same conventions as described for sets/, but the gNSF sets are omitted here because there are not enough responses in those pools.
To accommodate the smaller gNSF pools in future experiments, I'll have to use a smaller N sample size.
