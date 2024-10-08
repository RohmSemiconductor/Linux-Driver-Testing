#!/bin/bash
source /home/kale/Linux-Driver-Testing/buildbot/worker_root/sandbox/bin/activate
#pytest -ra --lg-env=beagle$2.yaml _test_000_reboot.py
pytest -ra --lg-env=beagle$2.yaml _test_000_shell.py
pytest --lg-env beagle$2.yaml test_001_init_overlay.py
pytest -ra --lg-env beagle$2.yaml test_002_merge_dt_overlay.py --product=$1

