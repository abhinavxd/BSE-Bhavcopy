#!/bin/bash

sleep 1s

#For first time execution set last run date less than todays date.
lastRunDate="13-05-2021"

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_EXEC="${SCRIPTDIR}/../venv/bin/python"
APPDIR=${SCRIPTDIR}/..


while true
do
	LOG_FILE=${APPDIR}/logs/job-log-`date +%Y-%m-%d`.log

    # Get current hour, day, month and year for Asia/Calcutta region
    H=$(TZ=":Asia/Calcutta" date +%H)
    D=$(TZ=":Asia/Calcutta" date +%d)
    M=$(TZ=":Asia/Calcutta" date +%m)
    Y=$(TZ=":Asia/Calcutta" date +%y)

    # Get todays date for Asia/Calcutta region
    todaysDate=$(TZ=":Asia/Calcutta" date +%d-%m-%Y)

    echo "Current time ${H} hours"  >> ${LOG_FILE} 2>&1
    echo "Last run date is ${lastRunDate}"  >> ${LOG_FILE} 2>&1
    echo "Todays date is ${todaysDate}"  >> ${LOG_FILE} 2>&1

    # Run everyday at 18:00 IST
    if [[ ${lastRunDate} != ${todaysDate} ]] && ((10#${H} >= 18 )); then
        # Sleep for a 3 minutes, just to make sure that this job doesn't miss the uploaded file.
        sleep 3m
        printf "Job starting. \n" >> ${LOG_FILE} 2>&1
        ${PYTHON_EXEC} ${APPDIR}/manage.py importBhavCopy ${D}-${M}-${Y}
        lastRunDate=${todaysDate}
        printf "\n\nChanged lastRunDate to ${D}-${M}-${Y}\n" >> ${LOG_FILE} 2>&1
    fi
    echo "-----------------------------------------------------------------------------------"  >> ${LOG_FILE} 2>&1
    sleep 2m
done


