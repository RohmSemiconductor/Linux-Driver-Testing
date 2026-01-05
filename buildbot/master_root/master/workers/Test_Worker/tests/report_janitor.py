import sys
import os
import subprocess
from datetime import datetime, timezone
from time import sleep
sys.path.append('.')
from test_util import initialize_report, initialize_product, finalize_product, dts_error_report, kernel_error_report, bisect_result, overlay_merger_error_report, chipselect_makedtb_error_report

if sys.argv[1] == 'initialize_report':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    revision = sys.argv[4]
    stdout = subprocess.run('mkdir -p /tmp/rohm_linux_driver_tests/', shell=True)

    stdout = subprocess.run('rm -rf /tmp/rohm_linux_driver_tests/temp_results/', shell=True)
    stdout = subprocess.run('mkdir /tmp/rohm_linux_driver_tests/temp_results', shell=True)

    stdout = subprocess.run('rm -rf /tmp/rohm_linux_driver_tests/temp_results_PMIC/', shell=True)
    stdout = subprocess.run('mkdir /tmp/rohm_linux_driver_tests/temp_results_PMIC', shell=True)

    stdout = subprocess.run('rm -rf /tmp/rohm_linux_driver_tests/temp_results_sensor/', shell=True)
    stdout = subprocess.run('mkdir /tmp/rohm_linux_driver_tests/temp_results_sensor', shell=True)

    stdout = subprocess.run('rm -rf /tmp/rohm_linux_driver_tests/temp_results_ADDAC/', shell=True)
    stdout = subprocess.run('mkdir /tmp/rohm_linux_driver_tests/temp_results_ADDAC', shell=True)
    initialize_report(bb_project, linux_ver, revision)

elif sys.argv[1] == 'initialize_factories':
    stdout = subprocess.run('cp -r /tmp/rohm_linux_driver_tests/temp_results/* /tmp/rohm_linux_driver_tests/temp_results_PMIC/', shell=True)
    stdout = subprocess.run('cp -r /tmp/rohm_linux_driver_tests/temp_results/* /tmp/rohm_linux_driver_tests/temp_results_sensor/', shell=True)
    stdout = subprocess.run('cp -r /tmp/rohm_linux_driver_tests/temp_results/* /tmp/rohm_linux_driver_tests/temp_results_ADDAC/', shell=True)

elif sys.argv[1] == 'initialize_product':
    type = sys.argv[2]
    product = sys.argv[3]
    stdout = subprocess.run('mkdir /tmp/rohm_linux_driver_tests/temp_results_'+type+'/'+product, shell=True)
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

    stdout = subprocess.run('mv /tmp/rohm_linux_driver_tests/temp_results_'+type+'/temp_results.txt /tmp/rohm_linux_driver_tests/temp_results_'+type+'/'+product+'/'+product+'_results.txt', shell=True)
    stdout = subprocess.run('mv /tmp/rohm_linux_driver_tests/temp_results_'+type+'/console_main /tmp/rohm_linux_driver_tests/temp_results_'+type+'/'+product+'/'+product+'_UART_LOG', shell=True)

elif sys.argv[1] == 'finalize_sanitychecks':
    stdout = subprocess.run('mv /tmp/rohm_linux_driver_tests/temp_results/console_main /tmp/rohm_linux_driver_tests/temp_results/sanitychecks_UART_LOG', shell=True)

elif sys.argv[1] == 'kernel_error':
    stderr = sys.argv[2]
    kernel_error_report(stderr)

elif sys.argv[1] == 'overlay_merger_error':
    stderr = sys.argv[2]
    overlay_merger_error_report(stderr)

elif sys.argv[1] == 'chipselect_makedtb_error':
    stderr = sys.argv[2]
    chipselect_makedtb_error_report(stderr)

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
        stdout = subprocess.run('cp -r /tmp/rohm_linux_driver_tests/temp_results_sensor/ test-results/Sensor/', shell=True)
        stdout = subprocess.run('mv test-results/Sensor/temp_results_sensor/ test-results/Sensor/'+timestamped_dir+'_'+bb_project, shell=True)

    elif (factory_type == 'pmic'):
        stdout = subprocess.run('cp -r /tmp/rohm_linux_driver_tests/temp_results_PMIC/ test-results/PMIC', shell=True)
        stdout = subprocess.run('mv test-results/PMIC/temp_results_PMIC/ test-results/PMIC/'+timestamped_dir+'_'+bb_project, shell=True)

    elif (factory_type == 'addac'):
        stdout = subprocess.run('cp -r /tmp/rohm_linux_driver_tests/temp_results_ADDAC/ test-results/ADDAC', shell=True)
        stdout = subprocess.run('mv test-results/ADDAC/temp_results_ADDAC/ test-results/ADDAC/'+timestamped_dir+'_'+bb_project, shell=True)



