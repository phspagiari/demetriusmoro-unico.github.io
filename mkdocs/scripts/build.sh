#/bin/bash

pip3 install -r mkdocs/scripts/build.pip
rm -rf mkdocs/docs/temp
FETCH_DEPENDENCIES=$FETCH_DEPENDENCIES python3 mkdocs/scripts/build.py
