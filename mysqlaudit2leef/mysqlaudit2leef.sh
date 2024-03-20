#!/bin/bash
# Script to convert MySQL Audit logs to LEEF format on the fly
#
# Usage:
#     $ mysqlaudit2leef.sh <MySQL Audit Logfile> <Remote syslog address> { start | stop }
#

print_usage () {
    echo "   USAGE: $0 <MySQL Audit Logfile> <Remote syslog address> { start | stop }"
    echo
}

start_run() {
    # Invoke python3 script and feed into syslog
    tail -f $AUDIT_LOGFILE | python3 mysqlaudit2leef.py | logger -n $SYSLOG_TARGET -t mysqlaudit2leef
}

stop_run() {
    LGRPID=$(ps -ef | grep "logger -n $SYSLOG_TARGET -t mysqlaudit2leef" | grep -v "grep" | awk '{print $2}')
    CONVPID=$(ps -ef | grep "python3 mysqlaudit2leef.py" | grep -v "grep" | awk '{print $2}')
    TAILPID=$(ps -ef | grep "tail -f $AUDIT_LOGFILE" | grep -v "grep" | awk '{print $2}')
    kill $LGRPID
    kill $CONVPID
    kill $TAILPID
}

# Main
if [ "$1" == "--help" ]; then
    print_usage
    exit 0
fi

if [ "$#" -ne 3 ]; then
    echo "   ERROR: Invalid number of arguments"
    echo
    print_usage
    exit 1
fi

AUDIT_LOGFILE=$1
SYSLOG_TARGET=$2
OPR=$3

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

