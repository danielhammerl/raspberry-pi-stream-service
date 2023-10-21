#!/bin/bash
libcamera-vid -t 0 --width=1920 --height=1080 --framerate 24 --inline -o - | cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/stream}' :demux=h264