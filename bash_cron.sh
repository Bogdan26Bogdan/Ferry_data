#!/bin/bash

# Get the path to the script
SCRIPTPATH=$(dirname "$0")
cd $SCRIPTPATH

# Run the script to query the api
/usr/bin/python3 $SCRIPTPATH/Ferry_api_cron.py

# Add to git 
git add .

# Get the current time in seconds since epoch
current_time=$(date +%s)

# Get the last modification time from the environment variable TIME_FROM_LAST_PUSH
if [ -z "$TIME_FROM_LAST_PUSH" ]; then
    last_mod_time=0
else
    last_mod_time=$TIME_FROM_LAST_PUSH
fi

# Calculate the difference in time
time_diff=$((current_time - last_mod_time))

# Check if the difference is greater than or equal to 3600 seconds (1 hour) and if it is push to git
if [ $time_diff -ge 3600 ]; then
    # Update the environment variable TIME_FROM_LAST_PUSH
    export TIME_FROM_LAST_PUSH=$current_time
    echo $TIME_FROM_LAST_PUSH
    git pull
    git commit -m "cron job" -m "grabbed api data at $(TZ="America/Vancouver" date)"
    git push
    echo "Pushed to git at $(TZ="America/Vancouver" date)" >> $SCRIPTPATH/cron.log
fi

# Output the job was a success
echo "Cron job ran successfully at $(TZ="America/Vancouver" date)" >> $SCRIPTPATH/cron.log
