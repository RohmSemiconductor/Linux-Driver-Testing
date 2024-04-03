####### FACTORIES

from buildbot.plugins import util, steps


### HELPERS
factory_test_linux = util.BuildFactory()
factory_linux_next = util.BuildFactory()
factory_driver_test = util.BuildFactory()

beagle_power_port1 = "1"
beagle_power_port2 = "2"
beagle_power_port3 = "3"
beagle_power_port4 = "4"

import sys 
import os
sys.path.append(os.path.abspath("./configs"))
from kernel_modules import *
from projects import * 
from paths import *

def build_kernel_arm32(project_name):
    projects[project_name]['factory'].addStep(steps.Git(repourl=projects[project_name]['repo_git'], mode='incremental',name="Update linux source files from git"))
    projects[project_name]['factory'].addStep(steps.FileDownload(mastersrc="~/tools/kernel/.config",workerdest=".config",name="Copy kernel config to build directory"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],name="Update kernel config if needed"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000"],name="Build kernel binaries"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH="+dir_nfs, "modules_install"],name="Install kernel modules"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/Test_Linux/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"  ],name="Build device tree source binaries")) 

def build_test_kernel_modules(project_name):
    projects[project_name]['factory'].addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test-kernel-modules', alwaysUseLatest=True, mode='full', workdir="build/_test-kernel-modules", name="Update kernel module source files from git"))
    for key in kernel_modules['build']:
        projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./'}, workdir="build/_test-kernel-modules/"+key, name="Build test kernel modules: "+key))

def upload_kernel_binaries(project_name):
     projects[project_name]['factory'].addStep(steps.MultipleFileUpload(workersrcs=["arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/zImage"],
                                   masterdest=dir_tftpboot,
                                   mode=0o644,name="Upload compiled kernel binaries to tftp directory"))

def upload_test_kernel_modules(project_name):
#    x=0
    files = []
    for key in kernel_modules['build']:
#        x=x+1
        for value in kernel_modules['build'].get(key):

            files.append("_test-kernel-modules/"+key+"/"+value)
    projects[project_name]['factory'].addStep(steps.MultipleFileUpload(workersrcs=files,
    masterdest=dir_nfs,
    name="Upload test kernel modules to nfs directory"
#+str(x)+"/"+str(len(kernel_modules['test']))
))

def powercycle_ip_power(project_name, beagle_power_port):

    projects[project_name]["factory"].addStep(steps.ShellSequence(
    commands=[
        util.ShellArg(command=["/bin/bash", "ip-power-control.sh", beagle_power_port, "0"]),
        util.ShellArg(command=["/bin/bash", "ip-power-control.sh", beagle_power_port, "1"]),
        ], workdir="../tests",flunkOnFailure=False ,flunkOnWarnings=False ,name="Powercycle beagle bone"))

def run_driver_tests(project_name,beagle_ID):
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest", "--lg-env", beagle_ID+".yaml", "test_shell.py"], workdir="../tests/driver_tests", name="Test: Login to "+beagle_ID))

def linux_driver_test(project_name,beagle_ID,beagle_power_port):
    build_kernel_arm32(project_name)
    upload_kernel_binaries(project_name)
    build_test_kernel_modules(project_name)
    upload_test_kernel_modules(project_name)
    powercycle_ip_power(project_name,beagle_power_port)
    run_driver_tests(project_name,beagle_ID)
### END OF HELPES ###

####### FACTORIES #######

linux_driver_test('test_linux','beagle1',beagle_power_port1)
linux_driver_test('linux-next','beagle1',beagle_power_port1)
