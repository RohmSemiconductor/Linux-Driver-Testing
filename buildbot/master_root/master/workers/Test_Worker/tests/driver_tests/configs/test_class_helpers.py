import math
import subprocess
def bitshift_index_by_bitmask(bitmask, i2chex):
    shift_count = int(math.log2(bitmask & -bitmask))
    index = i2chex >> shift_count
    return index

def escape_path(path_str):
    path = path_str.translate(str.maketrans({'@':'\\@'}))
    path = path_str.translate(str.maketrans({':':'\\:'}))
    return path

def pc_to_int(percent):
    int_val = percent / 100
    return int_val

def frequency_to_ns(frequency):
    ns = (1/frequency) * pow(10,9)
    return ns

def combine_bytes(high_byte, low_byte):
    combined_bytes = (high_byte << 8) | low_byte
    return combined_bytes

def twos_complement(value, bits):
    if ( value & (1 << (bits -1 ))) != 0:
        mask = pow(2,bits) -1
        value = ((~value & mask) + 1) * -1
    return value

def bits_maxval(bits):
    ret = (2^bits)-1

    return ret

def find_iio_device_files(command, iio_name):
    try:
        stdout, stderr, returncode = command.run("grep -rH "+iio_name+" /sys/bus/iio/devices/*/name | sed 's![^/]*$!!'")
        x = 0
        for line in stdout:
            if "iio:" in line:
                correct_path_line = x
            x = x+1

        path = stdout[correct_path_line]
        path = escape_path(path)
    except Exception:
        path = "not_found"

    return path

### RTC / system time functions

def find_rtc_files(command, rtc_name):
    try:
        stdout, stderr, returncode = command.run("grep -rH "+rtc_name+" /sys/class/rtc/*/name | sed 's![^/]*$!!'")
        sysfs_path = stdout[0]
        dev_file = sysfs_path.replace('/sys/class/rtc/','')
        dev_file = dev_file.replace('/','')
    except Exception:
        sysfs_path = "sysfs file not found"
        dev_file = "device file not found"
        returncode = -1

    return sysfs_path, dev_file, returncode

def get_srv_time():
    stdout = subprocess.run("date -u \'+%Y-%m-%d %H:%M:%S\'", shell=True, encoding='UTF-8', stdout=subprocess.PIPE).stdout.splitlines()

    return stdout[0]

def get_srv_epoch():
    stdout = subprocess.run("date -u +%s", shell=True, encoding='UTF-8', stdout=subprocess.PIPE).stdout.splitlines()

    return int(stdout[0])

def get_beagle_epoch(command):
    stdout, stderr, returncode = command.run("date +%s")

    return int(stdout[0])

def set_beagle_time_from_rtc(command, dev_file):
    stdout, stderr, returncode = command.run("hwclock -f /dev/"+dev_file+" --hctosys")

    return returncode

def set_rtc_time_from_bbb_sys(command, dev_file):
    stdout, stderr, returncode = command.run("hwclock -f /dev/"+dev_file+" --systohc")

    return returncode

def set_rtc_time(command, dev_file, time):
    stdout, stderr, returncode = command.run("hwclock -f /dev/"+dev_file+" --set --date \'"+time+"\'")

    return stdout, stderr, returncode

def get_rtc_date(command, rtc_name):
    path, dev_file, returncode = find_rtc_files(command, rtc_name)
    stdout, stderr, returncode = command.run("cat "+path+"/date")

    return stdout[0]

def get_rtc_epoch(command, rtc_name):
    path, dev_file, returncode = find_rtc_files(command, rtc_name)
    stdout, stderr, returncode = command.run("cat "+path+"/since_epoch")

    return int(stdout[0])

def split_datetime(datetime):
    split = datetime.split(" ", 1)
    date = split[0]
    time = split[1]

    return date, time
