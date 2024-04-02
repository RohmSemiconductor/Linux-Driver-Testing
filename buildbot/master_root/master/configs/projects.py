import sys 
import os
sys.path.append(os.path.abspath("./configs"))

from factories import *

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
    'treeStableTimer': 30,
    'scheduler_name': 'scheduler-test_linux',
    'builderNames': ["builder_test_linux"],
    'builderNames': ["Test Linux"],
    'workerNames': ["worker1"],
    'factory': factory_test_linux,
#    'factory': factory_driver_test,
}
projects['linux-next']={
    'name': 'linux-next',
    'branches': tag_change,
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git',
    'polling': 60,
    'treeStableTimer': 600,
    'scheduler_name': 'scheduler-linux-next',
    'builderNames': ["linux-next"],
    'workerNames': ["worker1"],
    'factory': factory_linux_next,
}
#projects['test-kernel-modules']={
#    'name': 'test-kernel-modules',
#    'branches': ['test-kernel-modules'],
#    'repo_git': 'https://github.com/RohmSemiconductor/Linux-Driver-Testing.git',
#    'polling': 60,
#    'scheduler_name': 'scheduler-test-kernel-modules',
#    'builderNames': ["Test kernel modules"],
#    'workerNames': ["worker1"],
#    'factory': factory_test_kernel_modules,
#}
