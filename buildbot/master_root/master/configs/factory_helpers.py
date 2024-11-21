from buildbot.plugins import util, steps
from buildbot.process import buildstep, logobserver
from twisted.internet import defer
import re
import math
import functools
from kernel_modules import *

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
                    command=["pytest","--lg-log","../temp_results/","--lg-env="+self.test_board+".yaml",self.product+"/"+stage],
                    name=self.product+": "+stage,
                    workdir="../tests/pmic",
                    doStepIf=util.Property(self.product+'_do_steps') == True,
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


####### HELPERS TO ADD STEPS

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
####### Generic doStepIf_ and extract_ functions for
##      PMIC and sensor factories.

def doStepIf_initialize_product(step, product):
    if step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty('preparation_step_failed') != True:
            return True
        else:
            return False
    else:
        return False


def doStepIf_dts_test_preparation(step, product):
    if step.getProperty('kernel_build_failed') == True:
        return False
    elif step.getProperty('preparation_step_failed') == True:
        return False
    elif step.getProperty('overlay_merger_build_failed') == True:
        return False
    elif step.getProperty(product+'_do_steps') == False:
        return False
    elif step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty(product+'_skip_dts_tests') != True:
            return True
        else:
            return False
    else:
        return False

def doStepIf_dts_report(step, product, test_dts):
    if step.getProperty('preparation_step_failed') == True:
        return False
    elif step.getProperty('buildername') == 'linux-rohm-devel' or check_tag(step, product) == True:
        if step.getProperty(product+'_'+test_dts+'_dts_make_passed') == False:
            return True
    else:
        return False


def extract_dts_error(rc, stdout, stderr, product, test_dts='default'):
    if 'Error' in stderr:
        return {
                product+'_'+test_dts+'_dts_error': stderr,
                product+'_'+test_dts+'_dts_make_passed': False,
                product+'_do_steps' : False,
                product+'_skip_dts_tests' : True,
                'single_test_failed' : True,
                product+'_dts_fail': True
                }
    else:
        return {
                product+'_'+test_dts+'_dts_error': stderr,
                product+'_'+test_dts+'_dts_make_passed': True,
                product+'_do_steps' : True,
                product+'_skip_dts_tests' : False,
                product+'_dts_fail':False
                }
