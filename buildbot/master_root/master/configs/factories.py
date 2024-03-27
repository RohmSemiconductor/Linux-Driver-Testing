####### FACTORIES

from buildbot.plugins import util, steps


### HELPERS
factory_test_linux = util.BuildFactory()
factory_linux_next = util.BuildFactory()
import sys 
import os
sys.path.append(os.path.abspath("./configs"))
from kernel_modules import *
from projects import * 

def build_test_kernel_modules(project_name):
    for key in kernel_modules['test']:
        projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':'/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-','PWD':'./'}, workdir="build/_test-kernel-modules/"+key, name="Build test kernel modules: "+key))
    
# def build_kernel_arm32():


### END OF HELPES ###

#for key in kernel_modules['test']:
#    factory_test_linux.addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':'/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-','PWD':'./'}, workdir="build/_test-kernel-modules/"+key, name="Build test kernel modules: "+key))

####### FACTORIES #######

# factory_test_linux
factory_test_linux.addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test_linux', mode='incremental',name="Update kernel source files from git"))
factory_test_linux.addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test-kernel-modules', alwaysUseLatest=True, mode='incremental', workdir="build/_test-kernel-modules", name="Update kernel module source files from git"))

build_test_kernel_modules('test_linux')
factory_test_linux.addStep(steps.FileDownload(mastersrc="~/tools/kernel/.config",workerdest=".config",name="Copy kernel config to build directory"))
factory_test_linux.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],name="Update kernel config if needed"))
factory_test_linux.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000"],name="Build kernel binaries"))
factory_test_linux.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH=/home/user01/nfs"],name="Install kernel modules"))
factory_test_linux.addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"  ],name="Build device tree source binaries")) 

factory_test_linux.addStep(steps.MultipleFileUpload(workersrcs=["arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/zImage"],
                                   masterdest="/var/lib/tftpboot/",
                                   mode=0o644,name="Upload compiled binaries to tftp directory"))
factory_test_linux.addStep(steps.ShellCommand(command=["pytest", "--lg-env", "local.yaml", "test_shell.py"], workdir="../tests/first_test", name="Test script"))

# factory_linux_next
factory_linux_next.addStep(steps.Git(repourl='https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git', branch='master', mode='incremental',name="Update source files from git"))
factory_linux_next.addStep(steps.FileDownload(mastersrc="~/tools/kernel/.config",workerdest=".config",name="Copy kernel config to build directory"))
factory_linux_next.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],name="Update kernel config if needed"))
factory_linux_next.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000"],name="Build kernel binaries"))
factory_linux_next.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH=/home/user01/nfs"],name="Install kernel modules"))
factory_linux_next.addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/linux-next/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/linux-next/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"  ],name="Build device tree source binaries"))

factory_linux_next.addStep(steps.MultipleFileUpload(workersrcs=["arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/zImage"],
                                   masterdest="/var/lib/tftpboot/",
                                   mode=0o644,name="Upload compiled binaries to tftp directory"))
factory_linux_next.addStep(steps.ShellCommand(command=["pytest", "--lg-env", "local.yaml", "test_shell.py"], workdir="../tests/first_test", name="Test script"))

# factory_test_kernel_modules
#factory_test_kernel_modules = util.BuildFactory()
#factory_test_kernel_modules.addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test-kernel-modules', mode='incremental',name="Update source files from git"))

#factory_linux_next.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH=/home/user01/nfs"],name="Install kernel modules"))
#factory_linux_next.addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/linux-next/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/linux-next/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"  ],name="Build device tree source binaries"))

#factory_linux_next.addStep(steps.MultipleFileUpload(workersrcs=["arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/zImage"],
#                                   masterdest="/var/lib/tftpboot/",
#                                   mode=0o644,name="Upload compiled binaries to tftp directory"))
#factory_linux_next.addStep(steps.ShellCommand(command=["pytest", "--lg-env", "local.yaml", "test_shell.py"], workdir="../tests/first_test", name="Test script"))
