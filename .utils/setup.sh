#!/usr/bin/env bash
set -e
printf '
[Unit]
Description=EV3 debug bridge service
After=network.target
[Service]
Type=simple
User=robot
WorkingDirectory=/home/robot
ExecStart=/home/robot/ev3db-cli --server
Restart=on-failure
[Install]
WantedBy=multi-user.target
' > /etc/systemd/system/ev3db.service
systemctl daemon-reload
systemctl enable ev3db
systemctl start ev3db
