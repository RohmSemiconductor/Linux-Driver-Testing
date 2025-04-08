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
    'type':         'addac',
    'result_dir':   'AD-DA_converters',
    'stage':        None,
    'product':      None,
    'return':       [],
    'expect':       [],
    'diff':         [],
    })

    info: dict = field(default_factory=lambda: {
        'dac_path':     None,
        'adc_path':     None,
        'dac_mult':     None,
        'adc_mult':     None,
    })

    def test_init(self, command):
        self.info['dac_path'] = find_iio_device_files(command, self.board.data['iio_device']['name'])
        self.info['adc_path'] = find_iio_device_files(command, self.board.data['iio_device']['adc'])
        self.info['dac_mult'] = self.get_iio_device_mult(command, 'out')
        self.info['adc_mult'] = self.get_iio_device_mult(command, 'in')

        print(self.info['adc_path'])
        print(self.info['dac_path'])
        print(self.info['dac_mult'])
        print(self.info['adc_mult'])

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
        self.result['expect'].append(value*self.info['dac_mult'])
        stdout, stderr, rc = self._write_value(command, channel, value)

        retval = self._read_value(command, channel, value)
        retval = float(retval[0])
        returnvolt = retval * self.info['adc_mult']
        self.result['return'].append(returnvolt)

        self.result['diff'].append(self.result['expect'][value] - self.result['return'][value])
        return self.result

    def _write_value(self, command, channel, value):
#        path = find_iio_device_files(command, self.board.data['iio_device']['name'])
        stdout, stderr, returncode = command.run("echo "+str(value)+ " > "+self.info['dac_path']+"/"
                                                "out_voltage"+str(channel)+"_raw")
        if returncode != 0:
            print("jeejee")

        return stdout, stderr, returncode

    def _read_value(self, command, channel, value):
        stdout, stderr, returncode = command.run("cat "+self.info['adc_path']+"/"
                                                "in_voltage"+str(channel)+"_raw")

        return stdout
