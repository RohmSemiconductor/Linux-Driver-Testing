from buildbot.plugins import util, steps
from buildbot.process import buildstep, logobserver
from twisted.internet import defer
import re
import math
import functools
from kernel_modules import *
from test_boards import *
from paths import *
####### Generates steps for tests
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
                    command=["pytest","--lg-log","../temp_results_PMIC/","--lg-env="+self.test_board+".yaml",self.product+"/"+stage],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == 'True',
                    extract_fn=self.extract_driver_tests_partial)
                    for stage in self.extract_stages(self.observer.getStdout())
                ])
            elif self.test_type == "accelerometer":
                self.build.addStepsAfterCurrentStep([steps.SetPropertyFromCommand(
                    command=["pytest","--lg-log","../temp_results_sensor/","--lg-env="+self.test_board+".yaml",self.product+"/"+stage],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == 'True',
                    extract_fn=self.extract_driver_tests_partial)
                    for stage in self.extract_stages(self.observer.getStdout())
                ])
            elif self.test_type == "dts":
                self.build.addStepsAfterCurrentStep([steps.SetPropertyFromCommand(
                    command=["pytest","--lg-log","../temp_results/","--lg-env="+self.test_board+".yaml",self.product+"/dts/"+self.dts+"/"+stage,"--dts="+self.dts],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == True,
                    extract_fn=self.extract_driver_tests_partial)
                    for stage in self.extract_stages(self.observer.getStdout())
                ])
        return result

####### GENERIC HELPERS
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


def check_tag(step,product):
    if re.search('^next.*', step.getProperty('commit-description')):    #check for linux next
        print(step.getProperty('commit-description'))
        return True
    elif re.search('^'+product+'.*', step.getProperty('commit-description')): #check for driver fix
        return True
    elif step.getProperty('repository') == 'https://github.com/RohmSemiconductor/Linux-Kernel-PMIC-Drivers.git':
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


####### HELPERS TO ADD STEPS + RELATED doStepIf_ and extract_fn_ functions

def extract_kunit_login(rc, stdout, stderr):
    if 'FAILURES' in stdout:
        return { 'kunit_login_failed' : 'True', 'kunit_login_tried': 'True' }
    else:
        return { 'kunit_login_failed' : 'False', 'kunit_login_tried': 'True' }

def extract_kunit_test_error(rc, stdout, stderr):
    if rc != 0:
        return { 'preparation_step_failed': 'True' }
    else:
        return { 'kunit_test_passed': 'True' }

def doStepIf_kunit_iio_gts_test(step):
    if step.getProperty('kunit_login_failed') == 'False':
        if step.getProperty('preparation_step_failed') == 'False':
            if check_kunit_iio_gts_test(step) == 'True':
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def doStepIf_kunit_tests(step):
    if step.getProperty('kunit_login_failed') == 'False':
        if step.getProperty('preparation_step_failed') != 'True':
            return True
        else:
            return False
    else:
        return False


