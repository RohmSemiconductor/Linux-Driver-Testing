import math

def bitshift_index_by_bitmask(bitmask, i2chex):
    shift_count = int(math.log2(bitmask & -bitmask))
    index = i2chex >> shift_count
    return index


def escape_path(path_str):
    path = path_str.translate(str.maketrans({'@':'\\@'}))
    path = path_str.translate(str.maketrans({':':'\\:'}))
    return path
