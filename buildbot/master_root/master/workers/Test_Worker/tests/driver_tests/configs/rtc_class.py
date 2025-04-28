from dataclasses import dataclass, field
import pytest
from time import sleep
import sys
import os
import copy
import math
import numbers
sys.path.append(os.path.abspath("."))

from test_class_helpers import get_srv_time, get_srv_epoch, find_rtc_files, set_rtc_time, get_rtc_date, get_rtc_epoch, split_datetime, get_beagle_epoch, set_beagle_time_from_rtc, set_rtc_time_from_bbb_sys
@dataclass
class rtc:
    board: dict
    result: dict = field(default_factory=lambda: {
    'type':         None,
    'result_dir':   None,
    'stage':        None,
    'product':      None,
    'return':       [],
    'expect':       [],
    })

    info: dict = field(default_factory=lambda: {
        'srv_time':     None,
    })

    ### RTC functions
    def set_rtc_from_bbb_sys_time(self, command, rtc_name):
        self.result['rtc'] = rtc_name
        self.result['stage'] = 'set_rtc_from_bbb_sys_time'
        path, dev_file, returncode = find_rtc_files(command, rtc_name)
        if returncode == 0:
            self.result['expect_low'] = get_beagle_epoch(command)

            returncode = set_rtc_time_from_bbb_sys(command, dev_file)
            self.result['return'] = get_rtc_epoch(command, rtc_name)

            self.result['expect_high'] = get_beagle_epoch(command)
        else:
            self.result['return'] = "RTC files not found"
            self.result['rc'] = -1

        self.result['dev_file'] = dev_file
        self.result['sysfs_path'] = path

        return self.result

    def set_bbb_sys_from_rtc(self, command, rtc_name):
        self.result['rtc'] = rtc_name
        self.result['stage'] = 'set_bbb_from_rtc_time'

        path, dev_file, returncode = find_rtc_files(command, rtc_name)

        if returncode == 0:
            self.result['expect_low'] = get_rtc_epoch(command, rtc_name)

            returncode = set_beagle_time_from_rtc(command, dev_file)
            self.result['return'] = get_beagle_epoch(command)

            self.result['expect_high'] = get_rtc_epoch(command, rtc_name)
        else:
            self.result['return'] = "RTC files not found"
            self.result['rc'] = -1

        self.result['dev_file'] = dev_file
        self.result['sysfs_path'] = path

        return self.result

    def set_rtc_from_srv_time(self, command, rtc_name):
        self.result['rtc'] = rtc_name
        self.result['stage'] = 'set_rtc_from_srv_time'
        self.result['expect'] = 'range'

        path, dev_file, returncode = find_rtc_files(command, rtc_name)

        self.result['expect_low'] = get_srv_epoch()
        self.info['srv_time'] = get_srv_time()

        if returncode == 0:
            stdout, stderr, returncode = set_rtc_time(command, dev_file, self.info['srv_time'])
            self.result['return'] = int(get_rtc_epoch(command, rtc_name))
            self.result['expect_high'] = get_srv_epoch()

        else:
            self.result['return'] = "RTC files not found"
            self.result['rc'] = -1

        self.result['dev_file'] = dev_file
        self.result['sysfs_path'] = path

        return self.result

    def reset_and_check_date(self, command, rtc_name, datetime):
        self.result['rtc'] = rtc_name
        self.result['stage'] = 'reset_and_check_date'
        self.result['rc'] = 0

        path, dev_file, returncode = find_rtc_files(command, rtc_name)
        date, time = split_datetime(datetime)

        if returncode == 0:
            stdout, stderr, returncode = set_rtc_time(command, dev_file, datetime)
            self.result['return'] = get_rtc_date(command, rtc_name)

        else:
            self.result['return'] = "RTC files not found"
            self.result['rc'] = -1
        self.result['dev_file'] = dev_file
        self.result['sysfs_path'] = path

        self.result['expect'] = date

        return self.result
