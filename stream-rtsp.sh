#!/bin/bash
libcamera-vid -t 0 --mode=1920:1080:10 --framerate 24 --inline -o - | cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/stream}' :demux=h264