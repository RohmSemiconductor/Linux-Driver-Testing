#!/bin/bash
git checkout test_linux
echo 'x' >> README
git add README
git commit
git push origin test_linux
git tag $1
git push origin $1
