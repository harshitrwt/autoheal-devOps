#!/bin/bash
SCRIPT_PATH="/path/to/health_check.py"
LOG_PATH="/path/to/health_check.log"


(crontab -l 2>/dev/null; echo "*/2 * * * * /usr/bin/python3 $SCRIPT_PATH >> $LOG_PATH 2>&1") | crontab -

echo "Cron job set to run every 2 minutes."
