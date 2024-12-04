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
    stdout = subprocess.run('rm -rf temp_results_PMIC/', shell=True)
    stdout = subprocess.run('mkdir temp_results_PMIC', shell=True)
    stdout = subprocess.run('rm -rf temp_results_sensor/', shell=True)
    stdout = subprocess.run('mkdir temp_results_sensor', shell=True)
    initialize_report(bb_project, linux_ver, revision)

elif sys.argv[1] == 'initialize_factories':
    stdout = subprocess.run('cp -r ./temp_results/* temp_results_PMIC/', shell=True)
    stdout = subprocess.run('cp -r ./temp_results/* temp_results_sensor/', shell=True)

elif sys.argv[1] == 'initialize_product':
    type = sys.argv[2]
    product = sys.argv[3]
    stdout = subprocess.run('mkdir ./temp_results_'+type+'/'+product, shell=True)
    initialize_product(type, product)

elif sys.argv[1] == 'finalize_product':
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]

    type = sys.argv[4]
    product = sys.argv[5]
    do_steps = sys.argv[6]
    finalize_product(product, do_steps, type)

    stdout = subprocess.run('mv ./temp_results_'+type+'/temp_results.txt ./temp_results_'+type+'/'+product+'/'+product+'_results.txt', shell=True)
    stdout = subprocess.run('mv ./temp_results_'+type+'/console_main ./temp_results_'+type+'/'+product+'/'+product+'_UART_LOG', shell=True)

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
    factory_type = sys.argv[4]
    if factory_type == 'accelerometer':
        stdout = subprocess.run('cp -r temp_results_sensor/ test-results/Sensor/', shell=True)
        stdout = subprocess.run('mv test-results/Sensor/temp_results_sensor/ test-results/Sensor/'+timestamped_dir+'_'+bb_project, shell=True)

    elif (factory_type == 'PMIC'):
        stdout = subprocess.run('cp -r temp_results/ test-results/PMIC', shell=True)
        stdout = subprocess.run('mv test-results/PMIC/temp_results '+timestamped_dir+'_'+bb_project, shell=True)

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

    stdout = subprocess.run('mv '+branch+'/'+timestamp_git_dir+'_'+bb_project+'/ '+branch+'/'+timestamp_git_dir+'_'+bb_project+'_'+result+'/', shell=True)

    commands = (
        'cd '+branch+'/',
        'rm -f '+timestamp_git_dir+'_'+bb_project+'_'+result+'/temp_results.txt',
#        'git fetch origin',
#        'git checkout '+branch,
#        'git add '+timestamp_git_dir+'_'+bb_project+'_'+result+'/',
#        'git commit -m "Test results for: '+timestamp_git_dir+'_'+bb_project+'"',
#        'git push origin '+branch
    )

    subprocess.run(" && ".join(commands), shell=True)

elif sys.argv[1] == 'get_timestamp':
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    print(date)

