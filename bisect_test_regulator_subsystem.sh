#!/bin/bash
echo 'Push 1'
echo '-------'
git checkout test_linux
echo 'x' >> README
git add .
git commit -m "clean commit"
git push origin test_linux
echo '-------'

echo 'Push 2'
echo '-------'
cp ../bugged_driver.h include/linux/regulator/driver.h
git add .
git commit -m "bugged driver.h"
git push origin test_linux
echo '-------'

echo 'Push 3'
echo '-------'
echo 'x' >> README
git add .
git commit -m "bad commit"
git push origin test_linux
echo '-------'

cp ../driver.h include/linux/regulator/driver.h
