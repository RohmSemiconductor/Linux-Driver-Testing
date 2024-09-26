#!/bin/bash
cd ..
echo 'Push 1'
echo '-------'
git checkout test_linux
echo 'x' >> README
git add .
git commit -m "clean commit"
git push origin test_linux
echo '-------'

echo 'Push 1'
echo '-------'
cp ../bugged_test_linear_ranges.c lib/test_linear_ranges.c
git add .
git commit -m "bugged lib/test_linear_ranges.c"
git push origin test_linux
echo '-------'

cp ../test_linear_ranges.c lib/
