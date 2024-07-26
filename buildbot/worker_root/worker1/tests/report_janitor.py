import sys
import subprocess
from datetime import datetime, timezone
from time import sleep
sys.path.append('.')
from test_util import initialize_report, initialize_product, finalize_product, dts_error_report

if sys.argv[1] == 'initialize_report':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    initialize_report(bb_project, linux_ver)

elif sys.argv[1] == 'initialize_product':
    type = sys.argv[2]
    product = sys.argv[3]
    initialize_product(type, product)

elif sys.argv[1] == 'finalize_product':
    type = sys.argv[2]
    product = sys.argv[3]
    do_steps = sys.argv[4]
    finalize_product(product, do_steps)

elif sys.argv[1] == 'initialize_product':
    type = sys.argv[2]
    product = sys.argv[3]
    initialize_product(type, product)

elif sys.argv[1] == 'dts_error':
    target= sys.argv[2]
    dts = sys.argv[3]
    stdout = sys.argv[4]
    dts_error_report(target, dts, stdout)

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
