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

def check_dts_error(rc, stdout, stderr, product, test_dts):
    if 'Error' in stderr:
        return {product+'_'+test_dts+'_dts_error': stderr, product+'_'+test_dts+'_dts_make_passed': False , product+'_do_steps' : False, product+'_skip_dts_tests' : True }
    else:
        return {product+'_'+test_dts+'_dts_error': stderr, product+'_'+test_dts+'_dts_make_passed': True , product+'_do_steps' : True, product+'_skip_dts_tests' : False }

def check_dts_make(step, product, dts):
    if dts == 'default':
        if (util.Property(product+'_default_dts_make_passed') == True):
            return False
        else:
            return True
    else:
        if util.Property(product+'_'+dts+'_dts_make_passed') == True:
            return False
        if util.Property(product+'_skip_dts_tests') == True:
            return False
        else:
            return True

def check_init_driver_test(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_init_driver_tests_passed': False, product+'_do_steps' : False }
    else:
        return {product+'_init_driver_tests_passed': True, product+'_do_steps' : True }

def check_sanitycheck_error(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_sanitycheck_passed': False ,product+'_do_steps' : False }
    else:
        return {product+'_sanitycheck_passed': True , product+'_do_steps' : True }

def check_driver_tests(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_skip_dts_tests': True, product+'_do_steps': False}
    else:
        return {product+'_skip_dts_tests': False, product+'_do_steps' : True}

class GenerateStagesCommand(buildstep.ShellMixin, steps.BuildStep):

    def __init__(self,test_board, product,test_type, dts, check_driver_tests_partial, **kwargs):
        kwargs = self.setupShellMixin(kwargs)
        super().__init__(**kwargs)
        self.test_board = test_board
        self.product = product
        self.test_type = test_type
        self.dts = dts
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)
        self.check_driver_tests_partial = check_driver_tests_partial

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
                    extract_fn=self.check_driver_tests_partial)
                    for stage in self.extract_stages(self.observer.getStdout())
                ])
            elif self.test_type == "dts":
                self.build.addStepsAfterCurrentStep([steps.SetPropertyFromCommand(
                    command=["pytest","--lg-env="+self.test_board+".yaml",self.product+"/dts/"+self.dts+"/"+stage,"--dts="+self.dts],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == True,
                    extract_fn=self.check_driver_tests_partial)
                    for stage in self.extract_stages(self.observer.getStdout())
                ])

        return result

#         or re.search('^v('+kernel_modules['linux_ver'][product][0]+'.*$|[6-9]\\.[0-9]|[6-9]\\.[0-9\\].*$){1,2}(-rc[1-9][0-9]?)?$',step.getProperty('commit-description')):
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

def copy_test_kernel_modules_to_nfs(project_name, product, test_dts):
    copy_commands =[]
    for value in kernel_modules['build'][product]:
        copy_commands.append(util.ShellArg(command=["cp", "_test-kernel-modules/"+product+"/"+value, dir_nfs], logname="Copy "+value+" to nfs"))
    projects[project_name]['factory'].addStep(steps.ShellSequence(commands=copy_commands,doStepIf=util.Property(product+'_'+test_dts+'_dts_make_passed') == True or product == 'overlay_merger' and util.Property(product+'_skip_dts_tests') != True, hideStepIf=skipped, name=product+": Copy test kernel modules to nfs"))

def download_test_boards(project_name):
    projects[project_name]['factory'].addStep(steps.FileDownload(mastersrc="configs/kernel_modules.py",
                            workerdest="../../tests/pmic/configs/kernel_modules.py",
                            name="Download kernel_modules.py"))

