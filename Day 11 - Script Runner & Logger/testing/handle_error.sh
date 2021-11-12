#!/bin/sh
# Usage: ./test.sh

python script.py

ret=$?
if [ $ret -ne 0 ]; then
	echo FAIL
else
	echo PASS
fi
