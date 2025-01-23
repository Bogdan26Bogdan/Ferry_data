#!/bin/bash

# Get the path to the script
SCRIPTPATH=$(dirname "$0")

# Run the script to query the api
/usr/bin/python3 $SCRIPTPATH/Ferry_api_cron.py

# add to git and push 
cd $SCRIPTPATH
git add .
#TODO: uncomment this when ready to be pushed to main
#git commit -m "cron job" -m "grabbed api data at $(TZ="America/Vancouver" date)"
#git push


# output the job was a success
echo "Cron job ran successfully at $(TZ="America/Vancouver" date)" >> $SCRIPTPATH/cron.log