def extract_driver_tests(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_skip_dts_tests': 'True', product+'_do_steps': 'False', product+'_dts_collected': 'False', product+'_dmesg_collected': 'False', 'single_test_failed': 'True', 'git_bisect_trigger': 'True'}
    elif rc != 0:
        return {product+'_skip_dts_tests': 'True', product+'_do_steps': 'False', product+'_dts_collected': 'False', product+'_dmesg_collected': 'False', 'single_test_failed': 'True', 'git_bisect_trigger': 'True'}
    else:
        return {product+'_skip_dts_tests': 'False', product+'_do_steps' : 'True', 'single_test_passed': 'True'}

def doStepIf_powerdown_beagle(step, product):
    if step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty(product+'_dts_fail') == 'True':
            return False
        elif step.getProperty('preparation_step_failed') == 'True':
            return False
        elif step.getProperty('iio_generic_buffer_found') == 'False' and step.getProperty('factory_type') == 'accelerometer':
            return False
        else:
            return True
    else:
        return False

def doStepIf_generate_driver_tests(step, product, dts):
    if step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty(product+'_'+dts+'_dts_make_passed') == 'True':
            if step.getProperty(product+'_do_steps') == 'True':
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def generate_driver_tests(_factory, power_port, test_board, product, test_type='PMIC', dts=None):
    extract_driver_tests_partial = functools.partial(extract_driver_tests, product=product)
    doStepIf_kunit_iio_gts_test_partial = functools.partial(doStepIf_kunit_iio_gts_test, product=product, dts=dts)
    doStepIf_generate_driver_tests_partial = functools.partial(doStepIf_generate_driver_tests, product=product, dts=dts)
    doStepIf_powerdown_beagle_partial = functools.partial(doStepIf_powerdown_beagle, product=product)

    if test_type == "regulator":

        extract_sanitycheck_error_partial = functools.partial(extract_sanitycheck_error, product=product)
        _factory.addStep(steps.SetPropertyFromCommand(command=[
            'pytest','--lg-log', "../temp_results/", '--lg-env='+test_board+".yaml", product+'/test_000_sanitycheck.py'],
            workdir="../tests/pmic/",
            extract_fn=extract_sanitycheck_error_partial,
            doStepIf=doStepIf_generate_driver_tests_partial,
            hideStepIf=skipped,
            name=product+": test_000_sanitycheck.py"
            ))

        _factory.addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, extract_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type], workdir="../tests/pmic",
            haltOnFailure=True,
            doStepIf=doStepIf_generate_driver_tests_partial
            ))

        collect_dmesg_and_dts(project_name, test_board, product, test_dts=dts)

    elif test_type =="accelerometer":

        _factory.addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, extract_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type], workdir="../tests/pmic",
            haltOnFailure=True,
            doStepIf=doStepIf_generate_driver_tests_partial
            ))

    elif test_type == "dts":
        _factory.addStep(GenerateStagesCommand(
            test_board, product, test_type, dts, extract_driver_tests_partial,
            name=product+": Generate "+test_type+" test stages",
            command=["python3", "generate_steps.py", product, test_type, dts], workdir="../tests/pmic",
            haltOnFailure=True,
            doStepIf=doStepIf_generate_driver_tests_partial
            ))

        collect_dmesg_and_dts(project_name, test_board, product, test_dts=dts)

    _factory.addStep(steps.ShellCommand(
        command=["pytest","-W","ignore::DeprecationWarning", "-ra", "test_005_powerdown_beagle.py","--power_port="+power_port,"--beagle="+test_boards[test_type]['power_ports'][power_port][test_board]['name']],
        workdir="../tests/pmic/",
        doStepIf=doStepIf_powerdown_beagle_partial,
        hideStepIf=skipped,
        name=product+": power down beagle"
        ))

