import sys
import os

from buildbot.plugins import util

#### 5.15.* <- oldest linux-stable to be tested
tag_change = lambda ref: ref.startswith('refs/tags/')


factory_build_linux_test_linux = util.BuildFactory()
factory_test_linux = util.BuildFactory()
factory_linux_next = util.BuildFactory()
factory_linux_mainline = util.BuildFactory()
factory_linux_stable = util.BuildFactory()
factory_linux_rohm_devel = util.BuildFactory()
###### PROJECTS
# To trigger gitpoller on tag changes, use tag_change instead of ['branch_name'] in the 'branches'
projects = {}

projects['linux_mainline']={
    'name': 'linux_mainline',                                                           # Used in factories.py to add steps to factory
#    'branches': tag_change,                                                            # It is possible to poll for tag changes, but this proved problematic
    'branches': ['master'],                                                             # Poll for a list of branches, even single branch needs to be in a list
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git',   # This is the url for the git repository
    'polling': 480,                                                                     # Polling interval in seconds
    'treeStableTimer': 1100,                                                            # This is a timer which resets everytime a new change is made, helps during mergewindow so BB doesn't build every change
    'scheduler_name': 'scheduler-linux_mainline',                                       # Scheduler used for the project, in master.cfg there is regex rules for schedulers: change_commit_is_release(change)
    'builderNames': ["Linux_Mainline"],                                                 # Separate builder for each projects, these appear separately in the BuildBot Web view
    'workerNames': ["Linux_Worker"],                                                         # List of workers which can build and run this project, Linux_Worker is a local worker
    'factory': factory_linux_mainline,                                                  # Factory used for this project
}
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
    'workerNames': ["Linux_Worker"],
    'factory': factory_build_linux_test_linux,
#    'factory': factory_driver_test,
}
projects['linux-next']={
    'name': 'linux-next',
#    'branches': tag_change,
    'branches': ['master'],
    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git',
    'polling': 480,
    'treeStableTimer': 1100,
    'scheduler_name': 'scheduler-linux-next',
    'builderNames': ["linux-next"],
    'workerNames': ["Linux_Worker"],
    'factory': factory_linux_next,
}
projects['linux_rohm_devel']={
    'name': 'linux_rohm_devel',
    'branches': ['rohm-pmic-test-temporary'],
    'repo_git': 'https://github.com/RohmSemiconductor/Linux-Kernel-PMIC-Drivers.git',
    'polling': 20,
    'treeStableTimer': 30,
    'scheduler_name': 'scheduler-linux_rohm_devel',
    'builderNames': ["linux-rohm-devel"],
    'workerNames': ["Linux_Worker"],
    'factory': factory_linux_rohm_devel,
}

#stable_branches =   ['linux-5.15.y', 'linux-6.1.y', 'linux-6.6.y',  #LTS kernels
#                    'linux-6.10.y', 'linux-6.11.y']             #Short time stable


projects['linux_stable']={
    'name': 'linux_stable',
    'repo_git': 'https://github.com/KalleNiemi/linux_stable_testing.git',
    'workerNames': ["Linux_Worker"],
    'factory': factory_linux_stable,
}

stable_branches =   ['linux-5.15.y',  #LTS kernels
                     'linux-6.12.y']             #Short time stable

for stable_branch in stable_branches:

    stable_branch = stable_branch.replace(".","_")

    globals()['factory_linux_stable_'+stable_branch] = util.BuildFactory()
    stable_factory = globals()['factory_linux_stable_'+stable_branch]

    projects['linux_stable_'+stable_branch]={
    'name': 'linux_stable_'+stable_branch,
#    'branches': tag_change,
    'branches': [stable_branch],
#    'repo_git': 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git',
    'repo_git': 'https://github.com/KalleNiemi/linux_stable_testing.git',
    'polling': 30,
    'treeStableTimer': 60,
    'scheduler_name': 'scheduler-linux_stable_'+stable_branch,
    'builderNames': ['linux_stable_'+stable_branch],
    'workerNames': ["Linux_Worker"],
#    'factory': factory_linux_stable,
    'factory': stable_factory,
}
