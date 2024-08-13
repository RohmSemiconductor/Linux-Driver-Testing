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

    def __init__(self,test_board, product,test_type, dts, extract_driver_tests_partial, **kwargs):
        kwargs = self.setupShellMixin(kwargs)
        super().__init__(**kwargs)
        self.test_board = test_board
        self.product = product
        self.test_type = test_type
        self.dts = dts
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)
        self.extract_driver_tests_partial = extract_driver_tests_partial

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
                self.build.addStepsAfterCurrentStep([steps.SetPropertyFromCommand(
                    command=["pytest","--lg-env="+self.test_board+".yaml",self.product+"/"+stage],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == True,
                    extract_fn=self.extract_driver_tests_partial)
                    for stage in self.extract_stages(self.observer.getStdout())
                ])
            elif self.test_type == "dts":
                self.build.addStepsAfterCurrentStep([steps.SetPropertyFromCommand(
                    command=["pytest","--lg-env="+self.test_board+".yaml",self.product+"/dts/"+self.dts+"/"+stage,"--dts="+self.dts],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == True,
                    extract_fn=self.extract_driver_tests_partial)
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

def check_tag(step,product):
    if re.search('^next.*', step.getProperty('commit-description')):    #check for linux next
        print(step.getProperty('commit-description'))
        return True
    elif re.search('^'+product, step.getProperty('commit-description')): #check for driver fix
        return True

    else:
        product_ver = tagConvert(kernel_modules['linux_ver'][product][0])
        git_ver = tagConvert(step.getProperty('commit-description'))
        if product_ver[0] < git_ver[0]: #git bigger pass
            return True
        elif product_ver[0] > git_ver[0]: #product_ver bigger fail
            return False
        elif product_ver[0] == git_ver[0]: #same
            if type(product_ver[0])== int:
                if product_ver[1] <= math.floor(git_ver[1]): #same pass
                    return True
                else:
                    return False                            #same fail
            else:
                if product_ver[1]<=git_ver[1]:                #linux stable of same version or bigger
                    return True
                else:
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

def extract_dts_error(rc, stdout, stderr, product, test_dts):
    if 'Error' in stderr:
        return {product+'_'+test_dts+'_dts_error': stderr, product+'_'+test_dts+'_dts_make_passed': False , product+'_do_steps' : False, product+'_skip_dts_tests' : True }
    else:
        return {product+'_'+test_dts+'_dts_error': stderr, product+'_'+test_dts+'_dts_make_passed': True , product+'_do_steps' : True, product+'_skip_dts_tests' : False }

def doStepIf_copy_overlay_merger_to_nfs(step):
    if step.getProperty('preparation_step_failed') == True:
        return False
    else:
        return True

def extract_init_driver_test(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_init_driver_tests_passed': False, product+'_do_steps' : False }
#        return {product+'_init_driver_tests_passed': False, product+'_do_steps' : False, 'single_test_failed': True } #### FOR TESTING! REMOVE LATER
    else:
        return {product+'_init_driver_tests_passed': True, product+'_do_steps' : True }
#        return {product+'_init_driver_tests_passed': True, product+'_do_steps' : True, 'single_test_passed': True } #### FOR TESTING! REMOVE LATER

def extract_sanitycheck_error(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_sanitycheck_passed': False ,product+'_do_steps' : False }
    else:
        return {product+'_sanitycheck_passed': True , product+'_do_steps' : True }

def initialize_test_report(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_report", projects[project_name]['builderNames'][0], util.Property('commit-description'), util.Property('revision')],
        workdir="../tests",
        name="Initialize test report",
        doStepIf=util.Property('git_bisecting') != True
        ))

def extract_make_kernel(rc, stdout, stderr):
    if rc != 0:
        return {'kernel_build_failed':True, 'preparation_step_failed':True, 'kernel_error_stderr':stderr}
    if rc == 0:
        return {'preparation_step_failed':False}

### Executed steps start here
def build_kernel_arm32(project_name):
    projects[project_name]['factory'].addStep(steps.Git(
        repourl=projects[project_name]['repo_git'],
        mode='incremental',
        getDescription={'tags':True},
        name="Update linux source files from git",
        doStepIf=util.Property('git_bisect_state') != 'running'
        ))

    initialize_test_report(project_name)

    projects[project_name]['factory'].addStep(steps.FileDownload(
        mastersrc="../../../compilers/kernel_configs/arm32.config",
        workerdest=".config",
        name="Copy kernel config to build directory"
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000", "olddefconfig"],
        name="Update kernel config if needed"
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["make", "-j8", "ARCH=arm", "CROSS_COMPILE="+dir_compiler_arm32+"arm-linux-gnueabihf-", "LOADADDR=0x80008000"],
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

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["dtc", "-@", "-I", "dts", "-O", "dtb", "-o", dir_worker_root+projects[project_name]['workerNames'][0]+"/"+projects[project_name]['builderNames'][0]+"/build/arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_worker_root+projects[project_name]['workerNames'][0]+"/"+projects[project_name]['builderNames'][0]+"/build/arch/arm/boot/dts/ti/omap/.am335x-boneblack.dtb.dts.tmp"],
        name="Build Beagle device tree source binaries",
        hideStepIf=skipped,
        doStepIf=util.Property('kernel_build_failed') != True
        ))

def update_test_kernel_modules(project_name):
    projects[project_name]['factory'].addStep(steps.Git(
        repourl='https://github.com/RohmSemiconductor/Linux-Driver-Testing.git',
        branch='test-kernel-modules',
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

def copy_kernel_binaries_to_tftpboot(project_name):
     projects[project_name]['factory'].addStep(steps.ShellSequence(
        commands=[
        util.ShellArg(command=['cp',"arch/arm/boot/dts/ti/omap/am335x-boneblack.dtb", dir_tftpboot], logname='Copy BeagleBone .dtb to tftpboot'),
        util.ShellArg(command=['cp',"arch/arm/boot/zImage", dir_tftpboot], logname='Copy zImage to tftpboot')
        ],
        name="Copy kernel binaries to tftpboot",
        doStepIf=util.Property('preparation_step_failed') != True
        ))

def doStepIf_copy_test_kernel_modules_to_nfs(step, product, test_dts):
    if step.getProperty('kernel_build_failed') == True:
        return False
    elif step.getProperty('overlay_merger_build_failed') == True:
        return False
    elif step.getProperty(product+'_'+test_dts+'_dts_make_passed') == True:
        if step.getProperty(product+'_skip_dts_tests') != True:
            return True
    else:
        return False

def copy_test_kernel_modules_to_nfs(project_name, product, test_dts):
    doStepIf_copy_test_kernel_modules_to_nfs_partial = functools.partial(doStepIf_copy_test_kernel_modules_to_nfs, product=product, test_dts=test_dts)
    copy_commands =[]
    for value in kernel_modules['build'][product]:
        copy_commands.append(util.ShellArg(command=["cp", "_test-kernel-modules/"+product+"/"+value, dir_nfs], logname="Copy "+value+" to nfs"))

    projects[project_name]['factory'].addStep(steps.ShellSequence(
        commands=copy_commands,
        doStepIf=doStepIf_copy_test_kernel_modules_to_nfs_partial,
        hideStepIf=skipped,
        name=product+": Copy test kernel modules to nfs"
        ))

def download_test_boards(project_name):
    projects[project_name]['factory'].addStep(steps.FileDownload(
        mastersrc="configs/kernel_modules.py",
        workerdest="../../tests/pmic/configs/kernel_modules.py",
        name="Download kernel_modules.py",
        doStepIf=util.Property('preparation_step_failed') != True
        ))

def initialize_driver_test(project_name, test_board, product, test_dts):
    extract_init_driver_test_partial= functools.partial(extract_init_driver_test, product=product)
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra", "test_000_login.py","--power_port="+test_boards[test_board]['power_port'],"--beagle="+test_boards[test_board]['name']],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        name=product+": Login to "+test_boards[test_board]['name']
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "--lg-env", test_boards[test_board]['name']+".yaml", "test_001_init_overlay.py"],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped, name=product+": Install overlay merger"
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_002_merge_dt_overlay.py","--product="+product],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped, name=product+": Merge device tree overlays"
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_003_insmod_tests.py","--product="+product],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped,
        name=product+": insmod test modules"))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=[
        "pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_004_init_regulator_test.py","--product="+product],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped,
        name=product+": init_regulator_test.py"
        ))

def extract_driver_tests(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_skip_dts_tests': True, product+'_do_steps': False, product+'_dts_collected':False, product+'_dmesg_collected':False, 'single_test_failed': True, 'git_bisect_trigger': True}
    else:
        return {product+'_skip_dts_tests': False, product+'_do_steps' : True, 'single_test_passed': True}

def doStepIf_generate_driver_tests(step, product, dts):
    if check_tag(step, product) == True:
        if step.getProperty(product+'_'+dts+'_dts_make_passed') == True:
            if util.Property(product+'_do_steps') == True:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def generate_driver_tests(project_name,test_board,product, test_type, dts=None):
    extract_driver_tests_partial = functools.partial(extract_driver_tests, product=product)
    doStepIf_generate_driver_tests_partial = functools.partial(doStepIf_generate_driver_tests, product=product, dts=dts)
    if test_type == "regulator":
        extract_sanitycheck_error_partial = functools.partial(extract_sanitycheck_error, product=product)
        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=[
            'pytest', '--lg-env='+test_board+".yaml", product+'/test_000_sanitycheck.py'],
            workdir="../tests/pmic/",
            extract_fn=extract_sanitycheck_error_partial,
            doStepIf=doStepIf_generate_driver_tests_partial,
            hideStepIf=skipped,
            name=product+": test_000_sanitycheck.py"
            ))

        projects[project_name]['factory'].addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, extract_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type], workdir="../tests/pmic",
            haltOnFailure=True,
            doStepIf=doStepIf_generate_driver_tests_partial
            ))

        collect_dmesg_and_dts(project_name, test_board, product, test_dts=dts)

    elif test_type == "dts":
        projects[project_name]['factory'].addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, extract_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type, dts], workdir="../tests/pmic",
            haltOnFailure=True,
            doStepIf=doStepIf_generate_driver_tests_partial
            ))

        collect_dmesg_and_dts(project_name, test_board, product, test_dts=dts)

