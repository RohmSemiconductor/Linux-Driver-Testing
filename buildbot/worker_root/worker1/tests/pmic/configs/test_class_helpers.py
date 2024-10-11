import math

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
