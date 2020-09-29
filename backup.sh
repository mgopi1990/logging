#!/usr/bin/env bash

source ./password.sh

DATE=`date +'%d%b%Y'`
FILENAME="logs_${DATE}.7z"

cd /home/pi/gopi/gopi_updates/logging/bkp
7z a $FILENAME -p$PASSWORD ../logs/ ../scripts/
