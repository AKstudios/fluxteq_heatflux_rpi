#!/bin/bash
while true; do
    python /home/pi/heatflux/readserial.py &
    python /home/pi/heatflux/datalogger.py &
    wait $!
    sudo killall python
    sleep 10
done
exit