def check_dts_tests(product):
    dts_tests=[]
    if product in kernel_modules['dts_tests'].keys():
        for dts in kernel_modules['dts_tests'][product]:
            dts_tests.append(dts)
    return dts_tests

def doStepIf_dts_test_preparation(step, product):
    if step.getProperty('kernel_build_failed') == True:
        return False
    elif step.getProperty('overlay_merger_build_failed') == True:
        return False
    elif check_tag(step, product) == True:
        if step.getProperty(product+'_skip_dts_tests') != True:
            return True
        else:
            return False
    else:
        return False

def generate_dts(project_name, product, dts):
    doStepIf_dts_test_preparation_partial = functools.partial(doStepIf_dts_test_preparation, product=product)

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "generate_dts.py", product, dts],
        workdir="../tests/pmic",
        doStepIf=doStepIf_dts_test_preparation_partial,
        hideStepIf=skipped,
        name=product+": Generate dts: "+dts
        ))

def copy_generated_dts(project_name, product, dts):
    doStepIf_dts_test_preparation_partial = functools.partial(doStepIf_dts_test_preparation, product=product)

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["cp", "../../../tests/pmic/configs/dts_generated/"+product+"/generated_dts_"+dts+".dts", "./"+product],
        workdir="build/_test-kernel-modules",
        doStepIf=doStepIf_dts_test_preparation_partial,
        hideStepIf=skipped,
        name=product+": Copy generated dts: "+dts
        ))

