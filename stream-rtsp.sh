#!/bin/bash
libcamera-vid -t 0 --mode=1680:900:10 --framerate 5 --inline --listen -o tcp://0.0.0.0:8081 &>> /dev/null