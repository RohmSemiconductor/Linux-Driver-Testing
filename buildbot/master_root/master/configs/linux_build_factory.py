import sys
import os
import re
sys.path.append(os.path.abspath("./configs"))

from projects import *
from paths import *
from factory_helpers import *

def check_boneblack_old_dir(step):
    if re.search('^next.*', step.getProperty('commit-description')):    #check for linux next
        return False
    else:
        git_ver = tagConvert(step.getProperty('commit-description'))
        if git_ver[0] > 6:
            return False
        elif git_ver[0] == 6:
            if math.floor(git_ver[1]) <= 1:
                return True
            else:
                return False
        else:
            return True

def extract_boneblack_dts(rc, stdout, stderr):
    if rc != 0:
        return {'boneblack_dts_failed': True, 'preparation_step_failed':True }
    if rc == 0:
        return {'preparation_step_failed':False}

def initialize_test_report(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_report", projects[project_name]['builderNames'][0], util.Property('commit-description'), util.Property('revision')],
        workdir="../tests",
        name="Initialize test report",
        doStepIf=util.Property('git_bisecting') != True
        ))

def doStepIf_dtc_boneblack(step):
    if step.getProperty('kernel_build_failed') != True:
        if check_boneblack_old_dir(step) != True:
            return True
        else:
            return False
    else:
        return False

def doStepIf_dtc_boneblack_old_dir(step):
    if step.getProperty('kernel_build_failed') != True:
        if check_boneblack_old_dir(step) == True:
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
        return {'kernel_build_failed':True, 'preparation_step_failed':True, 'kernel_error_stderr':stderr}
    if rc == 0:
        return {'preparation_step_failed':False}

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
        workdir="../tests",
        name="Write kernel make stderr to log",
        doStepIf=util.Property('kernel_build_failed') == True,
        hideStepIf=skipped
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH="+dir_nfs, "modules_install"],
        name="Install kernel modules",
        doStepIf=util.Property('kernel_build_failed') != True
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
            doStepIf=util.Property('kernel_build_failed') != True ,
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
        doStepIf=util.Property('preparation_step_failed') != True
        ))

def extract_make_overlay_merger(rc, stdout, stderr):
    if rc != 0:
        return {'overlay_merger_build_failed':True, 'preparation_step_failed':True, 'overlay_merger_stderr':stderr}
    if rc == 0:
        return {'preparation_step_failed':False}

def build_overlay_merger(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["make"],
        env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./'},
        workdir="build/_test-kernel-modules/overlay_merger",
        name="Build test kernel module: overlay_merger",
        hideStepIf=skipped,
        extract_fn=extract_make_overlay_merger,
        doStepIf=util.Property('preparation_step_failed') != True
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "overlay_merger_error", util.Property('overlay_merger_error_stderr')],
        workdir="../tests",
        name="Write overlay merger make stderr to log",
        doStepIf=util.Property('overlay_merger_build_failed') == True,
        hideStepIf=skipped
        ))


def copy_overlay_merger_to_nfs(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["cp", "_test-kernel-modules/overlay_merger/mva_overlay.ko", dir_nfs],
        name="Copy overlay merger to nfs",
        hideStepIf=skipped,
        doStepIf=util.Property('preparation_step_failed') != True
        ))

def extract_get_timestamp(rc, stdout, stderr):
    stdout = stdout.split('\n')
    return {'timestamp':stdout[0], 'timestamped_dir':'test-results/'+stdout[0]}


def get_timestamp(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["python3", "report_janitor.py", "get_timestamp"],
        workdir="../tests",
        name="Set timestamp property for results",
        extract_fn=extract_get_timestamp,
        doStepIf=util.Property('git_bisecting') != True
        ))

def extract_check_iio_generic_buffer(rc, stdout, stderr):
    if 'FAILURES' in stdout:
        return { 'iio_generic_buffer_found': False }
    else:
        return { 'iio_generic_buffer_found': True }

def doStepIf_trigger_sensor_factory(step):
    if step.getProperty('preparation_step_failed') == False and step.getProperty('iio_generic_buffer_found') == True:
        return True
    else:
        return False

