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
    #    name: str
    #    of_match: str
    #    steps
    #    stepV
    #    address
    #    i2caddr
    #    i2cbus
    #start_mV: int
    #    dt_properties                   #device tree properties

    #def get_regulator_voltages(self):
        #for regulators in product:

            #regulator_voltages=[]
        #regulator_regvalues=[]
    def escape_path(self, path_str):
        path = path_str.translate(str.maketrans({'@':'\\@'}))
        return path
    
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

#    def regulator_voltage_run(self,regulator,command):

#        stdout,stderr,returncode= command.run("echo 1 > /sys/kernel/mva_test/regulators"
#        stdout,stderr,returncode= command.run("echo 1 > /sys/kernel/mva_test/regulators"
#        str="echo 1 > /sys/kernel/mva_test/regulators/"+pmic_data[target]['regulators']+"_en"


