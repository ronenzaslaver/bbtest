#!/bin/bash
# chkconfig: 35 20 80
# description: Xena REST server

# Source function library.
. /etc/init.d/functions

status=0

start() {
    cd /home/bbtest
    rpyc_classic.py --host 0.0.0.0
}

stop() {
	killall rpyc_classic.py
}

status() {
	if [ -z "$(ps -ef | grep rpyc_classic.py | grep -v grep)" ]; then
		echo "stopped"
		status=1
	else
		echo "running"
	fi
}

case "$1" in 
    start)
	start
	;;
    stop)
	stop
	;;
    restart)
	stop
	start
	;;
    status)
	status
	;;
    *)
	echo "Usage: $0 {start|stop|status|restart}"
esac

exit $status 
