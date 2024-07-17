####### FACTORIES
import functools
from buildbot.plugins import util, steps
from buildbot.process import buildstep, logobserver
from twisted.internet import defer

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

class GenerateStagesCommand(buildstep.ShellMixin, steps.BuildStep):

    def __init__(self,test_board, target,test_type, dts, **kwargs):
        kwargs = self.setupShellMixin(kwargs)
        super().__init__(**kwargs)
        self.test_board = test_board
        self.target = target
        self.test_type = test_type
        self.dts = dts
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)

    def extract_stages(self, stdout):
        stages = []
        for line in stdout.split('\n'):
            stage = str(line.strip())
            if stage:
                stages.append(stage)
        return stages

    @defer.inlineCallbacks
    def run(self):
        # run 'generate_steps.py' to generate the list of steps
        cmd = yield self.makeRemoteShellCommand()
        yield self.runCommand(cmd)

        # if the command passes extract the list of stages
        result = cmd.results()
        if result == util.SUCCESS:
            # create a ShellCommand for each stage and add them to the build
            if self.test_type == "regulator":
                self.build.addStepsAfterCurrentStep([
                    steps.ShellCommand(name=self.target+": "+stage, workdir="../tests/pmic", command=["pytest","--lg-env="+self.test_board+".yaml",self.target+"/"+stage])
                    for stage in self.extract_stages(self.observer.getStdout())
                ])
            elif self.test_type == "dts":
                self.build.addStepsAfterCurrentStep([
                    steps.ShellCommand(name=self.target+": "+stage, workdir="../tests/pmic", command=["pytest","--lg-env="+self.test_board+".yaml",self.target+"/dts/"+self.dts+"/"+stage,"--dts="+self.dts])
                    for stage in self.extract_stages(self.observer.getStdout())
                ])

        return result

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
    tagL = tagL.split("-",1)
    if tagL[-1].startswith("rc"):
        tagL.pop(-1)
    tagL = tagL[0].split(".",1)
    for e in range(len(tagL)):
        if isFloat(tagL[e]) == True:
            tagL[e]=float(tagL[e])
        if isFloat(tagL[e]) == False:
            tagL[e]=int(tagL[e])
    return tagL

