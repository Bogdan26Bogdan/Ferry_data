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

# Get the last time a push was made
last_mod_time=$(cat cron.log | python3 scripts/get_last_push.py)

# Calculate the difference in time
time_diff=$((current_time - last_mod_time))

# Check if the difference is greater than or equal to 3600 seconds (1 hour) and if it is push to git
if [ $time_diff -ge 3600 ]; then
    git pull
    git commit -m "cron job" -m "grabbed api data at $(TZ="America/Vancouver" date)"
    git push
    echo "Pushed to git at $(TZ="America/Vancouver" date)" >> $SCRIPTPATH/cron.log
fi

# Output the job was a success
echo "Cron job ran successfully at $(TZ="America/Vancouver" date)" >> $SCRIPTPATH/cron.log