from dataclasses import dataclass
import pytest
from time import sleep
import sys
import os
import copy

sys.path.append(os.path.abspath("."))
pmic_data={}

@dataclass
class pmic:
    board: dict

    def print_failures(self,failures):
        print("Regulator, Range, Index, Sent uV, Received uV")
        for i in range(len(failures[0])):
            print(failures[0][i])

    def escape_path(self, path_str):
        path = path_str.translate(str.maketrans({'@':'\\@'}))
        return path

    def mv_to_uv(self, mV):
        uV = mV * 1000
        return uV

    def read_dt(self,regulator,command,setting):
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("xxd -p "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/"+self.board.data['regulators'][regulator][setting]['of_match'])
        hex=('0x'+stdout[0])
        print(int(hex,0))
        int_hex= int(hex,0)
        return int_hex

    def dt_run(self, regulator, dts, command):
        for property in self.board.data['regulators'][regulator]['dt_properties'][dts]:
            dts_value = self.read_dt(regulator,property,command)
            
    def validate_config(self, target_name):
        assert target_name == self.board.data['name']
        assert type(self.board.data['i2c']['bus']) == int
        assert type(self.board.data['i2c']['address']) == int
        for regulator in self.board.data['regulators']:
            if ('volt_sel' in self.board.data['regulators'][regulator] and self.board.data['regulators'][regulator]['volt_sel'] == True):
                assert type(self.board.data['regulators'][regulator]['volt_sel_bitmask']) == int
            for r in self.board.data['regulators'][regulator]['range'].keys():
                if 'is_linear' in self.board.data['regulators'][regulator]['range'][r].keys() and self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
                    assert type(self.board.data['regulators'][regulator]['range'][r]['step_mV']) == int
                elif 'is_linear' in self.board.data['regulators'][regulator]['range'][r].keys() and self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
                    assert type(self.board.data['regulators'][regulator]['range'][r]['list_mV']) == list
                if 'is_bipolar' in self.board.data['regulators'][regulator].keys():
                    assert type(self.board.data['regulators'][regulator]['sign_bitmask']) == int

    def validate_config_basic(self):
        pass
        validation_fail = 0
        if (not 'name' in self.board.data.keys() and not 'i2c' in self.board.data.keys() and not 'regulators' in self.board.data.keys()):
            validation_fail = 1
        return validation_fail

    def sanity_check(self,regulator,command):
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("test -f "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/name ;echo $?")
        if stdout[0] == '0': #test -d returns 0 if file is found
            return 1
        elif stdout[0] == '1':
            return 0

    def disable_vr_fault(self,key,command):
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['debug'][key]['address'])))
        i2creturn = int(stdout[0],0)

        # new_val =hex string from bitwise operation: (debug bitmask & debug setting) | (~debug bitmask & read i2c value). This code retains bits in the register that we do not want to touch.
        new_val = str(hex((self.board.data['debug'][key]['bitmask'] & self.board.data['debug'][key]['setting']) | (~self.board.data['debug'][key]['bitmask'] & i2creturn)))
        stdout, stderr, returncode = command.run("i2cset -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['debug'][key]['address']))+" "+new_val)
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['debug'][key]['address'])))
        i2creturn = int(stdout[0],0)
        vr_fault_status = i2creturn & self.board.data['debug'][key]['bitmask']
        return vr_fault_status

    def check_regulator_enable_mode(self, regulator, command):
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("test -f "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/rohm,no-regulator-enable-control ;echo $?")
        return int(stdout[0])   #test -f returns 1 if regulator can be enabled

    def check_regulator_always_on_mode(self, regulator, command): 
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'")
        path = self.escape_path(stdout[0])

        stdout, stderr, returncode = command.run("test -f "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/regulator-always-on ;echo $?")
        if stdout[0] == '0': #test -f returns 0 if file is found
            return 1
        if stdout[0] == '1':
            return 0

    def check_bd9576_vout1_en_low(self,command):
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'")
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("test -f "+path+"rohm,vout1-en-low ;echo $?")
        if stdout[0] == '0':
            return 1
        if stdout[0] == '1':
            return 0

    def regulator_is_on_driver(self, regulator, command):
        stdout, stderr, returncode = command.run("cat /sys/kernel/mva_test/regulators/"+regulator+"_en")
        if stdout[0] == '0\x00':
            return 0
        elif stdout[0] == '1\x00':
            return 1

    def regulator_is_on(self, regulator, command):
        regulator_enable_mode = self.check_regulator_enable_mode(regulator,command)

        if (self.board.data['name'] == 'bd71837' or self.board.data['name'] == 'bd71847') and (regulator_enable_mode == 0):
            regulator_en_status = 1

        elif (self.board.data['name'] == 'bd9576'):
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
            i2creturn = int(stdout[0],0)
            if i2creturn != self.board.data['regulators'][regulator]['regulator_en_bitmask']:
                regulator_en_status = 1
            else:
                regulator_en_status = 0

        else:
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
            i2creturn = int(stdout[0],0)
            regulator_en_status = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']

        return regulator_en_status

    def regulator_enable(self,regulator,command):
        command.run("echo 1 > /sys/kernel/mva_test/regulators/"+regulator+"_en")
        sleep(0.2)
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
        i2creturn = int(stdout[0],0)
        regulator_en_status = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
        return regulator_en_status

    def regulator_disable(self,regulator,command):
        command.run("echo 0 > /sys/kernel/mva_test/regulators/"+regulator+"_en")
        sleep(0.2)
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
        i2creturn = int(stdout[0],0)
        regulator_en_status = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
        return regulator_en_status

    def regulator_voltage_driver_get(self, regulator, command):
        stdout, stderr, returncode = command.run("cat /sys/kernel/mva_test/regulators/"+regulator+"_set")
        print(stdout)
        print(stdout[0])
        return int(stdout[0],0)

    def calculated_uv(self, regulator,command,r, volt_index=None):
        if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['range'][r]['step_mV'] * volt_index)

        elif self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]

        uv = self.mv_to_uv(mv)
        return uv
    def regulator_limit_get(self, regulator,setting, command, r='values'):
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator][setting]['reg_address'])))
            i2creturn = int(stdout[0],0)
            unmasked_return = i2creturn & self.board.data['regulators'][regulator][setting]['reg_bitmask']
            
            volt_index = (i2creturn & self.board.data['regulators'][regulator][setting]['reg_bitmask']) - self.board.data['regulators'][regulator][setting][r]['start_reg']

            calculated_return_value = self.calculate_return_value(regulator, command,r, volt_index,i2creturn,setting)
            calculated_return_value = self.mv_to_uv(calculated_return_value)
            return calculated_return_value

    def regulator_voltage_get(self, regulator, command, r='not_given', volt_index=None):
        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]:
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['volt_reg_address'])))
            i2creturn = int(stdout[0],0)
            unmasked_return = i2creturn & self.board.data['regulators'][regulator]['volt_reg_bitmask']
        elif(not 'volt_reg_bitmask' in self.board.data['regulators'][regulator] and 'regulator_en_address' in self.board.data['regulators'][regulator]):
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
            i2creturn = int(stdout[0],0)
 
        if (self.board.data['regulators'][regulator]['volt_sel'] == False and r == 'not_given'):
            for found_r in self.board.data['regulators'][regulator]['range'].keys():
                if unmasked_return in range(self.board.data['regulators'][regulator]['range'][found_r]['start_reg'], self.board.data['regulators'][regulator]['range'][found_r]['stop_reg']+1):
                    r=found_r
                else:
                    r='range_error'
        
        if self.board.data['regulators'][regulator]['volt_sel'] == True:
            r = i2creturn & self.board.data['regulators'][regulator]['volt_sel_bitmask']

        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]:
            volt_index = (i2creturn & self.board.data['regulators'][regulator]['volt_reg_bitmask']) - self.board.data['regulators'][regulator]['range'][r]['start_reg']
        
        calculated_return_value = self.calculate_return_value(regulator, command, r, volt_index,i2creturn)
        return calculated_return_value
    
    def calculate_return_value(self, regulator,command, r, volt_index,i2creturn, setting='range'):
        operation = 'add'

        if 'is_offset_bipolar' in self.board.data['regulators'][regulator][setting][r]:
            unmasked_offset_sign = i2creturn & self.board.data['regulators'][regulator][setting][r]['offset_sign_bitmask']
            if unmasked_offset_sign == 1:
                operation = 'substract'

        if self.board.data['regulators'][regulator][setting][r]['is_linear'] == True:
            if operation == 'add':
                calculated_return_value = self.board.data['regulators'][regulator][setting][r]['start_mV']+(volt_index * self.board.data['regulators'][regulator][setting][r]['step_mV'])
            elif operation == 'substract':
                calculated_return_value = self.board.data['regulators'][regulator][setting][r]['start_mV']-(volt_index * self.board.data['regulators'][regulator][setting][r]['step_mV'])

        elif (self.board.data['regulators'][regulator][setting][r]['is_linear'] == False and not 'is_offset_bipolar' in self.board.data['regulators'][regulator][setting][r]):
            if operation == 'add':
                calculated_return_value = self.board.data['regulators'][regulator][setting][r]['list_mV'][volt_index]
            elif operation == 'substract':
                calculated_return_value = self.board.data['regulators'][regulator][setting][r]['list_mV'][volt_index]
        else:
            print("Regulator voltage calculation is not implemented yet!")

        return calculated_return_value
        
    def get_min_max_volt(self, regulator):
        last_min = 'default'
        last_max = 'default'
        for r in self.board.data['regulators'][regulator]['range'].keys():
            if (self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['range'][r]):
                min = self.board.data['regulators'][regulator]['range'][r]['start_mV']
                max = self.board.data['regulators'][regulator]['range'][r]['start_mV']+(self.board.data['regulators'][regulator]['range'][r]['stop_reg'] * self.board.data['regulators'][regulator]['range'][r]['step_mV'])
            
            elif (self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['range'][r]):
                min = self.board.data['regulators'][regulator]['range'][r]['list_mV'][0]
                max = self.board.data['regulators'][regulator]['range'][r]['list_mV'][-1]

            elif (self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['range'][r]):
                min = self.board.data['regulators'][regulator]['range'][r]['list_mV'][0]
                max = self.board.data['regulators'][regulator]['range'][r]['list_mV'][-1]
        
            elif (self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True and self.board.data['regulators'][regulator]['range'][r]['is_offset_bipolar'] == True):
                min = self.board.data['regulators'][regulator]['range'][r]['start_mV']-(self.board.data['regulators'][regulator]['range'][r]['stop_reg'] * self.board.data['regulators'][regulator]['range'][r]['step_mV'])
                max = self.board.data['regulators'][regulator]['range'][r]['start_mV']+(self.board.data['regulators'][regulator]['range'][r]['stop_reg'] * self.board.data['regulators'][regulator]['range'][r]['step_mV'])
        
            elif (self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False and self.board.data['regulators'][regulator]['range'][r]['is_offset_bipolar'] == True):
                min = self.board.data['regulators'][regulator]['range'][r]['start_mV']-(self.board.data['regulators'][regulator]['range'][r]['list_mV'][-1])
                max = self.board.data['regulators'][regulator]['range'][r]['start_mV']+(self.board.data['regulators'][regulator]['range'][r]['list_mV'][-1])
            
            if (last_min == 'default' or min < last_min):
                last_min = copy.copy(min)
            if (last_max == 'default' or max > last_max):
                last_max = copy.copy(max)
        
        last_min = self.mv_to_uv(min)
        last_max = self.mv_to_uv(max)

        return last_min, last_max

    def regulator_voltage_driver_set(self,regulator,uv,command):
        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")

    def regulator_voltage_set(self, regulator,r, command, volt_index=None):
        ######## SETS VOLTAGE THROUGH TEST KERNEL MODULE ######
        if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['range'][r]['step_mV'] * volt_index)

        elif self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]

        uv = int(self.mv_to_uv(mv))
        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")
        print("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")

        return uv

    def regulator_voltage_run(self,regulator,command):
        voltage_run={
            'test_failed': 0,
            'buck_fail':[]
            }

        for r in self.board.data['regulators'][regulator]['range'].keys():
            for x in range(self.board.data['regulators'][regulator]['range'][r]['start_reg'], self.board.data['regulators'][regulator]['range'][r]['stop_reg']+1):
                volt_index = x - self.board.data['regulators'][regulator]['range'][r]['start_reg']
                uv = self.regulator_voltage_set(regulator, r, command, volt_index)
                calculated_return_value = self.i2c_to_uv(regulator, command)

                if uv != calculated_return_value:
                    voltage_run['test_failed']=1
                    voltage_run['buck_fail'].append([regulator,r,volt_index,uv, calculated_return_value])
                    print(uv)
                    print(calculated_return_value)

        return voltage_run
    
    def i2c_to_uv(self, regulator, command):
        volt_config = self._i2c_to_volt_config(regulator,command)

        if volt_config['is_linear'] == True:
            mv = self._calculate_linear_mv(volt_config)
        else:
            mv = self._calculate_nonlinear_mv(volt_config)
        uv = self.mv_to_uv(mv)
        return uv

    def i2c_to_lim_uv(self, regulator, command):
        volt_config = self._i2c_to_lim_config(regulator,command)

    def _i2c_to_lim_config(self):
        pass
        volt_config={
                'r':            None,
                'volt_index':   None,
                'is_linear':    None,
                'operation':    'add',
                'start_mV':     None,
                'step_mV':      None,
                'list_mV':      None,
                }

    def _i2c_to_volt_config(self, regulator, command,setting ='range'):
        volt_config={
                'volt_index':   None,
                'is_linear':    None,
                'operation':    'add',
                'start_mV':     None,
                'step_mV':      None,
                'list_mV':      None,
                }
        #   Get unmasked voltage register value
        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]:
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['volt_reg_address'])))
            i2creturn = int(stdout[0],0)
            volt_config['volt_index'] = i2creturn & self.board.data['regulators'][regulator]['volt_reg_bitmask']
        elif(not 'volt_reg_bitmask' in self.board.data['regulators'][regulator] and 'regulator_en_address' in self.board.data['regulators'][regulator]):
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
            i2creturn = int(stdout[0],0)

        #   Get range
        if self.board.data['regulators'][regulator]['volt_sel'] == True:
            r = i2creturn & self.board.data['regulators'][regulator]['volt_sel_bitmask']

        if (self.board.data['regulators'][regulator]['volt_sel'] == False):
            for key in self.board.data['regulators'][regulator]['range'].keys():
                if volt_config['volt_index'] in range(self.board.data['regulators'][regulator]['range'][key]['start_reg'], self.board.data['regulators'][regulator]['range'][key]['stop_reg']+1):
                    r=key

        #   Turn voltage register value to index value of current range
        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]:
            volt_config['volt_index'] = (i2creturn & self.board.data['regulators'][regulator]['volt_reg_bitmask']) - self.board.data['regulators'][regulator]['range'][r]['start_reg']

        #   Get offset sign if present
        if 'is_offset_bipolar' in self.board.data['regulators'][regulator][setting][r]:
            unmasked_offset_sign = i2creturn & self.board.data['regulators'][regulator][setting][r]['offset_sign_bitmask']
            if unmasked_offset_sign == 1:
                volt_config['operation'] = 'substract'

        #   Gather linear / non-linear info of current range
        volt_config['is_linear'] = self.board.data['regulators'][regulator]['range'][r]['is_linear']
        if self.board.data['regulators'][regulator][setting][r]['is_linear'] == True:
            volt_config['start_mV'] = self.board.data['regulators'][regulator]['range'][r]['start_mV']
            volt_config['step_mV'] = self.board.data['regulators'][regulator]['range'][r]['step_mV']
        elif self.board.data['regulators'][regulator][setting][r]['is_linear'] == False:
            volt_config['list_mV'] = self.board.data['regulators'][regulator]['range'][r]['list_mV']

        return volt_config

    def _calculate_linear_mv(self, volt_config):
        if volt_config['operation'] == 'add':
            mv = volt_config['start_mV']+(volt_config['volt_index'] * volt_config['step_mV'])
        elif volt_config['operation'] == 'substract':
            mv = volt_config['start_mV']-(volt_config['volt_index'] * volt_config['step_mV'])

        return mv

    def _calculate_nonlinear_mv(self, volt_config):
        if volt_config['operation'] == 'add':
            mv = volt_config['list_mV'][volt_config['volt_index']]
        elif volt_config['operation'] == 'substract':
            mv = volt_config['list_mV'][volt_config['volt_index']]
        else:
            print("Regulator voltage calculation is not implemented yet!")

        return mv