def check_make_dts(step, target, test_dts):
#    if any(" Error " in s for s in step.getProperty('make_dts_stdout')) or step.getProperty('make_dts_stdout') == None:
    if step.getProperty(target+'_make_dts_'+test_dts) == None:
        return False
    else:
        return True

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

    projects[project_name]['factory'].addStep(steps.FileDownload(mastersrc="../../../compilers/kernel_configs/arm32.config",workerdest=".config",name="Copy kernel config to build directory"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],name="Update kernel config if needed"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000"],name="Build kernel binaries"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "INSTALL_MOD_PATH="+dir_nfs, "modules_install"],name="Install kernel modules"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", dir_worker_root+projects[project_name]['workerNames'][0]+"/"+projects[project_name]['builderNames'][0]+"/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_worker_root+projects[project_name]['workerNames'][0]+"/"+projects[project_name]['builderNames'][0]+"/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"],name="Build Beagle device tree source binaries"))

def update_test_kernel_modules(project_name):
    projects[project_name]['factory'].addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test-kernel-modules', alwaysUseLatest=True, mode='full', workdir="build/_test-kernel-modules", name="Update kernel module source files from git"))

def build_overlay_merger(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./'}, workdir="build/_test-kernel-modules/overlay_merger", name="Build test kernel module: overlay_merger"))

def copy_overlay_merger_to_nfs(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["cp", "_test-kernel-modules/overlay_merger/mva_overlay.ko", dir_nfs], name="Copy overlay merger to nfs"))

def build_test_kernel_modules(project_name):
    projects[project_name]['factory'].addStep(steps.Git(repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git', branch='test-kernel-modules', alwaysUseLatest=True, mode='full', workdir="build/_test-kernel-modules", name="Update kernel module source files from git"))
    for key in kernel_modules['build']:
        if key in kernel_modules['dts_files'].keys():
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./','DTS_FILE':kernel_modules['dts_files'][key]['default']}, workdir="build/_test-kernel-modules/"+key, name="Build test kernel modules: "+key))
        else:
            projects[project_name]['factory'].addStep(steps.ShellCommand(command=["make"], env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./'}, workdir="build/_test-kernel-modules/"+key, name="Build test kernel modules: "+key))

def copy_kernel_binaries_to_tftpboot(project_name):
     projects[project_name]['factory'].addStep(steps.ShellSequence(commands=[
         util.ShellArg(command=['cp',"arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_tftpboot], logname='Copy BeagleBone .dtb to tftpboot'),
         util.ShellArg(command=['cp',"arch/arm/boot/zImage", dir_tftpboot], logname='Copy zImage to tftpboot')
         ], name="Copy kernel binaries to tftpboot"))

def copy_test_kernel_modules_to_nfs(project_name, target, dts, check_make_dts_partial):
    copy_commands =[]
    for value in kernel_modules['build'][target]:
        copy_commands.append(util.ShellArg(command=["cp", "_test-kernel-modules/"+target+"/"+value, dir_nfs], logname="Copy "+value+" to nfs"))
    projects[project_name]['factory'].addStep(steps.ShellSequence(commands=copy_commands,doStepIf=check_make_dts_partial or target == 'overlay_merger', hideStepIf=skipped, name=target+": Copy test kernel modules to nfs"))

def build_dts(project_name, target, test_dts, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=['make'], env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./','DTS_FILE':'generated_dts_'+test_dts+'.dts'}, workdir="build/_test-kernel-modules/"+target, property=target+"_make_dts_"+test_dts, doStepIf=check_tag_partial, includeStdout=True, includeStderr=True, name=target+": Build dts: "+test_dts))

def download_test_boards(project_name):
    projects[project_name]['factory'].addStep(steps.FileDownload(mastersrc="configs/kernel_modules.py",
                            workerdest="../../tests/pmic/configs/kernel_modules.py",
                            name="Download kernel_modules.py"))

def initialize_driver_test(project_name, test_board, target, test_dts, check_make_dts_partial):
    check_tag_partial=functools.partial(check_tag, target=target)
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning", "-ra", "test_login.py","--power_port="+test_boards[test_board]['power_port'],"--beagle="+test_boards[test_board]['name'], "--type=PMIC", "--product="+target],  workdir="../tests/pmic",doStepIf=check_tag_partial and check_make_dts_partial, name=target+": Login to "+test_boards[test_board]['name']))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning", "--lg-env", test_boards[test_board]['name']+".yaml", "test_init_overlay.py"], workdir="../tests/pmic", doStepIf=check_tag_partial and check_make_dts_partial, hideStepIf=skipped, name=target+": Install overlay merger"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_merge_dt_overlay.py","--product="+target], workdir="../tests/pmic", doStepIf=check_tag_partial and check_make_dts_partial, hideStepIf=skipped, name=target+": Merge device tree overlays"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_insmod_tests.py","--product="+target], workdir="../tests/pmic", doStepIf=check_tag_partial and check_make_dts_partial, hideStepIf=skipped, name=target+": insmod test modules"))
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_init_regulator_test.py","--product="+target], workdir="../tests/pmic", doStepIf=check_tag_partial and check_make_dts_partial, hideStepIf=skipped, name=target+": init_regulator_test.py"))

def generate_driver_tests(project_name,test_board,target, check_make_dts_partial, check_tag_partial, test_type, dts=None):
    if test_type == "regulator":
        projects[project_name]['factory'].addStep(GenerateStagesCommand(
            test_board, target, test_type, dts,
            name=target+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", target, test_type], workdir="../tests/pmic",
            haltOnFailure=True, doStepIf=check_tag_partial and check_make_dts_partial, hideStepIf=skipped))
    elif test_type == "dts":
        projects[project_name]['factory'].addStep(GenerateStagesCommand(
            test_board, target, test_type, dts,
            name=target+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", target, test_type, dts], workdir="../tests/pmic",
            haltOnFailure=True, doStepIf=check_tag_partial and check_make_dts_partial, hideStepIf=skipped))

def check_dts_tests(target):
    dts_tests=[]
    if target in kernel_modules['dts_tests'].keys():
        for dts in kernel_modules['dts_tests'][target]:
            dts_tests.append(dts)
    return dts_tests

def copy_generated_dts(project_name, target, dts, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["cp", "../../../tests/pmic/configs/dts_generated/"+target+"/generated_dts_"+dts+".dts", "./"+target], workdir="build/_test-kernel-modules", doStepIf=check_tag_partial, name=target+": Copy generated dts: "+dts))

def generate_dts(project_name, target, dts, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["python3", "generate_dts.py", target, dts], workdir="../tests/pmic", doStepIf=check_tag_partial, name=target+": Generate dts: "+dts))

def run_driver_tests(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(command=["python3", "initialize_results.py", projects[project_name]['builderNames'][0], util.Property('commit-description')], workdir="../tests/pmic", name="Initialize test report" ))

    for test_board in test_boards:
        for target in test_boards[test_board]['targets']:
            check_tag_partial=functools.partial(check_tag, target=target)

            generate_dts(project_name, target, 'default', check_tag_partial)
            copy_generated_dts(project_name, target, 'default', check_tag_partial)
            build_dts(project_name, target, 'default', check_tag_partial)

            check_make_dts_partial=functools.partial(check_make_dts, target=target, test_dts='default')

            copy_test_kernel_modules_to_nfs(project_name, target, 'default', check_make_dts_partial)

            initialize_driver_test(project_name, test_board, target, 'default', check_make_dts_partial)
            generate_driver_tests(project_name,test_boards[test_board]['name'],target, check_make_dts_partial, check_tag_partial, "regulator", "default")

            dts_tests = check_dts_tests(target)

            for dts in dts_tests:
                generate_dts(project_name, target, dts, check_tag_partial)
                copy_generated_dts(project_name, target, dts, check_tag_partial)
                build_dts(project_name, target, dts, check_tag_partial)

                check_make_dts_partial=functools.partial(check_make_dts, target=target, test_dts=dts)
                copy_test_kernel_modules_to_nfs(project_name, target, dts, check_make_dts_partial)

                initialize_driver_test(project_name, test_board, target, dts, check_make_dts_partial)
                generate_driver_tests(project_name, test_boards[test_board]['name'], target,check_make_dts_partial, check_tag_partial, "dts", dts )

def linux_driver_test(project_name):
    build_kernel_arm32(project_name)
    copy_kernel_binaries_to_tftpboot(project_name)
    update_test_kernel_modules(project_name)
    build_overlay_merger(project_name)
#    copy_test_kernel_modules_to_nfs(project_name, 'overlay_merger')
    copy_overlay_merger_to_nfs(project_name)

    download_test_boards(project_name)
    run_driver_tests(project_name)

####### FACTORIES #######

linux_driver_test('test_linux')
linux_driver_test('linux-next')
linux_driver_test('linux_mainline')
linux_driver_test('linux_stable')
linux_driver_test('linux_rohm_devel')
