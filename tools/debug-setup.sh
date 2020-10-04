#!/usr/bin/env bash
set -e
sshpass -p 'maker' scp -r ev3db robot@ev3dev.local:~
sshpass -p 'maker' scp ev3db-cli robot@ev3dev.local:~
sshpass -p 'maker' scp .shebangs robot@ev3dev.local:~
sshpass -p 'maker' ssh robot@ev3dev.local 'fuser -k 55555/tcp; ./ev3db-cli --server'