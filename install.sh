#!/bin/bash

echo ""
echo "=========================================="
echo "lcarsde logout installation"
echo "=========================================="
echo ""
echo "This program requires:"
echo "* Python 3.8"
echo "* Python 3 PyGObject"
echo "* Python psutil"
echo ""

cp ./src/lcarsde-logout.py /usr/bin/lcarsde-logout.py
cp -R ./resources/usr/* /usr/
