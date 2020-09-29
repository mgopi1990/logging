#!/usr/bin/env bash

PHONE_IP="192.168.1.182"
DEST_DIR="/home/storage/shared/gopi/Logs/"
SRC_DIR="/home/pi/gopi/gopi_updates/logging/bkp/"

echo "just scp backup to phone"
echo "start termux in your phone"
echo "enable sshd"

scp -P 8022 ${SRC_DIR}/*.7z ${PHONE_IP}:${DEST_DIR}

