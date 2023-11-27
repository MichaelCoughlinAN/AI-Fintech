#!bin/sh

DIR=$(cd "$(dirname "$0")"; pwd) 

(trap 'kill 0' SIGINT; python3 $DIR/google_rising_trend.py )
