#!/usr/bin/env bash

source ./password.sh

DATE=`date +'%d%b%Y'`
FILENAME="logs_${DATE}.7z"
HOMEDIR="/home/pi/gopi/gopi_updates/logging/"

echo "- BACKUP: $DATE -"

cd ${HOMEDIR}/bkp/

## perform backup
7z a $FILENAME -p$PASSWORD ${HOMEDIR}/logs/ ${HOMEDIR}/scripts/.git/ ${HOMEDIR}/scripts/src/ ${HOMEDIR}/scripts/README.md ${HOMEDIR}/scripts/requirements.txt

## delete old archieve
ls -t logs_*.7z | tail -n+6 | xargs rm -vf

