#!/bin/bash

source ~/Linux-Driver-Testing/buildbot/master_root/sandbox/bin/activate

buildbot stop buildbot/master_root/master/

source ~/Linux-Driver-Testing/buildbot/worker_root/sandbox/bin/activate

buildbot-worker stop buildbot/worker_root/torvalds_worker/

