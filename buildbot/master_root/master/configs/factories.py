####### FACTORIES
import functools
from buildbot.plugins import util, steps


### HELPERS
factory_test_linux = util.BuildFactory()
factory_linux_next = util.BuildFactory()
factory_linux_mainline = util.BuildFactory()
factory_linux_stable = util.BuildFactory()
factory_linux_rohm_devel = util.BuildFactory()

beagle_power_port1 = "1"
beagle_power_port2 = "2"
beagle_power_port3 = "3"
beagle_power_port4 = "4"
import math
import sys 
import os
sys.path.append(os.path.abspath("./configs"))

from kernel_modules import *
from projects import * 
from paths import *
from test_boards import *
import re

def skipped(results, build):
  return results == 3

def isFloat(check):
    if type(check) == str:
        if '.' in check:
            return True
        else:
            return False
    if type(check)==int:
        return False

def tagConvert(tagS):
    tagL = tagS.replace("v","")
    tagL = tagL.split(".",1)
    for e in range(len(tagL)):
        if isFloat(tagL[e]) == True:
            tagL[e]=float(tagL[e])
        if isFloat(tagL[e]) == False:
            tagL[e]=int(tagL[e])
    return tagL

def check_tag(step,target):
    if re.search('^next.*', step.getProperty('commit-description')):    #check for linux next 
        print(step.getProperty('commit-description'))
        return True
    elif re.search('^'+target, step.getProperty('commit-description')): #check for driver fix
        return True

    else:
        target_ver = tagConvert(kernel_modules['linux_ver'][target][0])
        git_ver = tagConvert(step.getProperty('commit-description'))
        if target_ver[0] < git_ver[0]: #git bigger pass
            return True
        elif target_ver[0] > git_ver[0]: #target_ver bigger fail
            return False
        elif target_ver[0] == git_ver[0]: #same
            if type(target_ver[0])== int:
                if target_ver[1] <= math.floor(git_ver[1]): #same pass
                    return True
                else:
                    return False                            #same fail
            else:
                if target_ver[1]<=git_ver[1]:                #linux stable of same version or bigger
                    return True
                else:
                    return False

#         or re.search('^v('+kernel_modules['linux_ver'][target][0]+'.*$|[6-9]\\.[0-9]|[6-9]\\.[0-9\\].*$){1,2}(-rc[1-9][0-9]?)?$',step.getProperty('commit-description')):
def build_kernel_arm32(project_name):
    projects[project_name]['factory'].addStep(steps.Git(repourl=projects[project_name]['repo_git'], mode='incremental', getDescription={'tags':True},name="Update linux source files from git")) #source files
#    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["echo", util.Property('commit-description')],name="TEST property"))

    projects[project_name]['factory'].addStep(steps.FileDownload(mastersrc="../../../compilers/kernel_configs/arm32.config",workerdest=".config",name="Copy kernel config to build directory"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],name="Update kernel config if needed"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000"],name="Build kernel binaries"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH="+dir_nfs, "modules_install"],name="Install kernel modules"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", dir_worker_root+projects[project_name]['workerNames'][0]+"/"+projects[project_name]['builderNames'][0]+"/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_worker_root+projects[project_name]['workerNames'][0]+"/"+projects[project_name]['builderNames'][0]+"/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"],name="Build device tree source binaries"))

def build_test_kernel_modules(project_name):
    projects[project_name]['factory'].addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test-kernel-modules', alwaysUseLatest=True, mode='full', workdir="build/_test-kernel-modules", name="Update kernel module source files from git"))
    for key in kernel_modules['build']:
        projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./'}, workdir="build/_test-kernel-modules/"+key, name="Build test kernel modules: "+key))

def upload_kernel_binaries(project_name):
     projects[project_name]['factory'].addStep(steps.MultipleFileUpload(workersrcs=["arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/zImage"],
                                   masterdest=dir_tftpboot,
                                   mode=0o644,name="Upload compiled kernel binaries to tftp directory"))

def upload_test_kernel_modules(project_name):
    files = []
    for key in kernel_modules['build']:
        for value in kernel_modules['build'].get(key):
            files.append("_test-kernel-modules/"+key+"/"+value)
    projects[project_name]['factory'].addStep(steps.MultipleFileUpload(workersrcs=files,
    masterdest=dir_nfs,
    name="Upload test kernel modules to nfs directory"
))

def download_test_boards(project_name):
    projects[project_name]['factory'].addStep(steps.FileDownload(mastersrc="configs/kernel_modules.py",
                            workerdest="../../tests/driver_tests/kernel_modules.py",
                            name="Download kernel_modules.py"))

def run_driver_tests(project_name):
    for test_board in test_boards:
        for target in test_boards[test_board]['targets']:
            check_tag_partial=functools.partial(check_tag, target=target)

            #projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "test_powercycle.py","--power_port="+test_boards[test_board]['power_port']], workdir="../tests/driver_tests", name=target+": Powercycle "+test_boards[test_board]['name']))
            #projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning", "--lg-env", test_boards[test_board]['name']+".yaml", "test_shell.py"], workdir="../tests/driver_tests", name=target+": Login to "+test_boards[test_board]['name']))

            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning", "-ra", "test_login.py","--power_port="+test_boards[test_board]['power_port'],"--beagle="+test_boards[test_board]['name']],  workdir="../tests/driver_tests",doStepIf=check_tag_partial, name=target+": Login to "+test_boards[test_board]['name']))
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning", "--lg-env", test_boards[test_board]['name']+".yaml", "test_init_overlay.py"], workdir="../tests/driver_tests", doStepIf=check_tag_partial, hideStepIf=skipped, name=target+": Install overlay merger"))
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_merge_dt_overlay.py","--product="+target], workdir="../tests/driver_tests", doStepIf=check_tag_partial, hideStepIf=skipped, name=target+": Merge device tree overlays"))
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_insmod_tests.py","--product="+target], workdir="../tests/driver_tests", doStepIf=check_tag_partial, hideStepIf=skipped, name=target+": insmod test modules"))
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_init_regulator_test.py","--product="+target], workdir="../tests/driver_tests", doStepIf=check_tag_partial, hideStepIf=skipped, name=target+": init_regulator_test.sh"))
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_test_target.py","--product="+target], workdir="../tests/driver_tests", doStepIf=check_tag_partial, hideStepIf=skipped, name=target+": test_target.sh"))
    
def linux_driver_test(project_name,beagle_ID,beagle_power_port):
    build_kernel_arm32(project_name)
    upload_kernel_binaries(project_name)
    build_test_kernel_modules(project_name)
    upload_test_kernel_modules(project_name)
    download_test_boards(project_name)
#    powercycle_ip_power(project_name,beagle_power_port)
    run_driver_tests(project_name)
### END OF HELPES ###

####### FACTORIES #######

linux_driver_test('test_linux','beagle1',beagle_power_port1)
linux_driver_test('linux-next','beagle1',beagle_power_port1)
linux_driver_test('linux_mainline','beagle1',beagle_power_port1)
linux_driver_test('linux_stable','beagle1',beagle_power_port1)
linux_driver_test('linux_rohm_devel','beagle1',beagle_power_port1)