def initialize_driver_test(project_name, test_board, product, test_dts):
    check_tag_partial=functools.partial(check_tag, product=product)
    check_init_driver_test_partial= functools.partial(check_init_driver_test, product=product)

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra", "test_000_login.py","--power_port="+test_boards[test_board]['power_port'],"--beagle="+test_boards[test_board]['name']],
        workdir="../tests/pmic",
        extract_fn=check_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        name=product+": Login to "+test_boards[test_board]['name']))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "--lg-env", test_boards[test_board]['name']+".yaml", "test_001_init_overlay.py"],
        workdir="../tests/pmic",
        extract_fn=check_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped, name=product+": Install overlay merger"))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_002_merge_dt_overlay.py","--product="+product],
        workdir="../tests/pmic",
        extract_fn=check_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped, name=product+": Merge device tree overlays"))

    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_003_insmod_tests.py","--product="+product],
        workdir="../tests/pmic",
        extract_fn=check_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped,
        name=product+": insmod test modules"))
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=[
        "pytest","-W","ignore::DeprecationWarning","-ra", "--lg-env", test_boards[test_board]['name']+".yaml", "test_004_init_regulator_test.py","--product="+product],
        workdir="../tests/pmic",
        extract_fn=check_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == True,
        hideStepIf=skipped,
        name=product+": init_regulator_test.py"))

def generate_driver_tests(project_name,test_board,product, check_tag_partial, test_type, dts=None):
    check_driver_tests_partial = functools.partial(check_driver_tests, product=product)
    if test_type == "regulator":
        check_sanitycheck_error_partial = functools.partial(check_sanitycheck_error, product=product)
        projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(command=[
            'pytest', '--lg-env='+test_board+".yaml", product+'/test_000_sanitycheck.py'],
            workdir="../tests/pmic/",
            extract_fn=check_sanitycheck_error_partial,
            doStepIf=check_tag_partial and util.Property(product+'_'+dts+'_dts_make_passed') == True and util.Property(product+'_do_steps') == True,
            hideStepIf=skipped,
            name=product+": test_000_sanitycheck.py"))

        projects[project_name]['factory'].addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, check_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type], workdir="../tests/pmic",
            haltOnFailure=True,
            #            doStepIf=check_tag_partial and util.Property(product+'_'+dts+'_dts_make_passed') == True and util.Property(product+'_sanitycheck_passed') == True, hideStepIf=skipped))
            doStepIf=util.Property(product+'_do_steps') == True))

        collect_dmesg_and_dts(project_name, test_board, product, check_tag_partial, test_dts=dts)

    elif test_type == "dts":
        projects[project_name]['factory'].addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, check_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type, dts], workdir="../tests/pmic",
            haltOnFailure=True,
            doStepIf=util.Property(product+'_do_steps') == True))

        collect_dmesg_and_dts(project_name, test_board, product, check_tag_partial, test_dts=dts)

def check_dts_tests(product):
    dts_tests=[]
    if product in kernel_modules['dts_tests'].keys():
        for dts in kernel_modules['dts_tests'][product]:
            dts_tests.append(dts)
    return dts_tests

def copy_generated_dts(project_name, product, dts, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["cp", "../../../tests/pmic/configs/dts_generated/"+product+"/generated_dts_"+dts+".dts", "./"+product],
        workdir="build/_test-kernel-modules",
        doStepIf=check_tag_partial and util.Property(product+'_skip_dts_tests') != True,
        hideStepIf=skipped,
        name=product+": Copy generated dts: "+dts))

def generate_dts(project_name, product, dts, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "generate_dts.py", product, dts],
        workdir="../tests/pmic",
        doStepIf=check_tag_partial and util.Property(product+'_skip_dts_tests') != True,
        hideStepIf=skipped,
        name=product+": Generate dts: "+dts))

def build_dts(project_name, product, test_dts, check_tag_partial):
    check_dts_error_partial = functools.partial(check_dts_error, product=product, test_dts=test_dts)
    projects[project_name]['factory'].addStep(steps.SetPropertyFromCommand(
        command=['make'],
        env={'KERNEL_DIR':'../../','CC':dir_compiler_arm32+'arm-linux-gnueabihf-','PWD':'./','DTS_FILE':'generated_dts_'+test_dts+'.dts'},
        workdir="build/_test-kernel-modules/"+product,
        doStepIf=check_tag_partial and util.Property(product+'_skip_dts_tests') != True,
        hideStepIf=skipped,
        extract_fn=check_dts_error_partial,
        name=product+": Build dts: "+test_dts))