def build_dts(project_name, product, test_dts):
    extract_dts_error_partial = functools.partial(extract_dts_error, product=product, test_dts=test_dts)
    doStepIf_dts_test_preparation_partial = functools.partial(doStepIf_dts_test_preparation, product=product)
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=['make'],
        env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./','DTS_FILE':'generated_dts_'+test_dts+'.dts'},
        workdir="build/_test-kernel-modules/"+product,
        doStepIf=doStepIf_dts_test_preparation_partial,
        hideStepIf=skipped,
        extract_fn=extract_dts_error_partial,
        name=product+": Build dts: "+test_dts
        ))

def doStepIf_dts_report(step, product, test_dts):
    if step.getProperty('preparation_step_failed') == True:
        return False
    elif check_tag(step, product) == True:
        if step.getProperty(product+'_'+test_dts+'_dts_make_passed') != True:
            return True
    else:
        return False

def dts_report(project_name, product, test_dts):
    doStepIf_dts_report_partial=functools.partial(doStepIf_dts_report, product=product, test_dts=test_dts)
    if test_dts == 'default':
        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "dts_error", product, 'default', util.Property(product+'_default_dts_error')],
            workdir="../tests",
            doStepIf=doStepIf_dts_report_partial,
            hideStepIf=skipped,
            name=product+": write dts build fail to report"
            ))

    elif test_dts != 'default':
        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "dts_error", product, test_dts, util.Property(product+'_'+test_dts+'_dts_error')],
            workdir="../tests",
            doStepIf=doStepIf_dts_report_partial,
            hideStepIf=skipped,
            name=product+": write dts build fail to report"
            ))

def doStepIf_initialize_product(step, product):
    if check_tag(step, product) == True:
        if step.getProperty('preparation_step_failed') != True:
            return True
        else:
            return False
    else:
        return False

