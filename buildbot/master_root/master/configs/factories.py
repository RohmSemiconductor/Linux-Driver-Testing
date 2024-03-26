####### FACTORIES

from buildbot.plugins import util, steps

# factory_test_linux
factory_test_linux = util.BuildFactory()
factory_test_linux.addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test_linux', mode='incremental',name="Update source files from git"))
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
factory_linux_next = util.BuildFactory()
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
