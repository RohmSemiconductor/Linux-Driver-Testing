from dataclasses import dataclass, field
import pytest
from time import sleep
import sys
import os
import copy
import math
import numbers
sys.path.append(os.path.abspath("."))
pmic_data={}

@dataclass
class pmic:
    board: dict
    result: dict = field(default_factory=lambda: {
    'type':         'PMIC',
    'result_dir':   'PMIC',
    'stage':        None,
    'product':      None,
    'regulator':    None,
    'return':       [],
    'expect':       [],
    })

    def escape_path(self, path_str):
        path = path_str.translate(str.maketrans({'@':'\\@'}))
        return path

    def mv_to_uv(self, mV):
        uV = mV * 1000
        return uV

    #### Device tree functions

    #Unused
    def i2c_read_dt_property(self,command, test_dts, regulator, property):
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.dts['i2c']['bus'])+" "+str(hex(self.board.dts['i2c']['address']))+" "+str(hex(self.board.dts['regulators'][regulator]['test'][test_dts][property]['reg_address'])))
        i2creturn = int(stdout[0],0)
        ret_register_value = i2creturn & self.board.dts['regulators'][regulator]['test'][test_dts][property]['bitmask']
        return ret_register_value
    #Unused
    def test_property(self, command, test_dts, regulator, property):
        i2c_return = self.i2c_read_dt_property(command, test_dts, regulator, property)
        print(i2c_return)
        print(self.board.dts['regulators'][regulator]['test'][test_dts][property]['register_value'])
        assert i2c_return == self.board.dts['regulators'][regulator]['test'][test_dts][property]['register_value']
    #Unused
    def test_dts_properties(self, command, test_dts, property):
        for regulator in self.board.dts['regulators'].keys():
            if 'test' in self.board.dts['regulators'][regulator]:
                if test_dts in self.board.dts['regulators'][regulator]['test'].keys():
                    if property in self.board.dts['regulators'][regulator]['test'][test_dts].keys():
                        self.test_property(command, test_dts, regulator, property)


    def generate_dts(self, test_dts, source_file, target_file):
        in_dts = open(source_file)
        out_dts = open(target_file, 'w+', encoding="utf-8")
        regulator = 0
        for line in in_dts:
            #get regulator name from device tree property
            if "regulator-name =" in line:
                regulator_list = line.split('"',2)
                regulator = regulator_list[1]
                properties_found = []

            if  regulator != 0:
                prop_found=False
                x=0
                if 'dts' in self.board.data['regulators'][regulator].keys():
                    if test_dts in self.board.data['regulators'][regulator]['dts']:
                        for property in self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties']:
                            x=x+1
                            #if property in line or "//"+property in line:
                            if property in line:
                                self._print_property_to_dts(regulator, test_dts, property, out_dts)
                                prop_found=True
                                properties_found.append(property)
                            # if property was not found, copy line from template
                            if '};' in line and len(self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties'])-len(properties_found) != 0:
                                for property in self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties']:
                                    if property not in properties_found:
                                        properties_found.append(property)
                                        self._print_property_to_dts(regulator, test_dts, property, out_dts)

                            if x == len(self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties']) and prop_found==False:
                                print(line, end ='', file = out_dts)
                    else:
                        print(line, end ='', file = out_dts)
                else:
                    print(line, end ='', file = out_dts)
            else:
                print(line, end ='', file = out_dts)

        in_dts.close()
        out_dts.close()

    def _print_property_to_dts(self, regulator, test_dts, property, out_dts):
        if type(self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties'][property]) == int:
            print(property+" = <"+str(self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties'][property])+">;\n", end ='', file = out_dts)
        elif type(self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties'][property]) == bool:
            print(property+";\n", end='', file = out_dts)
        elif type(self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties'][property]) == str:
            print(property+" = <"+self.board.data['regulators'][regulator]['dts'][test_dts]['dts_properties'][property]+">;\n", end ='', file = out_dts)


    def read_dt_setting(self, regulator, setting, dts, command):
        self.result['stage'] = 'read_dt_setting'
        self.result['regulator'] = regulator

        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("xxd -p "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/"+self.board.data['regulators'][regulator]['settings'][setting]['of_match'])
        hex=('0x'+stdout[0])
        int_hex= int(hex,0)
        self.result['expect'] = [dts, setting, int_hex]
        return self.result

    #### /Device tree functions

    def find_sysfs_files(self, regulator, command):
        stdout, stderr, returncode = command.run('find /sys -name "'+self.board.data['regulators'][regulator]['name']+'_en"|'+" sed 's![^/]*$!!'")
        path = stdout[0]
        return path

    def validate_config(self, product_name):
        self.result['stage'] = 'validate_config'
        self.result['product_name'] = product_name
        self.result['expect_product_name'] = self.board.data['name']
        self.result['i2c_bus_type'] = type(self.board.data['i2c']['bus'])
        self.result['i2c_address_type'] = type(self.board.data['i2c']['address'])

        for regulator in self.board.data['regulators']:
            if 'dts_only' not in self.board.data['regulators'][regulator].keys() and 'no_voltage_register' not in self.board.data['regulators'][regulator].keys():
                if ('volt_sel' in self.board.data['regulators'][regulator]['settings']['voltage'] and self.board.data['regulators'][regulator]['settings']['voltage']['volt_sel'] == True):
                    self.result['return'].append(['volt_sel_bitmask', regulator, type(self.board.data['regulators'][regulator]['settings']['voltage']['volt_sel_bitmask'])])
                    self.result['expect'].append(['volt_sel_bitmask', regulator, int])

                for r in self.board.data['regulators'][regulator]['settings']['voltage']['range'].keys():
                    if 'is_linear' in self.board.data['regulators'][regulator]['settings']['voltage']['range'][r].keys() and self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == True:
                        self.result['return'].append(['step_mV', regulator, r, isinstance(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV'], numbers.Number)])
                        self.result['expect'].append(['step_mV', regulator, r, True])
                    elif 'is_linear' in self.board.data['regulators'][regulator]['settings']['voltage']['range'][r].keys() and self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == False:
                        self.result['return'].append(['list_mV', regulator, type(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'])])
                        self.result['expect'].append(['list_mV', regulator, list])
                    if 'is_bipolar' in self.board.data['regulators'][regulator]['settings']['voltage'].keys():
                        self.result['return'].append(['sign_bitmask', regulator, type(self.board.data['regulators'][regulator]['settings']['voltage']['sign_bitmask'])])
                        self.result['expect'].append(['sign_bitmask', regulator, list])

        return self.result

    def validate_config_basic(self):
        pass
        validation_fail = 0
        if (not 'name' in self.board.data.keys() and not 'i2c' in self.board.data.keys() and not 'regulators' in self.board.data.keys()):
            validation_fail = 1
        return validation_fail

    def sanity_check_sysfs_en(self, regulator, command):
        self.result['stage'] = 'sanity_check_sysfs_en'
        self.result['regulator'] = regulator
#        stdout, stderr, returncode = command.run("test -f /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"/name ;echo $?")
        if 'regulator_en_address' in self.board.data['regulators'][regulator].keys():
            stdout, stderr, returncode = command.run("test -f /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_en ;echo $?")
        print("sanity:")
        print(self.board.data['regulators'][regulator]['name'])

        self.result['return'] = stdout[0]
        self.result['expect'] = '0' #test -f returns 0 if file is found
        return self.result

    def sanity_check_sysfs_set(self, regulator, command):
        self.result['stage'] = 'sanity_check_sysfs_set'
        self.result['regulator'] = regulator
#        stdout, stderr, returncode = command.run("test -f /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"/name ;echo $?")
        if 'regulator_en_address' in self.board.data['regulators'][regulator].keys():
            stdout, stderr, returncode = command.run("test -f /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set ;echo $?")

        self.result['return'] = stdout[0]
        self.result['expect'] = '0' #test -f returns 0 if file is found
        return self.result

    def sanity_check(self,regulator,command):
        self.result['stage'] = 'sanity_check'
        self.result['regulator'] = regulator
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("test -f "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/name ;echo $?")

        self.result['return'] = stdout[0]
        self.result['expect'] = '0' #test -f returns 0 if file is found
        return self.result

    def disable_vr_fault(self,key,command):
        self.result['stage'] = 'disable_vr_fault'
        self.result['expect'] = self.board.data['debug'][key]['setting']
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['debug'][key]['address'])))
#        i2creturn = self._i2creturn(stdout[0])
       # if type(i2creturn) != int:
       #     return self.result
        try:
            i2creturn = int(stdout[0],0)
            # new_val =hex string from bitwise operation: (debug bitmask & debug setting) | (~debug bitmask & read i2c value). This code retains bits in the register that we do not want to touch.
            new_val = str(hex((self.board.data['debug'][key]['bitmask'] & self.board.data['debug'][key]['setting']) | (~self.board.data['debug'][key]['bitmask'] & i2creturn)))
            stdout, stderr, returncode = command.run("i2cset -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['debug'][key]['address']))+" "+new_val)
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['debug'][key]['address'])))
            i2creturn = int(stdout[0],0)

            self.result['return'] = i2creturn & self.board.data['debug'][key]['bitmask']
        except Exception:
            self.result['return'] = stdout[0]
        finally:
            return self.result

    def disable_idle_mode(self, regulator, command):
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings']['idle_on']['reg_address'])))
        i2creturn = int(stdout[0],0)

        new_val = str(hex((0 & self.board.data['regulators'][regulator]['settings']['idle_on']['reg_bitmask']) | (~self.board.data['regulators'][regulator]['settings']['idle_on']['reg_bitmask'] & i2creturn)))
        stdout, stderr, returncode = command.run("i2cset -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings']['idle_on']['reg_address']))+" "+new_val)
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings']['idle_on']['reg_address'])))
        i2creturn = int(stdout[0],0)
        idle_mode_status = i2creturn & self.board.data['regulators'][regulator]['settings']['idle_on']['reg_bitmask']
        print(idle_mode_status)
        return idle_mode_status

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
        self.result['regulator'] = regulator
        self.result['stage'] = 'regulator_is_on_driver'
        stdout, stderr, returncode = command.run("cat /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_en")
        if stdout[0] == '0\x00':
            self.result['return'] = 0
        elif stdout[0] == '1\x00':
            self.result['return'] = 1
        return self.result

    def regulator_is_on(self, regulator, command):
        self.result['regulator'] = regulator
        self.result['stage'] = 'regulator_is_on'
        self.result['expect'] = int

        regulator_enable_mode = self.check_regulator_enable_mode(regulator,command)
        try:
            if (self.board.data['name'] == 'bd71837' or self.board.data['name'] == 'bd71847') and (regulator_enable_mode == 0):
                self.result['return'] = 1

            elif (self.board.data['name'] == 'bd9576'):
                stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
                i2creturn = int(stdout[0],0)
                if i2creturn != self.board.data['regulators'][regulator]['regulator_en_bitmask']:
                    self.result['return'] = 1
                else:
                    self.result['return'] = 0

            elif (self.board.data['name'] == 'bd96801'):
                stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
                i2creturn = int(stdout[0],0)
                if (i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']) == self.board.data['regulators'][regulator]['regulator_en_bitmask']:
                    self.result['return'] = 0
                else:
                    self.result['return'] = 1

            else:
                stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
                i2creturn = int(stdout[0],0)
                self.result['return'] = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
        except Exception:
            self.result['return'] = stdout[0]
        finally:
            return self.result

    def regulator_enable(self,regulator,command):
        self.result['stage'] = 'regulator_enable'
        self.result['regulator'] = regulator
        self.result['expect'] = self.board.data['regulators'][regulator]['regulator_en_bitmask']

        command.run("echo 1 > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_en")
        sleep(0.2)
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
        try:
            i2creturn = int(stdout[0],0)
            regulator_en_status = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
            self.result['return'] = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
        except Exception:
            self.result['return'] = stdout[0]
        finally:
            return self.result

    def regulator_disable(self,regulator,command):
        self.result['stage'] = 'regulator_disable'
        self.result['regulator'] = regulator
        self.result['expect'] = 0

        command.run("echo 0 > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_en")
        sleep(0.2)

       #### bd71828 needs a bit more time to set the values to register, read fails without this
        if self.board.data['name'] == 'bd71828':
            sleep(2)

        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
        try:
            i2creturn = int(stdout[0],0)
            self.result['return'] = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
        except Exception:
            self.result['return'] = stdout[0]
        finally:
            return self.result

    def regulator_voltage_driver_get(self, regulator, command):
        self.result['stage'] = 'regulator_voltage_driver_get'
        self.result['regulator'] = regulator
        self.result['product'] = self.board.data['name']
        stdout, stderr, returncode = command.run("cat /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set")
        print(stdout)
        print(stdout[0])
        self.result['return'] = int(stdout[0],0)
        return self.result

    def calculated_uv(self, regulator,command,r, volt_index=None):
        if self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV'] * volt_index)

        elif self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][volt_index]

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

    def calculate_return_value(self, regulator,command, r, volt_index,i2creturn, setting='range'):
        operation = 'add'

        if 'is_offset_bipolar' in self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]:
            unmasked_offset_sign = i2creturn & self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]['offset_sign_bitmask']
            if unmasked_offset_sign == 1:
                operation = 'substract'

        if self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]['is_linear'] == True:
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
        self.result['regulator'] = regulator
        self.result['stage'] = 'out_of_range_voltages'

        last_min = 'default'
        last_max = 'default'
        for r in self.board.data['regulators'][regulator]['settings']['voltage']['range'].keys():
            if (self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == True and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]):
                min = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']
                max = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']+(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['stop_reg'] * self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV'])

            elif (self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == False and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]):
                min = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][0]
                max = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][-1]

            elif (self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == False and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]):
                min = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][0]
                max = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][-1]

            elif (self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == True and self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_offset_bipolar'] == True):
                min = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']-(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['stop_reg'] * self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV'])
                max = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']+(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['stop_reg'] * self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV'])

            elif (self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == False and self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_offset_bipolar'] == True):
                min = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']-(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][-1])
                max = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']+(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][-1])

            if (last_min == 'default' or min < last_min):
                last_min = copy.copy(min)
            if (last_max == 'default' or max > last_max):
                last_max = copy.copy(max)

        last_min = self.mv_to_uv(last_min)
        last_max = self.mv_to_uv(last_max)

        return self.result, last_min, last_max

    def regulator_voltage_driver_set(self,regulator,uv,command):
        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set")

    def regulator_voltage_set(self, regulator,r, command, volt_index=None):
        ######## SETS VOLTAGE THROUGH TEST KERNEL MODULE ######
        if self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV'] * volt_index)

        elif self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV'][volt_index]

        uv = int(self.mv_to_uv(mv))
        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set")
        print("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set")

        return uv

    def regulator_voltage_run(self,regulator,command):
        self.result['stage'] = 'voltage_run'
        self.result['regulator'] = regulator
        self.result['return'] = []
        self.result['expect'] = []

        for r in self.board.data['regulators'][regulator]['settings']['voltage']['range'].keys():
            if r != 'flat':
                for x in range(self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_reg'], self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['stop_reg']+1):
                    volt_index = x - self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_reg']

                    uv = self.regulator_voltage_set(regulator, r, command, volt_index)
                    calculated_return_value = self.i2c_to_uv(regulator, command)

                    self.result['return'].append([r, x, calculated_return_value])
                    self.result['expect'].append([r, x, uv])

        return self.result

    def regulator_tune_set(self, regulator, r, tune_index, command):
        initial_voltage = self.i2c_to_uv(regulator, command)
        if self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['is_linear'] == True:
            tune_mv = self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['start_mV'] + (self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['step_mV'] * tune_index)
        elif self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['is_linear'] == False:
            tune_mv = self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['list_mV'][volt_index]

        tune_uv=self.mv_to_uv(tune_mv)
        uv = initial_voltage + tune_uv

        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set")
        print("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+self.board.data['regulators'][regulator]['name']+"_set")

        return uv

    def regulator_tune_register_run(self, regulator, command):
        self.result['stage'] = 'tune_register_run'
        self.result['regulator'] = regulator
        self.result['return'] = []
        self.result['expect'] = []

        for r in self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'].keys():
            if r != 'flat':
                for x in range(self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['start_reg'], self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['stop_reg']+1):
                    tune_index = x - self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['start_reg']

                    uv = self.regulator_tune_set(regulator, r, tune_index, command)

                    tune_uv = self.i2c_to_tune_uv(regulator, command)
                    regulator_uv = self.i2c_to_uv(regulator, command)
                    calculated_return_value = regulator_uv + tune_uv

                    self.result['return'].append([r, x, calculated_return_value])
                    self.result['expect'].append([r, x, uv])

        return self.result

    def i2c_to_uv(self, regulator, command):
        try:
            volt_config = self._i2c_to_volt_config(regulator,command)

            if volt_config['is_linear'] == True:
                mv = self._calculate_linear_mv(volt_config)
            else:
                mv = self._calculate_nonlinear_mv(volt_config)
            uv = self.mv_to_uv(mv)
        except Exception:
            uv = 'Cannot get uv!! Most likely i2c read failed'
        finally:
            return uv

    def i2c_to_tune_uv(self, regulator, command):
        try:
            tune_config = self._i2c_to_tune_config(regulator, command)
            mv = self._calculate_linear_mv(tune_config)
            uv= self.mv_to_uv(mv)
        except Exception:
            uv = 'Cannot get uv!! Most likely i2c read failed'
        finally:
            return uv

    def i2c_to_lim_uv(self, regulator, setting, command):
        try:
            volt_config = self._i2c_to_lim_config(regulator,setting,command)

            if volt_config['is_linear'] == True:
                mv = self._calculate_linear_mv(volt_config)
            else:
                mv = self._calculate_nonlinear_mv(volt_config)
            uv = self.mv_to_uv(mv)
        except Exception:
            uv = 'Cannot get uv!! Most likely i2c read failed'
        finally:
            return uv

    def i2c_to_ramprate_uv(self, regulator, command):
        try:
            volt_config = self._i2c_to_ramprate_config(regulator, command)
            if volt_config['is_linear'] == True:
                mv = self._calculate_linear_mv(volt_config)
            else:
                mv = self._calculate_nonlinear_mv(volt_config)
            uv = self.mv_to_uv(mv)
        except Exception:
            uv = 'Cannot get uv!! Most likely i2c read failed'
        finally:
            return uv

    def _bitshift_by_bitmask(self, regulator, setting,i2c):
        bitmask = self.board.data['regulators'][regulator]['settings'][setting]['reg_bitmask']
        shift_count = int(math.log2(bitmask & -bitmask))

        volt_index = i2c >> shift_count
        return  volt_index

    def _i2c_to_ramprate_config(self, regulator, command):
        volt_config={
                'r':            None,
                'volt_index':   None,
                'is_linear':    None,
                'operation':    'add',
                'start_mV':     None,
                'step_mV':      None,
                'list_mV':      None,
                }

        #   Get limit register value
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings']['ramprate']['reg_address'])))
        i2creturn = int(stdout[0],0)
        volt_config['volt_index'] = i2creturn & self.board.data['regulators'][regulator]['settings']['ramprate']['reg_bitmask']

        #   Get range
        for key in self.board.data['regulators'][regulator]['settings']['ramprate']['range'].keys():
            if volt_config['volt_index'] in range(self.board.data['regulators'][regulator]['settings']['ramprate']['range'][key]['start_reg'], self.board.data['regulators'][regulator]['settings']['ramprate']['range'][key]['stop_reg']+1):
                r=key

        volt_config['volt_index'] = (i2creturn & self.board.data['regulators'][regulator]['settings']['ramprate']['reg_bitmask']) - self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['start_reg']
        volt_config['volt_index'] = self._bitshift_by_bitmask(regulator, 'ramprate', volt_config['volt_index'])
        #   Gather linear / non-linear info of current range
        volt_config['is_linear'] = self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['is_linear']
        if self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['is_linear'] == True:
            volt_config['start_mV'] = self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['start_mV']
            volt_config['step_mV'] = self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['step_mV']
        elif self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['is_linear'] == False:
            volt_config['list_mV'] = self.board.data['regulators'][regulator]['settings']['ramprate']['range'][r]['list_mV']

        return volt_config

    def _i2c_to_lim_config(self, regulator, setting, command):
        volt_config={
                'r':            None,
                'volt_index':   None,
                'is_linear':    None,
                'operation':    'add',
                'start_mV':     None,
                'step_mV':      None,
                'list_mV':      None,
                }

        #   Get limit register value
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings'][setting]['reg_address'])))
        i2creturn = int(stdout[0],0)
        volt_config['volt_index'] = i2creturn & self.board.data['regulators'][regulator]['settings'][setting]['reg_bitmask']

        #   Get range
        for key in self.board.data['regulators'][regulator]['settings'][setting]['range'].keys():
            if volt_config['volt_index'] in range(self.board.data['regulators'][regulator]['settings'][setting]['range'][key]['start_reg'], self.board.data['regulators'][regulator]['settings'][setting]['range'][key]['stop_reg']+1):
                r=key

        volt_config['volt_index'] = (i2creturn & self.board.data['regulators'][regulator]['settings'][setting]['reg_bitmask']) - self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['start_reg']

        #   Gather linear / non-linear info of current range
        volt_config['is_linear'] = self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['is_linear']
        if self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['is_linear'] == True:
            volt_config['start_mV'] = self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['start_mV']
            volt_config['step_mV'] = self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['step_mV']
        elif self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['is_linear'] == False:
            volt_config['list_mV'] = self.board.data['regulators'][regulator]['settings'][setting]['range'][r]['list_mV']

        return volt_config

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
        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]['settings']['voltage']:
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings']['voltage']['volt_reg_address'])))
            i2creturn = int(stdout[0],0)
            volt_config['volt_index'] = i2creturn & self.board.data['regulators'][regulator]['settings']['voltage']['volt_reg_bitmask']
        elif(not 'volt_reg_bitmask' in self.board.data['regulators'][regulator]['settings']['voltage'] and 'regulator_en_address' in self.board.data['regulators'][regulator]):
            stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))
            i2creturn = int(stdout[0],0)

        #   Get range
        if self.board.data['regulators'][regulator]['settings']['voltage']['volt_sel'] == True:
            r = i2creturn & self.board.data['regulators'][regulator]['settings']['voltage']['volt_sel_bitmask']

        if (self.board.data['regulators'][regulator]['settings']['voltage']['volt_sel'] == False):
            for key in self.board.data['regulators'][regulator]['settings']['voltage']['range'].keys():
                if volt_config['volt_index'] in range(self.board.data['regulators'][regulator]['settings']['voltage']['range'][key]['start_reg'], self.board.data['regulators'][regulator]['settings']['voltage']['range'][key]['stop_reg']+1):
                    r=key

        #   Turn voltage register value to index value of current range
        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]['settings']['voltage']:
            volt_config['volt_index'] = (i2creturn & self.board.data['regulators'][regulator]['settings']['voltage']['volt_reg_bitmask']) - self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_reg']

        #   Get offset sign if present
        if 'is_offset_bipolar' in self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]:
            unmasked_offset_sign = i2creturn & self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]['offset_sign_bitmask']
            if unmasked_offset_sign == 1:
                volt_config['operation'] = 'substract'

        #   Gather linear / non-linear info of current range
        volt_config['is_linear'] = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['is_linear']
        if self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]['is_linear'] == True:
            volt_config['start_mV'] = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['start_mV']
            volt_config['step_mV'] = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['step_mV']
        elif self.board.data['regulators'][regulator]['settings']['voltage'][setting][r]['is_linear'] == False:
            volt_config['list_mV'] = self.board.data['regulators'][regulator]['settings']['voltage']['range'][r]['list_mV']

        return volt_config

    def _i2c_to_tune_config(self, regulator, command):
        volt_config={
                'volt_index':   None,
                'is_linear':    None,
                'operation':    'add',
                'start_mV':     None,
                'step_mV':      None,
                'list_mV':      None,
                'tune_index':   None,
                }
        # Gather info of regulators voltage tune setting
        if 'voltage_tune' in self.board.data['regulators'][regulator]['settings'].keys():
            stdout, stderr, returncode = command.run("i2cget -f -y "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['settings']['voltage_tune']['reg_address'])))
            i2creturn = int(stdout[0],0)
            volt_config['volt_index'] = i2creturn & self.board.data['regulators'][regulator]['settings']['voltage_tune']['reg_bitmask']
            # Get the range where the returned i2c value is
            if self.board.data['regulators'][regulator]['settings']['voltage_tune']['volt_sel'] == False:
                for key in self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'].keys():
                    if volt_config['volt_index'] in range(self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][key]['start_reg'], self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][key]['stop_reg']+1):
                        r=key

                # This is the actual index of the found range
                volt_config['volt_index'] = (i2creturn & self.board.data['regulators'][regulator]['settings']['voltage_tune']['reg_bitmask']) - self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['start_reg']
                #   Gather linear / non-linear info of current range
                volt_config['is_linear'] = self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['is_linear']
                if self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['is_linear'] == True:
                    volt_config['start_mV'] = self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['start_mV']
                    volt_config['step_mV'] = self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['step_mV']
                elif self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['is_linear'] == False:
                    volt_config['list_mV'] = self.board.data['regulators'][regulator]['settings']['voltage_tune']['range'][r]['list_mV']

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