def extract_init_driver_test(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_init_driver_tests_passed': 'False', product+'_do_steps' : 'False' }
    elif rc != 0:
        return {product+'_init_driver_tests_passed': 'False', product+'_do_steps' : 'False' }
    else:
        return {product+'_init_driver_tests_passed': 'True', product+'_do_steps' : 'True' }


def extract_init_driver_test_login(rc, stdout, stderr, product):
    if 'FAILURES' in stdout:
        return {product+'_init_driver_tests_passed': 'False',product+'_login_failed': 'True',  product+'_do_steps' : 'False', 'single_login_failed' : 'True' }
    elif rc != 0:
        return {product+'_init_driver_tests_passed': 'False', product+'_login_failed': 'True', product+'_do_steps' : 'False', 'single_login_failed' : 'True' }
    else:
        return {product+'_init_driver_tests_passed': 'True', product+'_do_steps' : 'True', 'single_login_passed' : 'True' }


def doStepIf_login(step, product):
    if step.getProperty('factory_type') == 'accelerometer':
        if step.getProperty('iio_generic_buffer_found') == 'False':
            return False
    if step.getProperty(product+'_init_driver_test_passed') == 'False':
        return False
    elif step.getProperty(product+'_do_steps') == 'True':
        return True
    else:
        return False

def extract_check_iio_generic_buffer(rc, stdout, stderr):
    if 'FAILURES' in stdout:
        return {'iio_generic_buffer_found' : 'False' }
    else:
        return {'iio_generic_buffer_found' : 'True' }

def initialize_driver_test(_factory, power_port, test_board, product, test_dts,
                           test_type='PMIC', result_dir='PMIC', dev_setup='False', type=None):

    extract_init_driver_test_partial= functools.partial(extract_init_driver_test, product=product)
    extract_init_driver_test_login_partial= functools.partial(extract_init_driver_test_login, product=product)
    doStepIf_login_partial = functools.partial(doStepIf_login, product=product)

    if dev_setup == 'False':
        _factory.addStep(steps.SetPropertyFromCommand(
            command=["pytest","-W","ignore::DeprecationWarning", "-ra",
                     "test_000_login.py",
                     "--power_port="+power_port,
                     "--beagle="+test_boards[test_type]['power_ports'][power_port][test_board]['name'],
                     "--result_dir="+result_dir,],

            workdir="../tests/pmic",
            extract_fn=extract_init_driver_test_login_partial,
            doStepIf=doStepIf_login_partial,
            name=product+": Login to "+test_boards[test_type][test_board]['name']
            ))

    if dev_setup == 'True':
        _factory.addStep(steps.SetPropertyFromCommand(
            command=["pytest","-W","ignore::DeprecationWarning", "-ra",
                     "test_000_no_ippower_login.py",
                     "--power_port="+power_port,
                     "--beagle="+test_boards[test_type]['power_ports'][power_port][test_board]['name'],
                     "--result_dir="+result_dir,
                     ],

            workdir="../tests/pmic",
            extract_fn=extract_init_driver_test_login_partial,
            doStepIf=doStepIf_login_partial,
            name=product+": Login to "+test_boards[test_type]['power_ports'][power_port][test_board]['name']
            ))

    if type == 'accelerometer':
        _factory.addStep(steps.SetPropertyFromCommand(
            command=["pytest","-W","ignore::DeprecationWarning",
                     "--lg-log", "../temp_results/",
                     "--lg-env", test_boards[test_type]['power_ports'][power_port][test_board]['name']+".yaml",
                     "test_000_check_iio_generic_buffer.py",
                     "--beagle="+test_boards[test_type]['power_ports'][power_port][test_board]['name']],

            workdir="../tests/pmic",
            extract_fn=extract_check_iio_generic_buffer,
            doStepIf=doStepIf_login_partial,
            name="Check for iio_generic_buffer",
            ))


    _factory.addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning",
                 "--lg-log", "../temp_results/",
                 "--lg-env", test_boards[test_type]['power_ports'][power_port][test_board]['name']+".yaml",
                 "--result_dir="+result_dir,
                 "test_001_init_overlay.py"],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == 'True',
        hideStepIf=skipped, name=product+": Install overlay merger"
        ))

    _factory.addStep(steps.SetPropertyFromCommand(
        command=["pytest","-W","ignore::DeprecationWarning","-ra",
                 "--lg-log", "../temp_results/",
                 "--lg-env", test_boards[test_type]['power_ports'][power_port][test_board]['name']+".yaml",
                 "test_002_merge_dt_overlay.py",
                 "--product="+product,
                 "--result_dir="+result_dir],
        workdir="../tests/pmic",
        extract_fn=extract_init_driver_test_partial,
        doStepIf=util.Property(product+'_do_steps') == 'True',
        hideStepIf=skipped, name=product+": Merge device tree overlays"
        ))

    if test_type == 'PMIC':
        _factory.addStep(steps.SetPropertyFromCommand(
            command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-log", "../temp_results/", "--lg-env", test_boards[test_type]['power_ports'][power_port][test_board]['name']+".yaml", "test_003_insmod_tests.py","--product="+product],
            workdir="../tests/pmic",
            extract_fn=extract_init_driver_test_partial,
            doStepIf=util.Property(product+'_do_steps') == 'True',
            hideStepIf=skipped,
            name=product+": insmod test modules"))

    elif test_type == 'accelerometer':
        _factory.addStep(steps.SetPropertyFromCommand(
            command=["pytest","-W","ignore::DeprecationWarning","-ra", "--lg-log", "../temp_results/", "--lg-env", test_boards[test_type]['power_ports'][power_port][test_board]['name']+".yaml", "test_003_insmod_accel_tests.py","--product="+product],
            workdir="../tests/pmic",
            extract_fn=extract_init_driver_test_partial,
            doStepIf=util.Property(product+'_do_steps') == 'True',
            hideStepIf=skipped,
            name=product+": insmod test modules"))


def doStepIf_copy_test_kernel_modules_to_nfs(step, product, test_dts):
    if step.getProperty('kernel_build_failed') == 'True':
        return False
    elif step.getProperty('preparation_step_failed') == 'True':
        return False
    elif step.getProperty('overlay_merger_build_failed') == 'True':
        return False
    elif step.getProperty(product+'_'+test_dts+'_dts_make_passed') == 'True':
        if step.getProperty(product+'_skip_dts_tests') != 'True':
            return True
    else:
        return False


