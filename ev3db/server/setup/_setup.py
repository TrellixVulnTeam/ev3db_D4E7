from ev3db.server import local
from os import system

def setup():
    if local:
        commands=["sshpass -p 'maker' "]
    else:
        systemd='[Unit]\n' \
                'Description=EV3 debug bridge service\n' \
                'After=network.target\n' \
                '[Service]\n' \
                'Type=simple\n' \
                'User=robot\n' \
                'WorkingDirectory=/home/robot\n' \
                'ExecStart=/home/robot/.local/bin/ev3db-server\n' \
                'Restart=on-failure\n' \
                '[Install]\n' \
                'WantedBy=multi-user.target'

        commands=['printf "{}" > "/etc/systemd/system/ev3db.service"'.format(systemd),
                  'systemctl daemon-reload',
                  'systemctl enable ev3db',
                  'systemctl start ev3db']

    for command in commands:
        terminal(command)


def terminal(command:str):
    if system(command)!=0:
        raise Exception('"{}" execution failed'.format(command))