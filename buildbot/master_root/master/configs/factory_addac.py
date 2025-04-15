from buildbot.plugins import util, steps
from factory_helpers import *
from test_boards import *
from paths import *
import functools
import string

factory_addac_test = util.BuildFactory()


#def build_test_module_accelerometer(product, test_type):
#    extract_dts_error_partial = functools.partial(extract_dts_error, product=product, test_type=test_type)
#    doStepIf_dts_test_preparation_partial = functools.partial(doStepIf_dts_test_preparation, product=product)
#
#    factory_accelerometer_test.addStep(steps.SetPropertyFromCommand(
#        command=['make'],
#        env={'KERNEL_DIR':'../../',
#             'CC':dir_compiler_arm32+'arm-none-eabi-',
#             'PWD':'./','DTS_FILE':product+'_test.dts',
#             'TEST_TARGET':product},
#        workdir=util.Interpolate('../../Linux_Worker/%(prop:linuxdir)s/build/_test-kernel-modules/generic_accel_test'),
#        doStepIf=doStepIf_dts_test_preparation_partial,
#        hideStepIf=skipped,
#        extract_fn=extract_dts_error_partial,
#        name=product+": Build test module"
#        ))



def build_dtbo_addac(product, test_type):
    extract_dts_error_partial = functools.partial(extract_dts_error, product=product, test_type=test_type)
    doStepIf_dts_test_preparation_partial = functools.partial(doStepIf_dts_test_preparation, product=product)

    factory_addac_test.addStep(steps.SetPropertyFromCommand(
        command=['./makedtb', '-i', product+'/'+product+'_test.dts','-o', 'dtbo', '-n', product+'/'+product+'_test'],
        env={'KERNEL_DIR':'../',
             'CC':dir_compiler_arm32+'arm-none-eabi-',
             'TEST_TARGET':product},
        workdir=util.Interpolate('../../Linux_Worker/%(prop:linuxdir)s/build/_test-kernel-modules/'),
        doStepIf=doStepIf_dts_test_preparation_partial,
        hideStepIf=skipped,
        extract_fn=extract_dts_error_partial,
        name=product+": Build dtbo"
        )
                               )
    factory_addac_test.addStep(steps.SetPropertyFromCommand(
        command=['./makedtb', '-i',
                 kernel_modules['adc_pair'][product]['adc']+'/'+kernel_modules['adc_pair'][product]['adc']+'_test.dts',
                 '-o', 'dtbo', '-n', kernel_modules['adc_pair'][product]['adc']+'/'+kernel_modules['adc_pair'][product]['adc']+'_test'],
        env={'KERNEL_DIR':'../',
             'CC':dir_compiler_arm32+'arm-none-eabi-',
             'TEST_TARGET':product},
        workdir=util.Interpolate('../../Linux_Worker/%(prop:linuxdir)s/build/_test-kernel-modules/'),
        doStepIf=doStepIf_dts_test_preparation_partial,
        hideStepIf=skipped,
        extract_fn=extract_dts_error_partial,
        name=product+": Build ADC dtbo"
        ))

def initialize_addac_report(product):
    doStepIf_initialize_product_partial = functools.partial(doStepIf_initialize_product, product=product)
    factory_addac_test.addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_product", "ADDAC", product],
        workdir="../tests",
        name="Initialize test report: "+product,
        doStepIf=doStepIf_initialize_product_partial,
        ))


def run_addac_tests():
    for power_port in test_boards['addac']['power_ports']:
        for test_board in test_boards['addac']['power_ports'][power_port]:
            for product in test_boards['addac']['power_ports'][power_port][test_board]['products']:
                initialize_addac_report(product)
#                generate_dts(project_name, product, 'default')
#                copy_generated_dts(project_name, product, 'default')
                build_dtbo_addac(product,'default')
#                build_test_module_accelerometer(product, test_type='accelerometer')
                dts_report(factory_addac_test, product, 'default')

                copy_test_kernel_modules_to_nfs(factory_addac_test,
                                                product,
                                                'default',)

                copy_test_kernel_modules_to_nfs(factory_addac_test,
                                                product,
                                                'default',
                                                adc = kernel_modules['adc_pair'][product]['adc'],
                                                )

                initialize_driver_test(factory_addac_test,
                                       power_port,
                                       test_board,
                                       product, 'default',
                                       test_type='addac',
                                       result_dir='ADDAC',
                                       dev_setup='True',
                                       )
                generate_driver_tests(factory_addac_test,
                                      power_port,
                                      test_boards['addac']['power_ports'][power_port][test_board]['name'],
                                      product,
                                      test_type="addac",
                                      dts="default")

                finalize_product(factory_addac_test, product, "ADDAC")


run_addac_tests()
copy_temp_results(factory_addac_test)
save_properties(factory_addac_test, "addac")