def initialize_product(project_name, product):
    doStepIf_initialize_product_partial = functools.partial(doStepIf_initialize_product, product=product)
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_product", "PMIC", product],
        workdir="../tests",
        name="Initialize test report: "+product,
        doStepIf=doStepIf_initialize_product_partial,
        ))

def extract_dmesg_collected(rc, stdout, stderr, product):
    return {product+'_dmesg_collected' : True}

def extract_dts_collected(rc, stdout, stderr, product):
    return {product+'_dts_collected' : True}

def doStepIf_collect_dmesg(step, product):
    if check_tag(step, product) == True:
        if step.getProperty('preparation_step_failed') == True:
            return False
        elif step.getProperty('git_bisecting'):
            return False
        elif step.getProperty(product+'_do_steps') == False:
            if not step.getProperty(product+'_dmesg_collected'):
                return True
            else:
                return False
        else:
                return False
    else:
        return False

def doStepIf_collect_dts(step,  product):
    if check_tag(step, product) == True:
        if step.getProperty('preparation_step_failed') == True:
            return False
        elif step.getProperty('git_bisecting'):
            return False
        elif step.getProperty(product+'_do_steps') == False:
            if not step.getProperty(product+'_dts_collected'):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def collect_dmesg_and_dts(project_name, test_board, product, test_dts='default'):
    extract_dmesg_collected_partial = functools.partial(extract_dmesg_collected, product=product)
    extract_dts_collected_partial = functools.partial(extract_dts_collected, product=product)

    doStepIf_collect_dmesg_partial = functools.partial(doStepIf_collect_dmesg, product=product)
    doStepIf_collect_dts_partial = functools.partial(doStepIf_collect_dts, product=product)

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=['pytest', '--lg-env='+test_boards[test_board]['name']+'.yaml', 'test_get_dmesg.py', '--product='+product],
        workdir="../tests/pmic/",
        doStepIf=doStepIf_collect_dmesg_partial,
        extract_fn=extract_dmesg_collected_partial,
        hideStepIf=skipped,
        name=product+": Collect dmesg"
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=['cp','../../'+projects[project_name]['builderNames'][0]+'/build/_test-kernel-modules/'+product+'/generated_dts_'+test_dts+'.dts', '../temp_results/'+product+'/'],
        workdir="../tests/pmic/",
        doStepIf=doStepIf_collect_dts_partial,
        hideStepIf=skipped,
        extract_fn=extract_dts_collected_partial,
        name=product+": Collect "+test_dts+".dts"
        ))

def doStepIf_finalize_product(step, product):
    if step.getProperty('preparation_step_failed') == True:
        return False
    elif step.getProperty('git_bisecting') == True:
        return False
    elif check_tag(step, product) == True:
        return True
    else:
        return False

def finalize_product(project_name, product):
    doStepIf_finalize_product_partial = functools.partial(doStepIf_finalize_product, product=product)
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "finalize_product", projects[project_name]['builderNames'][0], util.Property('commit-description'), "PMIC", product, util.Property(product+'_do_steps')],
        workdir="../tests",
        name="Finalize test report: "+product,
        doStepIf=doStepIf_finalize_product_partial,
        hideStepIf=skipped
        ))

def run_driver_tests(project_name):
    for test_board in test_boards:
        for product in test_boards[test_board]['products']:
            initialize_product(project_name, product)
            generate_dts(project_name, product, 'default')
            copy_generated_dts(project_name, product, 'default')

            build_dts(project_name, product, 'default')
            dts_report(project_name, product, 'default')

            copy_test_kernel_modules_to_nfs(project_name, product, 'default')
            initialize_driver_test(project_name, test_board, product, 'default')
            generate_driver_tests(project_name,test_boards[test_board]['name'],product, "regulator", "default")

            dts_tests = check_dts_tests(product)
            for dts in dts_tests:
                generate_dts(project_name, product, dts)
                copy_generated_dts(project_name, product, dts)
                build_dts(project_name, product, dts)
                dts_report(project_name, product, dts)

                copy_test_kernel_modules_to_nfs(project_name, product, dts)
                initialize_driver_test(project_name, test_board, product, dts)
                generate_driver_tests(project_name, test_boards[test_board]['name'], product, "dts", dts )

            finalize_product(project_name, product)

def extract_get_timestamp(rc, stdout, stderr):
    stdout = stdout.split('\n')
    return {'timestamp':stdout[0], 'timestamped_dir':'results/'+stdout[0]}


def get_timestamp(project_name):
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["python3", "report_janitor.py", "get_timestamp"],
        workdir="../tests",
        name="Set timestamp property for results",
        extract_fn=extract_get_timestamp,
        doStepIf=util.Property('git_bisecting') != True
        ))