def trigger_sensor_factory(project_name):
        projects[project_name]['factory'].addStep(steps.Trigger(
            schedulerNames=['scheduler-accelerometer_tests'],
            updateSourceStamp=True,
            name="Trigger accelerometer tests",
            set_properties= {
                #'git_bisecting':True,
               # 'git_bisect_state':'running',
                'commit-description':util.Property('commit-description'),
             #   'timestamped_dir':util.Property('timestamped_dir'),
                'factory_type':'accelerometer',
                'timestamp':util.Property('timestamp'),
                'linuxdir':util.Property('buildername'),
              #  'RESULT':'FAILED',
                },
            doStepIf = doStepIf_trigger_sensor_factory
            ))

def trigger_pmic_factory(project_name):
        projects[project_name]['factory'].addStep(steps.Trigger(
            schedulerNames=['scheduler-pmic_tests'],
            updateSourceStamp=True,
            name="Trigger PMIC tests",
            set_properties= {
                #'git_bisecting':True,
               # 'git_bisect_state':'running',
                'commit-description':util.Property('commit-description'),
             #   'timestamped_dir':util.Property('timestamped_dir'),
                'factory_type':'PMIC',
                'timestamp':util.Property('timestamp'),
                'linuxdir':util.Property('buildername'),
              #  'RESULT':'FAILED',
                },
            doStepIf = util.Property('preparation_step_failed') != False
            ))

def download_test_boards(project_name):
    projects[project_name]['factory'].addStep(steps.FileDownload(
        mastersrc="configs/kernel_modules.py",
        workerdest="../../tests/pmic/configs/kernel_modules.py",
        name="Download kernel_modules.py",
        doStepIf=util.Property('preparation_step_failed') != True
        ))

def copy_results_for_factories(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_factories"],
        name="Copy result files to factories",
        workdir="../tests",
        ))

def sanity_checks(project_name):
    power_port = list(test_boards['accelerometer']['power_ports'])[0]
    test_board = list(test_boards['accelerometer']['power_ports'][power_port])[0]


    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra",
                "test_000_no_ippower_login.py",
                "--power_port="+power_port,
                "--beagle="+test_boards['accelerometer']['power_ports'][power_port][test_board]['name']],

        workdir="../tests/pmic",
        name="Login to "+test_boards['accelerometer']['power_ports'][power_port][test_board]['name']
        ))

    ### Check for iio_generic_buffer
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning",
                "test_000_check_iio_generic_buffer.py",
                "--lg-log", "../temp_results/",
                "--lg-env", test_boards['accelerometer']['power_ports'][power_port][test_board]['name']+".yaml",
                "--power_port="+power_port,
                "--beagle="+test_boards['accelerometer']['power_ports'][power_port][test_board]['name']],
        workdir="../tests/pmic",
        name="Check for iio_generic_buffer",
        doStepIf=util.Property('preparation_step_failed') != False,
        hideStepIf=skipped,
        extract_fn=extract_check_iio_generic_buffer
        ))

    ### Kunit test_linear_ranges test
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=[
        'pytest','--lg-log', "../temp_results/",
        '--lg-env='+test_board+".yaml",
        'test_get_kunit.py',
        '--kunit_test=test_linear_ranges'],
        workdir="../tests/pmic/",
        extract_fn=extract_kunit_test_error,
        doStepIf=doStepIf_kunit_tests,
        hideStepIf=skipped,
        name="Kunit linear ranges test"
        ))

    ### Kunit iio_test_gets
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=['pytest','--lg-log', "../temp_results/",
        '--lg-env='+test_board+".yaml",
        'test_get_kunit.py',
        '--kunit_test=iio_test_gts'],
        workdir="../tests/pmic/",
        extract_fn=extract_kunit_test_error,
        doStepIf=doStepIf_kunit_iio_gts_test,
        hideStepIf=skipped,
        name="Kunit IIO GTS test"
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "finalize_kunit"],
        workdir="../tests",
        name="Rename kunit UART log",
        doStepIf=util.Property('kunit_login_tried') == True,
        hideStepIf=skipped
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra",
                 "test_005_powerdown_beagle.py",
                 "--power_port="+power_port,
                 "--beagle="+test_board],
        workdir="../tests/pmic/",
        doStepIf=util.Property('kunit_login_tried') == True,
        hideStepIf=skipped,
        name="Power down beagle"
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
    ### Sanitycheks
    sanity_checks(project_name)
    ### Prepare and trigger
    copy_results_for_factories(project_name)
    trigger_sensor_factory(project_name)

build_deploy_kernel('test_linux')
