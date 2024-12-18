import sys
import os
import re
sys.path.append(os.path.abspath("./configs"))

from projects import *
from paths import *
from factory_helpers import *

def check_boneblack_old_dir(step):
    if re.search('^next.*', step.getProperty('commit-description')):    #check for linux next
        return 'False'
    else:
        git_ver = tagConvert(step.getProperty('commit-description'))
        if git_ver[0] > 6:
            return 'False'
        elif git_ver[0] == 6:
            if math.floor(git_ver[1]) <= 1:
                return 'True'
            else:
                return 'False'
        else:
            return 'True'

def extract_boneblack_dts(rc, stdout, stderr):
    if rc != 0:
        return {'boneblack_dts_failed': 'True', 'preparation_step_failed':'True' }
    if rc == 0:
        return {'preparation_step_failed':'False'}

def initialize_test_report(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_report", projects[project_name]['builderNames'][0], util.Property('commit-description'), util.Property('revision')],
        workdir="../../Test_Worker/tests",
        name="Initialize test report",
        doStepIf=util.Property('git_bisecting') != 'True'
        ))

def doStepIf_dtc_boneblack(step):
    if step.getProperty('kernel_build_failed') != 'True':
        if check_boneblack_old_dir(step) != 'True':
            return True
        else:
            return False
    else:
        return False

def doStepIf_dtc_boneblack_old_dir(step):
    if step.getProperty('kernel_build_failed') != 'True':
        if check_boneblack_old_dir(step) == 'True':
            return True
        else:
            return False
    else:
        return False

def doStepIf_linux_stable_copy_config(step, project_name, branch):
    if step.getProperty('branch') == branch:
        return True
    else:
        return False

def extract_make_kernel(rc, stdout, stderr):
    if rc != 0:
        return {'kernel_build_failed':'True', 'preparation_step_failed':'True', 'kernel_error_stderr':stderr}
    if rc == 0:
        return {'preparation_step_failed':'False'}

def build_kernel_arm32(project_name):
    projects[project_name]['factory'].addStep(steps.Git(
        repourl=projects[project_name]['repo_git'],
        mode='incremental',
        getDescription={'tags':True},
        name="Update linux source files from git",
        tags=True,
        doStepIf=util.Property('git_bisect_state') != 'running'
        ))

    initialize_test_report(project_name)

    if project_name == 'linux_stable':
        for branch in projects[project_name]['branches']:
            doStepIf_linux_stable_copy_config_partial = functools.partial(doStepIf_linux_stable_copy_config, project_name=project_name, branch=branch)
            projects[project_name]['factory'].addStep(steps.FileDownload(
                mastersrc="../../../compilers/kernel_configs/arm32_bbb_"+branch+".config",
                workerdest=".config",
                name="Copy "+branch+" config to build directory",
                doStepIf=doStepIf_linux_stable_copy_config_partial,
                hideStepIf=skipped
                ))

    else:
        projects[project_name]['factory'].addStep(steps.FileDownload(
            mastersrc="../../../compilers/kernel_configs/arm32_bbb_linux_mainline.config",
            workerdest=".config",
            name="Copy mainline kernel config to build directory"
            ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],
        name="Update kernel config if needed"
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["ccache", "make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000"],
        name="Build kernel binaries",
        extract_fn=extract_make_kernel
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "kernel_error", util.Property('kernel_error_stderr')],
        workdir="../../Test_Worker/tests",
        name="Write kernel make stderr to log",
        doStepIf=util.Property('kernel_build_failed') == 'True',
        hideStepIf=skipped
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH="+dir_nfs, "modules_install"],
        name="Install kernel modules",
        doStepIf=util.Property('kernel_build_failed') != 'True'
        ))

    if project_name == 'linux_rohm_devel':
        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"],
            name="Build Beagle device tree source binaries",
            extract_fn=extract_boneblack_dts,
            ))
    else:
        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"],
            name="Build Beagle device tree source binaries",
            extract_fn=extract_boneblack_dts,
            hideStepIf=skipped,
            doStepIf=doStepIf_dtc_boneblack,
            ))

        ### For Linux version <= 6.1
        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "arch/arm/boot/dts/am335x-boneblack.dtb", "arch/arm/boot/dts/.am335x-boneblack.dtb.dts.tmp"],
            name="Build Beagle device tree source binaries(old dir)",
            extract_fn=extract_boneblack_dts,
            hideStepIf=skipped,
            doStepIf=doStepIf_dtc_boneblack_old_dir
            ))

