from ev3db.server import local
from os import system

def setup():
    if local:
        commands=["git clone https://github.com/RikyIsola/ev3db.git .tmp",
                  "sshpass -p 'maker' scp -r .tmp/ev3db robot@ev3dev.local:~",
                  "sshpass -p 'maker' scp -r .tmp/.utils robot@ev3dev.local:~",
                  "sshpass -p 'maker' scp .tmp/ev3db-cli robot@ev3dev.local:~",
                  "sshpass -p 'maker' ssh robot@ev3dev.local 'echo \"maker\" | sudo -S bash .utils/setup.sh'",
                  "rm -rf .tmp"]
    else:
        systemd='[Unit]\n' \
                'Description=EV3 debug bridge service\n' \
                'After=network.target\n' \
                '[Service]\n' \
                'Type=simple\n' \
                'User=robot\n' \
                'WorkingDirectory=/home/robot\n' \
                'ExecStart=/home/robot/ev3db-cli --server\n' \
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
