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
    
    def escape_path(self, path_str):
        path = path_str.translate(str.maketrans({'@':'\\@'}))
        return path

    def mv_to_uv(self, mV):
        uV = mV * 1000
        return uV

    def sanity_check(self,regulator,command):
        stdout, stderr, returncode = command.run("grep -r -l rohm,"+self.board.data['name']+" /proc/device-tree | sed 's![^/]*$!!'") #sed removes everything from end until first"/", returning only the path instead of path/file
        path = self.escape_path(stdout[0])
        stdout, stderr, returncode = command.run("test -d "+stdout[0]+"regulators/"+self.board.data['regulators'][regulator]['of_match']+"/regulator-always-on ;echo $?")
        if stdout[0] == '0': #test -d returns 0 if file is found
            return 1
        if stdout[0] == '1':
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
        i2creturn = int(stdout[0],0);
        regulator_en_status = i2creturn & self.board.data['regulators'][regulator]['regulator_en_bitmask']
        return regulator_en_status

    def regulator_voltage(self,regulator, r,command, volt_index=None):
        if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
            mv = self.board.data['regulators'][regulator]['range'][r]['start_mV'] +(self.board.data['regulators'][regulator]['range'][r]['step_mV'] * volt_index)
            uv = self.mv_to_uv(mv)
        elif self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
            mv = self.board.data['regulators'][regulator]['range'][r]['list_mV'][volt_index]
            uv = self.mv_to_uv(mv)
        command.run("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")
        print("echo "+str(uv)+" "+str(uv)+" > /sys/kernel/mva_test/regulators/"+regulator+"_set")
#        sleep(0.2)
        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['volt_reg_address'])))
        i2creturn = int(stdout[0],0);
        if (self.board.data['regulators'][regulator]['volt_sel'] == False or not "volt_sel"in self.board.data['regulators'][regulator]):
            regulator_volt_status = i2creturn
#            print("or if not")
        regulator_volt_status = i2creturn
#       kokeile ensin käsin!!!!!!!!
#        force_fail = 1
#        assert force_fail == 0    
        return regulator_volt_status

    def regulator_voltage_run(self,regulator,command): 
            for r in self.board.data['regulators'][regulator]['range'].keys():
                if self.board.data['regulators'][regulator]['range'][r]['is_linear'] == True:
                    #                    print(r)
                    print("Range: "+r)
                    
                    for x in range(self.board.data['regulators'][regulator]['range'][r]['start_reg'], self.board.data['regulators'][regulator]['range'][r]['stop_reg']+1): 
                        volt_index = x - self.board.data['regulators'][regulator]['range'][r]['start_reg']
                        regulator_volt_status = self.regulator_voltage(regulator, r,command, volt_index)
                        print("Reg volt i2c hex: "+str(hex(regulator_volt_status)))
                        
                elif self.board.data['regulators'][regulator]['range'][r]['is_linear'] == False:
                    #for x in range(len(self.board.data['regulators'][regulator]['range'][r]['list_mV'])):
                    for x in range(self.board.data['regulators'][regulator]['range'][r]['start_reg'], self.board.data['regulators'][regulator]['range'][r]['stop_reg']+1):
                        #    print(x)
                        volt_index = x
                        regulator_volt_status = self.regulator_voltage(regulator, r, command, volt_index)
                        print("Reg volt i2c hex: "+str(hex(regulator_volt_status)))

#        stdout, stderr, returncode = command.run("i2cget -y -f "+str(self.board.data['i2c']['bus'])+" "+str(hex(self.board.data['i2c']['address']))+" "+str(hex(self.board.data['regulators'][regulator]['regulator_en_address'])))


#        command.run("echo ")
#        stdout,stderr,returncode= command.run("echo 1 > /sys/kernel/mva_test/regulators"
#        stdout,stderr,returncode= command.run("echo 1 > /sys/kernel/mva_test/regulators"
#        str="echo 1 > /sys/kernel/mva_test/regulators/"+pmic_data[target]['regulators']+"_en"


