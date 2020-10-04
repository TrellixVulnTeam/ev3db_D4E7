#!/usr/bin/env bash
set -e
python setup.py bdist_wheel
sshpass -p 'maker' scp dist/ev3db-0.1-py3-none-any.whl robot@ev3dev.local:~
rm -r build
rm -r dist
rm -r ev3db.egg-info
sshpass -p 'maker' ssh robot@ev3dev.local 'echo "maker" | sudo -S systemctl stop ev3db; sudo fuser 55555/tcp; pip3 install --upgrade ev3db-0.1-py3-none-any.whl && rm ev3db-0.1-py3-none-any.whl && .local/bin/ev3db --server'
echo -ne '\007'