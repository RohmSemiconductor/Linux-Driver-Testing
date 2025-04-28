import pytest
import sys
sys.path.append('..')
sys.path.append('./configs')
import bd71815
from test_util import check_result
from rtc_class import rtc
bd71815 = rtc(bd71815)

def test_005_rtc_test(command):
    bd71815.result['result_dir'] = 'PMIC'

    ## Set Component rtc to known date and check that it was set succesfully
    result = bd71815.reset_and_check_date(command, bd71815.board.data['rtc']['component_rtc'],
                                      bd71815.board.data['rtc']['rtc_reset'])
    check_result(result)

    ## Set BBB rtc to test server time
    result = bd71815.set_rtc_from_srv_time(command, bd71815.board.data['rtc']['sys_rtc'])
    check_result(result) #ei printtejä vielä

    ## Set BBB system clock to BBB rtc
    result = bd71815.set_bbb_sys_from_rtc(command, bd71815.board.data['rtc']['sys_rtc'])
    check_result(result)

#    ## Set Component RTC to BBB system clock
    result = bd71815.set_rtc_from_bbb_sys_time(command, bd71815.board.data['rtc']['component_rtc'])
    check_result(result)
