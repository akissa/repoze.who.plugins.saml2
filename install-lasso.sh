#!/bin/sh
set -ex
curl -O https://dev.entrouvert.org/releases/lasso/lasso-2.5.0.tar.gz
tar xzf lasso-2.5.0.tar.gz
cd lasso-2.5.0/
./configure --prefix=/usr --disable-java --disable-perl
make
sudo make install
baruwa_path=$(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
cp bindings/python/lasso.py ${baruwa_path}/
cp bindings/python/.libs/_lasso.so ${baruwa_path}/
cd -
