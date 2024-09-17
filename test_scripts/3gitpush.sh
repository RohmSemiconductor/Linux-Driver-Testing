#!/bin/bash
echo 'Push 1'
echo '-------'
git checkout test_linux
echo 'x' >> README
git add .
git commit -m 'Pull the plug!'
git push origin test_linux
echo '-------'

echo 'Push 2'
echo '-------'
echo 'x' >> README
git add .
git commit -m 'Commit 2'
git push origin test_linux
echo '-------'

echo 'Push 3'
echo '-------'
echo 'x' >> README
git add .
git commit -m 'Commit 3'
git push origin test_linux
echo '-------'

git tag $1
git push origin $1
