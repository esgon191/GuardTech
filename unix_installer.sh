#!/bin/bash
python3 -m ensurepip --upgrade
python3 -m venv GuardTech_venv
source GuardTech_venv/bin/activate
pip3 install -r requirments.txt
cp .do_not_launch.sh launch.sh
echo "type <./launch.sh> without <> to launch and precc control+C to exit"