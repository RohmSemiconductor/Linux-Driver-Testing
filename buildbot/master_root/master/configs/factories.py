####### FACTORIES

from buildbot.plugins import util, steps

# factory = util.BuildFactory()
# # check out the source
# factory.addStep(steps.Git(repourl='https://github.com/buildbot/hello-world.git', mode='incremental'))
# # run the tests (note that this will require that 'trial' is installed)
# factory.addStep(steps.ShellCommand(command=["trial", "hello"],
#                                    env={"PYTHONPATH": "."}))

#factory.addStep(steps.FileUpload(workersrc='.', masterdest='~/nfs', mode=0o755)) #example that sets permissions

factory_test_linux = util.BuildFactory()
factory_test_linux.addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test_linux', mode='incremental',name="Update source files from git"))
factory_test_linux.addStep(steps.FileDownload(mastersrc="~/tools/kernel/.config",workerdest=".config",name="Copy kernel config to build directory"))
factory_test_linux.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],name="Update kernel config if needed"))
factory_test_linux.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000"],name="Build kernel binaries"))
factory_test_linux.addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE=/home/user01/tools/beagle-dev-tools/bb-compiler/gcc-linaro-6.4.1-2017.11-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH=/home/user01/nfs"],name="Install kernel modules"))
# factory_test_linux.addStep(steps.ShellSequence(
#     commands=[
#         util.ShellArg(command=["cd" "arch/arm/boot/dts"]),
#         util.ShellArg(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", ""/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/"", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"]),
#     ]))
factory_test_linux.addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "/home/user01/Linux-Driver-Testing/buildbot/worker_root/worker1/builder_test_linux/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"  ],name="Build device tree source binaries")) 
#dtc -@ -I dts -O dtb -o "arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb" arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp

# factory_test_linux.addStep(steps.FileUpload(workersrc="arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", masterdest="/var/lib/tftpboot/am335x-boneblack.dtb", mode=0o644))
# factory_test_linux.addStep(steps.FileUpload(workersrc="arch/arm/boot/zImage", masterdest="/var/lib/tftpboot/zImage", mode=0o644))

factory_test_linux.addStep(steps.MultipleFileUpload(workersrcs=["arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", "arch/arm/boot/zImage"],
                                   masterdest="/var/lib/tftpboot/",
                                   mode=0o644,name="Upload compiled binaries to tftp directory"))

factory_test_linux.addStep(steps.ShellCommand(command=["pytest", "--lg-env", "local.yaml", "test_shell.py"], workdir="../tests/first_test", name="Test script"))
