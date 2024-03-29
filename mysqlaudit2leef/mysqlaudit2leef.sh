#!/bin/bash
# Script to convert MySQL Audit logs to LEEF format on the fly
#
# Usage:
#     $ mysqlaudit2leef.sh <MySQL Audit Logfile> { <Remote syslog address> | local } { start | stop }
#

print_usage () {
    echo "   USAGE: $0 <MySQL Audit Logfile> { <Remote syslog address> | local } { start | stop }"
    echo
}

start_run() {
    if [ $SYSLOG_TARGET = 'local' ]; then
        # Invoke python3 script and feed into local syslog
        tail --follow=name --retry $AUDIT_LOGFILE | python3 mysqlaudit2leef.py | logger --size 10000 --tag mysqlaudit2leef
    else
        # Invoke python3 script and feed into remote syslog
        tail --follow=name --retry $AUDIT_LOGFILE | python3 mysqlaudit2leef.py | logger --size 10000 --server $SYSLOG_TARGET --tag mysqlaudit2leef
    fi
}

stop_run() {
    LGRPID=$(ps -ef | grep "logger" | grep '--tag mysqlaudit2leef' | grep --invert-match "grep" | awk '{print $2}')
    CONVPID=$(ps -ef | grep "python3 mysqlaudit2leef.py" | grep --invert-match "grep" | awk '{print $2}')
    TAILPID=$(ps -ef | grep "tail --follow=name --retry $AUDIT_LOGFILE" | grep --invert-match "grep" | awk '{print $2}')
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

