#!/usr/bin/env bash

source ./password.sh

DATE=`date +'%d%b%Y'`
FILENAME="logs_${DATE}.7z"
HOMEDIR="/home/pi/gopi/gopi_updates/logging/"

cd ${HOMEDIR}/bkp/
7z a $FILENAME -p$PASSWORD ${HOMEDIR}/logs/ ${HOMEDIR}/scripts/.git/ ${HOMEDIR}/scripts/src/ ${HOMEDIR}/scripts/README.md ${HOMEDIR}/scripts/requirements.txt
