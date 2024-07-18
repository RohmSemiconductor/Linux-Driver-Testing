import sys

sys.path.append('.')
from test_util import initialize_report
if sys.argv[1] == 'initialize_report':
    bb_project = sys.argv[2]
    linux_ver = sys.argv[3]
    initialize_report(bb_project, linux_ver)