def copy_test_kernel_modules_to_nfs(_factory, product, test_dts, generic_module = None):
    doStepIf_copy_test_kernel_modules_to_nfs_partial = functools.partial(doStepIf_copy_test_kernel_modules_to_nfs, product=product, test_dts=test_dts)

    copy_commands =[]
    for value in kernel_modules['build'][product]:
        if generic_module == None:
            copy_commands.append(util.ShellArg(
                command=["cp", "_test-kernel-modules/"+product+"/"+value, dir_nfs],
                logname="Copy "+value+" to nfs"))
        else:
            copy_commands.append(util.ShellArg(
                command=util.Interpolate('cp ../../%(prop:linuxdir)s/build/_test-kernel-modules/'
                                         +generic_module+'/'+value+' '+dir_nfs),
                logname="Copy "+value+" to nfs"))

    _factory.addStep(steps.ShellSequence(
            commands=copy_commands,
            doStepIf=doStepIf_copy_test_kernel_modules_to_nfs_partial,
            hideStepIf=skipped,
            name=product+": Copy test kernel modules to nfs"
            ))


def doStepIf_dts_report(step, product, test_dts):
    if step.getProperty('preparation_step_failed') == 'True':
        return False
    elif step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == 'True':
        if step.getProperty(product+'_'+test_dts+'_dts_make_passed') == 'False':
            return True
    else:
        return False


def dts_report(_factory, product, test_dts='default'):
    doStepIf_dts_report_partial=functools.partial(doStepIf_dts_report, product=product, test_dts=test_dts)
    if test_dts == 'default':
        _factory.addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "dts_error", product, 'default', util.Property(product+'_default_dts_error')],
            workdir="../tests",
            doStepIf=doStepIf_dts_report_partial,
            hideStepIf=skipped,
            name=product+": write dts build fail to report"
            ))

    elif test_dts != 'default':
        _factory.addStep(steps.ShellCommand(
            command=["python3", "report_janitor.py", "dts_error", product, test_dts, util.Property(product+'_'+test_dts+'_dts_error')],
            workdir="../tests",
            doStepIf=doStepIf_dts_report_partial,
            hideStepIf=skipped,
            name=product+": write dts build fail to report"
            ))

def doStepIf_finalize_product(step, product):
    if step.getProperty('preparation_step_failed') == 'True':
        return False
    elif step.getProperty('iio_generic_buffer_found') == 'False' and step.getProperty('factory_type') == 'accelerometer':
        return False
    elif step.getProperty('git_bisecting') == 'True':
        return False
    elif step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        return True
    else:
        return False

def finalize_product(_factory, product, result_dir):
    doStepIf_finalize_product_partial = functools.partial(doStepIf_finalize_product, product=product)
    _factory.addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "finalize_product",
                 util.Property('buildername'),
                 util.Property('commit-description'),
                 result_dir,
                 product,
                 util.Property(product+'_do_steps')],
        workdir="../tests",
        name="Finalize test report: "+product,
        doStepIf=doStepIf_finalize_product_partial,
        hideStepIf=skipped
        ))
####### Generic doStepIf_ and extract_ functions for
##      PMIC and sensor factories.

def doStepIf_initialize_product(step, product):
    if step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty('factory_type') == 'accelerometer' and step.getProperty('iio_generic_buffer_found') == 'False':
            return False
        elif step.getProperty('preparation_step_failed') != 'True':
            return True
        else:
            return False
    else:
        return False


def doStepIf_dts_test_preparation(step, product):
    if step.getProperty('kernel_build_failed') == 'True':
        return False
    elif step.getProperty('preparation_step_failed') == 'True':
        return False
    elif step.getProperty('overlay_merger_build_failed') == 'True':
        return False
    elif step.getProperty('factory_type') == 'accelerometer' and step.getProperty('iio_generic_buffer_found')== 'False':
        return False
    elif step.getProperty(product+'_do_steps') == 'False':
        return False
    elif step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty(product+'_skip_dts_tests') != 'True':
            return True
        else:
            return False
    else:
        return False


def extract_dts_error(rc, stdout, stderr, product, test_dts='default'):
    if 'Error' in stderr:
        return {
                product+'_'+test_dts+'_dts_error': stderr,
                product+'_'+test_dts+'_dts_make_passed': 'False',
                product+'_do_steps' : 'False',
                product+'_skip_dts_tests' : 'True',
                'single_test_failed' : 'True',
                product+'_dts_fail': 'True'
                }
    else:
        return {
                product+'_'+test_dts+'_dts_error': stderr,
                product+'_'+test_dts+'_dts_make_passed': 'True',
                product+'_do_steps' : 'True',
                product+'_skip_dts_tests' : 'False',
                product+'_dts_fail': 'False'
                }
