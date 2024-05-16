from dataclasses import dataclass
import pytest
from time import sleep
import sys
import os

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

    def _print_reg_val(reg_val):
        pass 

    def sanity_check(self,regulator,command):
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("test -f "+path+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/name ;echo $?")
        print(stdout[0])
        print(path)
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

    def calculated_uv(self, regulator, r, command, volt_index=None):
        if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['range'][r]['step_mV'] * volt_index)

        elif self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]

        uv = self.mv_to_uv(mv)
        return uv

    def regulator_voltage_get(self, regulator, command, r='values', volt_index=None):
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['volt_reg_address'])))
        i2creturn = int(stdout[0],0)
        operation = 'add'

        if 'volt_reg_bitmask' in self.board.data['regulators'][regulator]:
            volt_index = i2creturn & self.board.data['regulators'][regulator]['volt_reg_bitmask']

        if self.board.data['regulators'][regulator]['volt_sel'] == True:
            r = i2creturn & self.board.data['regulators'][regulator]['volt_sel_bitmask']

        if 'is_offset_bipolar' in self.board.data['regulators'][regulator]['range'][r]:
            unmasked_offset_sign = i2creturn & self.board.data['regulators'][regulator]['range'][r]['offset_sign_bitmask']
            if unmasked_offset_sign == 1:
                operation = 'substract'

        if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
            if operation == 'add':
                calculated_return_value = self.board.data['regulators'][regulator]['range'][r]['start_mV']+(volt_index * self.board.data['regulators'][regulator]['range'][r]['step_mV'])
            elif operation == 'substract':
                calculated_return_value = self.board.data['regulators'][regulator]['range'][r]['start_mV']-(volt_index * self.board.data['regulators'][regulator]['range'][r]['step_mV'])

        elif (self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False and not 'is_offset_bipolar' in self.board.data['regulators'][regulator]['range'][r]):
            if operation == 'add':
                calculated_return_value = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]
            elif operation == 'substract':
                calculated_return_value = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]
        else:
            print("Regulator voltage calculation is not implemented yet!")

        return calculated_return_value

    def regulator_voltage_set(self, regulator, r, command, volt_index=None):
        ######## SETS VOLTAGE THROUGH TEST KERNEL MODULE ######
        if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['range'][r]['step_mV'] * volt_index)

        elif self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]

        uv = self.mv_to_uv(mv)
        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")
        print("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")

        return uv

    def regulator_voltage(self,regulator, r,command, volt_index=None):
        uv = self.regulator_voltage_set(regulator, r, command, volt_index)
        calculated_return_value = self.regulator_voltage_get(regulator, r, command, volt_index)
        calculated_return_value = self.mv_to_uv(calculated_return_value)
        return uv, calculated_return_value

    def regulator_voltage_run(self,regulator,command):
        voltage_run={
            'test_failed': 0,
            'buck_fail':[]
            }

        for r in self.board.data['regulators'][regulator]['range'].keys():
            for x in range(self.board.data['regulators'][regulator]['range'][r]['start_reg'], self.board.data['regulators'][regulator]['range'][r]['stop_reg']+1):
                volt_index = x - self.board.data['regulators'][regulator]['range'][r]['start_reg']
                uv, calculated_return_value = self.regulator_voltage(regulator, r,command, volt_index)
                if uv != calculated_return_value:
                    voltage_run['test_failed']=1
                    voltage_run['buck_fail'].append([regulator,r,volt_index,uv, calculated_return_value])
                    print(uv)
                    print(calculated_return_value)

        return voltage_run
