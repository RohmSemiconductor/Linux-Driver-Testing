#!/bin/bash
echo 'Push 1'
echo '-------'
git checkout test_linux
echo 'x' >> README
git add .
git commit -m 'Good commit'
git push origin test_linux
echo '-------'

echo 'Push 2'
echo '-------'
git add .
git commit -m 'Pull the plug!'
git push origin test_linux
git tag $1
git push origin $1
