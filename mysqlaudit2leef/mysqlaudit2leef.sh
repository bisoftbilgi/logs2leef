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
    tail -f $AUDIT_LOGFILE | python3 mysqlaudit2leef.py | logger -p local2.info -t mysqlaudit &
}

stop_run() {
    LOGGERPID=$(ps -ef | grep "logger -p local2.info -t mysqlaudit" | grep -v "grep" | awk '{print $2}')
    CONVPID=$(ps -ef | grep "python3 mysqlaudit2leef.py" | grep -v "grep" | awk '{print $2}')
    TAILPID=$(ps -ef | grep "tail -f $AUDIT_LOGFILE" | grep -v "grep" | awk '{print $2}')
    kill $LOGGERPID
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
COMM=$2

case "$1" in
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

