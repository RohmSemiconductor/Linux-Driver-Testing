#!/bin/bash
git checkout test_linux
echo 'x' >> README
git add .
git commit -m 'Linux 6.8'
git push origin test_linux
git tag $1
git push origin $1
