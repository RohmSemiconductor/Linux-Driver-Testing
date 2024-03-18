#!/bin/bash

#Start master
source ~/Linux-Driver-Testing/buildbot/master_root/sandbox/bin/activate
buildbot restart buildbot/master_root/master/

#Start worker
source ~/Linux-Driver-Testing/buildbot/worker_root/sandbox/bin/activate
buildbot-worker restart buildbot/worker_root/worker1
