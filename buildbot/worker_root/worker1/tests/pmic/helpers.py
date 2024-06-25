import operator

def checkStdOut(stdout,checkString):
    if any(checkString in s for s in stdout):
        return 0

def checkStr(stdout,checkString):
    if checkString in stdout:
        return 0

def initialize_report(bb_project):
    report_file = open('../results/temp_results.txt', 'w+', encoding='utf-8')
    print("BuildBot project: "+bb_project+"\n", end='', file=report_file)
    report_file.close()

#### Generic steps
def login_fail(power_port, beagle):
    report_file = open('../results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Login failed: Power port:"+power_port+" BeagleBone: "+beagle+"\n\n", end='', file=report_file)
    report_file.close()

def init_overlay_fail():
    report_file = open('../results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print("Installing overlay merger failed! This step is common to all PMICs.\n\n", end='', file=report_file)
    print("\n", end='', file=report_file)
    report_file.close()

def merge_dt_overlay_fail(product, dt_overlay):
    report_file = open('../results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print(product, ": Merge device tree overlay failed: "+dt_overlay+" module missing (lsmod) \n\n", end='', file=report_file)
    report_file.close()

def insmod_fail(product, insmod):
    report_file = open('../results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    print(product, ": insmod failed: "+insmod+" module missing (lsmod) \n\n", end='', file=report_file)
    report_file.close()

def generic_step_fail(tf, power_port=None, beagle=None, product=None,dt_overlay=None, insmod=None):
    report_file = open('../results/temp_results.txt', 'a', encoding='utf-8')
    report_file.seek(0,2)
    if tf == "login":
        print("Login failed: Power port:"+power_port+" BeagleBone: "+beagle+"\n\n", end='', file=report_file)

    elif tf == "init_overlay":
        print("Installing overlay merger failed! This step is common to all PMICs.\n\n", end='', file=report_file)

    elif tf == "insmod":
        print(product, ": insmod failed: "+insmod+" module missing (lsmod) \n\n", end='', file=report_file)

    elif tf == "dt_overlay":
        print(product, ": Merge device tree overlay failed: "+dt_overlay+" module missing (lsmod) \n\n", end='', file=report_file)

    report_file.close()

def generate_test_report(stage, regulator=None):
    pass