def copy_kernel_binaries_to_tftpboot(project_name):
    if project_name == 'linux_rohm_devel':
        projects[project_name]['factory'].addStep(steps.ShellSequence(
            commands=[
            util.ShellArg(command=['cp',"arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_tftpboot], logname='Copy BeagleBone .dtb to tftpboot'),
            util.ShellArg(command=['cp',"arch/arm/boot/zImage", dir_tftpboot], logname='Copy zImage to tftpboot')
            ],
            name="Copy kernel binaries to tftpboot",
            doStepIf=util.Property('kernel_build_failed') != 'True' ,
            hideStepIf=skipped
            ))
    else:
        projects[project_name]['factory'].addStep(steps.ShellSequence(
            commands=[
            util.ShellArg(command=['cp',"arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_tftpboot], logname='Copy BeagleBone .dtb to tftpboot'),
            util.ShellArg(command=['cp',"arch/arm/boot/zImage", dir_tftpboot], logname='Copy zImage to tftpboot')
            ],
            name="Copy kernel binaries to tftpboot",
            doStepIf=doStepIf_dtc_boneblack,
            hideStepIf=skipped
            ))

             ### For Linux version <= 6.1
        projects[project_name]['factory'].addStep(steps.ShellSequence(
            commands=[
            util.ShellArg(command=['cp',"arch/arm/boot/dts/am335x-boneblack.dtb", dir_tftpboot], logname='Copy BeagleBone .dtb to tftpboot'),
            util.ShellArg(command=['cp',"arch/arm/boot/zImage", dir_tftpboot], logname='Copy zImage to tftpboot')
            ],
            name="Copy kernel binaries to tftpboot(old dir)",
            doStepIf=doStepIf_dtc_boneblack_old_dir,
            hideStepIf=skipped
            ))

def update_test_kernel_modules(project_name):
    projects[project_name]['factory'].addStep(steps.Git(
        repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git',
        branch='dev-test-kernel-modules',
        alwaysUseLatest=True,
        mode='full',
        workdir="build/_test-kernel-modules",
        name="Update kernel module source files from git",
        hideStepIf=skipped,
        doStepIf=util.Property('preparation_step_failed') != 'True'
        ))

def extract_make_overlay_merger(rc, stdout, stderr):
    if rc != 0:
        return {'overlay_merger_build_failed':'True', 'preparation_step_failed':'True', 'overlay_merger_stderr':stderr}
    if rc == 0:
        return {'preparation_step_failed':'False'}

def build_overlay_merger(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["make"],
        env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./'},
        workdir="build/_test-kernel-modules/overlay_merger",
        name="Build test kernel module: overlay_merger",
        hideStepIf=skipped,
        extract_fn=extract_make_overlay_merger,
        doStepIf=util.Property('preparation_step_failed') != 'True'
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "overlay_merger_error", util.Property('overlay_merger_error_stderr')],
        workdir="../../Test_Worker/tests",
        name="Write overlay merger make stderr to log",
        doStepIf=util.Property('overlay_merger_build_failed') == 'True',
        hideStepIf=skipped
        ))


def copy_overlay_merger_to_nfs(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["cp", "_test-kernel-modules/overlay_merger/mva_overlay.ko", dir_nfs],
        name="Copy overlay merger to nfs",
        hideStepIf=skipped,
        doStepIf=util.Property('preparation_step_failed') != 'True'
        ))

def extract_get_timestamp(rc, stdout, stderr):
    stdout = stdout.split('\n')
    return {'timestamp':stdout[0], 'timestamped_dir':'test-results/'+stdout[0]}


def get_timestamp(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["python3", "report_janitor.py", "get_timestamp"],
        workdir="../../Test_Worker/tests",
        name="Set timestamp property for results",
        extract_fn=extract_get_timestamp,
        doStepIf=util.Property('git_bisecting') != 'True'
        ))

def doStepIf_trigger_sensor_factory(step):
    if step.getProperty('preparation_step_failed') == 'False' and step.getProperty('iio_generic_buffer_found') == 'True':
        return True
    else:
        return False

def trigger_test_factories(project_name):
        projects[project_name]['factory'].addStep(steps.Trigger(
            schedulerNames=['scheduler-accelerometer_tests', 'scheduler-pmic_tests'],
            updateSourceStamp=True,
            name="Trigger test factories",
            waitForFinish = True,
            set_properties= {
                'iio_generic_buffer_found':util.Property('iio_generic_buffer_found'),
                'preparation_step_failed':util.Property('preparation_step_failed'),
                'git_bisecting':util.Property('git_bisecting'),
                'commit-description':util.Property('commit-description'),
                'factory_type':'accelerometer',
                'timestamp':util.Property('timestamp'),
                'linuxdir':util.Property('buildername'),
                },
            ))

