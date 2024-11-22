from buildbot.plugins import util, steps
from factory_helpers import *
from test_boards import *
from paths import *
import functools
import string

factory_accelerometer_test = util.BuildFactory()


def build_dts_accelerometer(product):
    extract_dts_error_partial = functools.partial(extract_dts_error, product=product)
    doStepIf_dts_test_preparation_partial = functools.partial(doStepIf_dts_test_preparation, product=product)

    factory_accelerometer_test.addStep(steps.SetPropertyFromCommand(
        command=['make'],
        env={'KERNEL_DIR':'../../',
             'CC':dir_compiler_arm32+'arm-linux-gnueabihf-',
             'PWD':'./','DTS_FILE':product+'_test.dts',
             'TEST_TARGET':product},
        workdir=util.Interpolate('../%(prop:linuxdir)s/build/_test-kernel-modules/generic_accel_test'),
        doStepIf=doStepIf_dts_test_preparation_partial,
        hideStepIf=skipped,
        extract_fn=extract_dts_error_partial,
        name=product+": Build dts: "+product
        ))


def initialize_accelerometer_report(product):
    doStepIf_initialize_product_partial = functools.partial(doStepIf_initialize_product, product=product)
    factory_accelerometer_test.addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_product", "PMIC", product],
        workdir="../tests",
        name="Initialize test report: "+product,
        doStepIf=doStepIf_initialize_product_partial,
        ))


def run_accelerometer_tests():
####### IIO_GENERIC_BUFFER_CHECK_HERE!!!


    for test_board in test_boards:
        for product in test_boards[test_board]['products']:
            initialize_accelerometer_report(product)
##            generate_dts(project_name, product, 'default')
##            copy_generated_dts(project_name, product, 'default')
            build_dts_accelerometer(product)
            dts_report(factory_accelerometer_test, product, 'default')

            copy_test_kernel_modules_to_nfs(factory_accelerometer_test,
                                            product,
                                            'default',
                                            generic_module='generic_accel_test')

            initialize_driver_test(factory_accelerometer_test,
                                   test_board,
                                   product, 'default',
                                   dev_setup=True,
                                   type='accelerometer')
            generate_driver_tests(factory_accelerometer_test,
                                  test_boards[test_board]['name'],
                                  product,
                                  "accelerometer",
                                  "default")
#
#            dts_tests = check_dts_tests(product)
#            for dts in dts_tests:
#                generate_dts(project_name, product, dts)
#                copy_generated_dts(project_name, product, dts)
#                build_dts(project_name, product, dts)
#                dts_report(project_name, product, dts)
#
#                copy_test_kernel_modules_to_nfs(project_name, product, dts)
#                initialize_driver_test(project_name, test_board, product, dts)
#                generate_driver_tests(project_name, test_boards[test_board]['name'], product, "dts", dts )
#
#            finalize_product(project_name, product)

run_accelerometer_tests()
