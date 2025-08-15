#!/bin/bash

chmod +x "$(pwd)/healthcheck.py"

(crontab -l 2>/dev/null; echo "* * * * * $(which python3) $(pwd)/healthcheck.py >> $(pwd)/healthcheck.log 2>&1") | crontab -

echo "Cronjob installed to run health check every minute."
echo "Logs will be stored in $(pwd)/healthcheck.log"

