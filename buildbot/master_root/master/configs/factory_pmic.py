from buildbot.plugins import util, steps
from factory_helpers import *
from test_boards import *
from paths import *
import functools
import string

factory_pmic_test = util.BuildFactory()


def initialize_pmic_report(product):
    doStepIf_initialize_product_partial = functools.partial(doStepIf_initialize_product, product=product)
    factory_pmic_test.addStep(steps.ShellCommand(
        command=["python3", "report_janitor.py", "initialize_product", "PMIC", product],
        workdir="../tests",
        name="Initialize test report: "+product,
        doStepIf=doStepIf_initialize_product_partial,
        ))


def run_pmic_tests():
    for power_port in test_boards['pmic']['power_ports']:
        for test_board in test_boards['pmic']['power_ports'][power_port]:
            for product in test_boards['pmic']['power_ports'][power_port][test_board]['products']:
                initialize_pmic_report(product)
                generate_dts(factory_pmic_test, product, 'default')
                copy_generated_dts(factory_pmic_test, product, 'default')
                build_dtbo(factory_pmic_test, product, 'default', test_type='pmic')
                build_dts(factory_pmic_test, product, 'default', test_type='pmic')
                dts_report(factory_pmic_test, product, 'default')

                copy_test_kernel_modules_to_nfs(factory_pmic_test,
                                                product,
                                                'default')

                initialize_driver_test(factory_pmic_test,
                                       power_port,
                                       test_board,
                                       product, 'default',
                                       test_type='pmic')
                generate_driver_tests(factory_pmic_test,
                                      power_port,
                                      test_boards['pmic']['power_ports'][power_port][test_board]['name'],
                                      product,
                                      "pmic",
                                      "default")

                dts_tests = check_dts_tests(product)
                for dts in dts_tests:
                    generate_dts(factory_pmic_test, product, dts)
                    copy_generated_dts(factory_pmic_test, product, dts)
                    build_dts(factory_pmic_test, product, dts, test_type='pmic')
                    dts_report(factory_pmic_test, product, dts)

                    copy_test_kernel_modules_to_nfs(factory_pmic_test, product, dts)
                    initialize_driver_test(factory_pmic_test,
                                           power_port,
                                           test_board,
                                           product,
                                           dts,
                                           test_type='pmic')
                    generate_driver_tests(factory_pmic_test, power_port, test_board, product, "dts", dts )

                finalize_product(factory_pmic_test, product, "PMIC")

set_factory_type(factory_pmic_test, 'pmic')
run_pmic_tests()
copy_temp_results(factory_pmic_test)
save_properties(factory_pmic_test, "pmic")
