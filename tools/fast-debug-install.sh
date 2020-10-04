#!/usr/bin/env bash
set -e
tar -czvf ev3db.tar.gz ev3db
sshpass -p 'maker' scp -r ev3db.tar.gz robot@ev3dev.local:~
rm ev3db.tar.gz
sshpass -p 'maker' ssh robot@ev3dev.local 'echo "maker" | sudo -S systemctl stop ev3db; sudo fuser 55555/tcp; tar -zxvf ev3db.tar.gz && rm ev3db.tar.gz && python3 ev3db/server/_server.py'
echo -ne '\007'