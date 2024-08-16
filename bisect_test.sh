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
cp ../bugged2_bd718x7-regulator.c drivers/regulator/bd718x7-regulator.c
git add .
git commit -m "bugged bd718x8-regulator.c"
git push origin test_linux
echo '-------'

echo 'Push 3'
echo '-------'
echo 'x' >> README
git add .
git commit -m "bad commit"
git push origin test_linux
echo '-------'
git tag $1
git push origin $1

cp ../bd718x7-regulator.c drivers/regulator/
