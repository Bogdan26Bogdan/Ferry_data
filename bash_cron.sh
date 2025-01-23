#!/bin/bash

# Get the path to the script
SCRIPTPATH=$(dirname "$0")

# Run the script to query the api
/usr/bin/python3 $SCRIPTPATH/Ferry_api_cron.py

# add to git and push 
cd $SCRIPTPATH
git add .
git commit -m "cron job" -m "grabbed api data at $(TZ="America/Vancouver" date)"
git push
