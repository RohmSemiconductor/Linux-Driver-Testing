#!/bin/bash
git checkout test_linux
echo 'x' >> README
git add .
git commit -m 'Add linux-next specific files for 20240418'
git push origin test_linux
git tag $1
git push origin $1
