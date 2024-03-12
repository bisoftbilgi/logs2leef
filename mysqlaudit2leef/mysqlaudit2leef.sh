#!/bin/bash
# Script to convert MySQL Audit logs to LEEF format on the fly
#
# Usage:
#     $ mysqlaudit2leef.sh <MySQL Audit Logfile> { start | stop }
#

print_usage () {
    echo "   USAGE: $0 <MySQL Audit Logfile> { start | stop }"
    echo
}

start_run() {
    # Invoke python3 script and feed into syslog
    tail -f $AUDIT_LOGFILE | python3 mysqlaudit2leef.py
}

stop_run() {
    CONVPID=$(ps -ef | grep "python3 mysqlaudit2leef.py" | grep -v "grep" | awk '{print $2}')
    TAILPID=$(ps -ef | grep "tail -f $AUDIT_LOGFILE" | grep -v "grep" | awk '{print $2}')
    kill $CONVPID
    kill $TAILPID
}

# Main
if [ "$1" == "--help" ]; then
    print_usage
    exit 0
fi

if [ "$#" -ne 2 ]; then
    echo "   ERROR: Invalid number of arguments"
    echo
    print_usage
    exit 1
fi

AUDIT_LOGFILE=$1
OPR=$2

case "$OPR" in
    'start')
            start_run
            ;;
    'stop')
            stop_run
            ;;
    *)
            echo
            print_usage
            echo
            ;;
esac

