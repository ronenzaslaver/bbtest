#!/usr/bin/env bash
cp rpycserver.sh /home/bbtest
cp rpycserver.service /lib/systemd/system
systemctl enable rpycserver.service
systemctl start rpycserver.service

