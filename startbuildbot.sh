#!/bin/bash

#Start master
source ~/Linux-Driver-Testing/buildbot/master_root/sandbox/bin/activate
buildbot start buildbot/master_root/master/
sleep 1
#Start worker
source ~/Linux-Driver-Testing/buildbot/worker_root/sandbox/bin/activate
buildbot-worker start buildbot/worker_root/worker1
