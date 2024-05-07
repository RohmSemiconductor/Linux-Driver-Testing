#!/bin/bash
source /home/user01/Linux-Driver-Testing/buildbot/worker_root/sandbox/bin/activate
pytest -ra test_login.py --beagle=beagle1 --power_port=1
pytest --lg-env beagle1.yaml test_init_overlay.py
pytest -ra --lg-env beagle1.yaml test_merge_dt_overlay.py --product=$1
pytest -ra --lg-env beagle1.yaml test_insmod_tests.py --product=$1
pytest -ra --lg-env beagle1.yaml test_init_regulator_test.py --product=$1
#pytest -ra --lg-env beagle1.yaml test_test_target.py --product=$1 -W ignore::DeprecationWarning

