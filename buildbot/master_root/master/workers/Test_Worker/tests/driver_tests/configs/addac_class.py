from dataclasses import dataclass, field
import pytest
from time import sleep
import sys
import os
import copy
import math
import numbers

from test_class_helpers import bitshift_index_by_bitmask, escape_path, pc_to_int, frequency_to_ns, combine_bytes, twos_complement, bits_maxval, find_iio_device_files
sys.path.append(os.path.abspath("."))

@dataclass
class addac:
    board: dict
    result: dict = field(default_factory=lambda: {
    'type':             'ADDAC',
    'result_dir':       'ADDAC',
    'stage':            None,
    'product':          None,
    'return':           [],
    'expect':           [],
    'expect_perfect':   [],
    'expect_low':       [],
    'expect_high':      [],
    'diff':             [],
    'adc_value':        [],
    })

    info: dict = field(default_factory=lambda: {
        'dac_path':     None,
        'adc_path':     None,
        'dac_mult':     None,
        'adc_mult':     None,
    })

    def __post_init__(self):
        self.result['test_config'] = self.board.data

    def check_sysfs_information(self, command,addac):
        self.result['stage'] = 'check_sysfs'
        self.result['sub_stage'] = addac
        self.result['expect'] = 0

        if addac == 'dac':
            path = find_iio_device_files(command, self.board.data['iio_device']['name'])

        elif addac == 'adc':
            path = find_iio_device_files(command, self.board.data['iio_device']['adc'])

        if path in 'not_found':
            self.result['return'] = -2
        else:
            self.result['return'] = 0

        return self.result


    def get_sysfs_information(self, command, adc_only=False):

        try:
            if self.board.data['type'] == "DAC":
                self.info['dac_path'] = find_iio_device_files(command, self.board.data['iio_device']['name'])
                print(self.info['dac_path'])
                self.info['dac_mult'] = self.get_iio_device_mult(command, 'out')
                self.result['dac'] = self.board.data['iio_device']['name']
                self.result['adc_product'] = self.board.data['adc']

            self.info['adc_path'] = find_iio_device_files(command, self.board.data['iio_device']['adc'])
            print(self.info['adc_path'])
            self.info['adc_mult'] = self.get_iio_device_mult(command, 'in')

            self.result['adc'] = self.board.data['iio_device']['adc']
            self.result['product'] = self.board.data['name']

            retval = 0

        except Exception:
            retval = -1

        return retval

    def get_iio_device_mult(self, command, direction):
        if direction == 'in':
            stdout, stderr, returncode = command.run("cat "+self.info['adc_path']+"in_voltage_scale")
        elif direction == 'out':
            stdout, stderr, returncode = command.run("cat "+self.info['dac_path']+"out_voltage_scale")

        mult = float(stdout[0])
        return mult

    def bits_maxval(self):
        ret = pow(2,self.board.data['info']['bits'])-1

        return ret

    def _bits_to_volt(self, bits, res_bit, vcc):
        volt = bits/(res_bit/vcc)

        return volt

    def _volt_to_bits(self, volt, res_bit, vcc):
        bits = volt /(vcc/res_bit)
        bits = round(bits)

        return bits

    def write_and_read_value(self, command, channel, value):
        self.result['value'] = value
        self.result['expect'] = 'range'
        self.result['stage'] = 'write_read'
        self.result['dac_channel'] = str(channel)
        self.result['adc_channel'] = str(self.board.data['info']['channels'][channel])
        self.result['dac_volt'] = value*self.info['dac_mult']
        self.result['dac_mult'] = self.info['dac_mult']
        self.result['adc_mult'] = self.info['adc_mult']
#        self.result['tolerance'] = self.info['dac_mult'] + self.info['adc_mult']

        ### ['tolerance'] tolerance in millivolts
        self.result['tolerance'] = 70
        self.result['expect_low'] = self.result['tolerance'] * -1
        self.result['expect_high'] = self.result['tolerance']

        stdout, stderr, rc = self._write_value(command, channel, value)

        self.result['adc_value'] = self.read_adc10x(command, channel)
        self.result['adc_volt'] = self.result['adc_value'] * self.info['adc_mult']

        self.result['return'] = self.result['dac_volt'] - self.result['adc_volt']

        return self.result

    def _write_value(self, command, channel, value):
        stdout, stderr, returncode = command.run("echo "+str(value)+ " > "+self.info['dac_path']+"/"
                                                "out_voltage"+str(channel)+"_raw")
        if returncode != 0:
            print("jeejee")

        return stdout, stderr, returncode

    def read_adc10x(self, command, channel):
        try:
            if self.board.data['type'] == 'DAC':
                stdout, stderr, returncode = command. run("/./read_adc10x.sh "+self.info['adc_path']+" "
                                                          +str(self.board.data['info']['channels'][channel]))
            elif self.board.data['type'] == 'ADC':
                stdout, stderr, returncode = command. run("/./read_adc10x.sh "+self.info['adc_path']+" "
                                                          +str(channel))

            smooth_retval = 0
            for i in range(0,len(stdout)):
                smooth_retval = smooth_retval + int(stdout[i])
            smooth_retval = smooth_retval / 10

        except:
            smooth_retval = stdout[0]

        finally:
            return smooth_retval

    def read_adc_channel(self, command, channel):
        try:
            adc_value = self.read_adc10x(command, channel)
            adc_volt = adc_value * self.info['adc_mult']

        except:
            adc_volt = adc_value

        finally:
            return adc_value, adc_volt

    def _read_value(self, command, channel, value):
        stdout, stderr, returncode = command.run("cat "+self.info['adc_path']+"/"
                                                "in_voltage"+str(self.board.data['info']['channels'][channel])+"_raw")

        return stdout

    def check_stable_voltage(self, command, channel, tolerance):
        self.get_sysfs_information(command, adc_only=True)
        self.result['stage'] = 'stable_voltage'

        adc_value, adc_volt = self.read_adc_channel(command, self.board.data['info']['stable_voltage_channel'])
        self.result['return'] = adc_volt
        self.result['expect'] = 'range'
        self.result['expect_perfect'] = self.board.data['info']['stable_voltage_mv']
        self.result['expect_high'] = self.board.data['info']['stable_voltage_mv'] + tolerance
        self.result['expect_low'] = self.board.data['info']['stable_voltage_mv'] - tolerance

        return self.result
