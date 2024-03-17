#!/bin/bash

source ~/Linux-Driver-Testing/buildbot/master_root/sandbox/bin/activate

echo "Virtual environment activated"

buildbot restart buildbot/master_root/master/

source ~/Linux-Driver-Testing/buildbot/worker_root/sandbox/bin/activate

buildbot-worker restart buildbot/worker_root/torvalds_worker/
