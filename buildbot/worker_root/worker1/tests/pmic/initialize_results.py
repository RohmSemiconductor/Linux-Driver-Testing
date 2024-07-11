import sys
from pathlib import Path

sys.path.append('..')
from test_util import *

bb_project = sys.argv[1]
linux_ver = sys.argv[2]
initialize_report(bb_project, linux_ver)
print(sys.path)
