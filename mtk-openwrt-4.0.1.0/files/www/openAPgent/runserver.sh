#!/bin/sh

AP_IPADDR=0.0.0.0
AP_PORT=8001
MANAGE_PY=manage.py
APCLIENT=apClient

APSERVER_LOG_FILE="/var/log/apServer.log"
APCLIENT_LOG_FILE="/var/log/apClient.log"

KILLALL=killall5


check_log_file () {
	if [ ! -f "$APSERVER_LOG_FILE" ]; then
	    touch $APSERVER_LOG_FILE
	fi
	if [ ! -f "$APCLIENT_LOG_FILE" ]; then
	    touch $APCLIENT_LOG_FILE
	fi
}

do_start () {
    if [ "$MANAGE_PY" ]
    then
	if [ -f /usr/bin/sudo ]; then
	    SUDO="sudo"
	else
	    SUDO=""
	fi
	
	echo "++ Start apServer $SUDO ++"
	$SUDO python $MANAGE_PY runserver $AP_IPADDR:$AP_PORT &
	
	sleep 5

	echo "++ Start $APCLIENT $SUDO ++"
	$SUDO python -m $APCLIENT &

	check_log_file
    else
	echo "Error: Cannot find $MANAGE_PY file."
    fi
}

do_stop ()
{
    if [ -f /usr/bin/killall ] ; then
	echo "killall : python"
        $KILLALL python
    else
	echo "Kill: python $MANAGE_PY runserver"
	sudo pkill -f "python $MANAGE_PY runserver"
	echo "Kill: python $APCLIENT"
	sudo pkill -f "python -m $APCLIENT"
    fi
}

do_client_start ()
{
    python -m $APCLIENT &
}

do_client_stop ()
{
    echo "Kill: python $APCLIENT"
    pkill -f "python -m $APCLIENT"
}

case "$1" in
    start)
	do_start
	;;
    restart|reload|force-reload)
	do_stop
	sleep 3
	do_start
	;;
    stop)
	do_stop
	;;
    client_start)
	do_client_start
	;;
    client_stop)
	do_client_stop
	;;
    *)
	echo "Usage: $0 start|stop" >&2
	exit 3
    ;;
esac