def dts_report(project_name, product, test_dts, check_dts_make_partial=None, check_tag_partial=None):
    if test_dts == 'default':
        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "dts_error", product, 'default', util.Property(product+'_default_dts_error')],
            workdir="../tests",
            doStepIf=check_tag_partial and util.Property(product+'_default_dts_make_passed') != True,
            hideStepIf=skipped,
            name=product+": write dts build fail to report"))

    elif test_dts != 'default':
        projects[project_name]['factory'].addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "dts_error", product, test_dts, util.Property(product+'_'+test_dts+'_dts_error')],
            workdir="../tests",
            doStepIf=check_dts_make_partial,
            hideStepIf=skipped,
            name=product+": write dts build fail to report"))

def initialize_product(project_name, product, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_product", "PMIC", product],
        workdir="../tests",
        name="Initialize test report: "+product,
        doStepIf=check_tag_partial,
        hideStepIf=skipped))

def collect_dmesg_and_dts(project_name, test_board, product, check_tag_partial, test_dts='default'):
    projects[project_name]['factory'].addStep(steps.ShellSequence(
        commands=[
            util.ShellArg(command=['pytest', '--lg-env='+test_boards[test_board]['name']+'.yaml', 'test_get_dmesg.py', '--product='+product]),
            util.ShellArg(command=['cp','../../'+projects[project_name]['builderNames'][0]+'/build/_test-kernel-modules/'+product+'/generated_dts_'+test_dts+'.dts', '../results/'+product+'/'])],
        workdir="../tests/pmic/",
        doStepIf=check_tag_partial and util.Property(product+'_do_steps') != True,
        hideStepIf=skipped,
        name=product+": Collect dmesg and .dts"
    ))

def finalize_product(project_name, product, check_tag_partial):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "finalize_product", projects[project_name]['builderNames'][0], util.Property('commit-description'), "PMIC", product, util.Property(product+'_do_steps')],
        workdir="../tests",
        name="Finalize test report: "+product,
        doStepIf=check_tag_partial,
        hideStepIf=skipped))

def run_driver_tests(project_name):
    projects[project_name]['factory'].addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_report", projects[project_name]['builderNames'][0], util.Property('commit-description')],
        workdir="../tests",
        name="Initialize test report" ))

    for test_board in test_boards:
        for product in test_boards[test_board]['products']:
            check_tag_partial=functools.partial(check_tag, product=product)
            initialize_product(project_name, product, check_tag_partial)
            generate_dts(project_name, product, 'default', check_tag_partial)
            copy_generated_dts(project_name, product, 'default', check_tag_partial)

            build_dts(project_name, product, 'default', check_tag_partial)
            dts_report(project_name, product, 'default', check_tag_partial=check_tag_partial)

            copy_test_kernel_modules_to_nfs(project_name, product, 'default')

            initialize_driver_test(project_name, test_board, product, 'default')

            generate_driver_tests(project_name,test_boards[test_board]['name'],product, check_tag_partial, "regulator", "default")

            dts_tests = check_dts_tests(product)
            for dts in dts_tests:
                check_dts_make_partial=functools.partial(check_dts_make, product=product, dts=dts)
                generate_dts(project_name, product, dts, check_tag_partial)
                copy_generated_dts(project_name, product, dts, check_tag_partial)
                build_dts(project_name, product, dts, check_tag_partial)
                dts_report(project_name, product, dts, check_dts_make_partial)

                copy_test_kernel_modules_to_nfs(project_name, product, dts)

                initialize_driver_test(project_name, test_board, product, dts)
                generate_driver_tests(project_name, test_boards[test_board]['name'], product, check_tag_partial, "dts", dts )
            finalize_product(project_name, product, check_tag_partial)

def linux_driver_test(project_name):
    build_kernel_arm32(project_name)
    copy_kernel_binaries_to_tftpboot(project_name)
    update_test_kernel_modules(project_name)
    build_overlay_merger(project_name)
    copy_overlay_merger_to_nfs(project_name)

    download_test_boards(project_name)
    run_driver_tests(project_name)

####### FACTORIES #######

linux_driver_test('test_linux')
linux_driver_test('linux-next')
linux_driver_test('linux_mainline')
linux_driver_test('linux_stable')
linux_driver_test('linux_rohm_devel')
