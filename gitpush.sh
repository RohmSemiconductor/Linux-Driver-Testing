#!/bin/bash
git checkout test_linux
echo 'x' >> README
git add .
git commit -m 'Changed README to make a change'
git push origin test_linux
git tag $1
git push origin $1