elif sys.argv[1] == 'save_factory_properties':
    factory = sys.argv[2]
    try:
        os.mkdir("/tmp/rohm_linux_driver_tests/")
    except FileExistsError:
        print("tmp dir exists, proceeding...\n")
    except PermissionError:
        print("Permission denied: Unable to create /tmp/rohm_linux_driver_tests/.")
    except Exception as e:
        print(f"An error occurred: {e}")

    property_file = open('/tmp/rohm_linux_driver_tests/properties_'+factory+'.txt', 'w+',
                         encoding='utf-8')

    for x in range(3, len(sys.argv)):
        print(sys.argv[x])
        print(sys.argv[x]+'\n', end='', file=property_file)

    property_file.close()



elif sys.argv[1] == 'read_factory_properties':

    saved_properties_pmic = {
            'pmic_single_test_failed'    : '',
            'pmic_single_test_passed'    : '',
            'single_login_failed'   : '',
            'single_login_passed'   : '',
    }

    saved_properties_sensor = {
            'sensor_single_test_failed'    : '',
            'sensor_single_test_passed'    : '',
            'single_login_failed'   : '',
            'single_login_passed'   : '',
    }

    saved_properties_addac = {
            'addac_single_test_failed'    : '',
            'addac_single_test_passed'    : '',
            'single_login_failed'   : '',
            'single_login_passed'   : '',
    }

    property_files = ['properties_pmic', 'properties_sensor', 'properties_addac']

    for property_file in property_files:
        opened_file = property_file
        try:
            property_file = open('/tmp/rohm_linux_driver_tests/'+property_file+'.txt',
                                 'r', encoding='utf-8')
            for line in property_file:
                if opened_file == 'properties_pmic':
                    for property in saved_properties_pmic.keys():
                        if ((property+'=True' in line) and (saved_properties_pmic[property] =='')):
                            print(line)
                elif opened_file == 'properties_sensor':
                    for property in saved_properties_sensor.keys():
                        if ((property+'=True' in line) and (saved_properties_sensor[property] =='')):
                            print(line)
                elif opened_file == 'properties_addac':
                    for property in saved_properties_addac.keys():
                        if ((property+'=True' in line) and (saved_properties_addac[property] =='')):
                            print(line)
        except:
            print("")



elif sys.argv[1] == 'bisect_result':
    timestamp = sys.argv[2]
    bb_project = sys.argv[3]
    final_output = sys.argv[4]
    bisect_state = sys.argv[5]

    for x in range(6, len(sys.argv)):
        branch = sys.argv[x]
        bisect_result(timestamp, bb_project, final_output, bisect_state, branch)

elif sys.argv[1] == 'publish_results_git':
    timestamp_git_dir = sys.argv[2]
    bb_project = sys.argv[3]
    branch = sys.argv[4]
    if sys.argv[5] == "FAILED":
        result = sys.argv[5]
    else:
        result = sys.argv[6]

    stdout = subprocess.run('mv '+branch+'/'+timestamp_git_dir+'_'+bb_project+'/ '+branch+'/'+timestamp_git_dir+'_'+bb_project+'_'+result+'/', shell=True)

    commands = (
        'cd '+branch+'/',
        'rm -f '+timestamp_git_dir+'_'+bb_project+'_'+result+'/temp_results.txt',
        'git add .',
        'git commit -m "Test results for: '+timestamp_git_dir+'_'+bb_project+'"',
        'git fetch origin '+branch,
        'git pull origin '+branch,
        'git checkout '+branch,
        'git push origin '+branch
    )

    subprocess.run(" && ".join(commands), shell=True)

elif sys.argv[1] == 'rm_old_results':
    branch = sys.argv[2]
    days = sys.argv[3]
    old_results = []

    commands = (
        'cd '+branch+'/',
        'find ./ -maxdepth 1 -type d -ctime +'+days #mtime now, change to ctime
    )

    results_stdout = subprocess.run(" && ".join(commands), shell=True, encoding='UTF-8', stdout=subprocess.PIPE).stdout.splitlines()
    to_be_removed = " ".join(str(i) for i in results_stdout)

    if len(to_be_removed) > 0:
        stdout = subprocess.run("cd "+branch+"/ && rm -rf "+to_be_removed, shell=True)
    else:
        print("No older results than "+days+" days to remove")

elif sys.argv[1] == 'get_timestamp':
    date = datetime.now()
    date = date.strftime('%Y_%m_%d_%H%M%S')
    print(date)

