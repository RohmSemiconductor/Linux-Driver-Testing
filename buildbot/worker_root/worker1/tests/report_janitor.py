import sys
import subprocess
from datetime import datetime, timezone
from time import sleep
sys.path.append('.')
from test_util import initialize_report

if sys.argv[1] == 'initialize_report':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    initialize_report(bb_project, linux_ver)

elif sys.argv[1] == 'finalize':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    if len(sys.argv)>3:
        target = sys.argv[4]
        stdout = subprocess.run('rm -rf ./results/'+target, shell=True)
        stdout = subprocess.run('mkdir ./results/'+target, shell=True)
        stdout = subprocess.run('cp ./results/temp_results.txt ./results/'+target, shell=True)
        stdout = subprocess.run('mv ./results/'+target+'/temp_results.txt ./results/'+target+'/'+date+'_'+bb_project+'_'+target+'.txt', shell=True)
        print(date)