def download_test_boards(project_name):
    projects[project_name]['factory'].addStep(steps.FileDownload(
        mastersrc="configs/kernel_modules.py",
        workerdest="../../../Test_Worker/tests/pmic/configs/kernel_modules.py",
        name="Download kernel_modules.py",
        doStepIf=util.Property('preparation_step_failed') != 'True'
        ))

def copy_results_for_factories(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_factories"],
        name="Copy result files to factories",
        workdir="../../Test_Worker/tests",
        ))

def sanity_checks(project_name):
    board_type = list(test_boards.keys())[0]
    power_port = list(test_boards[board_type]['power_ports'])[0]
    test_board = list(test_boards[board_type]['power_ports'][power_port])[0]


    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra",
                "test_000_no_ippower_login.py",
                "--power_port="+power_port,
                "--beagle="+test_boards[board_type]['power_ports'][power_port][test_board]['name']],

        workdir="../../Test_Worker/tests/pmic",
        name="Login to "+test_boards[board_type]['power_ports'][power_port][test_board]['name'],
        doStepIf=util.Property('preparation_step_failed') != False,
        hideStepIf=skipped,
        extract_fn=extract_sanitycheck_login
        ))

    ### Check for iio_generic_buffer
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning",
                "test_000_check_iio_generic_buffer.py",
                "--lg-log", "/tmp/rohm_linux_driver_tests/temp_results/",
                "--lg-env", test_boards[board_type]['power_ports'][power_port][test_board]['name']+".yaml",
                "--power_port="+power_port,
                "--beagle="+test_boards[board_type]['power_ports'][power_port][test_board]['name']],
        workdir="../../Test_Worker/tests/pmic",
        name="Check for iio_generic_buffer",
        doStepIf=util.Property('preparation_step_failed') != 'True',
        hideStepIf=skipped,
        extract_fn=extract_check_iio_generic_buffer
        ))

    ### Kunit test_linear_ranges test
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=[
        'pytest','--lg-log', "/tmp/rohm_linux_driver_tests/temp_results/",
        '--lg-env='+test_board+".yaml",
        'test_get_kunit.py',
        '--kunit_test=test_linear_ranges'],
        workdir="../../Test_Worker/tests/pmic/",
        extract_fn=extract_kunit_test_error,
        doStepIf=doStepIf_kunit_tests,
        hideStepIf=skipped,
        name="Kunit linear ranges test"
        ))

    ### Kunit iio_test_gts
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=['pytest','--lg-log', "/tmp/rohm_linux_driver_tests/temp_results/",
        '--lg-env='+test_board+".yaml",
        'test_get_kunit.py',
        '--kunit_test=iio_test_gts'],
        workdir="../../Test_Worker/tests/pmic/",
        extract_fn=extract_kunit_test_error,
        doStepIf=doStepIf_kunit_iio_gts_test,
        hideStepIf=skipped,
        name="Kunit IIO GTS test"
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "finalize_sanitychecks"],
        workdir="../../Test_Worker/tests",
        name="Rename sanity check UART log",
        doStepIf=util.Property('sanitycheck_login_tried') == 'True',
        hideStepIf=skipped
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra",
                 "test_005_powerdown_beagle.py",
                 "--power_port="+power_port,
                 "--beagle="+test_board],
        workdir="../../Test_Worker/tests/pmic/",
        doStepIf=util.Property('kunit_login_tried') == 'True',
        hideStepIf=skipped,
        name="Power down beagle"
        ))

def publish_results_git_sensor(project_name, branch_dir):
    projects[project_name]['factory'].addStep(steps.SetProperty(
        name="Tests: FAILED",
        property="RESULT",
        value="FAILED",
        doStepIf=doStepIf_setProperty_RESULT_FAILED,
        hideStepIf=skipped
        ))

    projects[project_name]['factory'].addStep(steps.SetProperty(
        name="Tests: PASSED",
        property="RESULT",
        value="PASSED",
        doStepIf=doStepIf_setProperty_RESULT_PASSED,
        hideStepIf=skipped
        ))


    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "../report_janitor.py", "publish_results_git",
                 util.Property('timestamp'), util.Property('buildername'),
                 branch_dir, util.Property('RESULT')],
        name="Publish results to github.com",
        workdir="../../Test_Worker/tests/test-results",
        doStepIf=doStepIf_git_push,
        ))

