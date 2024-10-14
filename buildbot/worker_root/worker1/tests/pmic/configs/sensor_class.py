from dataclasses import dataclass, field
import pytest
from time import sleep
import sys
import os
import copy
import math
import numbers

from test_class_helpers import bitshift_index_by_bitmask, escape_path, pc_to_int, frequency_to_ns, combine_bytes, twos_complement
sys.path.append(os.path.abspath("."))

@dataclass
class sensor:
    board: dict

    g_force: int = 9.80665      #Standard gravitational acceleration, Used to calculate m/s²
    halved_16bit: int = 32768   #This is halved 16 bit used to calculate the multiplier to get a G out of register value
                                # G with scale +-2G => register_value *( 2/32768 ) = G, G * g_force = ms/²

    result: dict = field(default_factory=lambda: {
    'type':         'Sensor',
    'stage':        None,
    'product':      None,
    'return':       [],
    'expect':       [],
    })

    def find_iio_device_files(self, command):
        stdout, stderr, returncode = command.run("grep -RIn "+self.board.data['iio_device']['name']+" /sys/bus/iio/devices/*/name | sed 's![^/]*$!!'")
        x = 0
        for line in stdout:
            if "iio:" in line:
                correct_path_line = x
            x = x+1

        path = stdout[correct_path_line]
        path = escape_path(path)

        return path

                                                            ### tolerance  = +/- #%
    def test_sampling_frequency_match_timestamp(self, command, frequency, count=2, tolerance=2):
        self.result['return'] =[]
        self.result['return_diff'] = []
        self.result['stage'] = 'test_sampling_frequency_match_timestamp'
        self.result['sampling_frequency'] = frequency
        self.result['expect'] = 'range'
        self.result['tolerance'] = tolerance

        frequency_ns = frequency_to_ns(frequency)
        self.result['expect_perfect'] = frequency_ns

        high_limit =(frequency_ns * pc_to_int(tolerance)) + frequency_ns
        self.result['expect_high']= high_limit

        low_limit = ((frequency_ns * pc_to_int(tolerance)) * -1) + frequency_ns
        self.result['expect_low'] = low_limit

        self.set_sampling_frequency_driver(frequency, command)

        timestamps = self.read_timestamps(command, count = count)

        self.result['return']
        timestamp_intervals = []

        for x in range(1,(len(timestamps))):
            ts_interval = (int(timestamps[x]) - int(timestamps[x-1]))
            self.result['return'].append(ts_interval)
            self.result['return_diff'].append(ts_interval - frequency_ns)
            interval_count = x

        return self.result

    def set_watermark(self, command, watermark):
        path = self.find_iio_device_files(command)
        stoud, stderr, returncode = command.run("echo "+str(watermark)+" > "+path+"/buffer0/watermark")

    def set_sampling_frequency_driver(self, frequency, command):
        frequency = str(frequency)
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo "+frequency+" > "+path+"/in_accel_sampling_frequency")

    def enable_all_accel_channels(self, command):
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_x_en")
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_y_en")
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_z_en")
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_timestamp_en")

    def enable_single_xyz_channel(self, command, xyz):
        path = self.find_iio_device_files(command)
        self.disable_all_channels(command)
        stdout, stderr, returncode = command.run("echo 1 > "+path+"/scan_elements/in_accel_"+xyz+"_en")


    def disable_all_channels(self, command):
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo 0 > "+path+"/scan_elements/in_accel_x_en")
        stdout, stderr, returncode = command.run("echo 0 > "+path+"/scan_elements/in_accel_y_en")
        stdout, stderr, returncode = command.run("echo 0 > "+path+"/scan_elements/in_accel_z_en")
        stdout, stderr, returncode = command.run("echo 0 > "+path+"/scan_elements/in_timestamp_en")

    def read_timestamps(self, command, count=1):
        self.enable_all_accel_channels(command)
        count_str = str(count)
        stdout = self.read_enabled_channels(command, count=count_str)
        timestamps = self.extract_timestamp_iio_generic_buffer(stdout)

        return timestamps

    def extract_timestamp_iio_generic_buffer(self, stdout):
        split_lines = []
        timestamps = []
        for x in range(0, len(stdout)):
            split_lines.append(stdout[x].split())
        for x in range(0, len(split_lines)):
            timestamps.append(split_lines[x][-1])

        return timestamps

    def read_enabled_channels(self, command, count=1):
        count = str(count)
        stdout, stderr, returncode = command.run("/./iio_generic_buffer -c "+count+" -g -n "+self.board.data['iio_device']['name'])
        return stdout

    def test_gsel(self, scale, command):
        self.result['stage'] = 'test_gsel'
        self.result['expect'] = scale
        self.result['product'] = self.board.data['name']

        self.write_in_accel_scale(scale, command)
        gsel_index = self._i2c_to_gsel_index(command)
        self.result['return'] = self.board.data['settings']['gsel']['list_values'][gsel_index]

        return self.result

    def write_in_accel_scale(self, scale, command):
        scale = str(scale)
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("echo "+scale+" > "+path+"in_accel_scale")

        return returncode

    def _i2c_to_gsel_index(self, command):
        stdout, stderr, returncode = command.run("i2cget -f -y "+str(self.board.data['i2c']['bus'])+" "+str(self.board.data['i2c']['address'])+" "+str(self.board.data['settings']['gsel']['reg_address']))

        i2creturn = int(stdout[0],0)
        unmasked_return = i2creturn & self.board.data['settings']['gsel']['reg_bitmask']
        index = bitshift_index_by_bitmask(self.board.data['settings']['gsel']['reg_bitmask'], unmasked_return)

        return index

    def driver_read_raw_xyz(self, command, xyz):
        path = self.find_iio_device_files(command)
        stdout, stderr, returncode = command.run("cat "+path+"in_accel_"+xyz+"_raw")

        return stdout[0]

    def reg_read_raw_xyz(self, command, xyz):
        if self.board.data['settings']['axis']['bits'] == 16:
            return self._reg_read_xyz_16bit(command, xyz)

    def _reg_read_xyz_16bit(self, command, xyz):
        stdout, stderr, returncode = command.run("i2cget -f -y "+str(self.board.data['i2c']['bus'])+" "+str(self.board.data['i2c']['address'])+" "+str(self.board.data['settings']['axis']['regs'][xyz]['low_reg'])+" w")
        word = int(stdout[0], 0)
        raw_xyz = twos_complement(word, 16)

        return raw_xyz

    def driver_read_ms2_xyz(self, command, xyz):
        self.set_watermark(command, 1)
        self.enable_single_xyz_channel(command, xyz)
        xyz_value = self.read_enabled_channels(command)

        return xyz_value
