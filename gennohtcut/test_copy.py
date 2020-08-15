#$ sites_blacklist *
#$ sites_whitelist T2_IT_Pisa

with open('myfile2.txt', 'w') as f:
    f.write('a'*10)

import os
os.system(
    'xrdcp -d2 -p myfile2.txt root://cmseos.fnal.gov//store/user/klijnsma/testdircmsconn/myfile2.txt'
    )