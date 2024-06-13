import sys 
import os
sys.path.append(os.path.abspath("./configs"))

from factories import *

#### 5.15.* <- oldest linux-stable to be tested
tag_change = lambda ref: ref.startswith('refs/tags/')




###### PROJECTS
# To trigger gitpoller on tag changes, use tag_change instead of ['branch_name'] in the 'branches'
projects = {}

projects['test_linux']= {
    'name': 'test_linux',
    'branches': ['test_linux'],
#    'branches': tag_change,
    'repo_git': 'https://github.com/RohmSemiconductor/Linux-Driver-Testing.git',
    'polling': 60,
    'treeStableTimer': 80,
    'scheduler_name': 'scheduler-test_linux',
#    'builderNames': ["builder_test_linux"],
    'builderNames': ["Test_Linux"],
    'workerNames': ["worker1"],
    'factory': factory_test_linux,
#    'factory': factory_driver_test,
}
projects['linux-next']={
    'name': 'linux-next',
#    'branches': tag_change,
    'branches': ['master'],
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git',
    'polling': 480,
    'treeStableTimer': 1000,
    'scheduler_name': 'scheduler-linux-next',
    'builderNames': ["linux-next"],
    'workerNames': ["worker1"],
    'factory': factory_linux_next,
}
projects['linux_mainline']={
    'name': 'linux_mainline',
#    'branches': tag_change,
    'branches': ['master'],
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git',
    'polling': 480,
    'treeStableTimer': 1000,
    'scheduler_name': 'scheduler-linux_mainline',
    'builderNames': ["Linux_Mainline"],
    'workerNames': ["worker1"],
    'factory': factory_linux_mainline,
}
projects['linux_stable']={
    'name': 'linux_stable',
#    'branches': tag_change,
    'branches': ['linux-5.15.y','linux-6.1.y','linux-6.6.y',    #LTS kernels
    'linux-6.8.y'],                                             #short time stable
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/',
    'polling': 480,
    'treeStableTimer': 1000,
    'scheduler_name': 'scheduler-linux_stable',
    'builderNames': ["linux-stable"],
    'workerNames': ["worker1"],
    'factory': factory_linux_stable,
}
projects['linux_rohm_devel']={
    'name': 'linux_rohm_devel',
    'branches': ['rohm-pmic-test-temporary'],
    'repo_git': 'https://github.com/RohmSemiconductor/Linux-Kernel-PMIC-Drivers.git',
    'polling': 20,
    'treeStableTimer': 30,
    'scheduler_name': 'scheduler-linux_rohm_devel',
    'builderNames': ["linux-rohm-devel"],
    'workerNames': ["worker1"],
    'factory': factory_linux_rohm_devel,
}
