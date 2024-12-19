#!/bin/bash
source /home/user01/Linux-Driver-Testing/buildbot/master_root/sandbox/bin/activate
pytest -ra test_000_login.py --beagle=beagle$2 --power_port=$3 --type=PMIC --product=$1
pytest --lg-env beagle$2.yaml test_001_init_overlay.py
pytest -ra --lg-env beagle$2.yaml test_002_merge_dt_overlay.py --product=$1
pytest -ra --lg-env beagle$2.yaml test_003_insmod_tests.py --product=$1
pytest -ra --lg-env beagle$2.yaml test_004_init_regulator_test.py --product=$1
#pytest -ra --lg-env beagle1.yaml test_test_target.py --product=$1 -W ignore::DeprecationWarning

