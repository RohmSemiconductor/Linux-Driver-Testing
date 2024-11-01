import sys
import subprocess
from datetime import datetime, timezone
from time import sleep
sys.path.append('.')
from test_util import initialize_report, initialize_product, finalize_product, dts_error_report, kernel_error_report, bisect_result

if sys.argv[1] == 'initialize_report':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    revision = sys.argv[4]
    stdout = subprocess.run('rm -rf temp_results/', shell=True)
    stdout = subprocess.run('mkdir temp_results', shell=True)
    initialize_report(bb_project, linux_ver, revision)

elif sys.argv[1] == 'initialize_product':
    type = sys.argv[2]
    product = sys.argv[3]
    stdout = subprocess.run('mkdir ./temp_results/'+product, shell=True)
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

    stdout = subprocess.run('mv ./temp_results/temp_results.txt ./temp_results/'+product+'/'+product+'_results.txt', shell=True)
    stdout = subprocess.run('mv ./temp_results/console_main ./temp_results/'+product+'/'+product+'_UART_LOG', shell=True)

elif sys.argv[1] == 'finalize_kunit':
    stdout = subprocess.run('mv ./temp_results/console_main ./temp_results/Kunit_UART_LOG', shell=True)

elif sys.argv[1] == 'kernel_error':
    stderr = sys.argv[2]
    kernel_error_report(stderr)

elif sys.argv[1] == 'overlay_merger_error':
    stderr = sys.argv[2]
    overlay_merger_error_report(stderr)

elif sys.argv[1] == 'dts_error':
    product= sys.argv[2]
    dts = sys.argv[3]
    stdout = sys.argv[4]
    dts_error_report(product, dts, stdout)

elif sys.argv[1] == 'copy_results':
    timestamped_dir = sys.argv[2]
    bb_project = sys.argv[3]

    stdout = subprocess.run('cp -r temp_results/ test-results/', shell=True)
    stdout = subprocess.run('mv test-results/temp_results '+timestamped_dir+'_'+bb_project, shell=True)

elif sys.argv[1] == 'bisect_result':
    timestamped_dir = sys.argv[2]
    bb_project = sys.argv[3]
    final_output = sys.argv[4]
    bisect_state = sys.argv[5]
    bisect_result(timestamped_dir, bb_project, final_output, bisect_state)

elif sys.argv[1] == 'publish_results_git':
    timestamp_git_dir = sys.argv[2]
    bb_project = sys.argv[3]
    branch = sys.argv[4]
    result = sys.argv[5]

    stdout = subprocess.run('mv '+timestamp_git_dir+'_'+bb_project+'/ '+timestamp_git_dir+'_'+bb_project+'_'+result+'/', shell=True)

    stdout = subprocess.run('git fetch', shell=True)
    stdout = subprocess.run('git checkout '+branch, shell=True)
    stdout = subprocess.run('git add '+timestamp_git_dir+'_'+bb_project+'_'+result+'/', shell=True)
    stdout = subprocess.run('git commit -m "Test results for: '+timestamp_git_dir+'_'+bb_project+'"', shell=True)
    stdout = subprocess.run('git push origin '+branch, shell=True)

elif sys.argv[1] == 'get_timestamp':
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    print(date)