#### Git bisect helpers
def doStepIf_good_commit_write(step):
    if step.getProperty('git_bisecting') != "True":
        if step.getProperty('preparation_step_failed') == "True":
            return False
        elif (not step.getProperty('single_test_failed') and step.getProperty('single_test_passed')):
            return True
        else:
            return False
    else:
        return False

def extract_git_get_current_commit(rc, stdout, stderr):
    return {'current_git_commit':stdout}

def save_good_commit(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["git", "rev-parse", "HEAD"],
        workdir="build",
        name= "Get commit hash for git bisect good",
        extract_fn=extract_git_get_current_commit,
        doStepIf=doStepIf_good_commit_write
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "bisect_good_commit.py", "write", projects[project_name]['name'], util.Property('branch'), util.Property('current_git_commit')],
        name="Save commit hash to file",
        workdir="../../Test_Worker/tests",
        doStepIf=doStepIf_good_commit_write
        ))

def doStepIf_git_bisect_start(step):
    if not step.getProperty('git_bisecting'):
        if step.getProperty('preparation_step_failed') == "True":
            return True
        elif step.getProperty('single_test_failed') == "True":
            return True
        elif step.getProperty('single_login_failed') == "True":
            if step.getProperty('single_login_passed') == "True":
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def doStepIf_git_bisect_good(step):
    if step.getProperty('git_bisecting') == "True":
        if step.getProperty('preparation_step_failed') == "True":
            return False
        elif (not step.getProperty('single_test_failed') and (step.getProperty('single_test_passed') == "True")):
            if step.getProperty('single_login_failed') == "True":
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def doStepIf_git_bisect_bad(step):
    if step.getProperty('preparation_step_failed') == "True":
        return True
    elif step.getProperty('single_test_failed') == "True":
        return True
    elif step.getProperty('single_login_failed') == "True":
        if step.getProperty('single_login_passed') == "True":
            return False
        else:
            return True
    else:
        return False

def doStepIf_git_bisect_trigger(step):
    if step.getProperty('git_bisect_state') == 'failed':
        return False
    elif step.getProperty('git_bisect_state') == 'success':
        return False
    elif step.getProperty('git_bisect_state') == 'cannot_start':
        return False
    elif step.getProperty('git_bisect_state') == 'running':
        return True
    elif step.getProperty('preparation_step_failed') == "True":
        return True
    elif step.getProperty('single_test_failed') == "True":
        return True
    elif step.getProperty('single_login_failed') == "True":
        if step.getProperty('single_login_passed') == "True":
            return False
        else:
            return True
    else:
        return False

def doStepIf_git_bisect_report(step):
    if step.getProperty('git_bisect_state') == 'success':
        return True
    elif step.getProperty('git_bisect_state') == 'cannot_start':
        return True
    elif step.getProperty('git_bisect_state') == 'failed':
        return True
    else:
        return False

def extract_fn_read_good_commit(rc, stdout, stderr):
    if rc == 0:
        stdout = stdout.split('\n')
        return {'good_commit':stdout[0]}
    elif rc != 0:
        return {'no_good_commmit':True, 'no_good_commit_reason':stdout}

def extract_git_bisect_output(rc, stdout, stderr):
    if rc != 0:
        return {'git_bisecting': False, 'git_bisect_failed':True, 'git_bisect_output':stdout, 'git_bisect_state':'failed'}
    elif rc == 0:
        # Git bisect needs atleast 1 good and bad commit for the command to start returning commits to test
        if (('waiting for both good and bad commits' in stdout) or ('waiting for bad commit' in stdout) or ('waiting for good commit' in stdout)):
            return {'git_bisecting': False, 'git_bisect_output':stdout, 'git_bisect_state': 'cannot_start'}
        # '...revisions left to test aftert this....' is a printed when bisect is running and 'git bisect good/bad' is given
        elif 'revisions left to test after this' in stdout:
            return {'git_bisecting': "True" , 'git_bisect_output':stdout, 'git_bisect_state': 'running'}
        elif 'revision left to test after this' in stdout:
            return {'git_bisecting': "True" , 'git_bisect_output':stdout, 'git_bisect_state': 'running'}
        elif 'a merge base must be tested' in stdout:
            return {'git_bisecting': "True" , 'git_bisect_output':stdout, 'git_bisect_state': 'running'}
        # '...is the first bad commit' is printed after final 'git bisect good/bad'
        elif 'is the first bad commit' in stdout:
            return {'git_bisecting': False, 'git_bisect_output':stdout, 'git_bisect_state': 'success'}
        else:
            return {'git_bisect_wtf_stdout': stdout, 'git_bisect_wtf_rc':rc,'git_bisect_wtf_stder':stderr, 'git_bisect_output':stdout, 'git_bisect_state':'failed'}
