#!/bin/bash

function start() {
    podman start api-checkpoint
}

function stop() {
    podman stop api-checkpoint
}

function restart() {
    stop
    sleep 1
    start
}

case $1 in
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

        *)
            echo $"Usage: $0 {start|stop|restart}"
            exit 1
esac

exit 0
