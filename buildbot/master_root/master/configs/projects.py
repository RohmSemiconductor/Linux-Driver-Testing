import sys 
import os
sys.path.append(os.path.abspath("."))

from configs.factories import *

tag_change = lambda ref: ref.startswith('refs/tags/')

###### PROJECTS
# To trigger gitpoller on tag changes, use tag_change instead of ['branch_name'] in the 'branches'
projects = {}

projects['test_linux']= {
    'name': 'test_linux',
    #'branches': ['test_linux'],
    'branches': tag_change,
    'repo_git': 'https://github.com/RohmSemiconductor/Linux-Driver-Testing.git',
    'polling': 60,
    'scheduler_name': 'scheduler-test_linux',
    'builderNames': ["builder_test_linux"],
    'workerNames': ["worker1"],
    'factory': factory_test_linux,
}
projects['linux_next']={
    'name': 'linux_next',
    'branches': tag_change,
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git',
    'polling': 60,
}
