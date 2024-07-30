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
    stdout = subprocess.run('rm -rf ./results/'+product, shell=True)
    stdout = subprocess.run('mkdir ./results/'+product, shell=True)
    initialize_product(type, product)

elif sys.argv[1] == 'finalize_product':
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]

    type = sys.argv[4]
    product = sys.argv[5]
    do_steps = sys.argv[6]
    finalize_product(product, do_steps)

    stdout = subprocess.run('cp ./results/temp_results.txt ./results/'+product, shell=True)
    stdout = subprocess.run('mv ./results/'+product+'/temp_results.txt ./results/'+product+'/'+date+'_'+bb_project+'_'+product+'.txt', shell=True)

elif sys.argv[1] == 'dts_error':
    product= sys.argv[2]
    dts = sys.argv[3]
    stdout = sys.argv[4]
    dts_error_report(product, dts, stdout)

elif sys.argv[1] == 'finalize':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    product = sys.argv[4]
    stdout = subprocess.run('cp ./results/temp_results.txt ./results/'+product, shell=True)
    stdout = subprocess.run('mv ./results/'+product+'/temp_results.txt ./results/'+product+'/'+date+'_'+bb_project+'_'+product+'.txt', shell=True)
