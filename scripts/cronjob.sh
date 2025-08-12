#!/bin/bash

chmod +x "$(pwd)/cloudflare-health-check.py"

(crontab -l 2>/dev/null; echo "* * * * * $(which python3) $(pwd)/cloudflare-health-check.py >> $(pwd)/healthcheck.log 2>&1") | crontab -

echo "Cronjob installed to run Cloudflare health check every minute."
echo "Logs will be stored in $(pwd)/healthcheck.log"