#### /Git bisect helpers

def git_bisect(project_name):
    if project_name != 'linux-next' and project_name != 'linux_stable':
        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=['git','bisect','start'],
            workdir="build",
            name="Git bisect: start",
            doStepIf=doStepIf_git_bisect_start
            ))

        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=["python3", "bisect_good_commit.py", "read", projects[project_name]['name'], util.Property('branch')],
            name="Get good commit hash from file",
            workdir="../../Test_Worker/tests",
            doStepIf=doStepIf_git_bisect_start,
            extract_fn=extract_fn_read_good_commit
            ))

        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=['git','bisect','good', util.Property('good_commit')],
            workdir="build",
            name="Git bisect: start good",
            extract_fn=extract_git_bisect_output,
            doStepIf=doStepIf_git_bisect_start
            ))

        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=['git','bisect','good'],
            workdir="build",
            name="Git bisect: good",
            extract_fn=extract_git_bisect_output,
            doStepIf=doStepIf_git_bisect_good
            ))

        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
            command=['git','bisect','bad'],
            workdir="build",
            name="Git bisect: bad",
            extract_fn=extract_git_bisect_output,
            doStepIf=doStepIf_git_bisect_bad
            ))

        projects[project_name]['factory'].addStep(steps.Trigger(
            schedulerNames=['git_bisect_'+projects[project_name]['scheduler_name']],
            updateSourceStamp=True,
            name="Trigger git bisect",
            set_properties= {
                'git_bisecting':'True',
                'git_bisect_state':'running',
                'commit-description':util.Property('commit-description'),
                'timestamped_dir':util.Property('timestamped_dir'),
                'timestamp':util.Property('timestamp'),
                'RESULT':'FAILED',
                },
            doStepIf=doStepIf_git_bisect_trigger
            ))

        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "bisect_result",
                     util.Property('timestamp'),
                     projects[project_name]['builderNames'][0],
                     util.Property("git_bisect_output"),
                     util.Property("git_bisect_state"),
                     "PMIC",
                     "Sensor"
                     ],
            name="Report git bisect results",
            workdir="../../Test_Worker/tests",
            doStepIf=doStepIf_git_bisect_report
            ))

        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=["git", "bisect", "reset"],
            name="Git bisect reset",
            workdir="build",
            doStepIf=doStepIf_git_bisect_report
            ))

def extract_get_factory_properties(rc, stdout, stderr):
    extracted_factory_properties = {}
    lines = stdout.split('\n')
    for line in lines:
        prop = line.split('=',2)
        prop_key = prop[0]
        prop_val = prop[-1]
        prop_val = prop_val.split('\n',1)
        prop_val = prop_val[0]
        extracted_factory_properties[str(prop_key)] = str(prop_val)
    return extracted_factory_properties



def get_factory_properties(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command = ['python3', 'report_janitor.py', 'read_factory_properties'],
        workdir = '../../Test_Worker/tests',
        extract_fn = extract_get_factory_properties
        ))

def build_deploy_kernel(project_name):

    ### Build and deploy
    build_kernel_arm32(project_name)
    copy_kernel_binaries_to_tftpboot(project_name)
    update_test_kernel_modules(project_name)
    build_overlay_merger(project_name)
    copy_overlay_merger_to_nfs(project_name)

    get_timestamp(project_name)
    download_test_boards(project_name)
    ### Sanitychecks
    sanity_checks(project_name)
    ### Prepare and trigger
    copy_results_for_factories(project_name)
    trigger_test_factories(project_name)
    get_factory_properties(project_name)
    save_good_commit(project_name)
    git_bisect(project_name)
    publish_results_git_sensor(project_name, 'Sensor')
    publish_results_git_sensor(project_name, 'PMIC')

for stable_branch in stable_branches:
    stable_branch = stable_branch.replace(".","_")
    build_deploy_kernel('linux_stable_'+stable_branch)

build_deploy_kernel('test_linux')
build_deploy_kernel('linux-next')