def copy_temp_results(project_name):
    projects[project_name]['factory'].addStep(steps.ShellSequence(
        commands=[
        util.ShellArg(command=["cp", "-r", "temp_results/", "results/"]),
        util.ShellArg(command=["mv", "results/temp_results", util.Property('timestamped_dir')]),
        ],
        workdir="../tests",
        name="Copy temp_results/ to results/",
        doStepIf=util.Property('git_bisecting') != True
        ))

#### Git bisect helpers
def doStepIf_good_commit_write(step):
    if step.getProperty('git_bisecting') != True:
        if step.getProperty('preparation_step_failed') == True:
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
        workdir="../tests",
        doStepIf=doStepIf_good_commit_write
        ))

def doStepIf_git_bisect_start(step):
    if not step.getProperty('git_bisecting'):
        if step.getProperty('preparation_step_failed') == True:
            return True
        elif step.getProperty('single_test_failed') == True:
            return True
        else:
            return False
    else:
        return False

def doStepIf_git_bisect_good(step):
    if step.getProperty('git_bisecting') == True:
        if step.getProperty('preparation_step_failed') == True:
            return False
        elif (not step.getProperty('single_test_failed') and step.getProperty('single_test_passed')):
            return True
        else:
            return False
    else:
        return False

def doStepIf_git_bisect_bad(step):
    if step.getProperty('preparation_step_failed') == True:
        return True
    elif step.getProperty('single_test_failed') == True:
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
    elif step.getProperty('preparation_step_failed') == True:
        return True
    elif step.getProperty('single_test_failed') == True:
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
        return {'git_bisecting': False, 'git_bisect_failed':True, 'git_bisect_final_output':stdout, 'git_bisect_state':'failed'}
    elif rc == 0:
        # Git bisect needs atleast 1 good and bad commit for the command to start returning commits to test
        if (('waiting for both good and bad commits' in stdout) or ('waiting for bad commit' in stdout) or ('waiting for good commit' in stdout)):
            return {'git_bisecting': False, 'git_bisect_output':stdout, 'git_bisect_state': 'cannot_start'}
        # '...revisions left to test aftert this....' is a printed when bisect is running and 'git bisect good/bad' is given
        elif 'revisions left to test after this' in stdout:
            return {'git_bisecting': True , 'git_bisect_output':stdout, 'git_bisect_state': 'running'}
        # '...is the first bad commit' is printed after final 'git bisect good/bad'
        elif 'is the first bad commit' in stdout:
            return {'git_bisecting': False, 'git_bisect_final_output':stdout, 'git_bisect_state': 'success'}
        else:
            return {'git_bisect_wtf_stdout': stdout, 'git_bisect_wtf_rc':rc,'git_bisect_wtf_stder':stderr}
#### /Git bisect helpers

def git_bisect(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=['git','bisect','start'],
        workdir="build",
        name="Git bisect: start",
        doStepIf=doStepIf_git_bisect_start
        ))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["python3", "bisect_good_commit.py", "read", projects[project_name]['name'], util.Property('branch')],
        name="Get good commit hash from file",
        workdir="../tests",
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
            'git_bisecting':True,
            'git_bisect_state':'running',
            'commit-description':util.Property('commit-description'),
            'timestamped_dir':util.Property('timestamped_dir'),
            'timestamp':util.Property('timestamp')
            },
        doStepIf=doStepIf_git_bisect_trigger
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "bisect_result", util.Property('timestamped_dir'), util.Property("git_bisect_final_output")],
        name="Report git bisect results",
        workdir="../tests",
        doStepIf=util.Property("git_bisect_state") == "success"
        ))

    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["git", "bisect", "reset"],
        name="Git bisect reset",
        workdir="build",
        doStepIf=util.Property("git_bisect_state") == "success"
        ))

def linux_driver_test(project_name):
    build_kernel_arm32(project_name)
    copy_kernel_binaries_to_tftpboot(project_name)
    update_test_kernel_modules(project_name)
    build_overlay_merger(project_name)
    copy_overlay_merger_to_nfs(project_name)

    download_test_boards(project_name)
    run_driver_tests(project_name)
    get_timestamp(project_name)
    copy_temp_results(project_name)
    save_good_commit(project_name)
    git_bisect(project_name)

####### FACTORIES #######
linux_driver_test('test_linux')
linux_driver_test('linux-next')
linux_driver_test('linux_mainline')
linux_driver_test('linux_stable')
linux_driver_test('linux_rohm_devel')
